VENV_DIR = .venv
PYTHON = python3
PIP = $(VENV_DIR)/bin/pip
UVICORN = $(VENV_DIR)/bin/uvicorn
PYTHON_VENV = $(VENV_DIR)/bin/python3

venv:
	$(PYTHON) -m venv $(VENV_DIR)

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:
	$(PYTHON_VENV) ./src/main.py

clean:
	rm -rf $(VENV_DIR) __pycache__

.PHONY: venv install run clean