BUILD_TARGETS = dist/menugen wheel

all: build

build: $(BUILD_TARGETS)

dist/menugen:
	poetry run pyinstaller -n menugen --onefile __main__.py

wheel:
	poetry build -f wheel

sdist:
	poetry build -f sdist

clean:
	rm -fr dist build menugen.spec

.PHONY: all build wheel clean
