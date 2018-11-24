#!/bin/bash
g++ $(pkg-config --libs --cflags opencv) -o $1 $1.cpp
