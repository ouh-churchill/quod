#!/usr/bin/python
# coding: utf-8
from __future__ import absolute_import, unicode_literals

from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailsearch import index


# BLOCKS
class PublicationBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    url = blocks.URLBlock(required=False)
    authors = blocks.CharBlock()

    class Meta:
        label = 'Publication'


class QandABlock(blocks.StructBlock):
    question = blocks.RichTextBlock()
    answer = blocks.RichTextBlock()

    class Meta:
        label = 'Question and Answer'


# PAGES
class MultiPage(Page):

    # Database fields
    author = models.CharField(max_length=255)
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('publications_list', blocks.ListBlock(
            'publication', PublicationBlock()
        )),
        ('qa_list', blocks.ListBlock(
            'entry', QandABlock()
        )),
    ])
    date = models.DateField("Post date")
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    # Search index configuration

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.SearchField('author'),
        index.FilterField('date'),
    ]

    # Editor panels configuration

    content_panels = Page.content_panels + [
        FieldPanel('author'),
        FieldPanel('date'),
        StreamFieldPanel('body'),
        InlinePanel('related_links', label="Related links"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        ImageChooserPanel('feed_image'),
    ]

    # Parent page / subpage type rules

    parent_page_types = []
    subpage_types = []


class MultiPageRelatedLink(Orderable):
    page = ParentalKey(MultiPage, related_name='related_links')
    name = models.CharField(max_length=255)
    url = models.URLField()

    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
    ]
