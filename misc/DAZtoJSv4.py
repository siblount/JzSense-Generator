""" Web scrabbing the DAZ Documentation Website and outputting a JS file to utilize Intellisense. """

from http.client import RemoteDisconnected                                  # Used for one of the excepts.
from bs4 import BeautifulSoup as bs                                         # Our helpful HTML Parser. Used very often.
from urllib.request import urlopen                                          # Download html sourcecode.
import os                                                                   # Path joining.
import multiprocessing                                                      # Process multiple pages at a time.
import time                                                                 # Sleep for a moment.
import DAZtoJSv3                                                            # Used to get documentation from old documentation website (zipped).
from datetime import datetime                                               # Timestamp JzSense file because I'm lazy ._.

### Mine.
from jzsense.common.constants import *                                      # Used to get constants for project
from jzsense.common.ds4 import *                                            # Common functions for Daz Studio 4 documentation
from jzsense.js import *                                                    # Classes for this project
# Methods need to check to see if they return themselves.


# Functions to parse information from web page source and create JSObjects. Returns nothing. Requires DzObj.
def GetClassDescription(DzObj:DazObject):
    """ Gets the class detailed description and will be stored to `DzObj.classinfo`."""
    # This seriously needs to be reworked.
    soup = try_connect(DzObj.link)
    try:
        DzObj.dzPage = urlopen(DzObj.link).read()
    except:
        while True:
            try:
                DzObj.dzPage = urlopen(DzObj.link).read()
            except:
                pass 
            else:
                break
    # Pattern: h2 source line - previous sibling source line.
    # Get all the h2's with class = level2. 
    results1 = soup.find_all("div",{"class": "level2"})
    for r in results1:
        result = r # type: bs
        prevSib = fetch_prev_sibling(result)
        workingDiv = None
        if prevSib is not None and prevSib.text == "Detailed Description":
            workingDiv = r
            break
    if workingDiv is not None:
        # Find all Example: and Attention.
        totalMsg = ""
        # Find normal description before text.
        for y in workingDiv.find_all("p"):
            workingP = y # type: bs
            if is_in_range(get_parent_source_line_range(workingDiv),workingP.sourceline):
                if "Example" in workingP.text:
                    break
                else:
                    totalMsg += "\n" + str(workingP.text.encode("UTF-8"),"UTF-8").strip()
        for x in workingDiv.find_all("strong"):
            strong = x # type: bs
            if strong.text == "Example:":
                # Get the parent of strong.
                p = strong.parent # type: bs
                nextP = p.findNext("p") # type: bs
                if nextP is not None or nextP != None:
                    totalMsg += str(nextP.text.encode("UTF-8"),"UTF-8").strip() + "\n"
                code = p.findNext("pre", {"class" : "code ecmascript"}) # type: bs
                if code != None or code is not None:
                    msg = "\n### Example:\n```\n" + code.text.strip() + "\n```\n" # type: str
                    totalMsg += str(msg.encode("UTF-8"),"UTF-8")
            elif strong.text == "Attention:":
                # Get the parent of strong
                p = strong.parent # type: bs
                # Get next object.
                nextObj = p.findNext() #type: bs
                if nextObj is not None or nextObj != None:
                    totalMsg += "@attention " + str(nextObj.text.encode("UTF-8"),"UTF-8").strip()

        DzObj.classinfo = str(totalMsg.encode("UTF-8"),"UTF-8").strip()
def CreateImplements(x:DazObject):
    """ Reads the source code, recursively searches for the lowest level class and adds it to implements in the DzObj. """
    try:
        soup = bs(x.dzPage,features=HTML_PARSER)
    except OSError:
        print("Couldnt open URL. Trying again in 5 seconds... ")
        time.sleep(5)
        soup = try_connect(x.dzPage)
    except:
        soup = try_connect(x.dzPage)

    if soup.find(text="Inherits :"):
        global HTML_LVL1_NAMES
        lowestInherits = []
        for name in HTML_LVL1_NAMES:
            # Find all "level1" classes.
            level1Classes = soup.find_all(attrs={"class": name})
            for c in level1Classes:
                Class = c # type: bs
                # Find li class with "level1" or "level1 node":
                workingLi = None # type: bs
                for y in HTML_LVL1_NAMES:
                    lis = Class.find_all("li",{"class" : y}) # type: bs
                    for l in lis:
                        li = l # type: bs
                        li = li.text.strip().split(" ")
                        if DazObject.ExistsAll(li[-1]):
                            if li[-1] not in lowestInherits:
                                lowestInherits.append(li[-1])
                                workingLi = l
                if workingLi is not None:
                    for l in lowestInherits:
                        x.implements.append(l)
