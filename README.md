# Attendance Tracker
This web application can be used to track attendace by scanning barcodes with your smartphone camera.

A Python Flask backend is used to talk to a MySQL database and a React frontend is used to dynamically update the browser with information about attendance.

## Setup
1. Ensure you have Python 3 installed (project was developed using Python 3.6). Installation instructions are provided [here](http://docs.python-guide.org/en/latest/starting/installation/).
2. Ensure that you have `npm` installed.
3. Ensure you have `virtualenv` installed as a virtual environment will be needed to run the Flask server. Installation instructions can be found [here](https://virtualenv.pypa.io/en/stable/installation/).
4. Create a virtualenv in the root of the project and install requirements:
```
$ virtualenv -p python3 env
$ source env/bin/activate
$ pip install -r requirements.txt
```
5. Navigate to the static folder and install node dependencies:
```
$ cd app/static
$ npm install
```

## Usage
1. Initiate the Flask server (if no port parameter is provided it will be set to run on port 8000):
```
$ python app/server/app.py --hostname localhost --port 1234
```
2. Use the `watch` command to build the frontend assets and watch for changes:
```
$ cd app/static
$ npm run watch
```
3. Navigate to `localhost:port` to see the application.

## Running tests
1. Add the app to your python path:
$ export PYTHONPATH=$PYTHONPATH:/home/td/dev/barcode/attendance-tracker/app
2. Run the test
$ python mytest.py