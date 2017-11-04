all: requirements

env:
	virtualenv -p python3 env
	echo "export PYTHONPATH=$$PYTHONPATH:$$PWD/app" >> env/bin/activate

requirements: env
	./env/bin/pip install -r ./etc/requirements.txt

exportpath:
	source env/bin/activate
	export PYTHONPATH:$PWD/app