from jzsense.common.constants import *                                      # Get constants. Don't think is necessary right now.
from jzsense.js import *                                                    # Get dataclasses.
from jzsense.scrappers.ds3 import *                                         # Scrap data from Daz Studio Version 3 Documentation.
from jzsense.scrappers.ds4 import *                                         # Scrap data from Daz Studio Version 4 Documentation.
from jzsense.converters.javascript import convert
from jzsense.converters import csv
import jsonpickle                                                           # Python Object <--> Json
import os                                                                   # Path joining.
import multiprocessing                                                      # Process multiple pages at a time.
import time                                                                 # Sleep on error.
from datetime import datetime                                               # Timestamp JzSense file because I'm lazy ._.
def main():
    FILE_NAME = "test_JzSense-V3.js"
    KNOWN_ERRORED_OBJS = {"DzComboBox", "DzScriptedRenderer", } # "DzRSLShader"
    daz_objects_v4 = get_ds4_objects()
    daz_objects_v3 = get_ds3_objects(daz_objects_v4)
    successful_results = []
    # for object_ in daz_objects_v4:
    #     try:
    #         if ProcessObject(object_):
    #             successful_results.append(object_)
    #     except AttributeError as e:
    #         print(f"An error occured while processing {object_}. REASON: {e}")
    #         errored_objs.append((object_, e))
    #         time.sleep(8)
    #         continue

    # for object_ in daz_objects_v3:
    #     try:
    #         if object_.name in KNOWN_ERRORED_OBJS: 
    #             print("break here.")
    #         if process_object(object_):
    #             successful_results.append(object_)
    #     except Exception as e:
    #         print(f"Something went wrong while processing v3: {object_}. REASON: {e}")

    #         # after renderNode()
    #         errored_objs.append((object_, e))
    #         time.sleep(8)
    #         continue

    # Issues with JSType. references.
    with open("test.json", "r") as f:
        a = f.read()
        JSType.types = jsonpickle.decode(a)
    errored_objs = []

    print("===============\n===============ERRORS\n===============\n===============")
    for errored_object, error_msg in errored_objs:
        print(f"Errored Object: {errored_object} | Errored Message: {error_msg}")

    # Just in case it doesnt work.
    for error in errored_objs:
        print(f"Errored Object: {error[0]} | Message: {error[1]}")

    print("Writing to disk...")
    
    with open(FILE_NAME, "wb") as file:
        for result in successful_results:
            json_doc = convert(result)
            file.write(bytes(json_doc,"utf-8","replace") + b"\n")

    # Write to csv.
    with open("test.csv", "wb") as file:
        # Header
        file.write(b"Object Name,Symbol Type,Symbol Name,Documentation / Misc,Additional Info\n")
        for result in successful_results:
            info = csv.convert(result)
            if len(info.strip()) != 0:
                file.write(bytes(info,"utf-8","replace") + b"\n")
    
    # Write to json
    with open("test.json", "wb") as file:
        # Convert to bytes.
        b = bytes(jsonpickle.encode(JSType.types),"utf-8",errors="replace")
        file.write(b)
    

    

# The default cube, ctrl + a, ctrl + c, wombo combo.
if __name__ == "__main__":
    # main()
    import timeit
    time_taken = timeit.timeit(main, number=1)
    print(f"Time Taken: {time_taken:.3f} seconds")