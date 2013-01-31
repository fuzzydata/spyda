#!/bin/bash

extract -f "title=#title-block h1" -f "content=article .entry-content" index.html | ./test_calais.py
