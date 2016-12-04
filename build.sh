rm -rf build
rm -rf dist
rm *.spec
pyinstaller main.py --onefile
