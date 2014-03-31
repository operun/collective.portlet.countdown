from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from zope.interface import Interface
from zope.interface import implements
from zope.component import getMultiAdapter

from plone.app.portlets.portlets import base
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget

from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

from zope import schema
from zope.formlib import form
from zope.app.form.browser import DateWidget, DatetimeWidget

from collective.portlet.countdown import MessageFactory as _
from collective.portlet.countdown.widget import ImageWidget

from DateTime import DateTime
from datetime import date


class ICountdownPortlet(IPortletDataProvider):
    """A portlet
    """

    title = schema.TextLine(title=_(u"Title"),
                            description=_(u"The title of the portlet."),
                            required=True)
    
    date = schema.Date(title=_(u"Date"),
                            description=_(u"Date for the countdown"),
                            required=True)
        
    image = schema.Choice(title=_(u"Image"),
                                description=_(u"Select an image to show in the portlet"),
                                required=False,
                                source=SearchableTextSourceBinder({'portal_type': ('ATImage', 'Image')}, default_query='path:'))


class Assignment(base.Assignment):
    """Portlet assignment.
    """

    implements(ICountdownPortlet)

    title = u"Countdown"
    date = u""
    image = None

    def __init__(self, title=u'', date=u'', image=None):
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
        delta = self.data.date - date.today()
        days = delta.days
        
        return days


    def date(self):
        """ return wpd date
        """
        date = self.data.date.strftime('%Y/%m/%d')
        dt = DateTime(date)
        
        return dt

    
    def image_tag(self):
        """ return image tag
        """
        image = self.get_image_path()
        
        if image:
            scales = getMultiAdapter((image, self.request), name="images")
            return scales.tag('image', scale='mini')
        else:
            return None
            
    def get_image_path(self):
        image = self.data.image
        
        if not image:
            return None
        
        if image.startswith('/'):
            image = image[1:]

        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        portal = portal_state.portal()
        
        path = portal.restrictedTraverse(image, default=None)
        
        return path


class AddForm(base.AddForm):
    """ Portlet add form.
    """
    form_fields = form.Fields(ICountdownPortlet)
    form_fields['image'].custom_widget = UberSelectionWidget
    form_fields['date'].custom_widget = DateWidget

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """ Portlet edit form.
    """
    form_fields = form.Fields(ICountdownPortlet)
    form_fields['image'].custom_widget = UberSelectionWidget
    form_fields['date'].custom_widget = DateWidget

