> Google cals with api and social auth
> Better styling/design maybe use layouts??
> Wiring up all the signals
> prefs, e.g. timezone and exit min to tray checkbox
> stop user fucking it up with various resizing
> validation
> Sound alert doesnt work on my laptop, but beep doesnt even work in bash :(

> Not sure threads are properly being killed (ps aux|grep -i main.py)
  sometimes show it remaining and when this happens the reminder loop
  ends up running twice leading to double notifications etc

> If the app is min to sys tray and then a reminder messagebox launches it
  seems to quit the thread?? doing self.show() first on main window seems to resolve it
