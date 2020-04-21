CWD    = $(CURDIR)
MODULE = kbase
#$(notdir $(CWD))

NOW = $(shell date +%d%m%y)
REL = $(shell git rev-parse --short=4 HEAD)

PIP = $(CWD)/bin/pip3
PY  = $(CWD)/bin/python3

WGET = wget -c --no-check-certificate



.PHONY: all py
all: py

py: $(PY) app.py
	$^

#	$(MODULE).py $(MODULE).ini



.PHONY: install
install: $(PIP) js
	$(PIP) install    -r requirements.txt
	$(MAKE) requirements.txt

.PHONY: update
update: $(PIP)
	$(PIP) install -U -r requirements.txt
	$(MAKE) requirements.txt

$(PIP) $(PY):
	python3 -m venv .
	$(CWD)/bin/pip3 install -U pip pylint autopep8

.PHONY: requirements.txt
requirements.txt: $(PIP)
	$< freeze | grep -v 0.0.0 > $@

.PHONY: debian
debian:
	sudo apt update
	sudo apt install -u \
		python3 python3-venv \
		mariadb-server mariadb-client

.PHONY: js
js: static/jquery.js static/bootstrap.min.css static/bootstrap.min.js

JQUERY_VER = 3.4.1
static/jquery.js:
	$(WGET) -O $@ https://code.jquery.com/jquery-3.5.0.min.js

BOOTSTRAP_VER = $(JQUERY_VER)
BOOTSTRAP_URL = https://stackpath.bootstrapcdn.com/bootstrap/$(BOOTSTRAP_VER)/
static/bootstrap.min.css:
	$(WGET) -O $@ https://bootswatch.com/3/darkly/bootstrap.min.css
static/bootstrap.min.js:
	$(WGET) -O $@ $(BOOTSTRAP_URL)/js/bootstrap.min.js



.PHONY: master shadow release zip

MERGE  = Makefile README.md .gitignore .vscode
MERGE += requirements.txt *.py $(MODULE).* static templates

master:
	git checkout $@
	git checkout shadow -- $(MERGE)
shadow:
	git checkout $@

release:
	git tag $(NOW)-$(REL)
	git push -v && git push -v --tags
	git checkout shadow
