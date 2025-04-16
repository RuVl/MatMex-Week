import re


def escape_md_v2(text: str | None) -> str | None:
	""" Escape str for telegram (MarkdownV2) """
	if isinstance(text, str):
		return re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', text)
