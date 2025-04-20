import asyncio
import math
import os
import time
from typing import Any

from aiogram.enums import ChatAction
from aiogram.types import Message, FSInputFile
from structlog.typing import FilteringBoundLogger


class MessageActionWrapper:
	def __init__(
			self,
			msg: Message,
			max_delay: float,
			typing_speed: float,
			max_upload_delay: float,
			adaptive: bool,
			log: FilteringBoundLogger = None
	):
		self._msg = msg
		self._max_delay = max_delay
		self._speed = typing_speed
		self._max_upload_delay = max_upload_delay
		self._adaptive = adaptive
		self._log = log

	def __getattr__(self, name: str) -> Any:
		orig_attr = getattr(self._msg, name)

		if callable(orig_attr) and name.startswith(("answer", "reply", "edit")):
			async def wrapped(*args, **kwargs):
				actions = []

				# 1. Other action (not typing)
				action = self._detect_action_and_delay(kwargs)
				if action is not None:
					actions.append(action)

				# 2. Typing action
				if self._should_show_typing(args, kwargs):
					delay = self._calc_typing_delay(args, kwargs)
					if delay > 0:
						actions.append((ChatAction.TYPING, delay))

				# 3. Perform all actions sequentially
				for action_type, delay in actions:
					await self._perform_action(action_type, delay)

				return await orig_attr(*args, **kwargs)

			return wrapped

		return orig_attr

	def _calc_typing_delay(self, args, kwargs) -> float:
		if not self._adaptive:
			return self._max_delay

		text = self._extract_text(args, kwargs)
		if not text:
			return self._max_delay

		calculated = len(text) / self._speed
		return min(calculated, self._max_delay)

	def _detect_action_and_delay(self, kwargs: dict) -> tuple[ChatAction, float] | None:
		file_keys = {
			"photo": ChatAction.UPLOAD_PHOTO,
			"video": ChatAction.UPLOAD_VIDEO,
			"video_note": ChatAction.UPLOAD_VIDEO_NOTE,
			"voice": ChatAction.UPLOAD_VOICE,
			"audio": ChatAction.UPLOAD_VOICE,
			"document": ChatAction.UPLOAD_DOCUMENT,
			"sticker": ChatAction.CHOOSE_STICKER,
			"location": ChatAction.FIND_LOCATION,
		}

		# Check only kwargs!
		for key, action in file_keys.items():
			if key in kwargs:
				return self._calculate_upload_delay(kwargs[key], action)

		return None

	def _calculate_upload_delay(self, file: Any, action: ChatAction) -> tuple[ChatAction, float] | None:
		if not self._adaptive:
			return action, self._max_delay

		file_size = None

		if hasattr(file, "file_size"):
			file_size = file.file_size

		# if the file is dict
		elif isinstance(file, dict) and "file_size" in file:
			file_size = file["file_size"]

		# if the file is FSInputFile
		elif isinstance(file, FSInputFile) and os.path.exists(file.path):
			try:
				file_size = os.path.getsize(file.path)
			except OSError:
				pass  # no permissions

		if file_size is None:
			return action, self._max_delay

		kB = file_size / 1024
		log_size = math.log(kB) if file_size > 0 else 0

		# базовая задержка (при > 3MB - максимальная задержка)
		base_delay = self._max_upload_delay / 8.27814569536

		delay = min(log_size * base_delay, self._max_upload_delay)
		return action, delay

	@staticmethod
	def _should_show_typing(args: tuple, kwargs: dict) -> bool:
		return bool(kwargs.get("text") or kwargs.get("caption")) or isinstance(args[0], str)

	async def _perform_action(self, action: str, total_delay: float):
		if self._log is not None:
			await self._log.adebug("send-chat-action", action=action, delay=total_delay)

		interval = 5.0  # Telegram action lives for 5 sec
		start = time.monotonic()
		elapsed = 0.0

		while elapsed < total_delay:
			await self._msg.bot.send_chat_action(self._msg.chat.id, action)
			sleep_time = min(interval, total_delay - elapsed)
			elapsed = time.monotonic() - start
			await asyncio.sleep(sleep_time)

	@staticmethod
	def _extract_text(args, kwargs) -> str | None:
		for key in ("text", "caption"):
			if key in kwargs:
				return kwargs[key]

		if args and isinstance(args[0], str):
			return args[0]

		return None
