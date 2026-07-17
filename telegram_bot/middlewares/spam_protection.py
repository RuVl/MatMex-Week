import time
from typing import Any, Awaitable, Callable, Dict, Optional

from aiogram import BaseMiddleware
from aiogram.dispatcher.event.bases import CancelHandler
from aiogram.dispatcher.flags import get_flag
from aiogram.dispatcher.middlewares.user_context import EVENT_FROM_USER_KEY
from aiogram.exceptions import TelegramAPIError
from aiogram.types import CallbackQuery, Message, TelegramObject, User
from redis.asyncio import Redis
from structlog import get_logger
from structlog.typing import FilteringBoundLogger

from includes import get_redis
from middlewares import LOGGING_KEY


class SpamProtectionMw(BaseMiddleware):
	"""
	Middleware for protection against spam messages and callback floods.
	Uses Redis to track and limit message frequency from users.
	"""

	def __init__(
			self,
			*,
			redis_prefix: str = 'spam_protection',
			message_limit: int = 20,
			message_interval: int = 60,  # 20 messages per minute
			callback_limit: int = 15,
			callback_interval: int = 30,  # 15 callbacks per 30 seconds
			flag_key: str = 'skip_spam_check',
			ban_threshold: int = 100,
			ban_time: int = 300  # 5 minutes
	):
		self.logger: FilteringBoundLogger = get_logger()
		self.redis: Redis = get_redis(decode_responses=True)

		self.redis_prefix = redis_prefix
		self.message_limit = message_limit
		self.message_interval = message_interval
		self.callback_limit = callback_limit
		self.callback_interval = callback_interval
		self.flag_key = flag_key
		self.ban_threshold = ban_threshold
		self.ban_time = ban_time

	def _get_message_key(self, user_id: int) -> str:
		return f"{self.redis_prefix}:msg:{user_id}"

	def _get_callback_key(self, user_id: int) -> str:
		return f"{self.redis_prefix}:cb:{user_id}"

	def _get_ban_key(self, user_id: int) -> str:
		return f"{self.redis_prefix}:ban:{user_id}"

	async def _check_banned(self, user_id: int) -> bool:
		"""Check if a user is currently banned for spam"""
		ban_key = self._get_ban_key(user_id)
		return await self.redis.exists(ban_key) == 1

	async def _increment_and_check(
			self,
			key: str,
			limit: int,
			interval: int,
			user_id: int
	) -> tuple[bool, int]:
		"""
		Increment counter and check if it's over limit
		Returns: (is_allowed, current_count)
		"""
		# Get current time for pipeline
		current_time = time.time()
		pipe = self.redis.pipeline()

		# Add current timestamp to sorted set
		await pipe.zadd(key, {str(current_time): current_time})

		# Remove old timestamps
		await pipe.zremrangebyscore(key, 0, current_time - interval)

		# Get current count
		await pipe.zcard(key)

		# Set expiration to clean up
		await pipe.expire(key, interval * 2)

		# Execute pipeline
		_, _, count, _ = await pipe.execute()

		# Check if over limit
		is_allowed = count <= limit

		# If limit exceeded by a lot, consider banning
		if count > limit + 5:
			await self._handle_excessive_requests(user_id, count)

		return is_allowed, count

	async def _handle_excessive_requests(self, user_id: int, count: int):
		"""Handle a user sending excessive requests"""
		violation_score = count - self.message_limit

		if violation_score >= self.ban_threshold:
			ban_key = self._get_ban_key(user_id)
			await self.redis.set(ban_key, 1, ex=self.ban_time)

			await self.logger.awarning(
				"user-temp-banned",
				user_id=user_id,
				violation_score=violation_score,
				ban_time=self.ban_time
			)
		else:
			await self.logger.adebug(
				"excessive-requests",
				user_id=user_id,
				count=count
			)

	async def __call__(
			self,
			handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
			event: TelegramObject,
			data: Dict[str, Any],
	) -> Any:
		# Skip if handler has the skip_spam_check flag
		if get_flag(data, self.flag_key):
			return await handler(event, data)

		# Get user from event
		user: Optional[User] = data.get(EVENT_FROM_USER_KEY)
		if not user:
			return await handler(event, data)

		# Get logger from data or use default
		logger = data.get(LOGGING_KEY, self.logger)
		user_id = user.id

		# Check if user is banned
		if await self._check_banned(user_id):
			await logger.adebug("spam-ban-active", user_id=user_id)

			# Try to notify user if this is a message
			if isinstance(event, Message):
				try:
					await event.answer("Too many requests. Please wait a few minutes before trying again.")
				except TelegramAPIError:
					pass

			# Cancel handling
			raise CancelHandler()

		# Check rate limits based on event type
		if isinstance(event, Message):
			key = self._get_message_key(user_id)
			is_allowed, count = await self._increment_and_check(
				key,
				self.message_limit,
				self.message_interval,
				user_id
			)
			event_type = "message"

		elif isinstance(event, CallbackQuery):
			key = self._get_callback_key(user_id)
			is_allowed, count = await self._increment_and_check(
				key,
				self.callback_limit,
				self.callback_interval,
				user_id
			)
			event_type = "callback"

			# For callbacks, automatically answer to prevent UI hanging
			if not is_allowed:
				await event.answer("Too many requests. Please slow down.", show_alert=True)
		else:
			# Unknown event type, allow
			return await handler(event, data)

		# Check if allowed
		if not is_allowed:
			await logger.adebug(
				"rate-limit-exceeded",
				event_type=event_type,
				user_id=user_id,
				count=count
			)

			# If message, try to notify user
			if isinstance(event, Message) and count <= self.message_limit + 10:
				try:
					await event.answer("You're sending messages too quickly. Please slow down.")
				except TelegramAPIError:
					pass

			# Cancel handler for this event
			raise CancelHandler()

		# Continue with handler if allowed
		return await handler(event, data)

	async def close(self) -> None:
		"""Close redis connection when bot shuts down"""
		await self.redis.close()
