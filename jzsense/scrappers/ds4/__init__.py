""" Web scrabbing the DAZ Documentation Website and outputting a JS file to utilize Intellisense. """

from http.client import RemoteDisconnected                                  # Used for one of the excepts.
from bs4 import BeautifulSoup as bs                                         # Our helpful HTML Parser. Used very often.
from urllib.request import urlopen                                          # Download html sourcecode.
from os import path, mkdir
import threading, queue
### Mine.
from jzsense.common.constants import *                                      # Used to get constants for project
from jzsense.common.ds4 import *                                            # Common functions for Daz Studio 4 documentation
from jzsense.js import *                                                    # Classes for this project
# Methods need to check to see if they return themselves.

USE_LOCAL_FILES = True

# Functions to parse information from web page source and create JSObjects. Returns nothing. Requires DazObject.
def __GetClassDescription(DzObj:DazObject):
    """ Gets the class detailed description and will be stored to `DzObj.classinfo`."""
    if USE_LOCAL_FILES:
        soup = try_connect(DzObj.local_location)
        try:
            DzObj.dzPage = urlopen(DzObj.local_location).read()
        except:
            # Fallback to online.
            while True:
                try:
                    DzObj.dzPage = urlopen(DzObj.link).read()
                except Exception:
                    pass 
                else:
                    break
    else:
        soup = try_connect(DzObj.local_location)
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
def __CreateImplements(x:DazObject):
    """ Reads the source code, recursively searches for the lowest level class and adds it to implements in the DzObj. """
    try:
        soup = bs(x.dzPage,features=HTML_PARSER)
    except Exception:
        soup = try_connect(x.dzPage)

    if soup.find(text="Inherits :"):
        global HTML_LVL1_NAMES
        lowestInherits = [] # type: list[str]
        for name in HTML_LVL1_NAMES:
            # Find all "level1" classes.
            level1Classes = soup.find_all(attrs={"class": name})
            for c in level1Classes:
                Class = c # type: bs
                # Find li class with "level1" or "level1 node":
                workingLi = None # type: bs
                for y in HTML_LVL1_NAMES:
                    lis = Class.find_all("li",{"class" : y}) # type: list[bs]
                    for l in lis:
                        li = l # type: bs
                        li = li.text.strip().split(" ")
                        lowestInherit = remove_deprecated_str(li[-1])
                        if DazObject.ExistsAll(lowestInherit):
                            if lowestInherit not in lowestInherits:
                                lowestInherits.append(lowestInherit)
                                workingLi = l
                if workingLi is not None:
                    x.implements.extend(set(JSType.get_type(class_) for class_ in lowestInherits))
def __CreateProperties(DzObj:DazObject):
    soup = bs(DzObj.dzPage,features=HTML_PARSER)
    # Find all "level 3" class that is a div.
    level3s = soup.find_all(name="div", attrs={"class":"level3"})
    for level3 in level3s:
        search = level3 # type: bs
        prevSibling = fetch_prev_sibling(search)
        # If the next one we have doesn't have the id of "properties1" remove it.
        if (prevSibling is None or prevSibling.get("id","properties1") != "properties1" or prevSibling.name != "h3" or prevSibling.text != "Properties"):
            level3s.remove(level3)

        else:
            #print("Found 1")
            pass
    for level3 in level3s:
        # Check if there are <hr> tags. If so, do work. Otherwise, skip.
        search = level3 # type: bs
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
            JSprop = JSProperty(v,JSType.get_type(rV),desc,dzObj=DzObj)
            DzObj.properties.append(JSprop)
            #print(f"Return Value: {rV} | Variable Name: {v} | Definition: {desc}")
def __CreateConstuctors(DzObj:DazObject):
    try:
        soup = bs(DzObj.dzPage,features=HTML_PARSER)
    except OSError:
        print("FILE NOT DOWNLOADED: Retrying...")
        soup = try_connect(DzObj.link)
    
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
            JSconstructor = JSConstructor(cN,pA,desc)
            DzObj.constructors.append(JSconstructor)
            #print(f"Constructor Name: {cN} | Definition: {desc}")
def __CreateStaticMethods(DzObj:DazObject):
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
                rT = JSType.get_type(p.findNext("a",{"class" : "wikilink1"}).get_text()) # type: str
            elif p != None and p.findNext("a", {"class" : "wikilink2"}):
                aCandidate = p.findNext("a", {"class" : "wikilink2"})
                if is_in_range(hrSourcelineRange, aCandidate.sourceline):
                    rT = JSType.get_type(convert_to_daz_nomen(aCandidate.get_text())) # type: str
                else:
                    rT = "void"
            else:
                if p != None and p.name == "a" and p["class"] == "wikilink1":
                    rT = p.get_text()
                elif p != None and p.find("em") != None:
                    # We found a return type of ourselves.
                    rT = JSType.get_type(p.find("em").text)
                else:
                    rT = "void"
            # Get method name.
            mN = p.find("strong").get_text() # type: str
            # Get the parameters.
            # pA = pA[pA.index("(")+1:pA.index(")")].strip()
            pA = str(p.get_text().encode("UTF-8"),"UTF-8").strip()
            if "(" in pA and "deprecated" not in pA:
                pA = pA[pA.index("(")+1:pA.index(")")].strip()
            elif "(" in pA and "deprecated" in pA:
                first_end_parenthesis_index = pA.index(")")
                colon_index = pA.index(':')
                # If : is behind the first ), then it is normal.
                if colon_index < first_end_parenthesis_index:
                    pA = pA[pA.index("(")+1:pA.rfind(")")].strip()
                else:
                    # otherwise its in front of the :, meaning we gotta deal with this shit.
                    # void : addManipulator( DzImageManip (deprecated) manip ) <--- wtf
                    pA = pA[pA.index("(",first_end_parenthesis_index+1)+1:pA.rfind(")")].strip()
            else:
                pA = ""
            # Get variable definition.
            d = p.findNext("p") # type: bs
            desc = get_description(d, p)
            # Create our variable.
            JSmethod = JSFunction(mN,pA,rT,desc,True,DzObj)
            DzObj.functions.append(JSmethod)
            #print(f"Static Method Name: {mN} | Method Parameters: {pA} |  Method Return Type: {rT} | Definition: {desc}")
    print("Created static methods.")
