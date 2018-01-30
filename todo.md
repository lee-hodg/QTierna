> Right click the row should also offer edit/remove menu

> Would be nice to have timezone as a search box and first letter shows relevant chocies, rather than massive
combo box. This would be LineEdit with signal textChanged .connect self.updateZones slot. Updating a listwidget
with a scrollbar...or something like that....

> Add completed tickbox to add/edit dlg. 

> Google cals with api and social auth

> Remove the hide complete tasks opts from preferences as we don't need it.

ISSUES

> Sound alert doesnt work on my laptop, but beep doesnt even work in bash :(

> Not sure threads are properly being killed (ps aux|grep -i main.py)
  sometimes show it remaining and when this happens the reminder loop
  ends up running twice leading to double notifications etc

> If the app is min to sys tray and then a reminder messagebox launches it
  seems to quit the thread?? doing self.show() first on main window seems to resolve it



