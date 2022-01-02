from jzsense.common.constants import *
from jzsense.js import *
from jzsense.scrappers.ds4 import *
from jzsense.converters.javascript import convert
import os                                                                   # Path joining.
import multiprocessing                                                      # Process multiple pages at a time.
# import DAZtoJSv3                                                            # Used to get documentation from old documentation website (zipped).
# from DAZtoJSv4 import *
from datetime import datetime                                               # Timestamp JzSense file because I'm lazy ._.
def main():
    daz_objects = get_ds4_objects()

    # Multiprocessing code: hasn't been tested.
    # with multiprocessing.Pool(10) as p:
    #     results = p.map(ProcessObject, daz_objects)
    
    # Better for debugging or just doing it on one CPU.
    results = []
    for object in daz_objects:
        try:
            results.append(ProcessObject(object).dzObj)
        except AttributeError:
            continue
    # Now call DAZtoJSv3 and get the objects. We don't need to update same classes with OLD info pass in DzObjects already created.
    # processedClasses = DAZtoJSv3.BeginWork()
    # Write to file.
    fileLocation = os.path.join(os.getcwd(),f"test_{JS_NAME}")
    with open(fileLocation, "ab+") as file:
        totalStr = bytes()
        # results.extend(processedClasses) # Add  v3 documentation.
        for dazObj in results:
            json_doc = convert(dazObj)
            file.write(str.encode(json_doc, "utf-8"))
        file.write(b"\n" + totalStr)
        file.close()
    # Print a victory message!
    print("JzIntellisense.js complete!\n=================================================\n=================================================\n\n")
    print("ERRORED ENUMS\n")
    for error in ERRORED_ENUMS:
        print(error,end="\n")
    print("\nSKIPPED DZOBJS\n")
    for obj in SKIPPED_DZOBJS:
        print(obj,end="\n")

# The default cube, ctrl + a, ctrl + c, wombo combo.
if __name__ == "__main__":
    main()