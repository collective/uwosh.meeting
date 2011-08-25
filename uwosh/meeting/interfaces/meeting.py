from zope.interface import Interface
# -*- Additional Imports Here -*-
from zope import schema

from uwosh.meeting import meetingMessageFactory as _



class IMeeting(Interface):
    """a content type that includes agenda and minutes rich text fields"""

#     # -*- schema definition goes here -*-
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

