"""Definition of the Meeting content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import document
from Products.ATContentTypes.content import event
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.configuration import zconf
from Products.CMFCore.utils import getToolByName

# -*- Message Factory Imported Here -*-
from uwosh.meeting import meetingMessageFactory as _

from uwosh.meeting.interfaces import IMeeting
from uwosh.meeting.config import PROJECTNAME

from Products.ATBackRef.backref import BackReferenceWidget, BackReferenceBrowserWidget, BackReferenceField
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget \
     import ReferenceBrowserWidget

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
            rows = 40,
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
            rows = 40,
            allow_file_upload = zconf.ATDocument.allow_document_upload,
        ),
    ),

    atapi.TextField(
        'actionItems',
        required=False,
        searchable=True,
        storage=atapi.AnnotationStorage(),
        validators = ('isTidyHtmlWithCleanup',),
        default_output_type = 'text/x-html-safe',
        allowable_content_types=('text/plain', 'text/structured', 'text/html',
                                 'application/msword'),
        widget=atapi.RichWidget(
            label=_(u"Action Items"),
            description=_(u"things to do for the next meeting"),
            rows = 20,
            allow_file_upload = zconf.ATDocument.allow_document_upload,
        ),
    ),

    atapi.DateTimeField(
        'nextMeetingDateTime',
        storage=atapi.AnnotationStorage(),
        widget=atapi.CalendarWidget(
            label=_(u"Next Meeting Date and Time"),
            description=_(u"Field description"),
        ),
        validators=('isValidDate'),
    ),


    atapi.BooleanField(
        'attendeesCanEdit',
        storage=atapi.AnnotationStorage(),
        widget=atapi.BooleanWidget(
            label=_(u"Allow Attendees to Edit?"),
            description=_(u"If checked, allows listed attendees to edit this Meeting object and add/edit contained items"),
        ),
        default=True,
    ),

    atapi.StringField(
        'notifyAttendeesByEmail',
        storage=atapi.AnnotationStorage(),
        widget=atapi.SelectionWidget(
            label=_(u"Notify Attendees by Email?"),
            description=_(u"Select which type of email notification to send to listed attendees"),
        ),
        required=True,
        default=_(u"None"),
        vocabulary=['None', 'One-time only', 'On every edit',],
    ),

    atapi.ReferenceField(
        name='previousMeeting',
        widget=atapi.ReferenceWidget(
            label='Previous Meeting',
        ),
        allowed_types=('Meeting',),
        multiValued=0,
        relationship='previous_meeting'
    ),

    BackReferenceField(
        name='nextMeeting',
        widget=BackReferenceWidget(
        #widget=BackReferenceBrowserWidget(
            label='Next Meeting',
        ),
        allowed_types=('Meeting',),
        multiValued=0,
        relationship='previous_meeting'
    ),

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

MeetingSchema['title'].storage = atapi.AnnotationStorage()
MeetingSchema['description'].storage = atapi.AnnotationStorage()
MeetingSchema['description'].widget.label = _(u'label_summary', default=u'Summary')
MeetingSchema['contactName'].default_method = "getDefaultContactName"
MeetingSchema['contactEmail'].default_method = "getDefaultContactEmail"
MeetingSchema['contactPhone'].default_method = "getDefaultContactPhone"

schemata.finalizeATCTSchema(
    MeetingSchema,
    folderish=True,
    moveDiscussion=False
)

# finalizeATCTSchema moves 'location' into 'categories', we move it back:
MeetingSchema.changeSchemataForField('location', 'default')
MeetingSchema.moveField('location', before='startDate')
MeetingSchema.changeSchemataForField('relatedItems', 'default')
MeetingSchema['relatedItems'].widget.visible['edit'] = 'visible'
MeetingSchema['relatedItems'].widget.visible['view'] = 'visible'
MeetingSchema.changeSchemataForField('allowDiscussion', 'default')

class Meeting(folder.ATFolder, document.ATDocument, event.ATEvent):
    """a content type that includes agenda and minutes rich text fields"""
    implements(IMeeting, document.IATDocument, document.IDAVAware, event.IATEvent)

    meta_type = "Meeting"
    schema = MeetingSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    nextMeetingDateTime = atapi.ATFieldProperty('nextMeetingDateTime')

    notifyAttendeesByEmail = atapi.ATFieldProperty('notifyAttendeesByEmail')

    attendeesCanEdit = atapi.ATFieldProperty('attendeesCanEdit')

    actionItems = atapi.ATFieldProperty('actionItems')

    minutes = atapi.ATFieldProperty('minutes')

    agenda = atapi.ATFieldProperty('agenda')

    def getDefaultContactName(self):
        pm = getToolByName(self, 'portal_membership', None)
        if pm:
            m = pm.getAuthenticatedMember()
            return m.getProperty('fullname', '')

    def getDefaultContactEmail(self):
        pm = getToolByName(self, 'portal_membership', None)
        if pm:
            m = pm.getAuthenticatedMember()
            return m.getProperty('email', '')

    def getDefaultContactPhone(self):
        pass

def meetingSendEmailNotification(obj, event):
    if obj.notifyAttendeesByEmail <> 'None':
        if len(obj.attendees) > 0:
            mh = getToolByName(obj, 'MailHost', None)
            if mh:
                pm = getToolByName(obj, 'portal_membership', None)
                if pm:
                    m = pm.getAuthenticatedMember()
                    mEmail = m.getProperty('email', None)
                    mName = m.getProperty('fullname', None)
                    if not mName:
                        mName = '<unknown name>'
                    if mEmail:
                        mMsg = """
