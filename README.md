# Attendance Tracker
This web application can be used to track attendace by scanning barcodes with your smartphone camera.

A Python Flask backend is being used to talk to a MySQL database and a React frontend is being used to dynamically update the browser with information about attendance.

## Setup
1. Ensure you have Python 3 installed (project was developed using Python 3.6). Installation instructions are provided [here](http://docs.python-guide.org/en/latest/starting/installation/).
1. Ensure you have `virtualenv` installed as a virtual environment will be needed to run the Flask server. Installation instructions can be found [here](https://virtualenv.pypa.io/en/stable/installation/).
2. Create a virtualenv in the root of the project and install requirements:
```
$ virtualenv -p python3 env
$ source env/bin/activate
$ pip install -r requirements.txt
```
3. Navigate to the static folder and install node dependencies:
```
$ cd app/static
$ npm install
```

## Usage
1. Initiate the Flask server (if no port parameter is provided it will be set to run on port 5000):
```
$ python app/server/app.py 1234
```
2. Use the `watch` command to build the frontend assets and watch for changes:
```
$ cd app/static
$ npm run watch
```
3. Navigate to `localhost:port` to see the application.