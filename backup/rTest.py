from http.client import RemoteDisconnected
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import os
import sys
import multiprocessing
import time
import re
import urllib
import bs4

print("Initializing")
# Global variables
OBJECT_INDEX_PAGE = "http://docs.daz3d.com/doku.php/public/software/dazstudio/4/referenceguide/scripting/api_reference/object_index/start"
JS_NAME = "DzIntellisense.js"
HTML_RETRIES = 3
HTML_PARSER = "html5lib"
HTML_LVL1_NAMES = ["level1", "level1 node"]
IGNORE_OBJECTS = []
COMMENT_TEMPLATE_BEGINNING = "/**"
COMMENT_TEMPLATE_ENDING = "*/"
COMMENT_TEMPLATE_NEWLINE = " * "
COMMENT_TEMPLATE_PARAM = "@param {} {}}"
COMMENT_TEMPLATE_CONSTRUCTOR = "@constructor {}"
COMMENT_UNICODE_REPLACEMENTS = {"“".encode("UTF-8") : b'"', "”".encode("UTF-8") : b'"'}
ERRORED_ENUMS = []
SKIPPED_DZOBJS = []

def TryReconnect(link) -> bs:
    for _ in range(HTML_RETRIES):
        try:
            return bs(urlopen(link),features=HTML_PARSER)
        except:
            print("Retry failed...trying again in 3 seconds.")
            time.sleep(3)
            continue
    print("Couldn't reconnect.")

def FetchNextSibling(s) -> bs:
    soup = s # type: bs
    e = soup.next_sibling
    while e is not None:
        try:
            foundEscapes = re.search(r'\n|\r|\t',e)
        except TypeError:
            if type(e) is not bs4.Comment:
                return e
        if foundEscapes:
            e = e.next_sibling
        else:
            if type(e) is not bs4.Comment:
                return e
            else:
                e = e.next_sibling
    return None
def FetchPrevSibling(s) -> bs:
    soup = s # type: bs
    e = soup.previous_sibling
    soup.previous
    while e is not None:
        try:
            foundEscapes = re.search(r'\n|\r|\t',e)
        except TypeError:
            if type(e) is not bs4.Comment:
                return e
        if foundEscapes:
            e = e.previous_sibling
        else:
            if type(e) is not bs4.Comment:
                return e
            else:
                e = e.previous_sibling
    return None
def FixStr(o: str) -> str:
    additionalSolutions = {"::".encode("UTF-8") : b"."}
    additionalSolutions.update(COMMENT_UNICODE_REPLACEMENTS)
    # Split into a list of words.
    listOfWords = o.split(' ')
    # Search for problems.
    changed = False
    skipNextKey = False
    for word in listOfWords:
        indexOfWord = listOfWords.index(word)
        for key in additionalSolutions.keys():
            if key.decode("utf-8") in word and not skipNextKey:
                changed = True
                # Special condition.
                if key.decode("utf-8") == "::":
                    skipNextKey
                indexOfKey = listOfWords[indexOfWord].find(key.decode("utf-8"))
                _wordlist_ = list(listOfWords[indexOfWord])
                _wordlist_[indexOfKey] = additionalSolutions[key].decode("utf-8")
                if key.decode("utf-8") == "::":
                    _wordlist_.pop(indexOfKey+1)
                listOfWords[indexOfWord] = "".join(_wordlist_)
            else:
                continue
    if changed:
        print(" ".join(listOfWords))
    return " ".join(listOfWords)
def IsFriend(element1: bs, element2: bs):
    # Get element1 prev and next.
    element1sourceline = element1.sourceline
    for x in element2.descendants:
        if type(x) is not bs4.NavigableString:
            if x.sourceline == element1sourceline:
                return True
    for x in element2.descendants:
        if type(x) is not bs4.NavigableString:
            if x.sourceline == element1sourceline:
                return True
def GetParentSourceLineRange(parent: bs):
    listOfDescendants = list()
    minSourceLine = 0
    maxSourceLine = 0
    def GetMinSourceLine() -> int:
        nonlocal minSourceLine
        minSourceLine = listOfDescendants[0].sourceline
        for c in listOfDescendants:
            if minSourceLine > c.sourceline:
                minSourceLine = c.sourceline
        return minSourceLine
    def GetMaxSourceLine() -> int:
        nonlocal maxSourceLine
        maxSourceLine = listOfDescendants[0].sourceline
        for c in listOfDescendants:
            if maxSourceLine < c.sourceline:
                maxSourceLine = c.sourceline
        return maxSourceLine
    if parent.descendants != None:
        listOfDescendants = [c for c in parent.descendants] # type: list[bs]
    return (minSourceLine, maxSourceLine)
