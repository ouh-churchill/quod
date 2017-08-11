#!/usr/bin/python
# coding: utf-8
from __future__ import absolute_import, unicode_literals

from django import template

register = template.Library()

@register.simple_tag
def get_model_fields(object_to_query):
    return dict(
        (field.name, field.value_to_string(object_to_query)) for field in object_to_query._meta.fields
    )

@register.simple_tag
def get_model_dir(object_to_query):
    return dir(object_to_query)

@register.simple_tag
def get_model_type(object_to_query):
    return type(object_to_query)
