import re
import colander

from kotti.views.edit import (
    ContentSchema,
    generic_edit,
    generic_add,
)
from kotti.views.util import (
    ensure_view_selector,
    template_api,
)
from kotti_etherpad import _

from kotti_etherpad.resources import Etherpad


# matches an IP, localhost or a domain
expr_url = re.compile(r"^(http|https):\/\/((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])"\
                      r"\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|"\
                      r"2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])|"\
                      r"localhost|[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3})$", re.IGNORECASE)


# TODO: translations
class EtherpadSchema(ContentSchema):
    pad_id = colander.SchemaNode(colander.String())
    default_user_name = colander.SchemaNode(colander.String())
    server_domain = colander.SchemaNode(
        colander.String(),
        default="http://",
        title=_(u"Domain"),
        description=_(u"The domain of the server."),
        validator=colander.Regex(expr_url,
            msg=_(u"This is not a valid domain.")),
    )
    server_port = colander.SchemaNode(
        colander.Integer(),
        missing=80,
        title=_(u"Port"),
        description=_(u"Port of the server. Defaults to 80."),
    )
    show_controls = colander.SchemaNode(
        colander.Boolean(),
        default=True,
        title=_(u"Show controls"),
        description=_(u"Decide if you want to show the controls."),
    )
    show_chat = colander.SchemaNode(
        colander.Boolean(),
        default=True,
        title=_(u"Show chat"),
        description=_(u"Show chat window in the right column."),
    )
    show_line_numbers = colander.SchemaNode(
                            colander.Boolean(),
                            default=True,
                            title=_(u"Show chat"),
                            description=_(u"Show chat window in the right column."),
                        )
    use_monospace_font = colander.SchemaNode(
                            colander.Boolean(),
                            default=True,
                        )
    no_colors = colander.SchemaNode(
                    colander.Boolean(),
                    default=False,
                )
    hide_QR_code = colander.SchemaNode(
                        colander.Boolean(),
                        default=False,
                    )
    width = colander.SchemaNode(
                colander.String(),
                default="100%"
            )
    height = colander.SchemaNode(
                colander.String(),
                default="800px",
            )
    border = colander.SchemaNode(
                colander.String(),
                default="0"
            )
    border_style = colander.SchemaNode(
                        colander.String(),
                        default="solid",
                   )


@ensure_view_selector
def edit_etherpad(context, request):
    return generic_edit(context, request, EtherpadSchema())


def add_etherpad(context, request):
    return generic_add(context, request, EtherpadSchema(), Etherpad, u'etherpad')


def view_etherpad(context, request):

    return {
        'api': template_api(context, request),
        'pad_id': context.pad_id,
        'host': context.host(),
        'base_url': '/p/',
        'show_controls': context.show_controls and 'true' or 'false',
        'show_chat': context.show_chat and 'true' or 'false',
        'show_line_numbers': context.show_line_numbers and 'true' or 'false',
        'user_name': context.default_user_name,  # TODO: use logged in name
        'use_monospace_font': context.use_monospace_font and 'true' or 'false',
        'no_colors': context.no_colors and 'true' or 'false',
        'hide_QR_code': context.hide_QR_code and 'true' or 'false',
        'width': context.width,
        'height': context.height,
        'border': context.border,
        'border_style': context.border_style,
        }


def includeme_edit(config):

    config.add_view(
        edit_etherpad,
        context=Etherpad,
        name='edit',
        permission='edit',
        renderer='kotti:templates/edit/node.pt',
        )

    config.add_view(
        add_etherpad,
        name=Etherpad.type_info.add_view,
        permission='add',
        renderer='kotti:templates/edit/node.pt',
        )


def includeme_view(config):
    config.add_view(
        view_etherpad,
        context=Etherpad,
        name='view',
        permission='view',
        renderer='templates/etherpad-view.pt',
        )

    config.add_static_view('static-kotti_etherpad', 'kotti_etherpad:static')


def includeme(config):
    includeme_edit(config)
    includeme_view(config)