def CreateProperties(x):
    DzObj = x # type: DazObject
    link = DzObj.dzPage
    try:
        soup = bs(link,features=HTML_PARSER)
    except RemoteDisconnected:
        print("REMOTE DISCONNECTED: Attempting to try again.")
        soup = try_connect(link)
    global COMMENT_TEMPLATE_CONSTRUCTOR
    global COMMENT_TEMPLATE_BEGINNING
    global COMMENT_TEMPLATE_ENDING
    global COMMENT_TEMPLATE_NEWLINE
    # Find all "level 3" class that is a div.
    level3s = soup.find_all(name="div", attrs={"class":"level3"})
    for x in level3s:
        search = x # type: bs
        prevSibling = fetch_prev_sibling(search)
        # If the next one we have doesn't have the id of "properties1" remove it.
        if (prevSibling is None or prevSibling.get("id","properties1") != "properties1" or prevSibling.name != "h3" or prevSibling.text != "Properties"):
            level3s.remove(x)

        else:
            #print("Found 1")
            pass
    for x in level3s:
        # Check if there are <hr> tags. If so, do work. Otherwise, skip.
        search = x # type: bs
        qx = search.find_all("hr")
        query = [] # type: list[bs]
        for x in qx:
            hr = x # type: bs
            prevSibling = fetch_prev_sibling(hr.parent) # type: bs
            if prevSibling is not None and prevSibling.get("id") == "properties1":
                query.append(hr)
        #query = [hr for hr in query if hr.parent.fetchPreviousSiblings(attrs={"id": "properties1"}, limit= 1) == "properties1"]
        if len(query) == 0:
            # Bye felisha
            continue
        previousHr = query[0]
        while True:
            nextHr = previousHr.find_next("hr") # type: bs
            if nextHr is not None:
                if is_element_neighbor(nextHr,query[0].parent):
                    query.append(nextHr)
                    previousHr = nextHr
                else:
                    previousHr = nextHr
            else:
                break

        # Else, we got a trash tree to go chop down.
        for property in query:
            # For every <hr> tag...
            _property = property # type: bs
            # Get the <p> tag below it.
            p = _property.findNext("p") # type: bs
            # Get property return value.
            rV = p.find("a").get_text() # type: str
            # Get variable name.
            v = p.find("strong").get_text() # type: str
            # Get variable definition.
            d = p.findNext("p") # type: bs
            desc = d.get_text() # type: str
            for prop in DzObj.properties:
                if prop.name == v:
                    return
            JSprop = JSProperty(v,rV,desc,dzObj=DzObj)
            DzObj.properties.append(JSprop)
            #print(f"Return Value: {rV} | Variable Name: {v} | Definition: {desc}")
