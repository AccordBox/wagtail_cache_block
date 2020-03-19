from wagtail.admin.edit_handlers import (FieldPanel, InlinePanel,
                                         MultiFieldPanel, PageChooserPanel,
                                         StreamFieldPanel)
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Orderable, Page

from taggit.models import TaggedItemBase

from wagtail.core.blocks import (CharBlock, ChoiceBlock, ListBlock,
                                 PageChooserBlock, RawHTMLBlock, RichTextBlock,
                                 StreamBlock, StructBlock, StructValue)


class ColumnStructBlock(StructBlock):
    heading = CharBlock(classname="full title")
    paragraph = RichTextBlock()
    reference_page = PageChooserBlock()

    class Meta:
        template = 'example/blocks/column_struct_block.html'


class ColumnStreamBlock(StreamBlock):
    sub_struct_data = ColumnStructBlock()

    class Meta:
        template = 'example/blocks/column_stream_block.html'


class ArticlePage(Page):
    body = StreamField([
        ('heading', CharBlock(classname="full title")),
        ('paragraph', RichTextBlock()),
        ('reference_page', PageChooserBlock()),

        # this is single StructBlock
        (
            'struct_data',
            StructBlock([
                ('heading', CharBlock(classname="full title")),
                ('paragraph', RichTextBlock()),
                ('reference_page', PageChooserBlock()),
            ])
        ),

        # this is StreamBlock
        (
            'stream_data',
            StreamBlock([
                (
                    'sub_struct_data',
                    StructBlock([
                        ('heading', CharBlock(classname="full title")),
                        ('paragraph', RichTextBlock()),
                        ('reference_page', PageChooserBlock()),
                    ])
                ),
            ])
        ),

        ('column_struct_data', ColumnStructBlock()),

        ('column_stream_data', ColumnStreamBlock())

    ], null=True, blank=True)

    # Editor panels configuration
    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]
