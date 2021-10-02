#!/bin/bash

build() {
	(cd $1; printf "\n\nFull Rebuild of $1\n"; ls; docker build --no-cache . -t argus-$1:latest)
}

build common
build trickster
build caterpillar
build janitor
build reporter
cd presenter
build curses
