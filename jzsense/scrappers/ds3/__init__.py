from jzsense.common.ds3 import *
from jzsense.common.constants import *
from jzsense.js import *

# NOTE: In DS4, we used .local_location. Here we use DazObject.link. local_location is not set.
def __GetClassDescription(DazObj:DazObject):
    """ Gets the class detailed description and will be stored to `DzObj.classinfo`."""
    #TODO: Update function for more advanced data dissecting.
    DazObj.dzPage = urlopen(DazObj.link).read()
    soup = bs(DazObj.dzPage, features=HTML_PARSER)
    h2 = soup.find("h2",text="Detailed Description") # type: bs
    if h2 is not None:
        DazObj.classinfo = str(h2.nextSibling)
    else:
        DazObj.classinfo = ""
def __CreateImplements(DazObj:DazObject):
    """ Reads the source code, recursively searches for the lowest level class and adds it to implements in the DzObj. """
    soup = bs(CLASS_HIERARCHY_PAGE,features=HTML_PARSER)
    us = soup.find('a', {"class" : "el"}, text=DazObj.name)
    aParent = us.parent
    liParent = aParent.parent
    # If we don't inherit from anything...
    if liParent.name == "ul" and liParent.parent.name != "body":
        parentClass = liParent.parent.find('a', {"class" : "el"})
        DazObj.implements.add(JSType.get_type(parentClass.text))
        print(DazObj.name, "implements", parentClass.text)
    else:
        print(DazObj.name, "does not implement anything.")
        return
def __CreateProperties(DazObj:DazObject):
    soup = bs(DazObj.dzPage, features=HTML_PARSER)
    # Find all "level 3" class that is a div.
    tableData = soup.find_all("td", {"colspan" : "2"}) # type: list[bs]
    for x in tableData:
        tD = x # type: bs
        possibleTDtext = tD.text == "Properties"
        if possibleTDtext:
            # We got the properties h2. Now to chop down the table rows below it.
            minSourceLine = tD.parent.sourceline # td parent is tr.
            maxSourceLine = FindMaxSourceLineGivenContextTable(tD.parent, True)+1
            lastTr = None
            while True:
                #rV = Return Value | pN = Property Name
                if lastTr is None:
                    workingTr = tD.parent.find_next("tr")
                else:
                    workingTr = GetNextSiblingBS(lastTr, {}, minSourceLine, maxSourceLine)
                # Now find detailed information.
                if workingTr is None:
                    break # We are done.
                tdReturnValue = workingTr.find("td", {"class" : "memItemLeft"})
                rV = tdReturnValue.find("a").text
                tdName = workingTr.find("td", {"class" : "memItemRight"})
                pN = tdName.find("a").text
                desc = GetDetailedInfo(workingTr, pN)
                JsProperty = JSProperty(pN, JSType.get_type(rV), desc[0], DazObj)
                DazObj.properties.add(JsProperty)
                lastTr = workingTr
def __CreateConstuctors(DazObj:DazObject):
    soup = bs(DazObj.dzPage, features=HTML_PARSER)
    tableData = soup.find_all("td", {"colspan" : "2"}) # type: list[bs]
    for DazObj in tableData:
        tD = DazObj # type: bs
        possibleTDtext = tD.text == "Constructors"
        if possibleTDtext:
            minSourceLine = tD.parent.sourceline # td parent is tr.
            maxSourceLine = FindMaxSourceLineGivenContextTable(tD.parent, True)+1
            lastTr = None
            while True:
                #rV = Return Value | pN = Property Name
                if lastTr == None:
                    workingTr = tD.parent.find_next("tr")
                else:
                    workingTr = GetNextSiblingBS(lastTr, {}, minSourceLine, maxSourceLine)
                # Now find detailed information.
                if workingTr is None or workingTr == None:
                    break # We are done.
                # Make sure we didn't get a fucking <br>
                possibleBr = workingTr.find("br")
                textAvailable = workingTr.text == None
                if possibleBr is not None and not textAvailable:
                    # Don't go any fruther, do next iteration.
                    lastTr = workingTr
                    continue
                cN = GetSymbolArgs(workingTr)
                pA = cN[cN.index("(")+1:cN.index(")")].strip()
                cN = cN[:cN.index("(")].strip()
                # TODO: Fix.
                desc = GetDetailedInfo(workingTr, cN, "Constructor & Destructor Documentation", pA)
                JsConstructor = JSConstructor(cN, pA, desc)
                DazObj.constructors.add(JsConstructor)
                print(desc,"|", cN)
                lastTr = workingTr   
