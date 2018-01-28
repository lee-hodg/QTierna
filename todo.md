> Google cals with api and social auth
> Better styling/design maybe use layouts??
> Wiring up all the signals
> prefs, e.g. timezone and exit min to tray checkbox
> stop user fucking it up with various resizing
> Sound alert doesnt work on my laptop, but beep doesnt even work in bash :(
> Not sure threads are properly being killed (ps aux|grep -i main.py)
  sometimes show it remaining and when this happens the reminder loop
  ends up running twice leading to double notifications etc
> If the app is min to sys tray and then a reminder messagebox launches it
  seems to quit the thread?? doing self.show() first on main window seems to resolve it
> We need to truncate the reminder note "Take dog for walk and..." when it appears in table
> There should be view/edit reminder dialog (same thing but different buttons)
> Right click the row should also offer edit/remove
> Ultimately we probably need 2 tables or 2 different widgets for the done/notdone pile as
sorting is a bitch and color coding isn't so clear
> The dialog offers choice of priority: high-priority, normal, low-priority (maybe this will be categories later
but for now this is easier)
> Time picker should init as now, and next to it there should be a QMenu with common choices, now, tomorrow, midnight etc
> If add dialog validation fails, it should launch the same dialog already partially complete


