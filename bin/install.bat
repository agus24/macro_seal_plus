set mypath=%0..\..\

@echo "DOWNLOADING PYTHON"
bitsadmin /transfer "Download Python" https://www.python.org/ftp/python/3.7.9/python-3.7.9-amd64.exe %mypath%.\python_installer.exe
%mypath%python_installer.exe
C:\users\%USERNAME%\AppData\Local\Programs\Python\Python37\python -m pip install -r %mypath%..\requirements.txt
DEL %mypath%python_installer.exe
pause
