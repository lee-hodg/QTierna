> layouts for main window, prob treee on left with cats, all, done, work, shopping etc
solving the done pile prob
> finish model managers
> wire in cats picker dialog on add pop...some list with add/remove buttons


> Make the view/edit reminder dlg. It should be essentially just a mod of the AddDialog,
  but making it standard rather than dumb, so it accepts existing reminder
  and the save does UPDATE not INSERT. Enforce they select only 1 row at once

> Better styling/design maybe use layouts?? Resizing issues etc

> Right click the row should also offer edit/remove menu

> Ultimately we probably need 2 tables or 2 different widgets for the done/notdone pile as
sorting is a bitch and color coding isn't so clear

> The dialog offers choice of priority: high-priority, normal, low-priority (maybe this will be categories later
but for now this is easier)

> Time picker should init as now, and next to it there should be a QMenu with common choices, now, tomorrow, midnight etc

> If add dialog validation fails, it should launch the same dialog already partially complete

> Google cals with api and social auth

ISSUES

> Sound alert doesnt work on my laptop, but beep doesnt even work in bash :(

> Not sure threads are properly being killed (ps aux|grep -i main.py)
  sometimes show it remaining and when this happens the reminder loop
  ends up running twice leading to double notifications etc
> If the app is min to sys tray and then a reminder messagebox launches it
  seems to quit the thread?? doing self.show() first on main window seems to resolve it
> We need to truncate the reminder note "Take dog for walk and..." when it appears in table



