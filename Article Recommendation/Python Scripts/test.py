import pandas as pd
import numpy as np

wp = pd.read_csv("../Sample Data/WP-7-9.csv")
ad = pd.read_csv("../Sample Data/Adobe article temp pages4.11-7.9.csv")

ad['Page'] = ad['Page'] + "/"
