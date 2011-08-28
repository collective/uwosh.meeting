from zope.interface import Interface
# -*- Additional Imports Here -*-
from zope import schema

from uwosh.meeting import meetingMessageFactory as _



class IMeeting(Interface):
    """a content type that includes agenda and minutes rich text fields"""

#     # -*- schema definition goes here -*-
    notifyAttendeesByEmail = schema.TextLine(
        title=_(u"Notify Attendees by Email?"),
        required=True,
        description=_(u"Select which type of email notification to send to listed attendees"),
    )
#
    attendeesCanEdit = schema.Bool(
        title=_(u"'Allow Attendees to Edit?'"),
        required=False,
        description=_(u"'If checked, allows listed attendees to edit this Meeting object and add/edit contained items'"),
    )
#
#     minutes = schema.Text(
#         title=_(u"Minutes"),
#         required=False,
#         description=_(u"enter the minutes of the meeting here"),
#     )
# #
    agenda = schema.Text(
        title=_(u"Agenda"),
        required=False,
        description=_(u"enter the agenda for the meeting here"),
    )

