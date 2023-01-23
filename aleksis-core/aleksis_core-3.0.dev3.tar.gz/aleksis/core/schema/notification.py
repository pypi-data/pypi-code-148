from django.core.exceptions import PermissionDenied

import graphene
from graphene_django import DjangoObjectType

from ..models import Notification


class NotificationType(DjangoObjectType):
    class Meta:
        model = Notification


class MarkNotificationReadMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()  # noqa

    notification = graphene.Field(NotificationType)

    @classmethod
    def mutate(cls, root, info, id):  # noqa
        notification = Notification.objects.get(pk=id)

        if not info.context.user.has_perm("core.mark_notification_as_read_rule", notification):
            raise PermissionDenied()
        notification.read = True
        notification.save()

        return MarkNotificationReadMutation(notification=notification)
