# builds zip files for AnkiWeb

all: zip

zip:
	./tools/build_zips.sh

clean:
	rm -rf build