def FindChildViaSourceLine(range: tuple[int, int], parent:bs):
    pass
        
        

class DzObject():
    DzObjects = [] #type: list[DzObject]
    def __init__(self, name, link, dzPage=None):
        self.enums = [] # type: list[JSEnum]
        self.functions = [] # type: list[JSFunction]
        self.properties = [] # type: list[JSProperty]
        self.constructors = [] # type: list[JSConstructor]
        self.signals = [] # type: list[JSSignal]
        self.implements = [] # type: list[str]
        self.name = name
        self.link = link
        self.classinfo = ""
        self.dzPage = dzPage
        DzObject.DzObjects.append(self)

    def __del__(self):
        DzObject.DzObjects.remove(self)

    @classmethod
    def ExistsAll(cls, strObj):
        foundIt =False
        for obj in cls.DzObjects:
            if strObj in obj.enums or strObj in obj.functions or strObj in obj.properties or strObj in obj.constructors or strObj in obj.signals or strObj in obj.implements or strObj in obj.link or strObj in obj.name:
                foundIt = True
                break
        return foundIt

    @classmethod
    def FindObjAll(cls, strObj):
        for obj in cls.DzObjects:
            if strObj in obj.enums or strObj in obj.functions or strObj in obj.properties or strObj in obj.constructors or strObj in obj.signals or strObj in obj.implements or strObj in obj.link or strObj in obj.name:
                return obj
        return None
class JSProperty():
    def __init__(self, name: str, vType: str, val:str = "", description:str = "", dzObj:DzObject = None):
        self.name = name
        self.description = str(description.encode("UTF-8"),"UTF-8")
        self.type = str(vType.encode("UTF-8"),"UTF-8")
        self.val = str(val.encode("UTF-8"),"UTF-8")
        self.dzObj = dzObj
    
    def GetConstructorVersion(self) -> str:
        return f"this.{self.name} = {self.type};"

    def GetMethodVersion(self) -> str:
        return f"{self.name}:{self.type};"

    def GetRegularVersion(self) -> str:
        return f"var {self.name}:{self.type};"

    def GetJSDocDescription(self) -> str:
        totalMsg = COMMENT_TEMPLATE_BEGINNING + "\n"
        totalMsg += COMMENT_TEMPLATE_NEWLINE + f"@description {self.description}\n"
        totalMsg += "\t" + COMMENT_TEMPLATE_ENDING
        return totalMsg
class JSParameter():
    def __init__(self, name:str, vType:str, val:str = ""):
        self.name = str(name.encode("UTF-8"),"UTF-8")
        self.type = str(vType.encode("UTF-8"),"UTF-8")
        self.val = str(val.encode("UTF-8"),"UTF-8")   
