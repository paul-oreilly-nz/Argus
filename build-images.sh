#!/bin/bash

build() {
	(cd $1; printf "\n\nBuilding $1\n"; ls; docker build . -t argus-$1:latest)
}

cd argus

build common
build caterpillar
build faker

cd presenter
build terminal
