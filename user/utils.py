import os
from django.core.mail import send_mail


def set_token_send_email(user):
    """
    This function sets a new password token for the user and sends an email to the user with the token.
    :param user:
    :return:
    """
    token = user.set_new_password_token()
    send_mail(
        'Création de votre mot de passe',
        f'Bonjour {user.first_name} {user.last_name},\n\n'
        f'Veuillez cliquer sur le lien suivant pour créer votre mot de passe:\n'
        f'http://localhost:3000/set-password?token={token}',
        os.environ.get("EMAIL_HOST_USER", "admin@localhost"),
        [user.email],
        fail_silently=False,
    )
    return token