def CreateConstuctors(x):
    DzObj = x # type: DazObject
    link = DzObj.dzPage
    try:
        soup = bs(link,features=HTML_PARSER)
    except RemoteDisconnected:
        print("REMOTE DISCONNECTED: Attempting to try again.")
        soup = try_connect(link)
    except OSError:
        print("LOST CONNECTION: Retrying...")
        soup = try_connect(link)
    global COMMENT_TEMPLATE_CONSTRUCTOR
    global COMMENT_TEMPLATE_BEGINNING
    global COMMENT_TEMPLATE_ENDING
    global COMMENT_TEMPLATE_NEWLINE
    # Find all "level 3" class that is a div.
    level3s = soup.find_all(name="div", attrs={"class":"level3"})
    # For each level 3, if the thing behind it is a h3 and has the id of constructors1. We found it in
    constructorDetailedSect = None # type: bs
    for x in level3s:
        lvl3 = x # type: bs
        # Get the one above it
        _previousSibling_ = fetch_prev_sibling(lvl3)
        # If
        if (_previousSibling_ is not None and _previousSibling_.get("id","constructors1") == "constructors1" and _previousSibling_.name == "h3"):
            constructorDetailedSect = x
            break
    if constructorDetailedSect is None:
        #print(f"Didn't find constructor for {DzObj.name}")
        return
    else:
        search = constructorDetailedSect
        qx = search.find_all("hr")
        query = []
        for x in qx:
            hr = x # type: bs
            prevSibling = fetch_prev_sibling(hr.parent) # type: bs
            #if prevSibling is not None and prevSibling.get("id") == "constructors1":
            query.append(hr)
        if len(query) == 0:
            # Bye felisha
            return
        # Else, we got a trash tree to go chop down.
        for property in query:
            # For every <hr> tag...
            _property = property # type: bs
            # Get the <p> tag below it.
            p = _property.findNext("p") # type: bs
            # Get constructor name.
            cN = p.find("a").get_text() # type: str
            # Get the parameters.
            pA = str(p.get_text().encode("UTF-8"),"UTF-8").strip()
            pA = pA[pA.index("(")+1:pA.index(")")].strip()
            # Get variable definition.
            d = p.findNext("p") # type: bs
            desc = get_description(d, p)
            # Create our variable.
            JSconstructor = JSConstructor(cN,pA,DzObj.properties,desc)
            DzObj.constructors.append(JSconstructor)
            #print(f"Constructor Name: {cN} | Definition: {desc}")
def CreateStaticMethods(DzObj:DazObject):
    try:
        soup = bs(DzObj.dzPage,features=HTML_PARSER)
    except OSError:
        print("Couldnt open URL. Trying again in 5 seconds... ")
        time.sleep(5)
        soup = try_connect(DzObj.dzPage)
    except:
        soup = try_connect(DzObj.dzPage)
    global COMMENT_TEMPLATE_CONSTRUCTOR
    global COMMENT_TEMPLATE_BEGINNING
    global COMMENT_TEMPLATE_ENDING
    global COMMENT_TEMPLATE_NEWLINE
    # Find all "level 3" class that is a div.
    level3s = soup.find_all(name="div", attrs={"class":"level3"})
    # For each level 3, if the thing behind it is a h3 and has the id of methods1. We found it in
    constructorDetailedSect = None # type: bs
    for x in level3s:
        lvl3 = x # type: bs
        # Get the one above it
        _previousSibling_ = fetch_prev_sibling(lvl3)
        # If
        if (_previousSibling_ is not None and _previousSibling_.get("id","static_methods1") == "static_methods1" and _previousSibling_.name == "h3"):
            constructorDetailedSect = x
            break
    if constructorDetailedSect is None:
        #print(f"Didn't find method for {DzObj.name}")
        return
    else:
        search = constructorDetailedSect
        qx = search.find_all("hr")
        query = []
        for x in qx:
            hr = x # type: bs
            prevSibling = fetch_prev_sibling(hr.parent) # type: bs
            #if prevSibling is not None and prevSibling.get("id") == "static_methods1":
            query.append(hr)
        if len(query) == 0:
            # Bye felisha
            return
        # Else, we got a trash tree to go chop down.
        for property in query:
            # For every <hr> tag...
            _property = property # type: bs
            # Get the <p> tag below it.
            p = _property.findNext("p") # type: bs
            # Get method return type.
            hrSourcelineRange = (_property.sourceline,get_parent_source_line_range(query[0].parent)[1])
            returnType = p.findNext("a",{"class" : "wikilink1"}) # type: bs
            if returnType is not None:
                returnNextSib = returnType.find_next_sibling("strong")
            if returnType != None and returnNextSib is not None and returnNextSib.name == "strong":
                rT = p.findNext("a",{"class" : "wikilink1"}).get_text() # type: str
            elif p != None and p.findNext("a", {"class" : "wikilink2"}):
                aCandidate = p.findNext("a", {"class" : "wikilink2"})
                if is_in_range(hrSourcelineRange, aCandidate.sourceline):
                    rT = convert_to_daz_nomen(aCandidate.get_text()) # type: str
                else:
                    rT = "void"
            else:
                if p != None and p.name == "a" and p["class"] == "wikilink1":
                    rT = p.get_text()
                elif p != None and p.find("em") != None:
                    # We found a return type of ourselves.
                    rT = p.find("em").text
                else:
                    rT = "void"
            # Get method name.
            mN = p.find("strong").get_text() # type: str
            # Get the parameters.
            pA = str(p.get_text().encode("UTF-8"),"UTF-8").strip()
            pA = pA[pA.index("(")+1:pA.index(")")].strip()
            # Get variable definition.
            d = p.findNext("p") # type: bs
            desc = get_description(d, p)
            # Create our variable.
            JSmethod = JSFunction(mN,pA,rT,desc,True,DzObj)
            DzObj.functions.append(JSmethod)
            #print(f"Static Method Name: {mN} | Method Parameters: {pA} |  Method Return Type: {rT} | Definition: {desc}")
