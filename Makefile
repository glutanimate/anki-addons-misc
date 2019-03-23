# Makefile for Anki add-ons
#
# Prepares zip file for upload to AnkiWeb
# 
# Copyright: (c) 2017-2018 Glutanimate <https://glutanimate.com/>
# License: GNU AGPLv3 <https://www.gnu.org/licenses/agpl.html>

all: clean zip

zip:
	./tools/build_zips.sh

ankiaddon:
	./tools/build_ankiaddon.sh

clean:
	rm -rf build
