# Clock animated with Matplotlib.

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime

my_circle = plt.Circle((0,0), 0.25, color="black")

def update(i):
    now = datetime.now().strftime("%H:%M:%S")
    obj = list(map(lambda x: int(x), now.split(":")))
    original_seconds = obj[2]
    original_minutes = obj[1]
    original_hours = obj[0]
    
    #print(original_hours, original_minutes, original_seconds)
    seconds = (original_seconds / 60) * 360
    minutes = (original_minutes / 60) * 360 + (seconds / 60)
    hours = (original_hours % 12) * 30 + (minutes / 12)
    plt.cla()
    #print(hours, minutes, seconds, "\n")
    plt.title(now, color="white")
    plt.pie([hours, 360 - hours], radius=1, startangle=90, counterclock=False, colors=['#2bbcff','black'])
    plt.pie([minutes, 360 - minutes], radius=0.75, startangle=90, counterclock=False, colors=['#2b7cff','black'])
    plt.pie([seconds, 360 - seconds], radius=0.5, startangle=90, counterclock=False, colors=['#5b64b0','black'])
    
    #my_circle = plt.Circle((0,0), 0.25, color="black")
    plt.gcf().gca().add_artist(my_circle)

figure = plt.figure(figsize=(6,6), facecolor='black')
animate = FuncAnimation(figure, update, interval=1000)

plt.show()