def __CreateStaticMethods(DazObj:DazObject):
    soup = bs(DazObj.dzPage, features=HTML_PARSER)
    tableData = soup.find_all("td", {"colspan" : "2"}) # type: list[bs]
    for x in tableData:
        tD = x # type: bs
        possibleTDtext = tD.text == "Methods (Static)"
        if possibleTDtext:
            minSourceLine = tD.parent.sourceline # td parent is tr.
            maxSourceLine = FindMaxSourceLineGivenContextTable(tD.parent, True)+1
            lastTr = None
            while True:
                #rV = Return Value | pN = Property Name
                if lastTr == None:
                    workingTr = tD.parent.find_next("tr")
                else:
                    workingTr = GetNextSiblingBS(lastTr, {}, minSourceLine, maxSourceLine)
                # Now find detailed information.
                if workingTr is None or workingTr == None:
                    break # We are done.
                # Make sure we didn't get a fucking <br>
                possibleBr = workingTr.find("br")
                textAvailable = workingTr.text == None
                if (possibleBr != None or possibleBr is not None) and not textAvailable:
                    # Don't go any fruther, do next iteration.
                    lastTr = workingTr
                    continue
                mN = GetSymbolArgs(workingTr)
                pA = mN[mN.index("(")+1:mN.index(")")].strip()
                mN = mN[:mN.index("(")].strip()
                rV = JSType.get_type(GetReturnType(workingTr))
                desc = GetDetailedInfo(workingTr, mN, "Member Function Documentation", pA)
                JsStaticMethod = JSFunction(mN, pA, rV, desc, True, DazObj)
                DazObj.functions.add(JsStaticMethod)
                print(desc,"|", mN)
                lastTr = workingTr   
def __CreateMethods(DazObj:DazObject):
    soup = bs(DazObj.dzPage, features=HTML_PARSER)
    tableData = soup.find_all("td", {"colspan" : "2"}) # type: list[bs]
    for x in tableData:
        tD = x # type: bs
        possibleTDtext = tD.text == "Methods"
        if possibleTDtext:
            minSourceLine = tD.parent.sourceline # td parent is tr.
            maxSourceLine = FindMaxSourceLineGivenContextTable(tD.parent, True)+1
            lastTr = None
            while True:
                #rV = Return Value | pN = Property Name
                if lastTr == None:
                    workingTr = tD.parent.find_next("tr")
                else:
                    workingTr = GetNextSiblingBS(lastTr, {}, minSourceLine, maxSourceLine)
                # Now find detailed information.
                if workingTr is None or workingTr == None:
                    break # We are done.
                # Make sure we didn't get a fucking <br>
                possibleBr = workingTr.find("br")
                textAvailable = workingTr.text == None
                if  possibleBr is not None and not textAvailable:
                    # Don't go any fruther, do next iteration.
                    lastTr = workingTr
                    continue
                mN = GetSymbolArgs(workingTr)
                # DzController - has methods without () in it.
                # god damn it.
                if "(" in mN:
                    pA = mN[mN.index("(")+1:mN.index(")")].strip()
                    mN = mN[:mN.index("(")].strip()
                else:
                    pA = ""
                    mN = mN.strip()
                rV = JSType.get_type(GetReturnType(workingTr).strip()) # wtf is char(180)
                desc = GetDetailedInfo(workingTr, mN, "Member Function Documentation", pA)
                JsStaticMethod = JSFunction(mN, pA, rV, desc, False, DazObj)
                DazObj.functions.add(JsStaticMethod)
                print(desc,"|", mN)
                lastTr = workingTr
