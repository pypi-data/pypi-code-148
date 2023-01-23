import graphene
from graphene_django import DjangoObjectType

from ..models import PDFFile
from .base import FieldFileType


class PDFFileType(DjangoObjectType):
    file = graphene.Field(FieldFileType)

    class Meta:
        model = PDFFile
        exclude = ["html_file"]
