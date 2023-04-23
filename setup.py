# Hi There!
# This python script is written to
# install some python modules using
# pip. You can go through the code.

import subprocess
import sys


# Installing Function
def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])


# Installing python-chess
try:
    print("[GAME] Trying to import python-chess")
    import chess
except:
    print("[EXCEPTION] python-chess not installed")

    try:
        print("[GAME] Trying to install python-chess via pip")
        import pip

        install("python-chess")
        print("[GAME] python-chess has been installed")
    except:
        print("[EXCEPTION] Pip not installed on system")


# Installing flask
try:
    print("[GAME] Trying to import flask")
    import flask
except:
    print("[EXCEPTION] flask not installed")

    try:
        print("[GAME] Trying to install flask via pip")
        import pip

        install("flask")
        print("[GAME] flask has been installed")
    except:
        print("[EXCEPTION] Pip not installed on system")


# Installing webbrowser
try:
    print("[GAME] Trying to import webbrowser")
    import webbrowser
except:
    print("[EXCEPTION] webbrowser not installed")

    try:
        print("[GAME] Trying to install webbrowser via pip")
        import pip

        install("webbrowser")
        print("[GAME] webbrowser has been installed")
    except:
        print("[EXCEPTION] Pip not installed on system")
