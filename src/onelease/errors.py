"""Ієрархія винятків застосунку: один корінь, кілька конкретних нащадків."""


class OneleaseError(Exception):
    """Базовий виняток застосунку."""


class SourceError(OneleaseError):
    """Проблема з джерелом даних: файл, мережа, формат."""


class ParseError(SourceError):
    """Запис не вдалося розібрати."""


class ConfigError(OneleaseError):
    """Некоректна конфігурація застосунку."""
