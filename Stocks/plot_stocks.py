# Plots the stocks listed in data.csv

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

path = "C:\\Users\\Aritra Kar\\Desktop\\Python Projects\\data.csv"

def get_data(i):
    data = pd.read_csv(path)
    x = data['x_value']

    plt.cla()
    for stock in list(data.columns)[1:]:
        plt.plot(x, data[stock], label=stock.upper())
    
    plt.legend(loc='upper left')

# Real time graph plotting the stock prices
animate = FuncAnimation(plt.gcf(), get_data, interval=1000)

# Show the graph
plt.show()