def CreateMethods(DzObj:DazObject):
    try:
        soup = bs(DzObj.dzPage,features=HTML_PARSER)
    except OSError:
        print("Couldnt open URL. Trying again in 5 seconds... ")
        time.sleep(5)
        soup = try_connect(DzObj.dzPage)
    except:
        soup = try_connect(DzObj.dzPage)
    global COMMENT_TEMPLATE_CONSTRUCTOR
    global COMMENT_TEMPLATE_BEGINNING
    global COMMENT_TEMPLATE_ENDING
    global COMMENT_TEMPLATE_NEWLINE
    # Find all "level 3" class that is a div.
    level3s = soup.find_all(name="div", attrs={"class":"level3"})
    # For each level 3, if the thing behind it is a h3 and has the id of methods1. We found it in
    constructorDetailedSect = None # type: bs
    for x in level3s:
        lvl3 = x # type: bs
        # Get the one above it
        _previousSibling_ = fetch_prev_sibling(lvl3)
        # If
        if (_previousSibling_ is not None and _previousSibling_.get("id","methods1") == "methods1" and _previousSibling_.name == "h3"):
            constructorDetailedSect = x
            break
    if constructorDetailedSect is None:
        #print(f"Didn't find method for {DzObj.name}")
        return
    else:
        search = constructorDetailedSect
        qx = search.find_all("hr")
        query = []
        for x in qx:
            hr = x # type: bs
            prevSibling = fetch_prev_sibling(hr.parent) # type: bs
            #if prevSibling is not None and prevSibling.get("id") == "methods1":
            query.append(hr)
        if len(query) == 0:
            # Bye felisha
            return
        # Else, we got a trash tree to go chop down.
        if query[0].parent.findNextSibling() is not None and query[0].parent.findNextSibling() != None:
            hrParentEndingSL = query[0].parent.findNextSibling().sourceline-1
        else:
            _, maxline = get_parent_source_line_range(query[0].parent)
            hrParentEndingSL = maxline + 1
        i = 0
        for property in query:
            # For every <hr> tag...
            _property = property # type: bs
            # We need to set a range for stuff to find.
            hrSourcelineRange = (_property.sourceline,hrParentEndingSL)
            # find next hr or parent
            nextHr = _property.findNext("hr")
            if nextHr != None and nextHr is not None and is_in_range((_property.parent.sourceline,hrParentEndingSL),nextHr.sourceline):
               hrSourcelineRange = (_property.sourceline,nextHr.sourceline)
            #if _property.findNext("hr")
            # Get the <p> tag below it.
            p = _property.findNext("p") # type: bs
            # Get method return type.
            returnType = p.findNext("a",{"class" : "wikilink1"}) # type: bs
            if returnType is not None:
                returnNextSib = returnType.find_next_sibling("strong")
            if returnType != None and returnNextSib is not None and returnNextSib.name == "strong" and is_in_range(hrSourcelineRange, returnType.sourceline):
                rT = p.findNext("a",{"class" : "wikilink1"}).get_text() # type: str
            elif p != None and p.findNext("a", {"class" : "wikilink2"}):
                aCandidate = p.findNext("a", {"class" : "wikilink2"})
                if is_in_range(hrSourcelineRange, aCandidate.sourceline):
                    rT = convert_to_daz_nomen(aCandidate.get_text()) # type: str
                else:
                    rT = "void"
            else:
                if p != None and p.name == "a" and p["class"] == "wikilink1":
                    rT = p.get_text()
                elif p != None and p.name == "a" and p["class"] == "wikilink2":
                    # If we got a link to a page that doesn't exist (which we probably do have now.)
                    rT = convert_to_daz_nomen(p.get_text())
                elif p != None and p.find("em") != None:
                    # We found a return type of ourselves.
                    rT = p.find("em").text
                else:
                    rT = "void"
            # Get method name.
            mN = p.find("strong").get_text() # type: str
            # Get the parameters.
            pA = str(p.get_text().encode("UTF-8"),"UTF-8").strip()
            if "(" in pA:
                pA = pA[pA.index("(")+1:pA.index(")")].strip()
            else:
                pA = pA.strip()+"()"
            # Get variable definition.
            d = p.findNext("p") # type: bs
            desc = get_description(d, p)
            # Create our variable.
            JSmethod = JSFunction(mN,pA,rT,desc,False,DzObj)
            DzObj.functions.append(JSmethod)
            i+= 1
            #print(f"Method Name: {mN} | Method Parameters: {pA} |  Method Return Type: {rT} | Definition: {desc}")