def __CreateMethods(DzObj:DazObject):
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
            if "(" in pA and "deprecated" not in pA:
                pA = pA[pA.index("(")+1:pA.rfind(")")].strip() # "DzApp:getVersion("
            elif "(" in pA and "deprecated" in pA:
                first_end_parenthesis_index = pA.index(")")
                colon_index = pA.index(':')
                # If : is behind the first ), then it is normal.
                if colon_index < first_end_parenthesis_index:
                    pA = pA[pA.index("(")+1:pA.rfind(")")].strip()
                else:
                    # otherwise its in front of the :, meaning we gotta deal with this shit.
                    # void : addManipulator( DzImageManip (deprecated) manip ) <--- wtf
                    pA = pA[pA.index("(",first_end_parenthesis_index+1)+1:pA.rfind(")")].strip()
            else:
                # someone forgot to add ().
                pA = ""
            # Get variable definition.
            d = p.findNext("p") # type: bs
            desc = get_description(d, p)
            # Create our variable.
            JSmethod = JSFunction(mN,pA,rT,desc,False,DzObj)
            DzObj.functions.append(JSmethod)
            i += 1
            #print(f"Method Name: {mN} | Method Parameters: {pA} |  Method Return Type: {rT} | Definition: {desc}")
    print("Created methods.")
def __CreateEnums(DzObj:DazObject):
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
    print("Created enums")
def __CreateSignals(DzObj:DazObject):
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
            if "(" in pA and "deprecated" not in pA:
                pA = pA[pA.index("(")+1:pA.index(")")].strip()
            elif "(" in pA and "deprecated" in pA:
                first_end_parenthesis_index = pA.index(")")
                colon_index = pA.index(':')
                # If : is behind the first ), then it is normal.
                if colon_index < first_end_parenthesis_index:
                    pA = pA[pA.index("(")+1:pA.rfind(")")].strip()
                else:
                    # otherwise its in front of the :, meaning we gotta deal with this shit.
                    # void : addManipulator( DzImageManip (deprecated) manip ) <--- wtf
                    pA = pA[pA.index("(",first_end_parenthesis_index+1)+1:pA.rfind(")")].strip()
            else:
                # someone forgot to add ().
                pA = ""
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
    print("Created signals.")
            #print(f"Signal Name: {mN} | Signal Parameters: {pA} |  Signal Signature: {signature} | Definition: {desc}")
def __DetermineIfEligible(x: DazObject):
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
    print(f"Processing {DzObj.name}...")
    if not __DetermineIfEligible(DzObj) or DzObj in IGNORE_OBJECTS:
        print(DzObj.name + " is not eligble. Deleting.")
        return None
    # Use local file at current working directory.
    file_name = f"pages/{DzObj.lowered_name}.html"
    if USE_LOCAL_FILES and path.exists(file_name):
        DzObj.local_location = "file:\\\\" + path.abspath(file_name)
    elif USE_LOCAL_FILES:
        try:
            mkdir("pages")
        except OSError:
            pass
        print(f"Downloading webpage to disk...")
        with open(file_name,"wb") as file:
            file.write(urlopen(DzObj.link).read())
        DzObj.local_location = "file:\\\\" + path.abspath(file_name)
    __GetClassDescription(DzObj)
    __CreateImplements(DzObj)
    __CreateConstuctors(DzObj)
    __CreateEnums(DzObj)
    __CreateProperties(DzObj)
    __CreateStaticMethods(DzObj)
    __CreateMethods(DzObj)
    __CreateSignals(DzObj)
    return JSClass(DzObj)

def ProcessAllObjects(DzObjs:list[DazObject]):
    q = queue.Queue()
    def __worker():
        while True:
            item = q.get(block=True,timeout=5)
            ProcessObject(item)
            print("Finished processing one item.")
            q.task_done()
    t = threading.Thread(target=__worker, daemon=True)
    t.start()
    
    for obj in DzObjs:
        q.put(obj)
    
    q.join()

    print("All done!")


def RedoImplements(x:DazObject):
    __CreateImplements(x)
# Generate object list from object index page.
def construct_daz_objects() -> list[DazObject]:
    """
    Gets objects from the `OBJECT_INDEX_PAGE` page and constructs `DazObject`s.
    
    Returns:
        A list of `DazObject`'s
     """
    soup = try_connect(OBJECT_INDEX_PAGE)
    uls = soup.find_all(attrs={"class" : "nspagesul"}) # type: list[bs]
    daz_objects = [] # type: list[DazObject]
    for ul in uls:
        objects = ul.find_all(attrs={"class" : "wikilink1"}) # type: list[bs]
        for object in objects:
            object_name = object.get_text()
            if "(" in object_name:
                object_name = object_name[:object_name.find("(")].strip()
            daz_objects.append(DazObject(object_name, object['href']))
    return daz_objects

if __name__ == "__main__":
    daz_objects = construct_daz_objects()
    for object_ in daz_objects:
        ProcessObject(object_)