class JSConstructor():
    def __init__(self, name:str, params="",properties=None, documentation:str = None):
        self.name = str(name.encode("UTF-8"),"UTF-8")
        self.params = self.ParseParams(params)
        self.properties = properties # type: list[JSProperty]
        self.message = self.ConvertToJS(self)
        self._rawdoc_ = str(documentation.encode("UTF-8"),"UTF-8")
        self.dzObj = DzObject.FindObjAll(name)
        self.documentation = self.GetJSDocDescription(self)
        
    
    @staticmethod
    def ParseParams(a):
        PARAM_IGNORE = ["…"]
    #[0] - Type [1] - var Name
        params = a # type: str
        # Check if commas.
        if "," in params:
            # Constructor has multiple parameters.
            _params = params.split(",")
            for x in _params:
                if x in PARAM_IGNORE:
                    _params.remove(x)
                    continue
                x = tuple(x.strip().split(" "))
            return _params
        else:
            # Constructor has one or none parameter.
            if params == "":
                return None
            else:
                return tuple(params.strip().split(" "))

    @classmethod
    def ConvertToJS(cls,j) -> str:
        SEPERATOR = ", "
        PARAM_IGNORE = ["…"]
        totalMsg = ""
        obj = j # type: cls
        # Get the length of params.
        if (obj.params is None or len(obj.params) == 0):
            totalMsg += "constructor() {\n\t"
        else:
            print(obj.params, obj.name, type(obj.params))
            if type(obj.params) is tuple:
                nameParams = f"{obj.params[1]}:{obj.params[0]}"
            else:
                nameParams = [name.strip().split(" ") for name in obj.params if name not in PARAM_IGNORE] # Get only the name value.
            if type(nameParams) is str:
                totalMsg += f"constructor({nameParams})" + " {\n\t"
            else:
                finalParam = []
                for param in nameParams:
                    paramVal = f"{param[1]}:{param[0]}"
                    finalParam.append(paramVal)
                
                totalMsg += f"constructor({SEPERATOR.join(finalParam)})" +" {\n\t"
        # Get our properties.
        # for prop in obj.properties:
        #     totalMsg += f"\n\t{prop.GetConstructorVersion()}"
        # Get our functions.
        # End it.
        totalMsg += "\n\t}"
        return totalMsg

    @classmethod
    def GetJSDocDescription(cls, self) -> str:
        if self._rawdoc_ is None:
            return ""
        totalMsg = COMMENT_TEMPLATE_BEGINNING + "\n"
        totalMsg += COMMENT_TEMPLATE_NEWLINE + f"@description {self._rawdoc_}\n"
        totalMsg += COMMENT_TEMPLATE_NEWLINE + "@constructor\n"
        totalMsg += COMMENT_TEMPLATE_ENDING + ";\n"
        return totalMsg
class JSFunction():
    def __init__(self, name, params, returnObj, desc, static = False, dzObj:DzObject=None):
        # Order of these are important. Some need to be intialized before the others.
        self.name = name
        self.params = self.ParseParams(params)
        self.returnObj = returnObj
        self.desc = self.GetJSDocDescription(desc)
        self.dzObj = dzObj
        self.static = static
        if dzObj.name == "Global":
            self.message = self.ConvertToJSGlobal(self)
        else:
            self.message = self.ConvertToJS(self)

    @staticmethod
    def ParseParams(a):

        PARAM_IGNORE = ["…"]
    #[0] - Type [1] - var Name
        params = a # type: str
        # Check if commas.
        if "," in params:
            # Constructor has multiple parameters.
            _params = params.split(",")
            for x in _params:
                if x in PARAM_IGNORE:
                    _params.remove(x)
                    continue
                if x == "function":
                    x = "_function"
                x = tuple(x.strip().split(" "))
            return _params
        else:
            # Constructor has one or none parameter.
            if params == "":
                return None
            else:
                #
                return tuple(params.strip().split(" "))

    @classmethod
    def ConvertToJS(cls,j) -> str:
        SEPERATOR = ", "
        PARAM_IGNORE = ["…"]
        totalMsg = ""
        obj = j # type: cls
        # Get the length of params.
        if (obj.params is None or len(obj.params) == 0):
            totalMsg += f"{obj.name}()" + " {\n\t"
        else:
            print(obj.params, obj.name, type(obj.params))
            if type(obj.params) is tuple:
                if len(obj.params) != 1:
                    if "=" in obj.params[1]:
                            # Get = index.
                            equalIndex = obj.params[1].index("=")
                            beforeEqualStr = obj.params[1][:equalIndex]
                            nameParams = f"{beforeEqualStr}:{obj.params[0]}"
                    else:
                        nameParams = f"{obj.params[1]}:{obj.params[0]}"
                else:
                    nameParams = obj.params[0]
            else:
                nameParams = [name.strip().split(" ") for name in obj.params if name not in PARAM_IGNORE]
                finalParam = []
                for param in nameParams:
                    if "=" in param[1]:
                        # Get = index.
                        equalIndex = param[1].index("=")
                        beforeEqualStr = param[1][:equalIndex]
                        paramVal = f"{beforeEqualStr}:{param[0]}"
                    else:
                        paramVal = f"{param[1]}:{param[0]}"
                    finalParam.append(paramVal)
            if type(nameParams) is str:
                if obj.static:
                    totalMsg += f"static {obj.name}({nameParams}):{j.returnObj.strip()}" + " {\n\t"
                else:
                    totalMsg += f"{obj.name}({nameParams}):{j.returnObj.strip()}" + " {\n\t"
            else:
                if obj.static:
                    totalMsg += f"static {obj.name}({SEPERATOR.join(finalParam)}):{j.returnObj.strip()}" + " {\n\t"
                else:
                    totalMsg += f"{obj.name}({SEPERATOR.join(finalParam)}):{j.returnObj.strip()}" +" {\n\t"
        # End it.
        totalMsg += "\n\t}"
        return totalMsg
    @classmethod
    def ConvertToJSGlobal(cls,j) -> str:
        SEPERATOR = ", "
        PARAM_IGNORE = ["…"]
        totalMsg = ""
        obj = j # type: cls
        # Get the length of params.
        if (obj.params is None or len(obj.params) == 0):
            totalMsg += f"function {obj.name}()" + " {\n\t"
        else:
            print(obj.params, obj.name, type(obj.params))
            if type(obj.params) is tuple:
                if len(obj.params) != 1:
                    if "=" in obj.params[1]:
                            # Get = index.
                            equalIndex = obj.params[1].index("=")
                            beforeEqualStr = obj.params[1][:equalIndex]
                            nameParams = f"{beforeEqualStr}:{obj.params[0]}"
                    else:
                        nameParams = f"{obj.params[1]}:{obj.params[0]}"
                else:
                    if obj.dzObj.ExistsAll(obj.params[0]):
                        obj.params = (obj.params[0],"val")
                        nameParams = obj.params
                    else:
                        nameParams = obj.params[0]
            else:
                nameParams = [name.strip().split(" ") for name in obj.params if name not in PARAM_IGNORE]
                finalParam = []
                for param in nameParams:
                    if "=" in param[1]:
                        # Get = index.
                        equalIndex = param[1].index("=")
                        beforeEqualStr = param[1][:equalIndex]
                        paramVal = f"{beforeEqualStr}:{param[0]}"
                    else:
                        paramVal = f"{param[1]}:{param[0]}"
                    finalParam.append(paramVal)
            if type(nameParams) is str:
                if obj.static:
                    totalMsg += f"static function {obj.name}({nameParams}):{j.returnObj.strip()}" + " {\n\t"
                else:
                    totalMsg += f"function {obj.name}({nameParams}):{j.returnObj.strip()}" + " {\n\t"
            else:
                if obj.static:
                    totalMsg += f"static function {obj.name}({SEPERATOR.join(finalParam)}):{j.returnObj.strip()}" + " {\n\t"
                else:
                    totalMsg += f"function {obj.name}({SEPERATOR.join(finalParam)}):{j.returnObj.strip()}" +" {\n\t"
        totalMsg += "\n\t}"
        return totalMsg
    @classmethod
    def GetJSDocDescription(cls, msg) -> str:
        totalMsg = COMMENT_TEMPLATE_BEGINNING + "\n"
        totalMsg += COMMENT_TEMPLATE_NEWLINE + f"@description {msg}\n"
        #totalMsg += COMMENT_TEMPLATE_NEWLINE + "@constructor\n"
        totalMsg += COMMENT_TEMPLATE_ENDING + "\n"
        return str(totalMsg.encode("utf-8"),"utf-8")