def CreateEnums(DzObj:DazObject):
    soup = bs(DzObj.dzPage,features=HTML_PARSER)
    # Find all "level 3" class that is a div.
    level3s = soup.find_all(name="div", attrs={"class":"level3"})
    for x in level3s:
        search = x # type: bs
        nextSibling = fetch_next_sibling(search)
        # If the next one we have doesn't have the id of "enumerations1" remove it.
        foundProperties = search.find_next_sibling("h3",{"id" : "enumerations1"},text="Enumerations")
        if (nextSibling is None or nextSibling.get("id","enumerations1") != "enumerations1" or nextSibling.name != "h3" or nextSibling.text != "Properties"):
            level3s.remove(x)
        else:
            #print("Found 1")
            pass
    for x in level3s:
        # Check if there are <hr> tags. If so, do work. Otherwise, skip.
        search = x # type: bs
        qx = search.find_all("hr")
        query = None # type: bs
        for x in qx:
            hr = x # type: bs
            prevSibling = fetch_prev_sibling(hr.parent) # type: bs
            if prevSibling is not None and prevSibling.get("id") == "enumerations1":
                query = hr
                break
        if query is not None:
            for p in query.find_all_next("li",{"class": "level1"}):
                if not is_element_neighbor(p,search):
                    continue
                # Get name.
                try:
                    enumName = p.find("strong").get_text() # type: str
                    e = p.get_text() #type: str
                    index = e.index("-") + 1
                    enumDesc = e[index:].strip()
                    JsEnum = JSEnum(enumName,enumDesc,DzObj)
                    DzObj.enums.append(JsEnum)
                    #print(f"ENUM Name: {enumName} | Definition: {enumDesc}")
                except:
                    #print(f"ENUM FAILED FOR {DzObj.name}.")
                    ERRORED_ENUMS.append(DzObj.name)
