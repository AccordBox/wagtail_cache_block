from django.core.cache import InvalidCacheBackendError, caches
from django.core.cache.utils import make_template_fragment_key
from django.template import (Library, Node, TemplateSyntaxError,
                             VariableDoesNotExist)
from wagtail.core.blocks import (CharBlock, ChoiceBlock, ChooserBlock,
                                 ListBlock, PageChooserBlock, RawHTMLBlock,
                                 RichTextBlock, StreamBlock, StreamValue,
                                 StructBlock, StructValue)

register = Library()


def extract_block(block_obj):
    """
    Extract block values to vary_on list
    """
    vary_on = []
    if isinstance(block_obj.block, StructBlock):
        tmp_dict = {}
        for k, v in block_obj.value.bound_blocks.items():
            tmp_dict[k] = extract_block(v)
        vary_on.append({block_obj.block.name: tmp_dict})
    elif isinstance(block_obj.block, StreamBlock):
        tmp_ls = []
        for child in block_obj.value:
            sub_value = extract_block(child)
            tmp_ls.extend(sub_value)
        vary_on.append({block_obj.block.name: tmp_ls})
    elif isinstance(block_obj.block, ChooserBlock):
        # do not query, only use PK for now
        vary_on.append({block_obj.block.name: block_obj.value.pk})
    else:
        vary_on.append({block_obj.block.name: str(block_obj.value)})

    return vary_on


class CacheBlockNode(Node):
    def __init__(self, nodelist, expire_time_var, request, block):
        self.nodelist = nodelist
        self.expire_time_var = expire_time_var
        self.request = request
        self.block = block

    def render(self, context):
        try:
            expire_time = self.expire_time_var.resolve(context)
        except VariableDoesNotExist:
            raise TemplateSyntaxError('"cache" tag got an unknown variable: %r' % self.expire_time_var.var)

        if expire_time is not None:
            try:
                expire_time = int(expire_time)
            except (ValueError, TypeError):
                raise TemplateSyntaxError('"cache" tag got a non-integer timeout value: %r' % expire_time)

        try:
            fragment_cache = caches['template_fragments']
        except InvalidCacheBackendError:
            fragment_cache = caches['default']

        request, block_obj = self.request.resolve(context), self.block.resolve(context)

        if getattr(request, 'is_preview', False):
            # preview mode, do not pull from cache
            return self.nodelist.render(context)
        else:
            vary_on = extract_block(block_obj)

            fragment_name = '%s.%s' % (
                block_obj.block.__class__.__module__,
                block_obj.block.__class__.__name__,
            )
            cache_key = make_template_fragment_key(fragment_name, vary_on)
            value = fragment_cache.get(cache_key)
            if value is None:
                value = self.nodelist.render(context)
                fragment_cache.set(cache_key, value, expire_time)
            return value


@register.tag('cache_block')
def do_cache_block(parser, token):
    nodelist = parser.parse(('endcache_block',))
    parser.delete_first_token()
    tokens = token.split_contents()
    if len(tokens) < 4:
        raise TemplateSyntaxError("'%r' tag requires at least 3 arguments." % tokens[0])

    return CacheBlockNode(
        nodelist, parser.compile_filter(tokens[1]),
        parser.compile_filter(tokens[2]),
        parser.compile_filter(tokens[3]),
    )
