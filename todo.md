> Reminder popup should be above all active windows if possible?

> Prevent multiple instances of app at one time
Consider siding, I think QSharedMemory doesn't work for Pyside any other ideas?

> pip/deb/windows installer testing

[Version 2]

> Google cals with api and social auth, (use the reminder from gcal not the event). Use
python social auth. Think about reccuring reminders


ISSUES

> When reminder is about to popup the ui briefly freezes, so this reminder should be in new thread?
Not sure. We only have one GUI thread, I'm not sure a second thread could show a reminder dialog anyway, only signal
to the main thread to show one...Would need a second GUI thread. It's kind of fine anyway that the popup blocks, it's modal
afterall, but why is there a brief pause of freeze before it actually shows?

> Sound alert doesnt work on my laptop, but beep doesnt even work in bash :(

> Not sure threads are properly being killed (ps aux|grep -i main.py)
  sometimes show it remaining and when this happens the reminder loop
  ends up running twice leading to double notifications etc

> If the app is min to sys tray and then a reminder messagebox launches it
  seems to quit the thread?? doing self.show() first on main window seems to resolve it



