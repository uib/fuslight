fuslight
========

FUSLight is fast userswitching light, for Mac OS X

* Author: Kristian Botnen
* Email: kristian@mbmedia.no
* License: The MIT License

###Introduction:

* Want to be able to use fastuserswitching on your Mac, without exposing all local accounts? yes,
* Searched the web for fast user switching without listing available accounts, and found nothing useful? yes,

If you answered yes to all of the above questions you have been in the same situation as me, and maybe this little snippet can help you out.

###Future plans:

* provide package instructions
* provide snippet as native .app or similar

###Packaging:

```
$ pip install py2app
$ py2applet --make-setup fuslight.py
$ rm -rf build dist
$ python setup.py py2app
$ defaults write $(pwd)/dist/fuslight.app/Contents/Info.plist LSUIElement 1
```

* The defaults write tell the launchservices to treat the application as an agent, to avoid it to be present on the dock.
* If the "python setup.py py2app" step fails, see: https://bitbucket.org/ronaldoussoren/py2app/issue/137/py2app-problems-using-enthought-python

###Installation:

soon to come...

```
$
```
###Usage:

soon to come...
```
$
```

