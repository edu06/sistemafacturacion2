
from xml.dom.expatbuilder import parseString
from appFactInv.models import productos
from django import template

register=template.Library()


@register.filter()

def codigo(val):
    return productos.pk