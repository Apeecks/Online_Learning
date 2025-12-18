import re
from urllib.parse import urlparse

from rest_framework.serializers import ValidationError


def extract_urls(text: str) -> list[str]:
    if not text:
        return []
    return re.findall(r"https?://[^\s]+", text)


class NoExternalLinksValidator:
    """
    Проверяет, что в указанном поле нет ссылок, кроме YouTube.
    """
    def __init__(self, field: str):
        self.field = field

    def __call__(self, attrs):
        value = attrs.get(self.field, "") if isinstance(attrs, dict) else attrs
        urls = extract_urls(value)

        for u in urls:
            host = (urlparse(u).netloc or "").lower()
            if "youtube.com" not in host:
                raise ValidationError(
                    {self.field: f"Сторонние ссылки запрещены: {host}. Разрешён YouTube."}
                )


def validate_youtube_url(value: str):
    """
    Валидатор для поля Lesson.url — разрешает только youtube.com
    """
    host = (urlparse(value).netloc or "").lower()
    if "youtube.com" not in host:
        raise ValidationError("Ссылка на видео должна вести на YouTube.")
    return value
