#!/bin/bash
# Grabs and kill a process from the pidlist that has the word myapp

for pid in `ps aux | grep seyren | awk '{print $2}'`
do
  kill -9 $pid
done