def __CreateEnums(DazObj:DazObject):
    soup = bs(DazObj.dzPage, features=HTML_PARSER)
    tableData = soup.find_all("td", {"colspan" : "2"}) # type: list[bs]
    for x in tableData:
        tD = x # type: bs
        possibleTDtext = tD.text == "Enumerations"
        if possibleTDtext:
            h2 = tD.parent.find_next('h2', text="Member Enumeration Documentation") # type: bs
            if h2 is not None:
                minSourceline = h2.find_next("div", {"class" : "memitem"}).sourceline
                maxSourceline = FindMaxSourceLineGivenContext(h2)
                # Find a tbody within memitem.
                fTBody = h2.find_next("tbody") #type: bs
                lastfTBody = None
                while True:
                    if lastfTBody is None or lastfTBody == None:
                        workingfT = fTBody
                    else:
                        workingfT = GetNextBS(lastfTBody, {}, minSourceline, maxSourceline)
                    # If none, we are done.
                    if workingfT is None or workingfT == None:
                        break
                    # Get all trs
                    listOfTrs = workingfT.find_all("tr")
                    # For each tr, append enum. 
                    for t in listOfTrs:
                        tr = t # type: bs
                        # Get enum name in em.
                        try:
                            eN = tr.find("em").text.strip()
                        except:
                            print("Fucking parser.")
                            continue
                        # Get enum description.
                        eD = tr.find("em").parent.find_next("td").text.strip()
                        # Create enum and append to DzObj enum list.
                        JsEnum = JSEnum(eN, eD, DazObj)
                        DazObj.enums.add(JsEnum)
                        print("ENUM:", eN, "DESC:",  eD, "Class:", DazObj.name)
                    lastfTBody = workingfT
def __CreateSignals(DazObj:DazObject):
    soup = bs(DazObj.dzPage, features=HTML_PARSER)
    tableData = soup.find_all("td", {"colspan" : "2"}) # type: list[bs]
    for x in tableData:
        # Confirm if we have enumerations.
        tD = x # type: bs
        possibleTDtext = tD.text == "Signals"
        # If so, do work.
        if possibleTDtext:
            h2 = tD.parent.parent.find_next('h2', text="Member Function Documentation") # type: bs
            if h2 is not None:
                minSourceline = h2.find_next("div", {"class" : "memitem"}).sourceline
                maxSourceline = FindMaxSourceLineGivenContext(h2)
                lastMemItem = None
                while True:
                    if lastMemItem is None:
                        workingMemItem = h2.find_next("div", {"class" : "memitem"}) # type: bs
                        if workingMemItem is not None:
                            workingMemName = workingMemItem.find("table", {"class" : "memname"})
                    else:
                        workingMemItem = GetNextBS(lastMemItem, {"class" : "memitem"}, minSourceline, maxSourceline)
                        if workingMemItem is not None:
                            workingMemName = workingMemItem.find("table", {"class" : "memname"})
                    if workingMemItem is None:
                        break
                    if re.search(GenerateRE("\[signal\]"), workingMemItem.text) == None:
                        lastMemItem = workingMemItem
                        continue
                    memdoc = workingMemItem.find("div", {"class" : "memdoc"}) # type: bs
                    try:
                        signatureBS = memdoc.find("code")
                        signature = signatureBS.text.strip()
                        desc = signatureBS.parent.find_next("p").text.strip()
                    except:
                        print("WARNING: No signature found and no desc found.")
                        desc = memdoc.text
                        signature = None
                    tdName = workingMemName.find("td", {"class" : "memname"}).text # type: str
                    if signature is None:
                        signature = f"{tdName}()"
                    lastColonIndex = tdName.rindex(":")
                    sName = tdName[lastColonIndex+1:].strip()
                    # Create the object.
                    # TODO: Handle very complicated parameters.
                    # Warning: It is C++ style and most likely contains Qt Variables not exposed.
                    JsSignal = JSSignal(sName, "", signature, desc, DazObj)
                    DazObj.signals.add(JsSignal)
                    print("JsSignal for", DazObj.name, ":", sName, ":", signature, ":" , desc)
                    lastMemItem = workingMemItem

