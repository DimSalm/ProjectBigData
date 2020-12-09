import pandas as pd
import numpy as np
from probables import CountMinSketch
import hyperloglog
from hashlib import sha1

files = list()
for number in range(46):
    files.append('C:/Users/dimsa/Desktop/ProjectBigData/twitter_world_cup_1m/tweets.json.'+str(number))
data = files[0:1]
