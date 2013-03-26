#!/bin/bash

#crawl -p "https?\:\/\/app\.griffith\.edu\.au\/news\/[0-9]+\/[0-9]+\/[0-9]+\/.*" -a "https?\:\/\/app\.griffith\.edu\.au\/news\/[0-9]+\/[0-9]+\/.*" http://app.griffith.edu.au/news/archives

#extract -f "title=#title-block h1" -f "content=article .entry-content" index.html | ./test_calais.py

#crawl -p "https?\:\/\/app\.griffith\.edu\.au\/news\/[0-9]+\/[0-9]+\/[0-9]+\/.*" -a "https?\:\/\/app\.griffith\.edu\.au\/news\/[0-9]+\/[0-9]+\/.*" http://app.griffith.edu.au/news/archives -d 5 | extract -v -j 4 -f "title=#title-block h1" -f "content=article .entry-content" -o ./tmp --calais --calais-key="xgaxkzq96ep5rfjsptg4h3fm" -

crawl -p "https?\:\/\/app\.griffith\.edu\.au\/news\/[0-9]+\/[0-9]+\/[0-9]+\/.*" -a "https?\:\/\/app\.griffith\.edu\.au\/news\/[0-9]+\/[0-9]+\/.*" http://app.griffith.edu.au/news/archives > urls