class JSEnum():
    def __init__(self, name:str, desc:str, dzObj:DzObject = None):
        self.name = name
        self.desc = self.GetJSDocDescription(desc)    
        self.dzObj = dzObj
        self.message = self.GetMethodVersion()

    @classmethod
    def GetJSDocDescription(cls, msg) -> str:
        totalMsg = COMMENT_TEMPLATE_BEGINNING + "\n"
        totalMsg += COMMENT_TEMPLATE_NEWLINE + f"@description ENUMERATOR: {msg}\n"
        #totalMsg += COMMENT_TEMPLATE_NEWLINE + "@constructor\n"
        totalMsg += COMMENT_TEMPLATE_ENDING + "\n"
        return str(totalMsg.encode("utf-8"),"utf-8")
    
    def GetMethodVersion(self) -> str:
        return f"static {self.name};"
class JSSignal():
    def __init__(self, name, params, signature, documentation, dzObj):
        self.name = name
        self.params = params
        self.signature = signature
        self.documentation = self.GetJsDocDescription(documentation)
        self.dzObj = dzObj

    @classmethod
    def GetJSDocDescription(cls, msg) -> str:
        totalMsg = COMMENT_TEMPLATE_BEGINNING + "\n"
        totalMsg += COMMENT_TEMPLATE_NEWLINE + f"@description {msg}\n"
        #totalMsg += COMMENT_TEMPLATE_NEWLINE + "@constructor\n"
        totalMsg += COMMENT_TEMPLATE_ENDING + "\n"
        return str(totalMsg.encode("utf-8"),"utf-8")

