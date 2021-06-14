# define the name of the virtual environment directory
# Makefile
VENV := venv

all: install run

install: venv
	. $(VENV)/bin/activate && pip install -r requirements.txt

venv:
	# create venv if doesn't exist
	sudo apt-get install -y python3-venv
	test -d $(VENV) || python3 -m venv $(VENV)

run:
	./$(VENV)/bin/python3 submission.py

clean:
	rm -rf $(VENV)

.PHONY: all venv run clean
