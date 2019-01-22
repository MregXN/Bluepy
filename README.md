<<<<<<< HEAD
# Thunderboard with Bluepy
This is a python framework for reading thunderboards\` sensors date by bluepy

* H
* Dockerfile setup
* User space infrastructure
* How test embedded with PyTest and Coverage
* Logging setup with LOGGING_LEVEL in ENV
* Create a basic backend api with `Flask`
* APScheduler embedded as task manager, and import its api
* Use Socket.io

# How to run it?

clone repo
```
$ git clone https://github.com/cpnetx/hexagon-getstarted-python.git
$ cd hexagon-getstarted-python
```
## API

enter `api` directory
```
$ cd api
$ cd deluxe
```

create python3 virtual environment and activate it
```
$ python3 -m venv venv
$ source venv/bin/activate
```

install dependences in virtual environment, production dependences only:
```
$ pip install -r requirements.pip
$ sudo setcap 'cap_net_raw,cap_net_admin+eip' PATH/TO/BLUEPY/venv/lib/python3.7/site-packages/bluepy/bluepy-helper
```

get a redis server running on port 6379 (the approach varies)
```
$ docker start h-redis
or
$ docker run --name h-redis -p 127.0.0.1:6379:6379 -d redis:alpine
```

create a `usr` folder
```
$ mkdir -p ../usr
```

run in development mode
```
$ FLASK_ENV=development FLASK_APP=app flask run -p 3200 --no-reload
```

run tests
```
$ pytest -s
```

## UI

Install NodeJS, latest LTS is recommended. Recommend using [n](https://github.com/tj/n). [Yarn](https://yarnpkg.com/) is also required.

enter `ui` directory
```
$ cd ui
```

install dependences
```
$ yarn install
```

run SPA develop server
```
$ yarn run serve
```

Then try it on `http://localhost:3201`

build app (docker image)
```
$ cd ..
$ make dist
$ make app
```

run the app in production mode (docker) with h-redis runnig
```
$ docker run -d --name=h-thunderboard -v /var/vertex/appdata/h-thunderboard:/code/usr cpnet/hexagon-thunderboard:develop-amd64
```



sudo setcap 'cap_net_raw,cap_net_admin+eip' PATH/TO/BLUEPY/venv/lib/python3.7/site-packages/bluepy/bluepy-helper
=======
# bluepy
>>>>>>> 582a8f73db4f377826b7c2638d9c51c09c5c71fa
