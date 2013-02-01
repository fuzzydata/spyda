#!/bin/bash

#spyda -p "https?\:\/\/app\.griffith\.edu\.au\/news\/[0-9]+\/[0-9]+\/[0-9]+\/.*" -a "https?\:\/\/app\.griffith\.edu\.au\/news\/[0-9]+\/[0-9]+\/.*"  http://app.griffith.edu.au/news/archives

extract -f "title=#title-block h1" -f "content=article .entry-content" index.html | ./test_calais.py
