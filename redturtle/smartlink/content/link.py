"""Definition of the SmartLink content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from Products.ATContentTypes.content.link import ATLink, ATLinkSchema

from redturtle.smartlink import smartlinkMessageFactory as _
from redturtle.smartlink.interfaces import ILink
from redturtle.smartlink.config import PROJECTNAME

LinkSchema = ATLinkSchema.copy() + atapi.Schema((

    atapi.ImageField('image',
        required = False,
        storage = AnnotationStorage(migrate=True),
        languageIndependent = True,
        max_size = zconf.ATNewsItem.max_image_dimension,
        sizes= {'large'   : (768, 768),
                'preview' : (400, 400),
                'mini'    : (200, 200),
                'thumb'   : (128, 128),
                'tile'    :  (64, 64),
                'icon'    :  (32, 32),
                'listing' :  (16, 16),
               },
        validators = (('isNonEmptyFile', V_REQUIRED),
                             ('checkNewsImageMaxSize', V_REQUIRED)),
        widget = ImageWidget(
            description = _(u'help_smartlink_image', default=u"Will be shown views that render content's images and in the link view itself"),
            label= _(u'label_smartlink_image', default=u'Image'),
            show_content_type = False)
        ),

    atapi.StringField('imageCaption',
        required = False,
        searchable = True,
        widget = StringWidget(
            description = '',
            label = _(u'label_image_caption', default=u'Image Caption'),
            size = 40)
        ),

))

LinkSchema['title'].storage = atapi.AnnotationStorage()
LinkSchema['description'].storage = atapi.AnnotationStorage()

ImagedEventSchema.moveField('image', after='text')
ImagedEventSchema.moveField('imageCaption', after='image')

schemata.finalizeATCTSchema(LinkSchema, moveDiscussion=False)

class Link(ATLink):
    """A link to an internal or external resource."""
    implements(ILink)

    meta_type = "Link"
    schema = LinkSchema

    security.declareProtected(permissions.View, 'tag')
    def tag(self, **kwargs):
        """Generate image tag using the api of the ImageField
        """
        if 'title' not in kwargs:
            kwargs['title'] = self.getImageCaption()
        return self.getField('image').tag(self, **kwargs)

    def __bobo_traverse__(self, REQUEST, name):
        """Transparent access to image scales
        """
        if name.startswith('image'):
            field = self.getField('image')
            image = None
            if name == 'image':
                image = field.getScale(self)
            else:
                scalename = name[len('image_'):]
                if scalename in field.getAvailableSizes(self):
                    image = field.getScale(self, scale=scalename)
            if image is not None and not isinstance(image, basestring):
                # image might be None or '' for empty images
                return image

        return ATLink.__bobo_traverse__(self, REQUEST, name)

atapi.registerType(Link, PROJECTNAME)