class JSClass():
    JsClasses = [] # type: list[JSClass]
    JS_CLASS_START = "class {}"
    def __init__(self, dzObj: DzObject):
        self.enums = dzObj.enums
        self.functions = dzObj.functions
        self.constructors = dzObj.constructors
        self.implements = dzObj.implements
        self.signals = dzObj.signals
        self.name = dzObj.name
        self.properties = dzObj.properties
        self.classinfo = dzObj.classinfo
        self.link = dzObj.link
        self.JsClasses.append(self)
    
    def __del__(self):
        self.JsClasses.remove(self)

    def __str__(self):
        if self.name != "Global":
            return self.WriteJSClass(self)
        else:
            return self.AddGlobals(self)
    
    
    @staticmethod
    def WriteJSClass(jsObj) -> str:
        jsClass = jsObj # type: JSClass
        implementMsg = ""
        """Returns a JS Class with required variables, functions, enums, etc."""
        totalMsg = ""
        # Start with class info.
        totalMsg += COMMENT_TEMPLATE_BEGINNING + "\n" + COMMENT_TEMPLATE_NEWLINE + "@classdesc " + jsObj.classinfo + "\n" + COMMENT_TEMPLATE_NEWLINE + "Go to documentation page at : {@link " + f"{jsObj.link}" + "}" + COMMENT_TEMPLATE_ENDING + "\n"
        # Start with implements.
        if len(jsClass.implements) != 0:
            implementMsg = " extends " + ", ".join(jsClass.implements)
        totalMsg += JSClass.JS_CLASS_START.format(jsClass.name) + implementMsg + " {\n"
        # Then variables.
        if len(jsClass.properties) !=0:
            for prop in jsClass.properties:
                totalMsg += "\t" + prop.GetMethodVersion() + "\n"
        # Then enums.
        if len(jsClass.enums) != 0:
            for enum in jsClass.enums:
                totalMsg += "\t" + enum.desc + "\t\n\t" + enum.message + "\n"
        # Then constructors.
        if len(jsClass.constructors) != 0:
            for constructor in jsClass.constructors:
                totalMsg += "\t" + constructor.documentation
                totalMsg += "\t" + constructor.message + "\n"
        # Then our functions/methods.
        if len(jsClass.functions) != 0:
            for function in jsClass.functions:
                totalMsg += "\t" + function.desc + "\t" + function.message + "\n"
        # End curly brace.
        if len(jsClass.constructors) != 0:
            totalMsg += "\n}"
        else:
            totalMsg += "\n}"
        return FixStr(totalMsg)

    @staticmethod
    def AddGlobals(jsObj) -> str:
        jsClass = jsObj # type: JSClass
        implementMsg = ""
        """Returns a JS Class with required variables, functions, enums, etc."""
        totalMsg = "\n////////////////////////////////////////GLOBALS/////////////////////////////////////////////\n"
        # Start with variables.
        if len(jsClass.properties) !=0:
            for prop in jsClass.properties:
                totalMsg +=prop.GetRegularVersion() + "\n"
        # Then our functions/methods.
        if len(jsClass.functions) != 0:
            for function in jsClass.functions:
                totalMsg += function.desc + function.message + "\n"
        return FixStr(totalMsg)

def GetClassDescription(DzObj:DzObject):
    try:
        soup = bs(urlopen(DzObj.link),features=HTML_PARSER)
    except OSError:
        print("Couldnt open URL. Trying again in 5 seconds... ")
        time.sleep(5)
        soup = TryReconnect(DzObj.link)
    except:
        soup = TryReconnect(DzObj.link)
    DzObj.dzPage = urlopen(DzObj.link).read()
    results1 = soup.find_all("div",{"class": "level2"})
    for r in results1:
        result = r #type: bs
        prevSib = FetchPrevSibling(result)
        workingDiv = None
        if prevSib is not None and prevSib.text == "Detailed Description":
            workingDiv = r
            break
    if workingDiv is not None:
        DzObj.classinfo = str(workingDiv.text.encode("UTF-8"),"UTF-8").strip()
