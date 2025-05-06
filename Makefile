build:
	pyinstaller --onefile magistri.py --collect-all=hy --collect-all=requests --collect-all=libmagistri

install-deps:
	pip install hy requests --user
