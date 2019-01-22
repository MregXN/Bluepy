# Thunderboard with Bluepy
This is a python framework for reading thunderboards\` sensors date by bluepy
in init.py is a minimum code for reading single thunderboard date

## How to run it?

clone repo
```
$ git clone https://github.com/MregXN/bluepy.git
$ cd bluepy
```

create python3 virtual environment and activate it
```
$ python3 -m venv venv
$ source venv/bin/activate
```

install dependences in virtual environment, production dependences only:
```
$ pip install -r requirements.pip
```

set up bluetooth authority
```
$ sudo setcap 'cap_net_raw,cap_net_admin+eip' PATH/TO/BLUEPY/venv/lib/python3.7/site-packages/bluepy/bluepy-helper
```
run the code
python __init__.py