def CreateImplements(x:DzObject):
    try:
        soup = bs(x.dzPage,features=HTML_PARSER)
    except OSError:
        print("Couldnt open URL. Trying again in 5 seconds... ")
        time.sleep(5)
        soup = TryReconnect(x.dzPage)
    except:
        soup = TryReconnect(x.dzPage)

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
                        if DzObject.ExistsAll(li[-1]):
                            if li[-1] not in lowestInherits:
                                lowestInherits.append(li[-1])
                                workingLi = l
                if workingLi is not None:
                    for l in lowestInherits:
                        x.implements.append(l)
def CreateProperties(x):
    DzObj = x # type: DzObject
    link = DzObj.dzPage
    try:
        soup = bs(link,features=HTML_PARSER)
    except RemoteDisconnected:
        print("REMOTE DISCONNECTED: Attempting to try again.")
        soup = TryReconnect(link)
    global COMMENT_TEMPLATE_CONSTRUCTOR
    global COMMENT_TEMPLATE_BEGINNING
    global COMMENT_TEMPLATE_ENDING
    global COMMENT_TEMPLATE_NEWLINE
    # Find all "level 3" class that is a div.
    level3s = soup.find_all(name="div", attrs={"class":"level3"})
    for x in level3s:
        search = x # type: bs
        nextSibling = FetchNextSibling(search)
        # If the next one we have doesn't have the id of "properties1" remove it.
        foundProperties = search.find_next_sibling("h3",{"id" : "properties1"},text="Properties")
        if (nextSibling is None or nextSibling.get("id","properties1") != "properties1" or nextSibling.name != "h3" or nextSibling.text != "Properties"):
            level3s.remove(x)
        else:
            print("Found 1")
    for x in level3s:
        # Check if there are <hr> tags. If so, do work. Otherwise, skip.
        search = x # type: bs
        qx = search.find_all("hr")
        query = [] # type: list[bs]
        for x in qx:
            hr = x # type: bs
            prevSibling = FetchPrevSibling(hr.parent) # type: bs
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
                if IsFriend(nextHr,query[0].parent):
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
            JSprop = JSProperty(v,rV,desc,dzObj=DzObj)
            DzObj.properties.append(JSprop)
            print(f"Return Value: {rV} | Variable Name: {v} | Definition: {desc}")
def CreateConstuctors(x):
    DzObj = x # type: DzObject
    link = DzObj.dzPage
    try:
        soup = bs(link,features=HTML_PARSER)
    except RemoteDisconnected:
        print("REMOTE DISCONNECTED: Attempting to try again.")
        soup = TryReconnect(link)
    except OSError:
        print("LOST CONNECTION: Retrying...")
        soup = TryReconnect(link)
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
        _previousSibling_ = FetchPrevSibling(lvl3)
        # If
        if (_previousSibling_ is not None and _previousSibling_.get("id","constructors1") == "constructors1" and _previousSibling_.name == "h3"):
            constructorDetailedSect = x
            break
    if constructorDetailedSect is None:
        print(f"Didn't find constructor for {DzObj.name}")
        return
    else:
        search = constructorDetailedSect
        qx = search.find_all("hr")
        query = []
        for x in qx:
            hr = x # type: bs
            prevSibling = FetchPrevSibling(hr.parent) # type: bs
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
            desc = d.get_text().strip() # type: str
            # Create our variable.
            JSconstructor = JSConstructor(cN,pA,DzObj.properties,desc)
            DzObj.constructors.append(JSconstructor)
            print(f"Constructor Name: {cN} | Definition: {desc}")
def CreateStaticMethods(DzObj:DzObject):
    try:
        soup = bs(DzObj.dzPage,features=HTML_PARSER)
    except OSError:
        print("Couldnt open URL. Trying again in 5 seconds... ")
        time.sleep(5)
        soup = TryReconnect(DzObj.dzPage)
    except:
        soup = TryReconnect(DzObj.dzPage)
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
        _previousSibling_ = FetchPrevSibling(lvl3)
        # If
        if (_previousSibling_ is not None and _previousSibling_.get("id","static_methods1") == "static_methods1" and _previousSibling_.name == "h3"):
            constructorDetailedSect = x
            break
    if constructorDetailedSect is None:
        print(f"Didn't find method for {DzObj.name}")
        return
    else:
        search = constructorDetailedSect
        qx = search.find_all("hr")
        query = []
        for x in qx:
            hr = x # type: bs
            prevSibling = FetchPrevSibling(hr.parent) # type: bs
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
            if p.find("a",{"class" : "wikilink1"}) != None:
                rT = p.find("a",{"class" : "wikilink1"}).get_text() # type: str
            else:
                rT = "void"
            # Get method name.
            mN = p.find("strong").get_text() # type: str
            # Get the parameters.
            pA = str(p.get_text().encode("UTF-8"),"UTF-8").strip()
            pA = pA[pA.index("(")+1:pA.index(")")].strip()
            # Get variable definition.
            d = p.findNext("p") # type: bs
            desc = d.get_text().strip() # type: str
            # Create our variable.
            JSmethod = JSFunction(mN,pA,rT,desc,True,DzObj)
            DzObj.functions.append(JSmethod)
            print(f"Static Method Name: {mN} | Method Parameters: {pA} |  Method Return Type: {rT} | Definition: {desc}")
