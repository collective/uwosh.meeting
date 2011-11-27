import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.PloneTestCase import PloneTestCase


class TestUWOshMeeting(PloneTestCase.PloneTestCase):

    def testBackRefBackward(self):
        self.folder.invokeFactory('Meeting', 'Meeting1')
        self.folder.invokeFactory('Meeting', 'Meeting2')
        m1 = self.folder.Meeting1
        m2 = self.folder.Meeting2
        # set and check two-way reference
        m2.setPreviousMeeting(m1)
        self.assertEqual(m2.getPreviousMeeting(), m1)
        self.assertEqual(m1.getNextMeeting(), m2)
        # unset and check two-way reference
        m2.setPreviousMeeting(None)
        self.assertEqual(self.folder.Meeting2.getPreviousMeeting(), None)
        self.assertEqual(m1.getNextMeeting(), None)

    def testAttributes(self):
        from DateTime import DateTime
        pm = self.portal.portal_membership
        self.folder.invokeFactory('Meeting', 'Meeting3')
        m = self.folder.Meeting3
        pm.addMember('user2', 'secret', [], [])
        pm.addMember('user3', 'secret', [], [])

        m.setTitle('My Meeting Number Three')
        m.setDescription('a description')
        m.edit(text_format='plain',
            text='event body goes here',
            actionItems='actions go here',
            agenda='agenda goes here',
            contactEmail='test@testing.com',
            contactName='Buford T. Justice',
            attendeesCanEdit=True,
            attendees=['user2', 'user3', ],
            eventUrl='http://slashdot.org',
            location='The Big Conference Room',
            minutes='These are the minutes of the meeting',
            nextMeetingDateTime=DateTime('2020-01-01 10:00'),
            # vocabulary=['None', 'One-time only', 'On every edit',],
            notifyAttendeesByEmail='One-time only',
            startDate=DateTime('2012-02-02 11:00'),
            endDate=DateTime('2012-02-02 12:00'),
            )

        # should be 'One-time only' before processForm() call
        self.assertEqual(m.getNotifyAttendeesByEmail(), 'One-time only')
        self.assertEqual(m.Title(), 'My Meeting Number Three')
        self.assertEqual(m.Description(), 'a description')
        self.assertEqual(m.getText(), '<p>event body goes here</p>')
        self.assertEqual(m.getActionItems(), '<p>actions go here</p>')
        self.assertEqual(m.getAgenda(), '<p>agenda goes here</p>')
        self.assertEqual(m.contact_email(), 'test@testing.com')
        self.assertEqual(m.contact_name(), 'Buford T. Justice')
        self.assertEqual(m.getAttendeesCanEdit(), True)

        # cause the setting of Editor role for attendees
        m.processForm()

        # check that user has Editor role
        localRoles2 = m.get_local_roles_for_userid('user2')
        localRoles3 = m.get_local_roles_for_userid('user3')
        self.assertEqual('Editor' in localRoles2, True)
        self.assertEqual('Editor' in localRoles3, True)

        self.assertEqual(m.getAttendees(), ('user2', 'user3',))
        self.assertEqual(m.event_url(), 'http://slashdot.org')
        self.assertEqual(m.getLocation(), 'The Big Conference Room')
        self.assertEqual(m.getMinutes(),
            '<p>These are the minutes of the meeting</p>')
        self.assertEqual(m.getNextMeetingDateTime(),
            DateTime('2020-01-01 10:00'))
        # should be None after processForm() call
        self.assertEqual(m.getNotifyAttendeesByEmail(), 'None')
        self.assertEqual(m.startDate, DateTime('2012-02-02 11:00'))
        self.assertEqual(m.endDate, DateTime('2012-02-02 12:00'))

        # test removal of an attendee
        m.edit(attendees=['user2', ],)
        m.processForm()
        #import pdb; pdb.set_trace()
        localRoles2b = m.get_local_roles_for_userid('user2')
        localRoles3b = m.get_local_roles_for_userid('user3')
        self.assertEqual('Editor' in localRoles2b, True)
        self.assertEqual(localRoles3b, ())

    def testBackRefForward(self):
        self.folder.invokeFactory('Meeting', 'Meeting2')
        self.folder.invokeFactory('Meeting', 'Meeting3')
        m2 = self.folder.Meeting2
        m3 = self.folder.Meeting3
        m2.setNextMeeting(m3)
        self.assertEqual(m2.getNextMeeting(), m3)
        self.assertEqual(m3.getPreviousMeeting(), m2)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestUWOshMeeting))
    return suite

if __name__ == '__main__':
    framework()

