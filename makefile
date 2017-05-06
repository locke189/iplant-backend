init:
    sudo python -m pip install -r requirements.txt
		sudo apt-get install mosquitto

test:
    nosetests tests
