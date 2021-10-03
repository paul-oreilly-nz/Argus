#!/bin/bash

build() {
	(cd $1; printf "\n\nBuilding $1\n"; ls; docker build . -t argus-$1:latest)
}

build common
#build trickster
build caterpillar
#build janitor
#build reporter
build faker
#cd presenter
#build curses
