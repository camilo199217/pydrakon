# app/core/i18n.py

from gettext import translation, NullTranslations
from contextvars import ContextVar
from babel.numbers import format_currency, format_decimal
from babel.dates import format_datetime
from secureauthapi.conf import get_settings
from datetime import datetime

settings = get_settings()

# Contextos por request
_current_gettext: ContextVar = ContextVar("_current_gettext", default=lambda x: x)
_current_ngettext: ContextVar = ContextVar(
    "_current_ngettext", default=lambda s, p, n: s if n == 1 else p
)
_current_locale: ContextVar = ContextVar(
    "_current_locale", default=settings.I18N_DEFAULT_LANGUAGE
)


def set_language(lang_code: str):
    try:
        t = translation(
            settings.I18N_DOMAIN,
            localedir=settings.I18N_LOCALES_DIR,
            languages=[lang_code],
        )
    except FileNotFoundError:
        t = NullTranslations()
    _current_gettext.set(t.gettext)
    _current_ngettext.set(t.ngettext)
    _current_locale.set(lang_code)


# Accesos globales
_ = lambda message: _current_gettext.get()(message)


def ngettext(singular: str, plural: str, n: int):
    return _current_ngettext.get()(singular, plural, n)


def get_locale() -> str:
    return _current_locale.get()


# Formato de moneda
def format_money(value: float, currency: str = "USD") -> str:
    return format_currency(value, currency, locale=get_locale())


# Formato de números
def format_number(value: float) -> str:
    return format_decimal(value, locale=get_locale())


# Formato de fechas
def format_date(dt: datetime, format_str: str = "medium") -> str:
    return format_datetime(dt, format=format_str, locale=get_locale())


# Middleware
from fastapi import Request


async def i18n_middleware(request: Request, call_next):
    lang = request.headers.get("Accept-Language", settings.I18N_DEFAULT_LANGUAGE)[:2]
    set_language(lang)
    response = await call_next(request)
    return response
