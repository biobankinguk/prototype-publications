
After cloning this repository, ensure that you have a Python3 installation, and then run the following:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

On windows: First make sure python 3 is installed and in your path
```
python -m venv venv
cd <wherever your virtual environment is>
Scripts\activate.bat
pip install -r requirements.txt
pip install -e .
```

The main function can then be run with
```
python manage.py runserver
```

To run the test suite using pytest
```
python manage.py test
```

To verify code style using pylint
```
pylint --load-plugins pylint_django europepmc
```

To contribute to this repository, please refer to `CONTRIBUTING.md`.

2020-03-13 
- This code was deployed on Azure using the information available at https://docs.microsoft.com/en-us/azure/app-service/containers/quickstart-python?toc=%2Fazure%2Fpython%2Ftoc.json&bc=%2Fazure%2Fpython%2Fbreadcrumb%2Ftoc.json&tabs=bash
- The command is az webapp up --sku F1 -n atlas-publications -l uksouth --subscription SV-ADAC-Biobanking-UK
