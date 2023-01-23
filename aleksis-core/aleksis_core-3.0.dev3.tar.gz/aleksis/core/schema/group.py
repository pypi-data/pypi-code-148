from graphene_django import DjangoObjectType

from ..models import Group


class GroupType(DjangoObjectType):
    class Meta:
        model = Group
