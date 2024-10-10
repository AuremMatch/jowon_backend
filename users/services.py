from users.consts import (
    SIGNUP_EMAIL_TITLE,
    SIGNUP_EMAIL_COMMON_BODY,
)
from django.conf import settings
from django.core.mail import send_mail


def send_verification_email(username: str, target_email: str, token: str):
    send_mail(
        SIGNUP_EMAIL_TITLE,
        SIGNUP_EMAIL_COMMON_BODY.format(username=username, verify_url=f'http://example/{token}'),
        settings.DEFAULT_FROM_EMAIL,
        [target_email],
    )


def register_user_by_register_token(token: str) -> User:
    aaaa = get_signup_token(token)
    if not aaaa:
        raise NoSignUpTokenExists
    
    user, _ = User.objects.get_or_create(username=aaaa['username'])
    return user
