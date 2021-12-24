from jzsense.common.constants import *                                                  # Get constants for this project.
from bs4 import BeautifulSoup as bs                                         # Our helpful HTML Parser. Used very often.
from urllib.request import urlopen                                          # Download html sourcecode.
import re                                                                   # Search for string escapes. Probably can remove. I'm not sure.
import bs4                                                                  # Except, I think.
import time                                                                 # Sleep for a moment.

def try_connect(link:str, retry_count:int=3) -> bs:
    """ Attempts to connect to given `link` parameter using `urlopen`. Sleeps for 3 seconds on failed attempts and retries for `HTML_RETRIES` times. 
    If successful, returns `bs` object. Otherwise, NONE."""
    for _ in range(retry_count):
        try:
            return bs(urlopen(link),features=HTML_PARSER)
        except Exception as e:
            print("Retry failed...trying again in 3 seconds.")
            print(e)
            time.sleep(3)
            continue
    print("Couldn't reconnect.")
def fetch_next_sibling(s) -> bs:
    """ Repeatedly gets the `bs.next_sibling` until a `bs4.Tag` is found (in other words, something useful). This probably can be deleted."""
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
def fetch_prev_sibling(s) -> bs:
    """ Repeatedly gets the `bs.previous_sibling` until a `bs4.Tag` is found (in other words, something useful). This probably can be deleted."""
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
def fix_str(o: str) -> str:
    """ Fixes strings with non UTF-8 chars. It also changes C++ `::` to `.`. Returns a fixed string. """
    # saveFile(filename, mode, filetype = "DAZ Script", version = DzApp.getVersion()  {};
    # Fix fix_str so it doesn't remove the required ).
    additionalSolutions = {"::".encode("UTF-8") : b"."}
    additionalSolutions.update(COMMENT_UNICODE_REPLACEMENTS)
    # Split into a list of words.
    listOfWords = o.split(' ')
    # Search for problems.
    changed = False
    skipNextKey = False

    # This obviously can be improved.
    # TODO: Improve performance.
    for word in listOfWords:
        indexOfWord = listOfWords.index(word)
        for key in additionalSolutions.keys():
            if key.decode("utf-8") in word and not skipNextKey:
                changed = True
                # Special condition.
                if key.decode("utf-8") == "::":
                    skipNextKey # wtf did i do o_o
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
def is_element_neighbor(element1: bs, element2: bs) -> bool:
    """ My 1 AM, 2 hours of sleep function that needs to be fixed. """
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
def get_parent_source_line_range(parent: bs) -> tuple[int,int]:
    """ Gets the parent's source line range. Returns a `tuple[min: int, max: int]` of the min and max source line. """
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
def get_description(desc:bs, descP:bs):
    """ Gets advanced description of stuff. Currently only used for constructors, static methods, and methods. Returns a tuple of descriptions seperated."""
    textDesc = None # type: str
    returnDesc = None # type: str
    sinceDesc = None # type: str
    paramsDesc = None # type: str
    attentionDesc = None # type: str
    text = desc.text.strip()
    listOfSpecialDesc = ["Return Value:","Since:","See Also:","Example:","Attention:","Parameter(s):"]
    def _GetNextDesc_(find:str, context:bs) -> list[str]:
        listOfDC = []
        if context == None or context is None:
            return None
        if context.findNext("li",{"class":"li"}) != None and context.findNext("li",{"class":"li"}):
            prevContext = context.findNext("li",{"class":"level1"})
            while prevContext is not None or prevContext != None:
                rvDescCand = prevContext
                if rvDescCand != None and is_element_neighbor(rvDescCand, context):
                    listOfDC.append(rvDescCand.text.strip())
                    nextDescCand = rvDescCand.findNext("li",{"class":"level1"})
                    if nextDescCand != None and is_element_neighbor(nextDescCand, context):
                        prevContext = nextDescCand
                    else:
                        prevContext = None
        elif context.findNext("li",{"class":"level1"}) != None and context.findNext("li",{"class":"level1"}):
            prevContext = context.findNext("li",{"class":"level1"})
            while prevContext is not None or prevContext != None:
                rvDescCand = prevContext
                if rvDescCand != None and is_element_neighbor(rvDescCand, context):
                    listOfDC.append(rvDescCand.text.strip())
                    nextDescCand = rvDescCand.findNext("li",{"class":"level1"})
                    if nextDescCand != None and is_element_neighbor(nextDescCand, context):
                        prevContext = nextDescCand
                    else:
                        prevContext = None
        # else:
        #     if context.findNextSibling("li",{"class":"level1"}):
        #         prevContext = context.findNextSibling("li",{"class":"level1"})
        #         while prevContext is not None or prevContext != None:
        #             rvDescCand = prevContext
        #             if rvDescCand != None and IsFriend(rvDescCand, descP.parent) and rvDescCand.text.strip() not in listOfDC:
        #                 listOfDC.append(rvDescCand.text.strip())
        #                 prevContext = rvDescCand
        #             else:
        #                 prevContext = None
        return listOfDC
    def GetInfo(p, nexthr):
        nonlocal textDesc, returnDesc, sinceDesc, paramsDesc, attentionDesc
        pText = p.text.strip() # type: str
        try:
            specialDescType = listOfSpecialDesc[listOfSpecialDesc.index(pText)]
        except ValueError:
            return
        if specialDescType == listOfSpecialDesc[0]:
            nextUL = p.findNext("ul")
            if returnDesc is None and nextUL != None and nextUL.sourceline < nexthr:
                returnDesc = "".join(_GetNextDesc_(listOfSpecialDesc[0],nextUL))
            if returnDesc == "":
                returnDesc = None
        elif specialDescType == listOfSpecialDesc[1]:
            nextUL = p.findNext("ul")
            if sinceDesc is None and nextUL != None and nextUL.sourceline < nexthr:
                sinceDesc = "".join(_GetNextDesc_(listOfSpecialDesc[1],nextUL))
            if sinceDesc == "":
                sinceDesc = None
        elif specialDescType == listOfSpecialDesc[4]:
            nextUL = p.findNext("ul")
            if attentionDesc is None and nextUL != None and nextUL.sourceline < nexthr:
                attentionDesc = "".join(_GetNextDesc_(listOfSpecialDesc[4],nextUL))
            if attentionDesc == "":
                attentionDesc = None
        elif specialDescType == listOfSpecialDesc[5]:
            nextUL = p.findNext("ul")
            if paramsDesc is None and nextUL != None and nextUL.sourceline < nexthr:
                paramsDesc = "|!|".join(_GetNextDesc_(listOfSpecialDesc[5],nextUL))
            if paramsDesc == "":
                paramsDesc = None
        else:
            pass

    def GetNextHr(context:bs) -> int:
        nexthr = context.findNext("hr")
        if nexthr != None:
            nexthr = nexthr.sourceline
        else:
            nexthr = context.parent.findNext().sourceline - 1
        return nexthr
    # If text is equal to one of these... we got work to do.
    if text in listOfSpecialDesc:
        textDesc = None
        hr = GetNextHr(descP)
        GetInfo(desc, hr)
    else:
        textDesc = text

    nexthr = GetNextHr(descP)
    listOfPs = desc.find_next_siblings("p")
    for x in listOfPs:
        next = fetch_next_sibling(x)
        if next != None and next.name != "ul" and next.sourceline > nexthr and next.sourceline < descP.sourceline -1:
            listOfPs.remove(x)
        elif next == None:
            pass
    for p in listOfPs:
        GetInfo(p,nexthr)

    return (textDesc, returnDesc, sinceDesc, paramsDesc, attentionDesc)
def is_in_range(nRange:tuple[int,int], number:int) -> bool:
    """ No, it wasn't at 1 AM. It was at 2 AM. """
    return number in range(nRange[0],nRange[1])
def convert_to_daz_nomen(o:str) -> str:
    """Converts a string like `shape_dz` to `DzShape`"""
    if "dz" not in o:
        return o
    oList = o.split("_")
    for x in range(len(oList)):
        oList[x] = oList[x].capitalize()
    dz = oList.index("Dz")
    del oList[dz]
    combinedStr = "Dz" + "".join(oList)
    if combinedStr.lower() in V3_OBJECTS:
        # Find it.
        for x in V3_OBJECTS:
            if combinedStr.lower() == x.lower():
                return x
    else:
        return combinedStr

def remove_deprecated_str(name:str) -> str:
    """ Returns a string where "(deprecated)" is removed. String is also trimmed."""
    if "(deprecated)" in name:
        return name[:name.find("(deprecated)")].strip()
    elif "( deprecated )" in name:
        return name[:name.find("( deprecated )")].strip()

    else:
        return name