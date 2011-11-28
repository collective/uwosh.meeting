This product helps you better manage all information related to meetings.


Before:
-------

Normally, meetings seem to happen like this:

- someone sends around an email on a topic, asking for a good date and time
  that works for everyone

- you get an email with the date and time that was agreed to; a location is
  still to be determined

- you get an email with the meeting location

- eventually an agenda gets emailed to all prospective attendees; documents to
  be discussed at the meeting are attached to this email

- the minutes of the meeting are sent around by email a day (or several) later

- possibly buried in the minutes: your action items, the date and time of the
  next meeting

When you try to piece together what happened at the last meeting, which
documents you reviewed at that meeting, and what you are on the hook for doing
by the next meeting... good luck finding it all in your inbox.


After:
------

Instead of having meeting-related information scattered across multiple email
messages and attachments, the Meeting content type puts everything in one
place:

- standard Plone Event content type attributes (date, time, location,
  attendees, iCal export, etc.)

- folderish so can contain attachments (documents)

- separate fields for agenda, minutes, action items, next meeting date/time

- ATBackRef-enabled links to previous and next Meeting objects so you can jump
  forward and backward in time to see what happened at previous meetings of
  your same working group

- optional email notification (one-time only or on every edit) to all
  attendees; email message contains all information (except attachments),
  including direct links to edit the Meeting object and add an attachment

- optional edit permission granted to all attendees

- integration with Solgema.fullcalendar view


Calendar Portlets
-----------------

To get Meeting objects to show on your calendar portlet: in the ZMI
of the site, go to portal_calendar -> Configure tab, then in the
"Portal Types to show in the calendar" list, Control-click or
Command-click the Meeting type so that both Event and Meeting types
are selected.  Then press Submit at the bottom of the page.

Remember: the calendar portlet will show only PUBLISHED items, as
per that Configure tab's default settings, so if you want a Meeting
(or an Event) to show up in the portlet, the Meeting or Event must
be published too.


Dependencies
------------

This product also depends on Products.ATBackRef to support
bidirectional relations between connected Meeting objects
(next/previous).  Add the following to your buildout.cfg eggs:

	Products.ATBackRef

and rerun bin/buildout.

If you'd like to view Meeting objects on a nice calendar view, install the
Solgema.fullcalendar product from

http://plone.org/products/solgema.fullcalendar

The uwosh.meeting product includes a view template that will be used by
Solgema.fullcalendar.


Credits
-------

I wish I could remember who it was at University of Wisconsin Oshkosh who
suggested this "killer app" for our Intranet project to me in person... Thank
you!


Miscellany
----------

- Code repository: https://github.com/collective/uwosh.meeting
- Questions and comments to nguyen@uwosh.edu
- Report bugs at https://github.com/collective/uwosh.meeting/issues
