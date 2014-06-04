$(eval VERSION := $(shell python setup.py --version))
SDIST := dist/cloudmetrics-$(VERSION).tar.gz

all: build

build: $(SDIST)

$(SDIST):
	python setup.py sdist
	rm -rf cloudmetrics.egg-info

.PHONY: install
install: $(SDIST)
	sudo pip install $(SDIST)

.PHONY: uninstall
uninstall:
	sudo pip uninstall cloudmetrics

.PHONY: register
register:
	python setup.py register

.PHONY: upload
upload:
	python setup.py sdist upload
	rm -rf cloudmetrics.egg-info

.PHONY: clean
clean:
	rm -rf dist cloudmetrics.egg cloudmetrics.egg-info
