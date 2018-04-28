pyinstaller  --onefile --windowd --icon clock.ico --add-data "alarm_beep.wav;." main.py

Now just use innosetup to generate the setup.exe using the main.exe