%s has shared the following meeting with you:

Title:       %s

Summary:     %s

%s

From:        %s

To:          %s

Location:    %s

Contact:     %s (%s %s)

Info URL:    %s

Attendees:   %s

Agenda:      %s

Minutes:     %s

Meeting URL: %s

%s

%s

Action Items: %s

Next Meeting: %s

Prev Meeting URL: %s

Next Meeting URL: %s
"""
                        obj_url = obj.absolute_url()
                        canAttachMessage = ("Click to add or upload attachments: %s/createObject?type_name=File" % obj_url) if obj.attendeesCanEdit else ""
                        mSubj = '%s has invited you to a meeting ("%s")' % (mName, obj.Title())
                        attachmentsListing = "\n\n".join([attachment.absolute_url() for attachment in obj.listFolderContents()])
                        if attachmentsListing:
                            attachmentsListing = "Attachments:\n\n" + attachmentsListing

                        # handle potential unicode problems
                        cleanMinutes = ''.join([x for x in obj.getMinutes(mimetype = 'text/plain') if ord(x) < 128])
                        cleanActionItems = ''.join([x for x in obj.getActionItems(mimetype = 'text/plain') if ord(x) < 128])
                        cleanAgenda = ''.join([x for x in obj.getAgenda(mimetype = 'text/plain') if ord(x) < 128])
                        cleanText = ''.join([x for x in obj.getText(mimetype = 'text/plain') if ord(x) < 128])

                        previousMeetingUrl = ''
                        previousMeetingAttr = obj.getPreviousMeeting()
                        if previousMeetingAttr:
                            previousMeetingUrl = previousMeetingAttr.absolute_url()

                        nextMeetingUrl = ''
                        nextMeetingAttr = obj.getNextMeeting()
                        if nextMeetingAttr:
                            nextMeetingUrl = nextMeetingAttr.absolute_url()

                        message = mMsg % (mName, obj.Title(),
                            obj.Description(), cleanText, obj.start(), obj.end(),
                            obj.getLocation(), obj.contact_name(),
                            obj.contact_phone(), obj.contact_email(),
                            obj.event_url(), 
                            ", ".join(["%s (%s / %s)" % 
                                (pm.getMemberById(a).getProperty('fullname'), a, 
                                 pm.getMemberById(a).getProperty('email')) for a in obj.attendees]),
                            cleanAgenda, cleanMinutes, obj_url,
                            attachmentsListing, canAttachMessage,
                            cleanActionItems, obj.getNextMeetingDateTime(),
                            previousMeetingUrl, nextMeetingUrl)

                        mFrom = mEmail
                        for attendee in obj.attendees:
                            member = pm.getMemberById(attendee)
                            if member:
                                mTo = member.getProperty('email', None)
                                if mTo:
                                    mh.send(message, mTo, mFrom, mSubj)
        # reset one-time email notification
        if obj.notifyAttendeesByEmail == 'One-time only':
            obj.notifyAttendeesByEmail = 'None'
                                
def meetingSetEditorRole(obj, event):
    #import pdb;pdb.set_trace()
    if not obj.attendeesCanEdit:
        # remove all attendees' Editor role
        # get_local_roles() return sequence like ( ("userid1", ("rolename1", "rolename2")), ("userid2", ("rolename1") )
        for attendee in obj.attendees:
            for userid, useridRoles in obj.get_local_roles():
                if 'Editor' in useridRoles and attendee == userid:
                    newUseridRoles = [r for r in useridRoles if r <> 'Editor']
                    if not newUseridRoles:
                        obj.manage_delLocalRoles([attendee])
                    else:
                        obj.manage_setLocalRoles(attendee, newUseridRoles)
    else:
        # remove Editor role from people who are not attendees (in case an attendee was removed)
        attendees = obj.attendees
        for userid, useridRoles in obj.get_local_roles():
            if 'Editor' in useridRoles and userid not in attendees:
                newUseridRoles = [r for r in useridRoles if r <> 'Editor']
                if not newUseridRoles:
                    obj.manage_delLocalRoles([userid])
                else:
                    obj.manage_setLocalRoles(userid, newUseridRoles)
        # add Editor role for attendees if they don't already have it
        pm = getToolByName(obj, 'portal_membership', None)
        if pm:
            for attendee in obj.attendees:
                m = pm.getMemberById(attendee)
                if m:
                    mRoles = obj.get_local_roles_for_userid(m.id)
                    if 'Editor' not in mRoles:
                        newRoles = mRoles + ('Editor', )
                        obj.manage_setLocalRoles(m.id, newRoles)
                    
                    


def meetingInitialized(obj, event):
    meetingSendEmailNotification(obj, event)
    meetingSetEditorRole(obj, event)
    
def meetingEdited(obj, event):
    meetingSendEmailNotification(obj, event)
    meetingSetEditorRole(obj, event)


atapi.registerType(Meeting, PROJECTNAME)
