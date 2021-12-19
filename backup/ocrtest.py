from timeit import timeit
from numpy.lib.function_base import average
import requests
import math
import numpy as np

def Time(iterations, name, url):
    def GetPage():
        requests.get(url)
    sumTime = 0
    averageTime = 0
    times = np.zeros(iterations, np.float64)
    for x in range(iterations):
        time = timeit(GetPage, number=1)
        times[x] = time
        sumTime += time
    averageTime = sumTime / iterations
    print(times)
    print(f"==========STATS FOR {name}==========")
    times = (times - averageTime) ** 2
    standardDev = math.sqrt(sum(times) / iterations)
    print(f'Average time taken: {"{:.4}".format(averageTime)} +/- {"{:.3}".format(standardDev)} seconds')
    

Time(15, "Google", "https://www.google.com")
Time(15, "Blackboard", "https://blackboard.waketech.edu/")
