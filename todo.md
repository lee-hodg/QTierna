> Right-click row should offer add/edit/remove reminder actions....Use the same actions as the toolbar and main menu, I don't think any need to repeat those things

> pip/deb/windows installer testing

> Google cals with api and social auth


ISSUES

> Sound alert doesnt work on my laptop, but beep doesnt even work in bash :(

> Not sure threads are properly being killed (ps aux|grep -i main.py)
  sometimes show it remaining and when this happens the reminder loop
  ends up running twice leading to double notifications etc

> If the app is min to sys tray and then a reminder messagebox launches it
  seems to quit the thread?? doing self.show() first on main window seems to resolve it