def CreateMethods(DzObj:DzObject):
    try:
        soup = bs(DzObj.dzPage,features=HTML_PARSER)
    except OSError:
        print("Couldnt open URL. Trying again in 5 seconds... ")
        time.sleep(5)
        soup = TryReconnect(DzObj.dzPage)
    except:
        soup = TryReconnect(DzObj.dzPage)
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
        _previousSibling_ = FetchPrevSibling(lvl3)
        # If
        if (_previousSibling_ is not None and _previousSibling_.get("id","methods1") == "methods1" and _previousSibling_.name == "h3"):
            constructorDetailedSect = x
            break
    if constructorDetailedSect is None:
        print(f"Didn't find method for {DzObj.name}")
        return
    else:
        search = constructorDetailedSect
        qx = search.find_all("hr")
        query = []
        for x in qx:
            hr = x # type: bs
            prevSibling = FetchPrevSibling(hr.parent) # type: bs
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
            if p.find("a",{"class" : "wikilink1"}) != None:
                rT = p.find("a",{"class" : "wikilink1"}).get_text() # type: str
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
            desc = d.get_text().strip() # type: str
            # Create our variable.
            JSmethod = JSFunction(mN,pA,rT,desc,False,DzObj)
            DzObj.functions.append(JSmethod)
            print(f"Method Name: {mN} | Method Parameters: {pA} |  Method Return Type: {rT} | Definition: {desc}")
def CreateEnums(DzObj:DzObject):
    try:
        soup = bs(DzObj.dzPage,features=HTML_PARSER)
    except RemoteDisconnected:
        print("REMOTE DISCONNECTED: Attempting to try again.")
        soup = TryReconnect(DzObj.dzPage)
    except:
        soup = TryReconnect(DzObj.dzPage)
    # Find all "level 3" class that is a div.
    level3s = soup.find_all(name="div", attrs={"class":"level3"})
    for x in level3s:
        search = x # type: bs
        nextSibling = FetchNextSibling(search)
        # If the next one we have doesn't have the id of "enumerations1" remove it.
        foundProperties = search.find_next_sibling("h3",{"id" : "enumerations1"},text="Enumerations")
        if (nextSibling is None or nextSibling.get("id","enumerations1") != "enumerations1" or nextSibling.name != "h3" or nextSibling.text != "Properties"):
            level3s.remove(x)
        else:
            print("Found 1")
    for x in level3s:
        # Check if there are <hr> tags. If so, do work. Otherwise, skip.
        search = x # type: bs
        qx = search.find_all("hr")
        query = None # type: bs
        for x in qx:
            hr = x # type: bs
            prevSibling = FetchPrevSibling(hr.parent) # type: bs
            if prevSibling is not None and prevSibling.get("id") == "enumerations1":
                query = hr
                break
        if query is not None:
            for p in query.find_all_next("li",{"class": "level1"}):
                if not IsFriend(p,search):
                    continue
                # Get name.
                try:
                    enumName = p.find("strong").get_text() # type: str
                    e = p.get_text() #type: str
                    index = e.index("-") + 1
                    enumDesc = e[index:].strip()
                    JsEnum = JSEnum(enumName,enumDesc,DzObj)
                    DzObj.enums.append(JsEnum)
                    print(f"ENUM Name: {enumName} | Definition: {enumDesc}")
                except:
                    print(f"ENUM FAILED FOR {DzObj.name}.")
                    ERRORED_ENUMS.append(DzObj.name)
