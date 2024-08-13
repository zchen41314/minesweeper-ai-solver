#!/bin/bash

rm -rf Problems
mkdir Problems

python3 WorldGenerator.py 1000 Expert_world_ 16 30 99

echo Finished generating worlds!
