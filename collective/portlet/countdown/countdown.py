from zope.interface import Interface
from zope.interface import implements
from zope.component import getMultiAdapter

from zope.schema.fieldproperty import FieldProperty

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

from plone.namedfile.field import NamedImage
from plone.namedfile.interfaces import IImageScaleTraversable

from zope import schema
from zope.formlib import form

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.portlet.countdown import MessageFactory as _
from collective.portlet.countdown.widget import ImageWidget

class ICountdownPortlet(IPortletDataProvider):
    """A portlet
    """

    title = schema.TextLine(title=_(u"Title"),
                            description=_(u"The title of the portlet."),
                            required=True)
    
    date = schema.TextLine(title=_(u"Date"),
                            description=_(u"Date for the countdown"),
                            required=True)
        
    image = schema.Field(title=_(u"Image"),
                       description=_(u"Please upload an image"),
                       required=False)


class Assignment(base.Assignment):
    """Portlet assignment.
    """

    implements(ICountdownPortlet)

    title = u"Countdown"
    date = u""
    image = None
    assignment_context_path = None

    def __init__(self, title=u'', date=u'', image=None, assignment_context_path=None):
        self.assignment_context_path = assignment_context_path
        self.portlet_title = title
        self.date = date
        self.image = image

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return self.portlet_title


class Renderer(base.Renderer):
    """Portlet renderer.
    """

    render = ViewPageTemplateFile('countdown.pt')

    def countdown(self):
        """ return countdown
        """
        return self.data.date

    #@property
    #@memoize
    def image_tag(self):
        """ return image tag to display image
        """
        if self.data.image:
            state=getMultiAdapter((self.context, self.request), name="plone_portal_state")
            portal=state.portal()
            assignment_url = portal.unrestrictedTraverse(self.data.assignment_context_path).absolute_url()
            width = self.data.image.width
            height = self.data.image.height
            
            return "<img src='%s/%s/@@image' width='%s' height='%s' alt='%s'/>" % \
                   (assignment_url, self.data.__name__, str(width), str(height), self.data.portlet_title)
                   
        return None


class AddForm(base.AddForm):
    """ Portlet add form.
    """
    form_fields = form.Fields(ICountdownPortlet)
    form_fields['image'].custom_widget = ImageWidget

    def create(self, data):
        assignment_context_path = '/'.join(self.context.__parent__.getPhysicalPath())
        return Assignment(assignment_context_path=assignment_context_path, **data)


class EditForm(base.EditForm):
    """ Portlet edit form.
    """
    form_fields = form.Fields(ICountdownPortlet)
    form_fields['image'].custom_widget = ImageWidget

