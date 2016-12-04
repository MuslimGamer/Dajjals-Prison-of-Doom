rd /s /q build
rd /s /q dist
del *.spec
pyinstaller main.py