def DetermineIfEligible(x: DzObject):
    """ Checks if the class is a ECMAScript. If it is, we will return false. Otherwise true."""
    try:
        soup = bs(urlopen(x.link),features=HTML_PARSER)
    except RemoteDisconnected:
        print("REMOTE DISCONNECTED: Attempting to try again.")
        soup = TryReconnect(x.link)
    except OSError:
        print("LOST CONNECTION: Attempting to try again.")
        soup = TryReconnect(x.link)
    results = soup.find_all("div",attrs={"class" : "level1"})
    classDescription = None
    # Double check to see that we got the description.
    for y in results:
        result = y # type: bs
        prevElement = FetchPrevSibling(result)
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
def ProcessObject(DzObj: DzObject) -> None: 
    # Check if the a JS file has been made for this file.
    fileLocation = os.path.join(os.getcwd(),JS_NAME)
    with open(fileLocation, "ab+") as file:
        # Add header.
        if file.tell() == 0:
            HEADER = b"""// This script has been auto-generated by TheRealSolly | Solomon Blount.
// The following contents is all directly imported from DAZ's Documentation Website and inherits the license set, which is the following...
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Attribution 3.0 Unported (CC BY 3.0) | https://creativecommons.org/licenses/by/3.0/ | (C) Daz Productions, Inc 224 S 200 W, Salt Lake City, UT 84101
// I DO NOT WORK FOR DAZ PRODUCTIONS INC AND THIS SCRIPT WAS NOT SUPPORTED BY OR ENDORSED BY ANYONE AT DAZ PRODUCTIONS INC.
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// If I made your life wonderful, if you're feeling generious enough to donate to make me feel wonderful, you can do so by going here:
//                                                         https://www.buymeacoffee.com/therealsoll
// Anyway, here are some things you need to know.
//                                                THIS VERSION DOES NOT INCLUDE ENUMERATORS NOR SIGNALS AS OF YET.
//                                      THIS VERSION ALSO DOES NOT INCLUDE GLOBAL, STRING, NUMBER, BOOLEAN, ETC FUNCTIONS
//                                     THIS FILE PURPOSEFULLY HAS ERRORS SO THE INTELLISENSE CAN ASSIST YOU WITH YOUR CODE.
//                                             THIS HAS ONLY BEEN TESTED ON VISUAL STUDIO CODE VERSION 1.55.0.
// ok enough yelling. 
// To make .dsa scripts use the JS/TS interpreter, create a new file with the .dsa extension, on the lower-right of VSCode click on the file type and select "Configure file assocations for .dsa" and then select in JavaScript.
// Do not select TS as the interpreted language. Use JS. 
// There will be more adjustments to this script but i'm in school...so yeah: https://github.com/siblount/JzIntellisense
// Happy Coding!"""

            file.write(HEADER)
        GetClassDescription(DzObj)
        CreateImplements(DzObj)
        CreateConstuctors(DzObj)
        CreateEnums(DzObj)
        CreateProperties(DzObj)
        CreateStaticMethods(DzObj)
        CreateMethods(DzObj)
        workingClass = JSClass(DzObj)
        file.write(b"\n" + workingClass.__str__().encode("utf-8"))
        file.close()

def main():
    try:
        soup = bs(urlopen(OBJECT_INDEX_PAGE),features=HTML_PARSER)
    except OSError:
        print("Couldnt open URL. Trying again in 5 seconds... ")
        time.sleep(5)
        soup = TryReconnect(OBJECT_INDEX_PAGE)

    divCats = soup.find_all(attrs={"class" : "nspagesul"})
    objectLinks = []
    for x in divCats:
        DzLink = x # type: bs
        DzLinks = DzLink.find_all(attrs={"class" : "wikilink1"},text="DzERCLink")
        objectLinks.extend(DzLinks)
    #Initalize DzObjects.
    for link in objectLinks: 
        DzObject(link.get_text(),link["href"])
    # Process each DzObject.
    for x in DzObject.DzObjects:
        if not DetermineIfEligible(x) or x.name in IGNORE_OBJECTS:
            print(x.name + " is not eligble. Deleting.")
            x.__del__()
            continue
        ProcessObject(x)
        # CreateProperties(x)
    print("JzIntellisense.js complete!\n=================================================\n=================================================\n\n")
    print("ERRORED ENUMS\n")
    for error in ERRORED_ENUMS:
        print(error,end="\n")
    print("\nSKIPPED DZOBJS\n")
    for obj in SKIPPED_DZOBJS:
        print(obj,end="\n")

if __name__ == "__main__":
    main()