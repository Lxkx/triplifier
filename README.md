# Triplifier

**Web interface application allowing to convert .csv files into .ttl files**

### 1. TO SET UP THE PROJECT

*1.1.1 ON MAC*

Be sure to have python, you can download the latest version on:
[Python.org](https://www.python.org/downloads/)

Create a virtual environment where you will store the dependencies:
```
python3 -m venv /path/to/new/virtual/environment
```

Switch to your new virtual environment using:
```
source /path/to/new/virtual/environment/bin/activate
```

Verify that you are using your new virtual environment created:
```
which pip 
```
--> This should show you your new path environment


*1.2 Install the dependencies:*
```
pip install -r /path/to/requirements.txt
```

### 2. CLONE THE PROJECT

Clone the project in the same folder as your environment for simplicity:
```
git clone https://github.com/Lxkx/triplifier.git
```



### 3. TO LAUNCH THE PROJECT

In your terminal, go inside the Django project folder
```
cd triplifier
```

Now, enter this command to run the Django server (be sure to have your virtual env activated):
```
python manage.py runserver
```
Finally, go in your web browser at [localhost port 8000](http://localhost:8000/)



