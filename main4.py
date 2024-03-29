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
    FILE_NAME = "DzIntellisense.js"
    KNOWN_ERRORED_OBJS = {"DzComboBox", "DzScriptedRenderer", } # "DzRSLShader"
    daz_objects_v4 = get_ds4_objects()
    daz_objects_v3 = get_ds3_objects(daz_objects_v4)
    successful_results = []
    errored_objs = []
    for object_ in daz_objects_v4:
        try:
            if ProcessObject(object_):
                successful_results.append(object_)
        except AttributeError as e:
            print(f"An error occured while processing {object_}. REASON: {e}")
            errored_objs.append((object_, e))
            time.sleep(8)
            continue

    for object_ in daz_objects_v3:
        try:
            if object_.name in KNOWN_ERRORED_OBJS:
                print("break here.")
            if process_object(object_):
                successful_results.append(object_)
        except Exception as e:
            print(f"Something went wrong while processing v3: {object_}. REASON: {e}")

            # after renderNode()
            errored_objs.append((object_, e))
            time.sleep(8)
            continue

    print("===============ERRORS===============")
    for errored_object, error_msg in errored_objs:
        print(f"Errored Object: {errored_object} | Errored Message: {error_msg}")

    # Just in case it doesnt work.
    # for error in errored_objs:
    #     print(f"Errored Object: {error[0]} | Message: {error[1]}")
    print("====================================")
    print("Writing to disk...")

    # Write js file.
    with open(FILE_NAME, "wb") as file:
        TODAYSDATE = datetime.date(datetime.now()).strftime("%B %d, %Y")
        HEADER = f"""// LAST UPDATED: {TODAYSDATE}
//                                       This script has been auto-generated by TheRealSolly | Solomon Blount.
// The following contents is all directly imported from DAZ's Documentation Website and inherits the license set, which is the following...
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Attribution 3.0 Unported (CC BY 3.0) | https://creativecommons.org/licenses/by/3.0/ | (C) Daz Productions, Inc 224 S 200 W, Salt Lake City, UT 84101
// I DO NOT WORK FOR DAZ PRODUCTIONS INC AND THIS SCRIPT WAS NOT SUPPORTED BY OR ENDORSED BY ANYONE AT DAZ PRODUCTIONS INC.
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// If I made your life wonderful, if you're feeling generious enough to donate to make me feel wonderful, you can do so by going here:
//                                                         https://www.buymeacoffee.com/therealsoll
// Anyway, here are some things you need to know.
//                                                   THIS VERSION ALSO DOES NOT INCLUDE ECMASCRIPT CLASSES
//                                                THIS FILE MAY SHOW ERRORS - IT IS PERFECTLY FINE. PLEASE IGNORE.
//                                             THIS HAS ONLY BEEN TESTED ON VISUAL STUDIO CODE VERSION 1.55.0 - 1.74.0
//
// To make .dsa scripts use the JS/TS interpreter, create a new file with the .dsa extension, on the lower-right of VSCode click on the file type and select "Configure file assocations for .dsa" and then select in JavaScript.
// JzSense now includes v3 Documentation to fill in missing classes from v4 documentation.
// Do not select TS as the interpreted language. Use JS.
// There will be more adjustments to this script but i'm in school...so yeah.
// To check and see if there are any updates, please go here: https://github.com/siblount/JzSense
// If you wish to work on the code that generates this file, you can contribute here at: https://github.com/siblount/JzSense-Generator
// Happy Coding!
"""
        file.write(HEADER.encode("utf-8"))
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
        b = bytes(jsonpickle.encode(successful_results),"utf-8",errors="replace")
        file.write(b)
    

    

# The default cube, ctrl + a, ctrl + c, wombo combo.
if __name__ == "__main__":
    # main()
    import timeit
    time_taken = timeit.timeit(main, number=1)
    print(f"Time Taken: {time_taken:.3f} seconds")