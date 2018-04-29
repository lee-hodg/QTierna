pyinstaller  --onefile --windowd --icon clock.ico --add-data "alarm_beep.wav;." main.py

Now just use innosetup to generate the setup.exe using the main.exe

## Ubuntu

For a deb:
    apt-file update
    python setup.py --command-packages=stdeb.command bdist_deb

https://stackoverflow.com/questions/17401381/debianzing-a-python-program-to-get-a-deb

The `apt-file update` is because we have `install_requires`
