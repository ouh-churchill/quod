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
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailsnippets.blocks import SnippetChooserBlock
# from wagtailmenus.models import MenuPage


# SNIPPETS
@register_snippet
class Publication(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField(null=True, blank=True)
    authors = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('url'),
        FieldPanel('authors')
    ]

    def __str__(self):
        return "{0} : {1}".format(self.title, self.authors)


# SNIPPET LINKS


# BLOCKS


class QandABlock(blocks.StructBlock):
    question = blocks.RichTextBlock()
    answer = blocks.RichTextBlock()

    class Meta:
        label = 'Question and Answer'


# PAGES
class MultiPage(Page):
    """
    Multipurpose page model, allowing pretty much all types to be combined onto one page

    From Page:
        title - Char(255)
        slug - Slug/Char(255)
        content_type - FK(content_type)
        live - Boolean
        has_unpublished_changes - Boolean
        url_path - Text
        owner - FK(auth_user)
        seo_title - Char(255)
        show_in_menus - Boolean
        search_description - Text
        go_live_at - DateTime
        expire_at - DateTime
        expired - Boolean
        locked - Boolean
        first_published_at - DateTime
        latest_revision_created_at - DateTime
    """

    # Database fields
    author = models.CharField(max_length=255)
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('text', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('publications_list', blocks.ListBlock(SnippetChooserBlock(Publication, label="publication"))),
        ('qa_list', blocks.ListBlock(QandABlock(label="entry"))),
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

    # parent_page_types = []
    # subpage_types = []


class MultiPageRelatedLink(Orderable):
    page = ParentalKey(MultiPage, related_name='related_links')
    name = models.CharField(max_length=255)
    url = models.URLField()

    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
    ]