import discord
from discord.ext import commands, tasks
import random
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
import pyautogui
import time
import random

def write_numbers():
   
    time.sleep(5)

    for i in range(10000):
        number = str(i).zfill(4)
        loc = random.choice(locations)
        x, y = loc
        pyautogui.moveTo(x, y)
        pyautogui.click()
        pyautogui.typewrite(number)
        print(f"Writing {number} at {x}, {y}")
        time.sleep(interval)

#  stuff to autoclick
locations = [(100, 250), (300, 250), (500, 250),(100, 330), (300, 330), (500, 330),(100, 400), (300, 400), (500, 400),(300, 480)]  
interval = 1  # time between each click
write_numbers()



