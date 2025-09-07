PYTHON ?= python3
PIP := $(PYTHON) -m pip
PYINSTALLER := $(PYTHON) -m PyInstaller

ICON_LINUX := resources/icon.png
ICON_WINDOWS := resources/icon.ico
DIST_DIR := dist

UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Linux)
	OS := linux
endif
ifeq ($(UNAME_S),Darwin)
	OS := mac
endif
ifeq ($(OS),)
	ifeq ($(OS),Windows_NT)
		OS := windows
	endif
endif

.PHONY: all deps clean build

all: deps build

deps:
	@echo "Installing dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install pyinstaller

build:
ifeq ($(OS),linux)
	@echo "Building Linux ELF..."
	$(PYINSTALLER) --onefile run.py --icon=$(ICON_LINUX)
endif
ifeq ($(OS),windows)
	@echo "Building Windows EXE..."
	$(PYINSTALLER) --onefile run.py --icon=$(ICON_WINDOWS)
endif
ifeq ($(OS),mac)
	@echo "Building macOS App..."
	$(PYINSTALLER) --onefile run.py --icon=$(ICON_LINUX)
endif

build-linux:
	$(PYINSTALLER) --onefile run.py --icon=$(ICON_LINUX)

build-windows:
	$(PYINSTALLER) --onefile run.py --icon=$(ICON_WINDOWS)

clean:
	@echo "Cleaning build artifacts..."
	rm -rf build $(DIST_DIR) *.spec
