from jzsense.common.constants import *
from jzsense.js import *
from jzsense.scrappers.ds3 import *
from jzsense.converters.javascript import convert
import os                                                                   # Path joining.
import multiprocessing                                                      # Process multiple pages at a time.
# import DAZtoJSv3                                                            # Used to get documentation from old documentation website (zipped).
# from DAZtoJSv4 import *
from datetime import datetime                                               # Timestamp JzSense file because I'm lazy ._.
def main():
    FILE_NAME = "test_JzSense-V3.js"
    daz_objects = get_ds3_objects()
    results = []
    for object in daz_objects:
        try:
            results.append(process_object(object).dzObj)
        except AttributeError:
            continue
    with open(FILE_NAME, "w") as file:
        
        for result in results:
            json_doc = convert(result)
            file.write(json_doc + "\n")
    
    


# The default cube, ctrl + a, ctrl + c, wombo combo.
if __name__ == "__main__":
    # main()
    import timeit
    time_taken = timeit.timeit(main, number=1)
    print(f"Time Taken: {time_taken:.3f} seconds")