"""Definition of the Meeting content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import document
from Products.ATContentTypes.content import event
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.configuration import zconf

# -*- Message Factory Imported Here -*-
from uwosh.meeting import meetingMessageFactory as _

from uwosh.meeting.interfaces import IMeeting
from uwosh.meeting.config import PROJECTNAME

MeetingSchema = folder.ATFolderSchema.copy() + event.ATEventSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.TextField(
        'agenda',
        required=False,
        searchable=True,
        storage=atapi.AnnotationStorage(),
        validators = ('isTidyHtmlWithCleanup',),
        default_output_type = 'text/x-html-safe',
        allowable_content_types=('text/plain', 'text/structured', 'text/html',
                                 'application/msword'),
        widget=atapi.RichWidget(
            label=_(u"Agenda"),
            description=_(u"the agenda for the meeting"),
            rows = 25,
            allow_file_upload = zconf.ATDocument.allow_document_upload,
        ),
    ),

    atapi.TextField(
        'minutes',
        required=False,
        searchable=True,
        storage=atapi.AnnotationStorage(),
        validators = ('isTidyHtmlWithCleanup',),
        default_output_type = 'text/x-html-safe',
        allowable_content_types=('text/plain', 'text/structured', 'text/html',
                                 'application/msword'),
        widget=atapi.RichWidget(
            label=_(u"Minutes"),
            description=_(u"the minutes of the meeting"),
            rows = 25,
            allow_file_upload = zconf.ATDocument.allow_document_upload,
        ),
    ),

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

MeetingSchema['title'].storage = atapi.AnnotationStorage()
MeetingSchema['description'].storage = atapi.AnnotationStorage()
MeetingSchema['description'].widget.label = _(u'label_summary', default=u'Summary')


schemata.finalizeATCTSchema(
    MeetingSchema,
    folderish=True,
    moveDiscussion=False
)


class Meeting(folder.ATFolder, document.ATDocument, event.ATEvent):
    """a content type that includes agenda and minutes rich text fields"""
    implements(IMeeting, document.IATDocument, document.IDAVAware, event.IATEvent)

    meta_type = "Meeting"
    schema = MeetingSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    minutes = atapi.ATFieldProperty('minutes')

    agenda = atapi.ATFieldProperty('agenda')


atapi.registerType(Meeting, PROJECTNAME)
