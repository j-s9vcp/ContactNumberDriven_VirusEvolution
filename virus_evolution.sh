#!/bin/bash

n_processes=4
max_duration=1000
d50=1000000
dk=7.5
iteration=500

echo `date`

python vi_amount.py --max_duration $max_duration --n_processes $n_processes

python inf_id_search.py --d50 $d50 --dk $dk --max_duration $max_duration --n_processes $n_processes

python vi_amount_include_inf.py --max_duration $max_duration --n_processes $n_processes

python main.py --iteration $iteration --max_duration $max_duration --n_processes $n_processes

echo `date`