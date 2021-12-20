import os
import time
from jzsense.js import DazObject

def ClassStillExists(DzObj:DazObject) -> bool:
    # Create a .dsa file.
    fileName = f"CLASS_STILL_EXIST-{DzObj.name}.dsa"
    with open(fileName, "w") as file:
        tryStatement = "var failed = false;\ntry {\n\t" + DzObj.name + "\n} catch (e) {\n\tvar newFile = new DzFile(\"D:/Python Test Folder/New folder/" + DzObj.name + ".txt\");\n\tnewFile.open(DzFile.WriteOnly);\n\tnewFile.write(\"Failed\");\n\tnewFile.close();\n\tfailed=true;\n} finally {\n\tif (!failed) {\n\t\tvar newFile = new DzFile(\"D:/Python Test Folder/New folder/" + DzObj.name + ".txt\");\n\t\tnewFile.open(DzFile.WriteOnly);\n\t\tnewFile.write(\"Success\");\n\t\tnewFile.close();\n\t}\n}"
        file.write(tryStatement)
        file.close()
    time.sleep(1)
    os.popen("\"C:\Program Files\DAZ 3D\DAZStudio4\DAZStudio.exe\" " + f"\"{os.path.abspath(fileName)}\"")
    time.sleep(1)
    # Find the result.
    expectedFile = DzObj.name
    count = 0
    while not os.path.isfile(f"D:/Python Test Folder/New folder/{expectedFile}.txt"):
        time.sleep(0.25)
        count += 1
        if count >= 8:
            print(f"Something didn't work out for {DzObj.name}")
            return False
    with open(f"D:/Python Test Folder/New folder/{expectedFile}.txt") as outputFile:
        if "Success" in outputFile.read():
            return True
        else:
            return False
