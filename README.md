
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

To contribute to this repository, please use separate branches for 
development of each feature, and use the Pull Request system rather
than merging directly into `master`.