def CreateSignals(DzObj:DazObject):
    try:
        soup = bs(DzObj.dzPage,features=HTML_PARSER)
    except OSError:
        print("Couldnt open URL. Trying again in 5 seconds... ")
        time.sleep(5)
        soup = try_connect(DzObj.dzPage)
    except:
        soup = try_connect(DzObj.dzPage)
    global COMMENT_TEMPLATE_CONSTRUCTOR
    global COMMENT_TEMPLATE_BEGINNING
    global COMMENT_TEMPLATE_ENDING
    global COMMENT_TEMPLATE_NEWLINE
    # Find all "level 3" class that is a div.
    level3s = soup.find_all(name="div", attrs={"class":"level3"})
    # For each level 3, if the thing behind it is a h3 and has the id of methods1. We found it in
    signalDetailSect = None # type: bs
    for x in level3s:
        lvl3 = x # type: bs
        # Get the one above it
        _previousSibling_ = fetch_prev_sibling(lvl3)
        # If
        if (_previousSibling_ is not None and _previousSibling_.get("id","signals1") == "signals1" and _previousSibling_.name == "h3"):
            signalDetailSect = x
            break
    if signalDetailSect is None:
        #print(f"Didn't find signal for {DzObj.name}")
        return
    else:
        search = signalDetailSect
        qx = search.find_all("hr")
        query = []
        for x in qx:
            hr = x # type: bs
            # prevSibling = fetch_prev_sibling(hr.parent) # type: bs
            #if prevSibling is not None and prevSibling.get("id") == "methods1":
            query.append(hr)
        if len(query) == 0:
            # Bye felisha
            return
        # Else, we got a trash tree to go chop down.
        for property in query:
            # For every <hr> tag...
            _property = property # type: bs
            # Get the <p> tag below it.
            p = _property.findNext("p") # type: bs
            # Get method return type.
            rT = "void"
            # Get method name.
            mN = p.find("strong").get_text() # type: str
            # Get the parameters.
            pA = str(p.get_text().encode("UTF-8"),"UTF-8").strip()
            if "(" in pA:
                pA = pA[pA.index("(")+1:pA.index(")")].strip()
            else:
                pA = pA.strip()+"()"
            workingP = fetch_next_sibling(p)
            if workingP is not None and workingP.name == "p":
                code = workingP.find("code")
                if code != None:
                    signature = workingP.find("code").text
                else:
                    signature = mN + "()"
            else:
                signature = "TODO: Add Description"
            # Get variable definition.
            workingP = fetch_next_sibling(workingP)
            if workingP is not None and workingP.name == "p":
                desc = workingP.text.strip()
            else:
                desc = "TODO: Add Description"
            # Create our variable.
            JSsignal = JSSignal(mN, pA, signature, desc, DzObj)
            DzObj.signals.append(JSsignal)
            #print(f"Signal Name: {mN} | Signal Parameters: {pA} |  Signal Signature: {signature} | Definition: {desc}")
def DetermineIfEligible(x: DazObject):
    """ Checks if the class is a ECMAScript. If it is, we will return false. Otherwise true."""
    try:
        soup = bs(urlopen(x.link),features=HTML_PARSER)
    except RemoteDisconnected:
        print("REMOTE DISCONNECTED: Attempting to try again.")
        soup = try_connect(x.link)
    except OSError:
        print("LOST CONNECTION: Attempting to try again.")
        soup = try_connect(x.link)
    results = soup.find_all("div",attrs={"class" : "level1"})
    classDescription = None
    # Double check to see that we got the description.
    for y in results:
        result = y # type: bs
        prevElement = fetch_prev_sibling(result)
        if prevElement.text == x.name:
            print("We got our class description.")
            classDescription = y
            break
    if classDescription is not None:
        if "ECMAScript".lower() in classDescription.text.lower():
            SKIPPED_DZOBJS.append(x.name)
            return False
        else:
            return True
    else:
        return True
def ProcessObject(DzObj: DazObject) -> JSClass:
    """ Assigns attributes to `DzObj` and returns a JSClass which has a string interprolation ready with comments and code."""
    if not DetermineIfEligible(DzObj) or DzObj in IGNORE_OBJECTS:
        print(DzObj.name + " is not eligble. Deleting.")
        return None
    GetClassDescription(DzObj)
    CreateImplements(DzObj)
    CreateConstuctors(DzObj)
    CreateEnums(DzObj)
    CreateProperties(DzObj)
    CreateStaticMethods(DzObj)
    CreateMethods(DzObj)
    CreateSignals(DzObj)
    return JSClass(DzObj)

