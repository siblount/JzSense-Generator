from jzsense.common.constants import *                                      # Get constants for this project.
from bs4 import BeautifulSoup as bs                                         # Our helpful HTML Parser. Used very often.
from urllib.request import urlopen                                          # Download html sourcecode.
from platform import system                                                 # For paths for different OS'
import re                                                                   # Search for string escapes. Probably can remove. I'm not sure.
import bs4                                                                  # Except, I think.
import time                                                                 # Sleep for a moment.

def TryReconnect(link) -> bs:
    for _ in range(HTML_RETRIES):
        try:
            return bs(urlopen(link),features=HTML_PARSER)
        except:
            print("Retry failed...trying again in 3 seconds.")
            time.sleep(3)
            continue
    print("Couldn't reconnect.")
def GenerateRE(msg:str) -> str:
    words = msg.strip().split(" ")
    for word in words:
        if word.strip() == "":
            words.remove(word)
        else:
            words[words.index(word)] = "(" + word + ")"
    return "|".join(words)
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
        pass
        #print(" ".join(listOfWords))
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
def GetParentSourceLineRange(parent: bs) -> tuple[int,int]:
    listOfDescendants = list(parent.find_all())
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
    return (GetMinSourceLine(), GetMaxSourceLine())
def IsInRange(nRange:tuple[int,int], number:int) -> bool:
    return number in range(nRange[0],nRange[1])
def GetReturnType(tableRowBS:bs) -> str:
    """Requires the `<tr>` bs object. Returns a string of the return type."""
    returnType = tableRowBS.find("td", {"class" : "memItemLeft"}) # type: bs
    if returnType is not None:
        return returnType.text
    else:
        print("WARNING: returnType returned None.")
def GetSymbolArgs(tableRowBS:bs) -> str:
    """ Requires the `<tr>` bs object. Returns a string of the property, parameters, and function/signal name."""
    value = tableRowBS.find("td", {"class" : "memItemRight"}) # type: bs
    if value is not None:
        return value.get_text()
    else:
        print("WARNING: value returned None.")
def FindMaxSourceLineGivenContextTable(tableRowBS:bs, strict:bool) -> int:
    """Returns the maximum source line for a given context, such as: Methods, Static Methods, Properties, etc."""
    trRange = GetParentSourceLineRange(tableRowBS.parent)
    def GetLast(context:bs) -> bs:
        """Recursive function to chop down `tr` elements until the very last one. Also checks if it is in the parent sourceline range."""
        if not strict:
            possibleTR = context.find_next("tr") # type: bs
            headerTR = possibleTR.find("h2")
        else:
            someObj = context.find_next_sibling()
            if someObj is not None and someObj.name == "tr":
                possibleTR = someObj
                headerTR = possibleTR.find("h2")
            else:
                possibleTR = None
                headerTR = None
        if possibleTR is not None and possibleTR.sourceline in range(trRange[0], trRange[1]+1) and (headerTR == None or headerTR is None):
            return GetLast(possibleTR)
        else:
            return context
    
    lastTR = GetLast(tableRowBS)
    return lastTR.sourceline
def FindMaxSourceLineGivenContext(divBS:bs) -> int:
    """Returns the maximum source line for a given context, such as: Methods, Static Methods, Properties, etc."""
    divRange = GetParentSourceLineRange(divBS.parent)
    h2 = divBS.find_next("h2")
    if h2 is not None:
        max = h2.sourceline
    else:
        max = divRange[1]
    # def GetLast(context:bs) -> bs:
    #     """Recursive function to chop down `div` elements until the very last one. Also checks if it is in the parent sourceline range."""
    #     possibleDiv = context.find_next(context.name) # type: bs
    #     if possibleDiv != None or possibleDiv is not None and possibleDiv.sourceline in range(divRange[0], divRange[1]+1) and possibleDiv.sourceline < max:
    #         return GetLast(possibleDiv)
    #     else:
    #         return context
    # lastTR = GetLast(divBS)
    # return lastTR.sourceline
    return max
def GetNextSiblingBS(context: bs, attrs:dict, min: int, max: int) -> bs:
                nextTr = context.find_next_sibling(context.name, attrs)
                if nextTr is not None and nextTr.sourceline in range(min, max):
                    return nextTr
