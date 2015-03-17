# AXA-challenge
This is a part of team Villanova's final solution.
Created by Jiwei Liu and Xueer Chen

It generates solution with 0.90625 public LB

data is first cleaned by removing repeated points in the trip

usage:

python genfea.py    # generate features for all drivers
sh run.sh                 # run the model 16 times in parallel 
python combine.py # average the predictions

It takes about 4 hours in total.
