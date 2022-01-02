from jzsense.common.constants import *
from jzsense.js import *
from jzsense.scrappers.ds4 import *

import os                                                                   # Path joining.
import multiprocessing                                                      # Process multiple pages at a time.
# import DAZtoJSv3                                                            # Used to get documentation from old documentation website (zipped).
# from DAZtoJSv4 import *
from datetime import datetime                                               # Timestamp JzSense file because I'm lazy ._.
def main():
    daz_objects = get_ds4_objects()

    # with multiprocessing.Pool(10) as p:
    #     results = p.map(ProcessObject, daz_objects)
    # Better for debugging or just doing it on one CPU.
    results = []
    for object in daz_objects:
        results.append(ProcessObject(object))
    # Now call DAZtoJSv3 and get the objects. We don't need to update same classes with OLD info pass in DzObjects already created.
    # processedClasses = DAZtoJSv3.BeginWork()
    # Write to file.
    fileLocation = os.path.join(os.getcwd(),JS_NAME)
    with open(fileLocation, "ab+") as file:
        if file.tell() == 0:
            TODAYSDATE = datetime.date(datetime.now()).strftime("%B %d, %Y")
            HEADER = f"""// LAST UPDATED: {TODAYSDATE}
// This script has been auto-generated by TheRealSolly | Solomon Blount.
// The following contents is all directly imported from DAZ's Documentation Website and inherits the license set, which is the following...
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Attribution 3.0 Unported (CC BY 3.0) | https://creativecommons.org/licenses/by/3.0/ | (C) Daz Productions, Inc 224 S 200 W, Salt Lake City, UT 84101
// I DO NOT WORK FOR DAZ PRODUCTIONS INC AND THIS SCRIPT WAS NOT SUPPORTED BY OR ENDORSED BY ANYONE AT DAZ PRODUCTIONS INC.
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// If I made your life wonderful, if you're feeling generious enough to donate to make me feel wonderful, you can do so by going here:
//                                                         https://www.buymeacoffee.com/therealsoll
// Anyway, here are some things you need to know.
//                                                   THIS VERSION ALSO DOES NOT INCLUDE ECMASCRIPT CLASSES
//                                     THIS FILE PURPOSEFULLY HAS ERRORS SO THE INTELLISENSE CAN ASSIST YOU WITH YOUR CODE.
//                                             THIS HAS ONLY BEEN TESTED ON VISUAL STUDIO CODE VERSION 1.55.0.
//
// To make .dsa scripts use the JS/TS interpreter, create a new file with the .dsa extension, on the lower-right of VSCode click on the file type and select "Configure file assocations for .dsa" and then select in JavaScript.
// JzSense now includes v3 Documentation to fill in missing classes from v4 documentation.
// Do not select TS as the interpreted language. Use JS.
// There will be more adjustments to this script but i'm in school...so yeah.
// To check and see if there are any updates, please go here: https://github.com/siblount/JzSense
// Happy Coding!"""
            file.write(HEADER.encode("utf-8"))
        totalStr = bytes()
        # results.extend(processedClasses) # Add  v3 documentation.
        for JsClass in results:
            if JsClass is not None:
                # Update implments one more time. Only needed if used multi-processing.
                RedoImplements(JsClass.dzObj)
                totalStr += str(JsClass).encode("utf-8") + b"\n"
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