def GetNextBS(context: bs, attrs:dict, min: int, max: int) -> bs:
                nextTr = context.find_next(context.name, attrs)
                if nextTr is not None and nextTr.sourceline in range(min, max):
                    return nextTr
def GetDetailedInfo(workingTr: bs, name: str, headerText="Member Data Documentation", params=None) -> tuple[str, str, str, str, str]:
    def GetParamsInfo(context:bs) -> str:
        """`context` is the `dl` object. Returns a string of parameter information. If multiple params, split text by `|!|`"""
        paramsInfo = []
        # Get the tbody.
        tbody = context.find("tbody") # type: bs
        if tbody is not None:
            # Get all trs.
            for x in tbody.find_all("tr"):
                tr = x # type: bs
                paramName = None
                paramDesc = None
                for y in tr.find_all("td"):
                    td = y # type: bs
                    potentialEm = td.find("em")
                    if potentialEm is None or paramName is not None: # DzScriptedRender::riAreaLightSource (desc for 'params' throws off em check because tokens is emphasized.
                        if td.text != (None or ""):
                            paramDesc = td.text
                        else:
                            continue
                    else:
                        paramName = potentialEm.text
                paramsInfo.append(f"{paramName} - {paramDesc.strip()}")
        if len(paramsInfo) == 0:
            return None
        else:
            return "|!|".join(paramsInfo)
    def GetReturnsInfo(context:bs) -> str:
        """`context` is the `dl` object. Returns a string of parameter information. If multiple params, split text by `|!|`"""
        # Get the tbody.
        dd = context.find("dd") # type: bs
        if dd is not None:
            return dd.text.strip()
    def GetAttentionInfo(context:bs) -> str:
        """`context` is the `dl` object. Returns a string of parameter information. If multiple params, split text by `|!|`"""
        # Get the tbody.
        dd = context.find("dd") # type: bs
        if dd is not None:
            return dd.text.strip()
        
    ###############################################
    
    # Find `h2` Member Data Documentation
    h2 = workingTr.find_next('h2', text=headerText)
    if h2 is not None:
        minSourceline = h2.find_next("div", {"class" : "memitem"}).sourceline
        maxSourceline = FindMaxSourceLineGivenContext(h2)
        lastDiv = None
        while True:
            if lastDiv is None:
                workingDiv = h2.find_next("div", {"class" : "memproto"})
            else:
                workingDiv = GetNextBS(lastDiv, {"class" : "memproto"}, minSourceline, maxSourceline)
            if workingDiv is None:
                break
            text = workingDiv.find("td", {"class" : "memname"}).parent.text # type: str
            if params != None:
                if text is not None and name in text and re.search(GenerateRE(params), text, re.ASCII) != None:
                    # We got our working Div.
                    lastDiv = workingDiv
                    break
                else:
                    lastDiv = workingDiv
            else:
                if text is not None and name in text:
                    # We got our working Div.
                    lastDiv = workingDiv
                    break
                else:
                    lastDiv = workingDiv
        workingDoc = lastDiv.find_next("div", {"class" : "memdoc"}) # type: bs
        # Do we need to chop down the workingDoc?
        if workingDoc.find("dl") == None:
            # If not, return only text info.
            return (workingDoc.text.strip(), None, None, None, None)
        else:
            # We got some work to do.
            # First find regular description.
            potentialP = workingDoc.findNext() # type: bs
            if potentialP is not None and potentialP.name == "p":
                regularDesc = potentialP.text.strip()
            else:
                regularDesc = None
            parametersDesc = None
            returnsDesc = None
            attentionDesc = None
            for d in workingDoc.find_all("dl"): # was lastDiv
                dl = d # type: bs
                boldType = dl.find("dt") # type: bs
                if boldType is not None:
                    workingBold = boldType.text
                    if "Parameters" in workingBold:
                        parametersDesc = GetParamsInfo(dl)
                    if "Returns" in workingBold:
                        returnsDesc = GetReturnsInfo(dl)
                    if "Attention" in workingBold:
                        attentionDesc = GetAttentionInfo(dl)
        return (regularDesc, returnsDesc, None, parametersDesc, attentionDesc)
    else:
        print("WARNING: Got properties but didn't find Member Data Documentation.")
def get_page_path(href:str) -> str:
    """ Returns the appropriate file path depending on your OS. """
    if system() == "Windows":
        return RF"file:pages\daz_v3\{href}"
    else:
        return RF"file:pages/daz_v3/{href}"