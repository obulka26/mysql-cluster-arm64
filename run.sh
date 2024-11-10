#!/bin/bash
#to fix Error while connecting to MySQL: 2008 (HY000): MySQL client ran out of memory Could not connect to database
ulimit -n unlimited #number of file descriptors(connections)
comments_per_thread=${comments_per_thread:-1000}
#echo ${comments_per_thread}
#echo $@
#echo ${empty_threads}
for num_threads in $@; do
  python3 paralel_load.py ${num_threads} ${comments_per_thread}
done
