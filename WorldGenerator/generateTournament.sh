#!/bin/bash

rm -rf Worlds
mkdir Worlds

python3 WorldGenerator.py 1000 beginner_world_ 8 8 10
python3 WorldGenerator.py 1000 intermediate_world_ 16 16 40
python3 WorldGenerator.py 1000 expert_world_ 16 30 99

echo Finished generating worlds!
