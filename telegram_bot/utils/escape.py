import re
from typing import Any


def escape_md_v2(text: Any | None) -> str | None:
	""" Escape str for telegram (MarkdownV2) """
	return re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', str(text))