def is_eligible(x: DazObject):
    """ Checks if the class is a ECMAScript. If it is, we will return false. Otherwise true."""
    soup = bs(urlopen(x.link),features=HTML_PARSER)
    detailed_description = soup.find("h2", text="Detailed Description")
    if detailed_description is not None:
        if "ECMAScript".lower() in detailed_description.text.lower():
            SKIPPED_DZOBJS.append(x.name)
            return False
        else:
            return True
    else:
        raise Exception("bro wtf")
def process_object(DzObj: DazObject) -> JSClass:
    if not is_eligible(DzObj):
        return None
    # if not DetermineIfEligible(DzObj) or DzObj in DS3_IGNORE_OBJECTS:
    #     print(DzObj.name + " is not eligble. Deleting.")
    #     return None
    __GetClassDescription(DzObj)
    __CreateImplements(DzObj)
    __CreateConstuctors(DzObj)
    __CreateEnums(DzObj)
    __CreateProperties(DzObj)
    __CreateStaticMethods(DzObj)
    __CreateMethods(DzObj)
    __CreateSignals(DzObj)
    return JSClass(DzObj)

def BeginWork(ignoreList = []):
    listOfLinks = []
    soup = bs(urlopen(DS3_OBJECT_INDEX_PAGE),features=HTML_PARSER)
    tds = soup.find_all("td")
    for x in tds:
        td = x # type: bs
        possibleLink = td.find_next("a",{"class" : "el"})
        if possibleLink:
            listOfLinks.append((os.path.join("D:\\Python Test Folder\\DAZScriptV3\\", possibleLink["href"]), possibleLink.text))
    for link in listOfLinks:
        if not JSType.find_type(link[1]) and link[1] not in ignoreList and link[1] not in DS3_IGNORE_OBJECTS:
            DazObject(link[1], link[0], urlopen("file:\\\\" + link[0]).read())
            print(f"Created DazObject for {link[1]}.")
    # Print working classes.
    for object in DazObject.DazObjects:
       process_object(object)
    # with multiprocessing.Pool(4) as p:
    #     results = p.map(ProcessObject, DazObject.DzObjects)
    return JSClass.JsClasses

def get_ds3_objects(dazobjects:list[DazObject]=None) -> list[DazObject]:
    """
    Gets objects from the `OBJECT_INDEX_PAGE` page and constructs `DazObject`s. 
    
    If `dazobjects` is not None, objects will be added if the object doesn't already exist. Scrapper will skip past objects already created.
    
    For example, if `DzObject` is in the dazobjects list, it will be skipped. Otherwise, we will extract data from the page source.
    
    Params:
        `dazobjects` - A list of `DazObject`s already generated from another scrapper. Used to merge information.
    Returns:
        A list of `DazObject`'s
    """
    merge = dazobjects != None
    soup = bs(urlopen(DS3_OBJECT_INDEX_PAGE),features=HTML_PARSER)
    objects = set() # type: set[DazObject]
    tds = soup.find_all("td")
    for x in tds:
        td = x # type: bs
        possibleLink = td.find_next("a",{"class" : "el"})
        if possibleLink:
            # Check if we are in merge mode.
            if merge:
                # Does the name exist yet?
                if (JSType.find_type(possibleLink.text) or possibleLink.text in DS3_DELETED_OBJECTS):
                    # if so, NEXT!!!
                    print(f"{possibleLink.text} was skipped due to already being processed or is already deleted.")
                    continue
                objects.add(DazObject(possibleLink.text, get_page_path(possibleLink['href']),ds_version=3))
            else:
                objects.add(DazObject(possibleLink.text, get_page_path(possibleLink['href']),ds_version=3))
    return objects



if __name__ == "__main__":
    BeginWork()
