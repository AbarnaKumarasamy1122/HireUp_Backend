from users.models import User

from .models import Notification


def notify_user(user, title, message):
    Notification.objects.create(
        user=user,
        title=title,
        message=message,
    )


def notify_admins(title, message):
    for admin in User.objects.filter(role="admin"):
        notify_user(admin, title, message)
