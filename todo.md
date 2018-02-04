> When user adds new reminder should switch to 'All' category to show it in the table

> When reminder is about to popup the ui briefly freezes, so this reminder should be in new thread

> Reminder popup should be above all active windows, and maybe a systray dialog would be cool too

> Sound alert???

> During the add a reminder clicking "Edit Categories" more than once seems to yield a bug
about rollback

> pip/deb/windows installer testing

> Google cals with api and social auth


ISSUES

> Sound alert doesnt work on my laptop, but beep doesnt even work in bash :(

> Not sure threads are properly being killed (ps aux|grep -i main.py)
  sometimes show it remaining and when this happens the reminder loop
  ends up running twice leading to double notifications etc

> If the app is min to sys tray and then a reminder messagebox launches it
  seems to quit the thread?? doing self.show() first on main window seems to resolve it



