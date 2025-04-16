from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluent.runtime import FluentLocalization

from keyboards.callback_factories import PKApplyFactory


def verification_request_ikb(l10n: FluentLocalization, apply_id: int) -> InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder()
	builder.row(
		InlineKeyboardButton(
			text=l10n.format_value("btn-approve-apply"),
			callback_data=PKApplyFactory(apply_id=apply_id, decision='approve').pack()
		),
		InlineKeyboardButton(
			text=l10n.format_value("btn-decline-apply"),
			callback_data=PKApplyFactory(apply_id=apply_id, decision='reject').pack()
		),
	)
	return builder.as_markup()


def verified_request_ikb(l10n: FluentLocalization, apply_id: int) -> InlineKeyboardMarkup:
	return InlineKeyboardMarkup(inline_keyboard=[[
		InlineKeyboardButton(
			text=l10n.format_value("btn-review-apply"),
			callback_data=PKApplyFactory(apply_id=apply_id, decision='review').pack()
		)
	]])
