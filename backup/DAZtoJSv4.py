# """ Web scrabbing the DAZ Documentation Website and outputting a JS file to utilize Intellisense. """

# from http.client import RemoteDisconnected                                  # Used for one of the excepts.
# from bs4 import BeautifulSoup as bs                                         # Our helpful HTML Parser. Used very often.
# from urllib.request import urlopen                                          # Download html sourcecode.
# import os                                                                   # Path joining.
# import multiprocessing                                                      # Process multiple pages at a time.
# import time                                                                 # Sleep for a moment.
# import re                                                                   # Search for string escapes. Probably can remove. I'm not sure.
# import bs4                                                                  # Except, I think.
# import DAZtoJSv3                                                            # Used to get documentation from old documentation website (zipped).
# from datetime import datetime                                               # Timestamp JzSense file because I'm lazy ._.

# # Methods need to check to see if they return themselves.

# print("Initializing...")

# OBJECT_INDEX_PAGE = "http://docs.daz3d.com/doku.php/public/software/dazstudio/4/referenceguide/scripting/api_reference/object_index/start"
# JS_NAME = "JzSense.js"
# HTML_RETRIES = 3
# HTML_PARSER = "html5lib"
# HTML_LVL1_NAMES = ["level1", "level1 node"]
# IGNORE_OBJECTS = []
# COMMENT_TEMPLATE_BEGINNING = "/**"
# COMMENT_TEMPLATE_ENDING = "*/"
# COMMENT_TEMPLATE_NEWLINE = " * "
# COMMENT_TEMPLATE_PARAM = "@param {} {}}" # Format
# COMMENT_TEMPLATE_CONSTRUCTOR = "@constructor {}" # Format
# COMMENT_UNICODE_REPLACEMENTS = {"“".encode("UTF-8") : b'"', "”".encode("UTF-8") : b'"'} # HTML Parser doesn't play nice. :(
# ERRORED_ENUMS = [] # Updated at runtime.
# SKIPPED_DZOBJS = []

# # The only objects to process. May ignore if we replace v3 Documentation for "TODO: Add Description" descriptions in v4.
# V3_OBJECTS = "DzElementClipboard , DzSceneShader , DzMorph , DzMorphDeltas , DzScriptedStepsPane , DzScriptPane , DzScriptTab , DzNaturalSpline , DzExpression , DzAppSettingsMgr , DzExpressionInput , DzFaceGroup , DzShape , DzOGLDefaultShader , DzSmoothShadedStyle , DzOpenGLShader , DzSolidBoxStyle , DzStepButton , DzGeometry , DzStorable , DzPBuffer , DzPBufferView , DzPickStyle , DzColorGradient , DzHiddenLineStyle , DzHierarchyPane , DzImageExporter , DzPoserIKTargetFlag , DzTexturedStyle , DzImageImporter , DzPresetHelper , DzDefaultStyle , DzPropertyClipboard , DzUnshadedStyle , DzIndexList , DzInFile , DzDFormModifier , DzVertexGroup , DzVertexMap , DzLayeredImageExporter , DzVertexMesh , DzLayeredImageImporter , DzWeightMap , DzLitWireFrameStyle , DzWinAudioClip , DzWireBoxStyle , DzMap , DzWireFrameStyle , DzWireShadedStyle , DzWireTexturedStyle , DzWSModifier".split(" , ")


# def TryConnect(link) -> bs:
#     """ Attempts to connect to given `link` parameter using `urlopen`. Sleeps for 3 seconds on failed attempts and retries for `HTML_RETRIES` times. If successful, returns `bs` object. Otherwise, NONE."""
#     for _ in range(HTML_RETRIES):
#         try:
#             return bs(urlopen(link),features=HTML_PARSER)
#         except:
#             print("Retry failed...trying again in 3 seconds.")
#             time.sleep(3)
#             continue
#     print("Couldn't reconnect.")
# def FetchNextSibling(s) -> bs:
#     """ Repeatedly gets the `bs.next_sibling` until a `bs4.Tag` is found (in other words, something useful). This probably can be deleted."""
#     soup = s # type: bs
#     e = soup.next_sibling
#     while e is not None:
#         try:
#             foundEscapes = re.search(r'\n|\r|\t',e)
#         except TypeError:
#             if type(e) is not bs4.Comment:
#                 return e
#         if foundEscapes:
#             e = e.next_sibling
#         else:
#             if type(e) is not bs4.Comment:
#                 return e
#             else:
#                 e = e.next_sibling
#     return None
# def FetchPrevSibling(s) -> bs:
#     """ Repeatedly gets the `bs.previous_sibling` until a `bs4.Tag` is found (in other words, something useful). This probably can be deleted."""
#     soup = s # type: bs
#     e = soup.previous_sibling
#     soup.previous
#     while e is not None:
#         try:
#             foundEscapes = re.search(r'\n|\r|\t',e)
#         except TypeError:
#             if type(e) is not bs4.Comment:
#                 return e
#         if foundEscapes:
#             e = e.previous_sibling
#         else:
#             if type(e) is not bs4.Comment:
#                 return e
#             else:
#                 e = e.previous_sibling
#     return None
# def FixStr(o: str) -> str:
#     """ Fixes strings with non UTF-8 chars. It also changes C++ `::` to `.`. Returns a fixed string. """
#     additionalSolutions = {"::".encode("UTF-8") : b"."}
#     additionalSolutions.update(COMMENT_UNICODE_REPLACEMENTS)
#     # Split into a list of words.
#     listOfWords = o.split(' ')
#     # Search for problems.
#     changed = False
#     skipNextKey = False
#     for word in listOfWords:
#         indexOfWord = listOfWords.index(word)
#         for key in additionalSolutions.keys():
#             if key.decode("utf-8") in word and not skipNextKey:
#                 changed = True
#                 # Special condition.
#                 if key.decode("utf-8") == "::":
#                     skipNextKey
#                 indexOfKey = listOfWords[indexOfWord].find(key.decode("utf-8"))
#                 _wordlist_ = list(listOfWords[indexOfWord])
#                 _wordlist_[indexOfKey] = additionalSolutions[key].decode("utf-8")
#                 if key.decode("utf-8") == "::":
#                     _wordlist_.pop(indexOfKey+1)
#                 listOfWords[indexOfWord] = "".join(_wordlist_)
#             else:
#                 continue
#     if changed:
#         pass
#         #print(" ".join(listOfWords))
#     return " ".join(listOfWords)
# def IsFriend(element1: bs, element2: bs) -> bool:
#     """ My 1 AM, 2 hours of sleep function that needs to be fixed. """
#     # Get element1 prev and next.
#     element1sourceline = element1.sourceline
#     for x in element2.descendants:
#         if type(x) is not bs4.NavigableString:
#             if x.sourceline == element1sourceline:
#                 return True
#     for x in element2.descendants:
#         if type(x) is not bs4.NavigableString:
#             if x.sourceline == element1sourceline:
#                 return True
# def GetParentSourceLineRange(parent: bs) -> tuple[int,int]:
#     """ Gets the parent's source line range. Returns a `tuple[min: int, max: int]` of the min and max source line. """
#     listOfDescendants = list(parent.find_all())
#     minSourceLine = 0
#     maxSourceLine = 0
#     def GetMinSourceLine() -> int:
#         nonlocal minSourceLine
#         minSourceLine = listOfDescendants[0].sourceline
#         for c in listOfDescendants:
#             if minSourceLine > c.sourceline:
#                 minSourceLine = c.sourceline
#         return minSourceLine
#     def GetMaxSourceLine() -> int:
#         nonlocal maxSourceLine
#         maxSourceLine = listOfDescendants[0].sourceline
#         for c in listOfDescendants:
#             if maxSourceLine < c.sourceline:
#                 maxSourceLine = c.sourceline
#         return maxSourceLine
#     return (GetMinSourceLine(), GetMaxSourceLine())
# def GetDescription(desc:bs, descP:bs):
#     """ Gets advanced description of stuff. Currently only used for constructors, static methods, and methods. Returns a tuple of descriptions seperated."""
#     textDesc = None # type: str
#     returnDesc = None # type: str
#     sinceDesc = None # type: str
#     paramsDesc = None # type: str
#     attentionDesc = None # type: str
#     text = desc.text.strip()
#     listOfSpecialDesc = ["Return Value:","Since:","See Also:","Example:","Attention:","Parameter(s):"]
#     def _GetNextDesc_(find:str, context:bs) -> list[str]:
#         listOfDC = []
#         if context == None or context is None:
#             return None
#         if context.findNext("li",{"class":"li"}) != None and context.findNext("li",{"class":"li"}):
#             prevContext = context.findNext("li",{"class":"level1"})
#             while prevContext is not None or prevContext != None:
#                 rvDescCand = prevContext
#                 if rvDescCand != None and IsFriend(rvDescCand, context):
#                     listOfDC.append(rvDescCand.text.strip())
#                     nextDescCand = rvDescCand.findNext("li",{"class":"level1"})
#                     if nextDescCand != None and IsFriend(nextDescCand, context):
#                         prevContext = nextDescCand
#                     else:
#                         prevContext = None
#         elif context.findNext("li",{"class":"level1"}) != None and context.findNext("li",{"class":"level1"}):
#             prevContext = context.findNext("li",{"class":"level1"})
#             while prevContext is not None or prevContext != None:
#                 rvDescCand = prevContext
#                 if rvDescCand != None and IsFriend(rvDescCand, context):
#                     listOfDC.append(rvDescCand.text.strip())
#                     nextDescCand = rvDescCand.findNext("li",{"class":"level1"})
#                     if nextDescCand != None and IsFriend(nextDescCand, context):
#                         prevContext = nextDescCand
#                     else:
#                         prevContext = None
#         # else:
#         #     if context.findNextSibling("li",{"class":"level1"}):
#         #         prevContext = context.findNextSibling("li",{"class":"level1"})
#         #         while prevContext is not None or prevContext != None:
#         #             rvDescCand = prevContext
#         #             if rvDescCand != None and IsFriend(rvDescCand, descP.parent) and rvDescCand.text.strip() not in listOfDC:
#         #                 listOfDC.append(rvDescCand.text.strip())
#         #                 prevContext = rvDescCand
#         #             else:
#         #                 prevContext = None
#         return listOfDC
#     def GetInfo(p, nexthr):
#         nonlocal textDesc, returnDesc, sinceDesc, paramsDesc, attentionDesc
#         pText = p.text.strip() # type: str
#         try:
#             specialDescType = listOfSpecialDesc[listOfSpecialDesc.index(pText)]
#         except ValueError:
#             return
#         if specialDescType == listOfSpecialDesc[0]:
#             nextUL = p.findNext("ul")
#             if returnDesc is None and nextUL != None and nextUL.sourceline < nexthr:
#                 returnDesc = "".join(_GetNextDesc_(listOfSpecialDesc[0],nextUL))
#             if returnDesc == "":
#                 returnDesc = None
#         elif specialDescType == listOfSpecialDesc[1]:
#             nextUL = p.findNext("ul")
#             if sinceDesc is None and nextUL != None and nextUL.sourceline < nexthr:
#                 sinceDesc = "".join(_GetNextDesc_(listOfSpecialDesc[1],nextUL))
#             if sinceDesc == "":
#                 sinceDesc = None
#         elif specialDescType == listOfSpecialDesc[4]:
#             nextUL = p.findNext("ul")
#             if attentionDesc is None and nextUL != None and nextUL.sourceline < nexthr:
#                 attentionDesc = "".join(_GetNextDesc_(listOfSpecialDesc[4],nextUL))
#             if attentionDesc == "":
#                 attentionDesc = None
#         elif specialDescType == listOfSpecialDesc[5]:
#             nextUL = p.findNext("ul")
#             if paramsDesc is None and nextUL != None and nextUL.sourceline < nexthr:
#                 paramsDesc = "|!|".join(_GetNextDesc_(listOfSpecialDesc[5],nextUL))
#             if paramsDesc == "":
#                 paramsDesc = None
#         else:
#             pass

#     def GetNextHr(context:bs) -> int:
#         nexthr = context.findNext("hr")
#         if nexthr != None:
#             nexthr = nexthr.sourceline
#         else:
#             nexthr = context.parent.findNext().sourceline - 1
#         return nexthr
#     # If text is equal to one of these... we got work to do.
#     if text in listOfSpecialDesc:
#         textDesc = None
#         hr = GetNextHr(descP)
#         GetInfo(desc, hr)
#     else:
#         textDesc = text

#     nexthr = GetNextHr(descP)
#     listOfPs = desc.find_next_siblings("p")
#     for x in listOfPs:
#         next = FetchNextSibling(x)
#         if next != None and next.name != "ul" and next.sourceline > nexthr and next.sourceline < descP.sourceline -1:
#             listOfPs.remove(x)
#         elif next == None:
#             pass
#     for p in listOfPs:
#         GetInfo(p,nexthr)

#     return (textDesc, returnDesc, sinceDesc, paramsDesc, attentionDesc)
# def IsInRange(nRange:tuple[int,int], number:int) -> bool:
#     """ No, it wasn't at 1 AM. It was at 2 AM. """
#     return number in range(nRange[0],nRange[1])
# def ConvertToDAZNomen(o:str) -> str:
#     """Converts a string like `shape_dz` to `DzShape`"""
#     if "dz" not in o:
#         return o
#     oList = o.split("_")
#     for x in range(len(oList)):
#         oList[x] = oList[x].capitalize()
#     dz = oList.index("Dz")
#     del oList[dz]
#     combinedStr = "Dz" + "".join(oList)
#     if combinedStr.lower() in V3_OBJECTS:
#         # Find it.
#         for x in V3_OBJECTS:
#             if combinedStr.lower() == x.lower():
#                 return x
#     else:
#         return combinedStr

# # Classes used to hold parsed info.
# class DzObject():
#     DzObjects = [] #type: list[DzObject]
#     def __init__(self, name, link, dzPage=None):
#         self.enums = [] # type: list[JSEnum]
#         self.functions = [] # type: list[JSFunction]
#         self.properties = [] # type: list[JSProperty]
#         self.constructors = [] # type: list[JSConstructor]
#         self.signals = [] # type: list[JSSignal]
#         self.implements = [] # type: list[str]
#         self.name = name
#         self.link = link
#         self.classinfo = ""
#         self.dzPage = dzPage
#         DzObject.DzObjects.append(self)

#     @classmethod
#     def ExistsAll(cls, strObj):
#         foundIt =False
#         for obj in cls.DzObjects:
#             if strObj in obj.enums or strObj in obj.functions or strObj in obj.properties or strObj in obj.constructors or strObj in obj.signals or strObj in obj.implements or strObj in obj.link or strObj in obj.name:
#                 foundIt = True
#                 break
#         return foundIt

#     @classmethod
#     def FindObjAll(cls, strObj):
#         for obj in cls.DzObjects:
#             if strObj in obj.enums or strObj in obj.functions or strObj in obj.properties or strObj in obj.constructors or strObj in obj.signals or strObj in obj.implements or strObj in obj.link or strObj in obj.name:
#                 return obj
#         return None
# class JSProperty():
#     def __init__(self, name: str, vType: str, description:str = "", dzObj:DzObject = None):
#         self.name = name
#         self.description = str(description.encode("UTF-8"),"UTF-8").strip()
#         self.type = str(vType.encode("UTF-8"),"UTF-8")
#         self.dzObj = dzObj

#     def GetConstructorVersion(self) -> str:
#         return f"this.{self.name} = {self.type};"

#     def GetMethodVersion(self) -> str:
#         return f"{self.name}:{self.type};"

#     def GetRegularVersion(self) -> str:
#         return f"var {self.name}:{self.type};"

#     def GetJSDocDescription(self) -> str:
#         totalMsg = COMMENT_TEMPLATE_BEGINNING + "\n"
#         totalMsg += COMMENT_TEMPLATE_NEWLINE + f"@description {self.description}\n"
#         totalMsg += "\t" + COMMENT_TEMPLATE_ENDING
#         return totalMsg
# class JSParameter():
#     def __init__(self, name:str, vType:str, val:str = ""):
#         self.name = str(name.encode("UTF-8"),"UTF-8")
#         self.type = str(vType.encode("UTF-8"),"UTF-8")
#         self.val = str(val.encode("UTF-8"),"UTF-8")
# class JSConstructor():
#     def __init__(self, name:str, params="",properties=None, documentation:str = None):
#         self.name = str(name.encode("UTF-8"),"UTF-8")
#         self.params = self.ParseParams(params)
#         self.properties = properties # type: list[JSProperty]
#         self.message = self.ConvertToJS(self)
#         self.dzObj = DzObject.FindObjAll(name)
#         self.documentation = self.GetJSDocDescription(documentation)


#     @staticmethod
#     def ParseParams(a):
#         PARAM_IGNORE = ["…"]
#     #[0] - Type [1] - var Name
#         params = a # type: str
#         # Check if commas.
#         if "," in params:
#             # Constructor has multiple parameters.
#             _params = params.split(",")
#             for x in _params:
#                 if x in PARAM_IGNORE:
#                     _params.remove(x)
#                     continue
#                 x = tuple(x.strip().split(" "))
#                 for y in x:
#                     y = FixStr(y)
#             return _params
#         else:
#             # Constructor has one or none parameter.
#             if params == "":
#                 return None
#             else:
#                 x = tuple(params.strip().split(" "))
#                 for y in x:
#                     y = FixStr(y)
#                 return x

#     @classmethod
#     def ConvertToJS(cls,j) -> str:
#         # SEPERATOR = ", "
#         # PARAM_IGNORE = ["…"]
#         # totalMsg = ""
#         # obj = j # type: cls
#         # # Get the length of params.
#         # if (obj.params is None or len(obj.params) == 0):
#         #     totalMsg += "constructor() {\n\t"
#         # else:
#         #     #print(obj.params, obj.name, type(obj.params))
#         #     if type(obj.params) is tuple:
#         #         nameParams = f"{obj.params[1]}:{obj.params[0]}"
#         #     else:
#         #         nameParams = [name.strip().split(" ") for name in obj.params if name not in PARAM_IGNORE] # Get only the name value.
#         #     if type(nameParams) is str:
#         #         totalMsg += f"constructor({nameParams})" + " {\n\t"
#         #     else:
#         #         finalParam = []
#         #         for param in nameParams:
#         #             paramVal = f"{param[1]}:{param[0]}"
#         #             finalParam.append(paramVal)

#         #         totalMsg += f"constructor({SEPERATOR.join(finalParam)})" +" {\n\t"
#         # # Get our properties.
#         # # for prop in obj.properties:
#         # #     totalMsg += f"\n\t{prop.GetConstructorVersion()}"
#         # # Get our functions.
#         # # End it.
#         # totalMsg += "\n\t};"
#         # return totalMsg
#         SEPERATOR = ", "
#         PARAM_IGNORE = ["…"]
#         totalMsg = ""
#         obj = j # type: cls
#         # Get the length of params.
#         if (obj.params is None or len(obj.params) == 0):
#             totalMsg += "constructor() {\n\t"
#         else:
#             #print(obj.params, obj.name, type(obj.params))
#             if type(obj.params) is tuple:
#                 if len(obj.params) != 1:
#                     if "=" in obj.params[1]:
#                             # Get = index.
#                             equalIndex = obj.params[1].index("=")
#                             beforeEqualStr = obj.params[1][:equalIndex] # type: str
#                             nameParams = f"{FixStr(beforeEqualStr)}:{obj.params[0]}"
#                     else:
#                         nameParams = f"{FixStr(obj.params[1])}:{obj.params[0]}"
#                 else:
#                     nameParams = obj.params[0]
#             else:
#                 nameParams = [name.strip().split(" ") for name in obj.params if name not in PARAM_IGNORE]
#                 finalParam = []
#                 for param in nameParams:
#                     if "=" in param[1]:
#                         # Get = index.
#                         equalIndex = param[1].index("=")
#                         beforeEqualStr = param[1][:equalIndex]
#                         paramVal = f"{FixStr(beforeEqualStr)}:{param[0]}"
#                     else:
#                         paramVal = f"{param[1]}:{param[0]}"
#                     finalParam.append(paramVal)
#             if type(nameParams) is str:
#                 totalMsg += f"constructor({nameParams})" + " {\n\t"
#             else:
#                 totalMsg += f"constructor({SEPERATOR.join(finalParam)})" +" {\n\t"
#         # End it.
#         totalMsg += "\n\t};"
#         return totalMsg

#     @staticmethod
#     def GetJSDocDescription(msg) -> str:
#         # [0] - textDesc [1] - returnDesc [2] - sinceDesc [3] - paramsDesc [4] - attentionDesc
#         totalMsg = COMMENT_TEMPLATE_BEGINNING + "\n"
#         if msg[0] != None:
#             totalMsg += COMMENT_TEMPLATE_NEWLINE + f"@description {msg[0]}\n"
#         if msg[1] != None:
#             totalMsg += COMMENT_TEMPLATE_NEWLINE + f"@returns {msg[1]}\n"
#         if msg[2] != None:
#             totalMsg += COMMENT_TEMPLATE_NEWLINE + f"@since {msg[2]}\n"
#         if msg[3] != None:
#             listOfParams = msg[3].split("|!|") #list[str]
#             for param in listOfParams:
#                 totalMsg += COMMENT_TEMPLATE_NEWLINE + f"@param {param}\n"
#         if msg[4] != None:
#             totalMsg += COMMENT_TEMPLATE_NEWLINE + f"@attention {msg[4]}\n"
#         totalMsg += COMMENT_TEMPLATE_NEWLINE + "@constructor\n"
#         totalMsg += COMMENT_TEMPLATE_ENDING + "\n"
#         return str(totalMsg.encode("utf-8"),"utf-8")
# class JSFunction():
#     def __init__(self, name, params, returnObj, desc, static = False, dzObj:DzObject=None, otherInfo:tuple[str,str,str,str,str]=tuple()):
#         # Order of these are important. Some need to be intialized before the others.
#         self.name = name
#         self.params = self.ParseParams(params)
#         self.returnObj = returnObj
#         self.desc = self.GetJSDocDescription(desc)
#         self.dzObj = dzObj
#         self.static = static
#         if dzObj.name == "Global":
#             self.message = self.ConvertToJSGlobal(self)
#         else:
#             self.message = self.ConvertToJS(self)

#     @staticmethod
#     def ParseParams(a):

#         PARAM_IGNORE = ["…"]
#     #[0] - Type [1] - var Name
#         params = a # type: str
#         # Check if commas.
#         if "," in params:
#             # Constructor has multiple parameters.
#             _params = params.split(",")
#             for x in _params:
#                 if x in PARAM_IGNORE:
#                     _params.remove(x)
#                     continue
#                 if x == "function":
#                     x = "_function"
#                 x = tuple(x.strip().split(" "))
#             return _params
#         else:
#             # Constructor has one or none parameter.
#             if params == "":
#                 return None
#             else:
#                 #
#                 return tuple(params.strip().split(" "))

#     @classmethod
#     def ConvertToJS(cls,j) -> str:
#         SEPERATOR = ", "
#         PARAM_IGNORE = ["…"]
#         totalMsg = ""
#         obj = j # type: cls
#         # Get the length of params.
#         if (obj.params is None or len(obj.params) == 0):
#             totalMsg += f"{obj.name}():{j.returnObj.strip()}" + " {\n\t"
#         else:
#             #print(obj.params, obj.name, type(obj.params))
#             if type(obj.params) is tuple:
#                 if len(obj.params) != 1:
#                     if "=" in obj.params[1]:
#                             # Get = index.
#                             equalIndex = obj.params[1].index("=")
#                             beforeEqualStr = obj.params[1][:equalIndex]
#                             nameParams = f"{beforeEqualStr}:{obj.params[0]}"
#                     else:
#                         nameParams = f"{obj.params[1]}:{obj.params[0]}"
#                 else:
#                     nameParams = obj.params[0]
#             else:
#                 nameParams = [name.strip().split(" ") for name in obj.params if name not in PARAM_IGNORE]
#                 finalParam = []
#                 for param in nameParams:
#                     if "=" in param[1]:
#                         # Get = index.
#                         equalIndex = param[1].index("=")
#                         beforeEqualStr = param[1][:equalIndex]
#                         paramVal = f"{beforeEqualStr}:{param[0]}"
#                     else:
#                         paramVal = f"{param[1]}:{param[0]}"
#                     finalParam.append(paramVal)
#             if type(nameParams) is str:
#                 if obj.static:
#                     totalMsg += f"static {obj.name}({nameParams}):{j.returnObj.strip()}" + " {\n\t"
#                 else:
#                     totalMsg += f"{obj.name}({nameParams}):{j.returnObj.strip()}" + " {\n\t"
#             else:
#                 if obj.static:
#                     totalMsg += f"static {obj.name}({SEPERATOR.join(finalParam)}):{j.returnObj.strip()}" + " {\n\t"
#                 else:
#                     totalMsg += f"{obj.name}({SEPERATOR.join(finalParam)}):{j.returnObj.strip()}" +" {\n\t"
#         # End it.
#         totalMsg += "\n\t};"
#         return totalMsg
#     @classmethod
#     def ConvertToJSGlobal(cls,j) -> str:
#         SEPERATOR = ", "
#         PARAM_IGNORE = ["…"]
#         totalMsg = ""
#         obj = j # type: cls
#         # Get the length of params.
#         if (obj.params is None or len(obj.params) == 0):
#             totalMsg += f"function {obj.name}()" + " {\n\t"
#         else:
#             #print(obj.params, obj.name, type(obj.params))
#             if type(obj.params) is tuple:
#                 if len(obj.params) != 1:
#                     if "=" in obj.params[1]:
#                             # Get = index.
#                             equalIndex = obj.params[1].index("=")
#                             beforeEqualStr = obj.params[1][:equalIndex]
#                             nameParams = f"{beforeEqualStr}:{obj.params[0]}"
#                     else:
#                         nameParams = f"{obj.params[1]}:{obj.params[0]}"
#                 else:
#                     if obj.dzObj.ExistsAll(obj.params[0]):
#                         obj.params = (obj.params[0],"val")
#                         nameParams = obj.params
#                     else:
#                         nameParams = obj.params[0]
#             else:
#                 nameParams = [name.strip().split(" ") for name in obj.params if name not in PARAM_IGNORE]
#                 finalParam = []
#                 for param in nameParams:
#                     if "=" in param[1]:
#                         # Get = index.
#                         equalIndex = param[1].index("=")
#                         beforeEqualStr = param[1][:equalIndex]
#                         paramVal = f"{beforeEqualStr}:{param[0]}"
#                     else:
#                         paramVal = f"{param[1]}:{param[0]}"
#                     finalParam.append(paramVal)
#             if type(nameParams) is str:
#                 if obj.static:
#                     totalMsg += f"static function {obj.name}({nameParams}):{j.returnObj.strip()}" + " {\n\t"
#                 else:
#                     totalMsg += f"function {obj.name}({nameParams}):{j.returnObj.strip()}" + " {\n\t"
#             else:
#                 if obj.static:
#                     totalMsg += f"static function {obj.name}({SEPERATOR.join(finalParam)}):{j.returnObj.strip()}" + " {\n\t"
#                 else:
#                     totalMsg += f"function {obj.name}({SEPERATOR.join(finalParam)}):{j.returnObj.strip()}" +" {\n\t"
#         totalMsg += "\n\t};"
#         return totalMsg
#     @staticmethod
#     def GetJSDocDescription(msg) -> str:
#         # [0] - textDesc [1] - returnDesc [2] - sinceDesc [3] - paramsDesc [4] - attentionDesc
#         totalMsg = COMMENT_TEMPLATE_BEGINNING + "\n"
#         if msg[0] != None:
#             totalMsg += COMMENT_TEMPLATE_NEWLINE + f"@description {msg[0]}\n"
#         if msg[1] != None:
#             totalMsg += COMMENT_TEMPLATE_NEWLINE + f"@returns {msg[1]}\n"
#         if msg[2] != None:
#             totalMsg += COMMENT_TEMPLATE_NEWLINE + f"@since {msg[2]}\n"
#         if msg[3] != None:
#             listOfParams = msg[3].split("|!|") #list[str]
#             for param in listOfParams:
#                 totalMsg += COMMENT_TEMPLATE_NEWLINE + f"@param {param}\n"
#         if msg[4] != None:
#             totalMsg += COMMENT_TEMPLATE_NEWLINE + f"@attention {msg[4]}\n"
#         totalMsg += COMMENT_TEMPLATE_ENDING + "\n"
#         return str(totalMsg.encode("utf-8"),"utf-8")
# class JSEnum():
#     def __init__(self, name:str, desc:str, dzObj:DzObject = None):
#         self.name = name
#         self.desc = self.GetJSDocDescription(desc)
#         self.dzObj = dzObj
#         self.message = self.GetMethodVersion(self)

#     @classmethod
#     def GetJSDocDescription(cls, msg) -> str:
#         totalMsg = COMMENT_TEMPLATE_BEGINNING + "\n"
#         totalMsg += COMMENT_TEMPLATE_NEWLINE + f"@description ENUMERATOR: {msg}\n"
#         #totalMsg += COMMENT_TEMPLATE_NEWLINE + "@constructor\n"
#         totalMsg += COMMENT_TEMPLATE_ENDING + "\n"
#         return str(totalMsg.encode("utf-8"),"utf-8")

#     @classmethod
#     def GetMethodVersion(cls,self) -> str:
#         return f"static {self.name};"

#     @classmethod
#     def ConvertToJS(cls,j) -> str:
#         SEPERATOR = ", "
#         PARAM_IGNORE = ["…"]
#         totalMsg = ""
#         obj = j # type: cls
#         # Get the length of params.
#         if (obj.params is None or len(obj.params) == 0):
#             totalMsg += f"{obj.name}():void" + " {\n\t"
#         else:
#             #print(obj.params, obj.name, type(obj.params))
#             if type(obj.params) is tuple:
#                 if len(obj.params) != 1:
#                     if "=" in obj.params[1]:
#                             # Get = index.
#                             equalIndex = obj.params[1].index("=")
#                             beforeEqualStr = obj.params[1][:equalIndex]
#                             nameParams = f"{beforeEqualStr}:{obj.params[0]}"
#                     else:
#                         nameParams = f"{obj.params[1]}:{obj.params[0]}"
#                 else:
#                     nameParams = obj.params[0]
#             else:
#                 nameParams = [name.strip().split(" ") for name in obj.params if name not in PARAM_IGNORE]
#                 finalParam = []
#                 for param in nameParams:
#                     if "=" in param[1]:
#                         # Get = index.
#                         equalIndex = param[1].index("=")
#                         beforeEqualStr = param[1][:equalIndex]
#                         paramVal = f"{beforeEqualStr}:{param[0]}"
#                     else:
#                         paramVal = f"{param[1]}:{param[0]}"
#                     finalParam.append(paramVal)
#             if type(nameParams) is str:
#                 if obj.static:
#                     totalMsg += f"static {obj.name}({nameParams}):void" + " {\n\t"
#                 else:
#                     totalMsg += f"{obj.name}({nameParams}):void" + " {\n\t"
#             else:
#                 if obj.static:
#                     totalMsg += f"static {obj.name}({SEPERATOR.join(finalParam)}):void" + " {\n\t"
#                 else:
#                     totalMsg += f"{obj.name}({SEPERATOR.join(finalParam)}):void" +" {\n\t"
#         # End it.
#         totalMsg += "\n\t}"
#         return totalMsg
# class JSSignal():
#     def __init__(self, name, params, signature, documentation, dzObj):
#         self.name = name
#         self.params = self.ParseParams(params)
#         self.signature = signature
#         self.documentation = self.GetJSDocDescription(documentation, signature)
#         self.message = self.ConvertToJS(self)
#         self.dzObj = dzObj
#     @staticmethod
#     def ParseParams(a):

#         PARAM_IGNORE = ["…"]
#     #[0] - Type [1] - var Name
#         params = a # type: str
#         # Check if commas.
#         if "," in params:
#             # Constructor has multiple parameters.
#             _params = params.split(",")
#             for x in _params:
#                 if x in PARAM_IGNORE:
#                     _params.remove(x)
#                     continue
#                 if x == "function":
#                     x = "_function"
#                 x = tuple(x.strip().split(" "))
#             return _params
#         else:
#             # Constructor has one or none parameter.
#             if params == "":
#                 return None
#             else:
#                 #
#                 return tuple(params.strip().split(" "))

#     @classmethod
#     def ConvertToJS(cls,j) -> str:
#         SEPERATOR = ", "
#         PARAM_IGNORE = ["…"]
#         totalMsg = ""
#         obj = j # type: cls
#         # Get the length of params.
#         if (obj.params is None or len(obj.params) == 0):
#             totalMsg += f"{obj.name}():void" + " {\n\t"
#         else:
#             #print(obj.params, obj.name, type(obj.params))
#             if type(obj.params) is tuple:
#                 if len(obj.params) != 1:
#                     if "=" in obj.params[1]:
#                             # Get = index.
#                             equalIndex = obj.params[1].index("=")
#                             beforeEqualStr = obj.params[1][:equalIndex]
#                             nameParams = f"{beforeEqualStr}:{obj.params[0]}"
#                     else:
#                         nameParams = f"{obj.params[1]}:{obj.params[0]}"
#                 else:
#                     nameParams = obj.params[0]
#             else:
#                 nameParams = [name.strip().split(" ") for name in obj.params if name not in PARAM_IGNORE]
#                 finalParam = []
#                 for param in nameParams:
#                     if "=" in param[1]:
#                         # Get = index.
#                         equalIndex = param[1].index("=")
#                         beforeEqualStr = param[1][:equalIndex]
#                         paramVal = f"{beforeEqualStr}:{param[0]}"
#                     else:
#                         paramVal = f"{param[1]}:{param[0]}"
#                     finalParam.append(paramVal)
#             if type(nameParams) is str:
#                     totalMsg += f"{obj.name}({nameParams}):void" + " {\n\t"
#             else:
#                     totalMsg += f"{obj.name}({SEPERATOR.join(finalParam)}):void" +" {\n\t"
#         # End it.
#         totalMsg += "\n\t};"
#         return totalMsg

#     @classmethod
#     def GetJSDocDescription(cls, msg, signature) -> str:
#         totalMsg = COMMENT_TEMPLATE_BEGINNING + "\n"
#         totalMsg += COMMENT_TEMPLATE_NEWLINE+ "**THIS IS A NOT AN ACTUAL FUNCTION**, THIS IS A `signal`! USE ONLY THE `signature`.\n "
#         totalMsg += COMMENT_TEMPLATE_NEWLINE + f"@description {msg}\n"
#         totalMsg += COMMENT_TEMPLATE_NEWLINE + f"@signature `{signature}`\n"
#         totalMsg += COMMENT_TEMPLATE_NEWLINE + f"@event\n"
#         #totalMsg += COMMENT_TEMPLATE_NEWLINE + "@constructor\n"
#         totalMsg += COMMENT_TEMPLATE_ENDING + "\n"
#         return str(totalMsg.encode("utf-8"),"utf-8")
# class JSClass():
#     JsClasses = [] # type: list[JSClass]
#     JS_CLASS_START = "class {}"
#     def __init__(self, dzObj: DzObject):
#         self.enums = dzObj.enums
#         self.functions = dzObj.functions
#         self.constructors = dzObj.constructors
#         self.implements = dzObj.implements
#         self.signals = dzObj.signals
#         self.name = dzObj.name
#         self.properties = dzObj.properties
#         self.classinfo = dzObj.classinfo
#         self.link = dzObj.link
#         self.dzObj = dzObj
#         self.JsClasses.append(self)

#     def __del__(self):
#         self.JsClasses.remove(self)

#     def __str__(self):
#         if self.name != "Global":
#             return self.WriteJSClass(self)
#         else:
#             return self.AddGlobals(self)

#     @classmethod
#     def BeautifyText(self, text:str):
#         lineList = text.split("\n")
#         for line in lineList:
#             wordList = line.split()
#             for word in wordList:
#                 for property in self.properties:
#                     if word in property.name :
#                         word = f"`{word}`"
#     # TODO

#     @staticmethod
#     def WriteJSClass(jsObj) -> str:
#         jsClass = jsObj # type: JSClass
#         implementMsg = ""
#         """Returns a JS Class with required variables, functions, enums, etc."""
#         totalMsg = ""
#         # Start with class info.
#         totalMsg += COMMENT_TEMPLATE_BEGINNING + "\n" + COMMENT_TEMPLATE_NEWLINE + "@classdesc " + jsObj.classinfo + "\n" + COMMENT_TEMPLATE_NEWLINE + " For more information, go to: {@link " + f"{jsObj.link}" + "} " + COMMENT_TEMPLATE_ENDING + "\n"
#         # Start with implements.
#         if len(jsClass.implements) != 0:
#             implementMsg = " extends " + ", ".join(jsClass.implements)
#         totalMsg += JSClass.JS_CLASS_START.format(jsClass.name) + implementMsg + " {\n"
#         # Then variables.
#         if len(jsClass.properties) !=0:
#             for prop in jsClass.properties:
#                 totalMsg += "\t" + prop.GetJSDocDescription() + "\n"
#                 totalMsg += "\t" + prop.GetMethodVersion() + "\n"
#         # Then enums.
#         if len(jsClass.enums) != 0:
#             for enum in jsClass.enums:
#                 totalMsg += "\t" + enum.desc + "\t\n\t" + enum.message + "\n"
#         # Then constructors.
#         if len(jsClass.constructors) != 0:
#             for constructor in jsClass.constructors:
#                 totalMsg += "\t" + constructor.documentation
#                 totalMsg += "\t" + constructor.message + "\n"
#         # Then our functions/methods.
#         if len(jsClass.functions) != 0:
#             for function in jsClass.functions:
#                 totalMsg += "\t" + function.desc + "\t" + function.message + "\n"
#         # Then signals
#         if len(jsClass.signals) != 0:
#             for signal in jsClass.signals:
#                 totalMsg += "\t" + signal.documentation + "\t" + signal.message + "\n"
#         # We are done.
#         # End curly brace.
#         if jsClass.name == "Global":
#             return FixStr(totalMsg)
#         else:
#             totalMsg += "\n}"
#         return FixStr(totalMsg)

#     @staticmethod
#     def AddGlobals(jsObj) -> str:
#         jsClass = jsObj # type: JSClass
#         implementMsg = ""
#         """Returns a JS Class with required variables, functions, enums, etc."""
#         totalMsg = "\n////////////////////////////////////////GLOBALS/////////////////////////////////////////////\n"
#         # Start with variables.
#         if len(jsClass.properties) !=0:
#             for prop in jsClass.properties:
#                 totalMsg +=prop.GetRegularVersion() + "\n"
#         # Then our functions/methods.
#         if len(jsClass.functions) != 0:
#             for function in jsClass.functions:
#                 totalMsg += function.desc + function.message + "\n"
#         return FixStr(totalMsg)

# # Functions to parse information from web page source and create JSObjects. Returns nothing. Requires DzObj.
# def GetClassDescription(DzObj:DzObject):
#     """ Gets the class detailed description and will be stored to `DzObj.classinfo`."""
#     # This seriously needs to be reworked.
#     soup = TryConnect(DzObj.link)
#     try:
#         DzObj.dzPage = urlopen(DzObj.link).read()
#     except:
#         while True:
#             try:
#                 DzObj.dzPage = urlopen(DzObj.link).read()
#             except:
#                 pass 
#             else:
#                 break
#     # Pattern: h2 source line - previous sibling source line.
#     # Get all the h2's with class = level2. 
#     results1 = soup.find_all("div",{"class": "level2"})
#     for r in results1:
#         result = r # type: bs
#         prevSib = FetchPrevSibling(result)
#         workingDiv = None
#         if prevSib is not None and prevSib.text == "Detailed Description":
#             workingDiv = r
#             break
#     if workingDiv is not None:
#         # Find all Example: and Attention.
#         totalMsg = ""
#         # Find normal description before text.
#         for y in workingDiv.find_all("p"):
#             workingP = y # type: bs
#             if IsInRange(GetParentSourceLineRange(workingDiv),workingP.sourceline):
#                 if "Example" in workingP.text:
#                     break
#                 else:
#                     totalMsg += "\n" + str(workingP.text.encode("UTF-8"),"UTF-8").strip()
#         for x in workingDiv.find_all("strong"):
#             strong = x # type: bs
#             if strong.text == "Example:":
#                 # Get the parent of strong.
#                 p = strong.parent # type: bs
#                 nextP = p.findNext("p") # type: bs
#                 if nextP is not None or nextP != None:
#                     totalMsg += str(nextP.text.encode("UTF-8"),"UTF-8").strip() + "\n"
#                 code = p.findNext("pre", {"class" : "code ecmascript"}) # type: bs
#                 if code != None or code is not None:
#                     msg = "\n### Example:\n```\n" + code.text.strip() + "\n```\n" # type: str
#                     totalMsg += str(msg.encode("UTF-8"),"UTF-8")
#             elif strong.text == "Attention:":
#                 # Get the parent of strong
#                 p = strong.parent # type: bs
#                 # Get next object.
#                 nextObj = p.findNext() #type: bs
#                 if nextObj is not None or nextObj != None:
#                     totalMsg += "@attention " + str(nextObj.text.encode("UTF-8"),"UTF-8").strip()

#         DzObj.classinfo = str(totalMsg.encode("UTF-8"),"UTF-8").strip()
# def CreateImplements(x:DzObject):
#     """ Reads the source code, recursively searches for the lowest level class and adds it to implements in the DzObj. """
#     try:
#         soup = bs(x.dzPage,features=HTML_PARSER)
#     except OSError:
#         print("Couldnt open URL. Trying again in 5 seconds... ")
#         time.sleep(5)
#         soup = TryConnect(x.dzPage)
#     except:
#         soup = TryConnect(x.dzPage)

#     if soup.find(text="Inherits :"):
#         global HTML_LVL1_NAMES
#         lowestInherits = []
#         for name in HTML_LVL1_NAMES:
#             # Find all "level1" classes.
#             level1Classes = soup.find_all(attrs={"class": name})
#             for c in level1Classes:
#                 Class = c # type: bs
#                 # Find li class with "level1" or "level1 node":
#                 workingLi = None # type: bs
#                 for y in HTML_LVL1_NAMES:
#                     lis = Class.find_all("li",{"class" : y}) # type: bs
#                     for l in lis:
#                         li = l # type: bs
#                         li = li.text.strip().split(" ")
#                         if DzObject.ExistsAll(li[-1]):
#                             if li[-1] not in lowestInherits:
#                                 lowestInherits.append(li[-1])
#                                 workingLi = l
#                 if workingLi is not None:
#                     for l in lowestInherits:
#                         x.implements.append(l)
# def CreateProperties(x):
#     DzObj = x # type: DzObject
#     link = DzObj.dzPage
#     try:
#         soup = bs(link,features=HTML_PARSER)
#     except RemoteDisconnected:
#         print("REMOTE DISCONNECTED: Attempting to try again.")
#         soup = TryConnect(link)
#     global COMMENT_TEMPLATE_CONSTRUCTOR
#     global COMMENT_TEMPLATE_BEGINNING
#     global COMMENT_TEMPLATE_ENDING
#     global COMMENT_TEMPLATE_NEWLINE
#     # Find all "level 3" class that is a div.
#     level3s = soup.find_all(name="div", attrs={"class":"level3"})
#     for x in level3s:
#         search = x # type: bs
#         prevSibling = FetchPrevSibling(search)
#         # If the next one we have doesn't have the id of "properties1" remove it.
#         if (prevSibling is None or prevSibling.get("id","properties1") != "properties1" or prevSibling.name != "h3" or prevSibling.text != "Properties"):
#             level3s.remove(x)

#         else:
#             #print("Found 1")
#             pass
#     for x in level3s:
#         # Check if there are <hr> tags. If so, do work. Otherwise, skip.
#         search = x # type: bs
#         qx = search.find_all("hr")
#         query = [] # type: list[bs]
#         for x in qx:
#             hr = x # type: bs
#             prevSibling = FetchPrevSibling(hr.parent) # type: bs
#             if prevSibling is not None and prevSibling.get("id") == "properties1":
#                 query.append(hr)
#         #query = [hr for hr in query if hr.parent.fetchPreviousSiblings(attrs={"id": "properties1"}, limit= 1) == "properties1"]
#         if len(query) == 0:
#             # Bye felisha
#             continue
#         previousHr = query[0]
#         while True:
#             nextHr = previousHr.find_next("hr") # type: bs
#             if nextHr is not None:
#                 if IsFriend(nextHr,query[0].parent):
#                     query.append(nextHr)
#                     previousHr = nextHr
#                 else:
#                     previousHr = nextHr
#             else:
#                 break

#         # Else, we got a trash tree to go chop down.
#         for property in query:
#             # For every <hr> tag...
#             _property = property # type: bs
#             # Get the <p> tag below it.
#             p = _property.findNext("p") # type: bs
#             # Get property return value.
#             rV = p.find("a").get_text() # type: str
#             # Get variable name.
#             v = p.find("strong").get_text() # type: str
#             # Get variable definition.
#             d = p.findNext("p") # type: bs
#             desc = d.get_text() # type: str
#             for prop in DzObj.properties:
#                 if prop.name == v:
#                     return
#             JSprop = JSProperty(v,rV,desc,dzObj=DzObj)
#             DzObj.properties.append(JSprop)
#             #print(f"Return Value: {rV} | Variable Name: {v} | Definition: {desc}")
# def CreateConstuctors(x):
#     DzObj = x # type: DzObject
#     link = DzObj.dzPage
#     try:
#         soup = bs(link,features=HTML_PARSER)
#     except RemoteDisconnected:
#         print("REMOTE DISCONNECTED: Attempting to try again.")
#         soup = TryConnect(link)
#     except OSError:
#         print("LOST CONNECTION: Retrying...")
#         soup = TryConnect(link)
#     global COMMENT_TEMPLATE_CONSTRUCTOR
#     global COMMENT_TEMPLATE_BEGINNING
#     global COMMENT_TEMPLATE_ENDING
#     global COMMENT_TEMPLATE_NEWLINE
#     # Find all "level 3" class that is a div.
#     level3s = soup.find_all(name="div", attrs={"class":"level3"})
#     # For each level 3, if the thing behind it is a h3 and has the id of constructors1. We found it in
#     constructorDetailedSect = None # type: bs
#     for x in level3s:
#         lvl3 = x # type: bs
#         # Get the one above it
#         _previousSibling_ = FetchPrevSibling(lvl3)
#         # If
#         if (_previousSibling_ is not None and _previousSibling_.get("id","constructors1") == "constructors1" and _previousSibling_.name == "h3"):
#             constructorDetailedSect = x
#             break
#     if constructorDetailedSect is None:
#         #print(f"Didn't find constructor for {DzObj.name}")
#         return
#     else:
#         search = constructorDetailedSect
#         qx = search.find_all("hr")
#         query = []
#         for x in qx:
#             hr = x # type: bs
#             prevSibling = FetchPrevSibling(hr.parent) # type: bs
#             #if prevSibling is not None and prevSibling.get("id") == "constructors1":
#             query.append(hr)
#         if len(query) == 0:
#             # Bye felisha
#             return
#         # Else, we got a trash tree to go chop down.
#         for property in query:
#             # For every <hr> tag...
#             _property = property # type: bs
#             # Get the <p> tag below it.
#             p = _property.findNext("p") # type: bs
#             # Get constructor name.
#             cN = p.find("a").get_text() # type: str
#             # Get the parameters.
#             pA = str(p.get_text().encode("UTF-8"),"UTF-8").strip()
#             pA = pA[pA.index("(")+1:pA.index(")")].strip()
#             # Get variable definition.
#             d = p.findNext("p") # type: bs
#             desc = GetDescription(d, p)
#             # Create our variable.
#             JSconstructor = JSConstructor(cN,pA,DzObj.properties,desc)
#             DzObj.constructors.append(JSconstructor)
#             #print(f"Constructor Name: {cN} | Definition: {desc}")
# def CreateStaticMethods(DzObj:DzObject):
#     try:
#         soup = bs(DzObj.dzPage,features=HTML_PARSER)
#     except OSError:
#         print("Couldnt open URL. Trying again in 5 seconds... ")
#         time.sleep(5)
#         soup = TryConnect(DzObj.dzPage)
#     except:
#         soup = TryConnect(DzObj.dzPage)
#     global COMMENT_TEMPLATE_CONSTRUCTOR
#     global COMMENT_TEMPLATE_BEGINNING
#     global COMMENT_TEMPLATE_ENDING
#     global COMMENT_TEMPLATE_NEWLINE
#     # Find all "level 3" class that is a div.
#     level3s = soup.find_all(name="div", attrs={"class":"level3"})
#     # For each level 3, if the thing behind it is a h3 and has the id of methods1. We found it in
#     constructorDetailedSect = None # type: bs
#     for x in level3s:
#         lvl3 = x # type: bs
#         # Get the one above it
#         _previousSibling_ = FetchPrevSibling(lvl3)
#         # If
#         if (_previousSibling_ is not None and _previousSibling_.get("id","static_methods1") == "static_methods1" and _previousSibling_.name == "h3"):
#             constructorDetailedSect = x
#             break
#     if constructorDetailedSect is None:
#         #print(f"Didn't find method for {DzObj.name}")
#         return
#     else:
#         search = constructorDetailedSect
#         qx = search.find_all("hr")
#         query = []
#         for x in qx:
#             hr = x # type: bs
#             prevSibling = FetchPrevSibling(hr.parent) # type: bs
#             #if prevSibling is not None and prevSibling.get("id") == "static_methods1":
#             query.append(hr)
#         if len(query) == 0:
#             # Bye felisha
#             return
#         # Else, we got a trash tree to go chop down.
#         for property in query:
#             # For every <hr> tag...
#             _property = property # type: bs
#             # Get the <p> tag below it.
#             p = _property.findNext("p") # type: bs
#             # Get method return type.
#             hrSourcelineRange = (_property.sourceline,GetParentSourceLineRange(query[0].parent)[1])
#             returnType = p.findNext("a",{"class" : "wikilink1"}) # type: bs
#             if returnType is not None:
#                 returnNextSib = returnType.find_next_sibling("strong")
#             if returnType != None and returnNextSib is not None and returnNextSib.name == "strong":
#                 rT = p.findNext("a",{"class" : "wikilink1"}).get_text() # type: str
#             elif p != None and p.findNext("a", {"class" : "wikilink2"}):
#                 aCandidate = p.findNext("a", {"class" : "wikilink2"})
#                 if IsInRange(hrSourcelineRange, aCandidate.sourceline):
#                     rT = ConvertToDAZNomen(aCandidate.get_text()) # type: str
#                 else:
#                     rT = "void"
#             else:
#                 if p != None and p.name == "a" and p["class"] == "wikilink1":
#                     rT = p.get_text()
#                 elif p != None and p.find("em") != None:
#                     # We found a return type of ourselves.
#                     rT = p.find("em").text
#                 else:
#                     rT = "void"
#             # Get method name.
#             mN = p.find("strong").get_text() # type: str
#             # Get the parameters.
#             pA = str(p.get_text().encode("UTF-8"),"UTF-8").strip()
#             pA = pA[pA.index("(")+1:pA.index(")")].strip()
#             # Get variable definition.
#             d = p.findNext("p") # type: bs
#             desc = GetDescription(d, p)
#             # Create our variable.
#             JSmethod = JSFunction(mN,pA,rT,desc,True,DzObj)
#             DzObj.functions.append(JSmethod)
#             #print(f"Static Method Name: {mN} | Method Parameters: {pA} |  Method Return Type: {rT} | Definition: {desc}")
# def CreateMethods(DzObj:DzObject):
#     try:
#         soup = bs(DzObj.dzPage,features=HTML_PARSER)
#     except OSError:
#         print("Couldnt open URL. Trying again in 5 seconds... ")
#         time.sleep(5)
#         soup = TryConnect(DzObj.dzPage)
#     except:
#         soup = TryConnect(DzObj.dzPage)
#     global COMMENT_TEMPLATE_CONSTRUCTOR
#     global COMMENT_TEMPLATE_BEGINNING
#     global COMMENT_TEMPLATE_ENDING
#     global COMMENT_TEMPLATE_NEWLINE
#     # Find all "level 3" class that is a div.
#     level3s = soup.find_all(name="div", attrs={"class":"level3"})
#     # For each level 3, if the thing behind it is a h3 and has the id of methods1. We found it in
#     constructorDetailedSect = None # type: bs
#     for x in level3s:
#         lvl3 = x # type: bs
#         # Get the one above it
#         _previousSibling_ = FetchPrevSibling(lvl3)
#         # If
#         if (_previousSibling_ is not None and _previousSibling_.get("id","methods1") == "methods1" and _previousSibling_.name == "h3"):
#             constructorDetailedSect = x
#             break
#     if constructorDetailedSect is None:
#         #print(f"Didn't find method for {DzObj.name}")
#         return
#     else:
#         search = constructorDetailedSect
#         qx = search.find_all("hr")
#         query = []
#         for x in qx:
#             hr = x # type: bs
#             prevSibling = FetchPrevSibling(hr.parent) # type: bs
#             #if prevSibling is not None and prevSibling.get("id") == "methods1":
#             query.append(hr)
#         if len(query) == 0:
#             # Bye felisha
#             return
#         # Else, we got a trash tree to go chop down.
#         if query[0].parent.findNextSibling() is not None and query[0].parent.findNextSibling() != None:
#             hrParentEndingSL = query[0].parent.findNextSibling().sourceline-1
#         else:
#             _, maxline = GetParentSourceLineRange(query[0].parent)
#             hrParentEndingSL = maxline + 1
#         i = 0
#         for property in query:
#             # For every <hr> tag...
#             _property = property # type: bs
#             # We need to set a range for stuff to find.
#             hrSourcelineRange = (_property.sourceline,hrParentEndingSL)
#             # find next hr or parent
#             nextHr = _property.findNext("hr")
#             if nextHr != None and nextHr is not None and IsInRange((_property.parent.sourceline,hrParentEndingSL),nextHr.sourceline):
#                hrSourcelineRange = (_property.sourceline,nextHr.sourceline)
#             #if _property.findNext("hr")
#             # Get the <p> tag below it.
#             p = _property.findNext("p") # type: bs
#             # Get method return type.
#             returnType = p.findNext("a",{"class" : "wikilink1"}) # type: bs
#             if returnType is not None:
#                 returnNextSib = returnType.find_next_sibling("strong")
#             if returnType != None and returnNextSib is not None and returnNextSib.name == "strong" and IsInRange(hrSourcelineRange, returnType.sourceline):
#                 rT = p.findNext("a",{"class" : "wikilink1"}).get_text() # type: str
#             elif p != None and p.findNext("a", {"class" : "wikilink2"}):
#                 aCandidate = p.findNext("a", {"class" : "wikilink2"})
#                 if IsInRange(hrSourcelineRange, aCandidate.sourceline):
#                     rT = ConvertToDAZNomen(aCandidate.get_text()) # type: str
#                 else:
#                     rT = "void"
#             else:
#                 if p != None and p.name == "a" and p["class"] == "wikilink1":
#                     rT = p.get_text()
#                 elif p != None and p.name == "a" and p["class"] == "wikilink2":
#                     # If we got a link to a page that doesn't exist (which we probably do have now.)
#                     rT = ConvertToDAZNomen(p.get_text())
#                 elif p != None and p.find("em") != None:
#                     # We found a return type of ourselves.
#                     rT = p.find("em").text
#                 else:
#                     rT = "void"
#             # Get method name.
#             mN = p.find("strong").get_text() # type: str
#             # Get the parameters.
#             pA = str(p.get_text().encode("UTF-8"),"UTF-8").strip()
#             if "(" in pA:
#                 pA = pA[pA.index("(")+1:pA.index(")")].strip()
#             else:
#                 pA = pA.strip()+"()"
#             # Get variable definition.
#             d = p.findNext("p") # type: bs
#             desc = GetDescription(d, p)
#             # Create our variable.
#             JSmethod = JSFunction(mN,pA,rT,desc,False,DzObj)
#             DzObj.functions.append(JSmethod)
#             i+= 1
#             #print(f"Method Name: {mN} | Method Parameters: {pA} |  Method Return Type: {rT} | Definition: {desc}")
# def CreateEnums(DzObj:DzObject):
#     soup = bs(DzObj.dzPage,features=HTML_PARSER)
#     # Find all "level 3" class that is a div.
#     level3s = soup.find_all(name="div", attrs={"class":"level3"})
#     for x in level3s:
#         search = x # type: bs
#         nextSibling = FetchNextSibling(search)
#         # If the next one we have doesn't have the id of "enumerations1" remove it.
#         foundProperties = search.find_next_sibling("h3",{"id" : "enumerations1"},text="Enumerations")
#         if (nextSibling is None or nextSibling.get("id","enumerations1") != "enumerations1" or nextSibling.name != "h3" or nextSibling.text != "Properties"):
#             level3s.remove(x)
#         else:
#             #print("Found 1")
#             pass
#     for x in level3s:
#         # Check if there are <hr> tags. If so, do work. Otherwise, skip.
#         search = x # type: bs
#         qx = search.find_all("hr")
#         query = None # type: bs
#         for x in qx:
#             hr = x # type: bs
#             prevSibling = FetchPrevSibling(hr.parent) # type: bs
#             if prevSibling is not None and prevSibling.get("id") == "enumerations1":
#                 query = hr
#                 break
#         if query is not None:
#             for p in query.find_all_next("li",{"class": "level1"}):
#                 if not IsFriend(p,search):
#                     continue
#                 # Get name.
#                 try:
#                     enumName = p.find("strong").get_text() # type: str
#                     e = p.get_text() #type: str
#                     index = e.index("-") + 1
#                     enumDesc = e[index:].strip()
#                     JsEnum = JSEnum(enumName,enumDesc,DzObj)
#                     DzObj.enums.append(JsEnum)
#                     #print(f"ENUM Name: {enumName} | Definition: {enumDesc}")
#                 except:
#                     #print(f"ENUM FAILED FOR {DzObj.name}.")
#                     ERRORED_ENUMS.append(DzObj.name)
# def CreateSignals(DzObj:DzObject):
#     try:
#         soup = bs(DzObj.dzPage,features=HTML_PARSER)
#     except OSError:
#         print("Couldnt open URL. Trying again in 5 seconds... ")
#         time.sleep(5)
#         soup = TryConnect(DzObj.dzPage)
#     except:
#         soup = TryConnect(DzObj.dzPage)
#     global COMMENT_TEMPLATE_CONSTRUCTOR
#     global COMMENT_TEMPLATE_BEGINNING
#     global COMMENT_TEMPLATE_ENDING
#     global COMMENT_TEMPLATE_NEWLINE
#     # Find all "level 3" class that is a div.
#     level3s = soup.find_all(name="div", attrs={"class":"level3"})
#     # For each level 3, if the thing behind it is a h3 and has the id of methods1. We found it in
#     signalDetailSect = None # type: bs
#     for x in level3s:
#         lvl3 = x # type: bs
#         # Get the one above it
#         _previousSibling_ = FetchPrevSibling(lvl3)
#         # If
#         if (_previousSibling_ is not None and _previousSibling_.get("id","signals1") == "signals1" and _previousSibling_.name == "h3"):
#             signalDetailSect = x
#             break
#     if signalDetailSect is None:
#         #print(f"Didn't find signal for {DzObj.name}")
#         return
#     else:
#         search = signalDetailSect
#         qx = search.find_all("hr")
#         query = []
#         for x in qx:
#             hr = x # type: bs
#             # prevSibling = FetchPrevSibling(hr.parent) # type: bs
#             #if prevSibling is not None and prevSibling.get("id") == "methods1":
#             query.append(hr)
#         if len(query) == 0:
#             # Bye felisha
#             return
#         # Else, we got a trash tree to go chop down.
#         for property in query:
#             # For every <hr> tag...
#             _property = property # type: bs
#             # Get the <p> tag below it.
#             p = _property.findNext("p") # type: bs
#             # Get method return type.
#             rT = "void"
#             # Get method name.
#             mN = p.find("strong").get_text() # type: str
#             # Get the parameters.
#             pA = str(p.get_text().encode("UTF-8"),"UTF-8").strip()
#             if "(" in pA:
#                 pA = pA[pA.index("(")+1:pA.index(")")].strip()
#             else:
#                 pA = pA.strip()+"()"
#             workingP = FetchNextSibling(p)
#             if workingP is not None and workingP.name == "p":
#                 code = workingP.find("code")
#                 if code != None:
#                     signature = workingP.find("code").text
#                 else:
#                     signature = mN + "()"
#             else:
#                 signature = "TODO: Add Description"
#             # Get variable definition.
#             workingP = FetchNextSibling(workingP)
#             if workingP is not None and workingP.name == "p":
#                 desc = workingP.text.strip()
#             else:
#                 desc = "TODO: Add Description"
#             # Create our variable.
#             JSsignal = JSSignal(mN, pA, signature, desc, DzObj)
#             DzObj.signals.append(JSsignal)
#             #print(f"Signal Name: {mN} | Signal Parameters: {pA} |  Signal Signature: {signature} | Definition: {desc}")
# def DetermineIfEligible(x: DzObject):
#     """ Checks if the class is a ECMAScript. If it is, we will return false. Otherwise true."""
#     try:
#         soup = bs(urlopen(x.link),features=HTML_PARSER)
#     except RemoteDisconnected:
#         print("REMOTE DISCONNECTED: Attempting to try again.")
#         soup = TryConnect(x.link)
#     except OSError:
#         print("LOST CONNECTION: Attempting to try again.")
#         soup = TryConnect(x.link)
#     results = soup.find_all("div",attrs={"class" : "level1"})
#     classDescription = None
#     # Double check to see that we got the description.
#     for y in results:
#         result = y # type: bs
#         prevElement = FetchPrevSibling(result)
#         if prevElement.text == x.name:
#             print("We got our class description.")
#             classDescription = y
#             break
#     if classDescription is not None:
#         if "ECMAScript".lower() in classDescription.text.lower():
#             SKIPPED_DZOBJS.append(x.name)
#             return False
#         else:
#             return True
#     else:
#         return True
# def ProcessObject(DzObj: DzObject) -> JSClass:
#     """ Assigns attributes to `DzObj` and returns a JSClass which has a string interprolation ready with comments and code."""
#     if not DetermineIfEligible(DzObj) or DzObj in IGNORE_OBJECTS:
#         print(DzObj.name + " is not eligble. Deleting.")
#         return None
#     GetClassDescription(DzObj)
#     CreateImplements(DzObj)
#     CreateConstuctors(DzObj)
#     CreateEnums(DzObj)
#     CreateProperties(DzObj)
#     CreateStaticMethods(DzObj)
#     CreateMethods(DzObj)
#     CreateSignals(DzObj)
#     return JSClass(DzObj)

# def main():
#     soup = TryConnect(OBJECT_INDEX_PAGE)
#     # Find all div's that has a class of "nspagesul"
#     divCats = soup.find_all(attrs={"class" : "nspagesul"}) # type: list[bs]
#     objectLinks = [] # Used to hold links later.
#     for x in divCats:
#         DzLink = x # type: bs
#         DzLinks = DzLink.find_all(attrs={"class" : "wikilink1"})
#         objectLinks.extend(DzLinks)
#     # Create our DzObjects with a name and the link to the page.
#     for link in objectLinks:
#         DzObject(link.get_text(),link["href"])
#     # Process each DzObject.
#     with multiprocessing.Pool(10) as p:
#         results = p.map(ProcessObject, DzObject.DzObjects)
#     # Better for debugging or just doing it on one CPU.
#     # for object in DzObject.DzObjects:
#     #     ProcessObject(object)
#     # Now call DAZtoJSv3 and get the objects. We don't need to update same classes with OLD info pass in DzObjects already created.
#     processedClasses = DAZtoJSv3.BeginWork()
#     # Write to file.
#     fileLocation = os.path.join(os.getcwd(),JS_NAME)
#     with open(fileLocation, "ab+") as file:
#         if file.tell() == 0:
#             TODAYSDATE = datetime.date(datetime.now()).strftime("%B %d, %Y")
#             HEADER = f"""// LAST UPDATED: {TODAYSDATE}
# // This script has been auto-generated by TheRealSolly | Solomon Blount.
# // The following contents is all directly imported from DAZ's Documentation Website and inherits the license set, which is the following...
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# // Attribution 3.0 Unported (CC BY 3.0) | https://creativecommons.org/licenses/by/3.0/ | (C) Daz Productions, Inc 224 S 200 W, Salt Lake City, UT 84101
# // I DO NOT WORK FOR DAZ PRODUCTIONS INC AND THIS SCRIPT WAS NOT SUPPORTED BY OR ENDORSED BY ANYONE AT DAZ PRODUCTIONS INC.
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# // If I made your life wonderful, if you're feeling generious enough to donate to make me feel wonderful, you can do so by going here:
# //                                                         https://www.buymeacoffee.com/therealsoll
# // Anyway, here are some things you need to know.
# //                                                   THIS VERSION ALSO DOES NOT INCLUDE ECMASCRIPT CLASSES
# //                                     THIS FILE PURPOSEFULLY HAS ERRORS SO THE INTELLISENSE CAN ASSIST YOU WITH YOUR CODE.
# //                                             THIS HAS ONLY BEEN TESTED ON VISUAL STUDIO CODE VERSION 1.55.0.
# //
# // To make .dsa scripts use the JS/TS interpreter, create a new file with the .dsa extension, on the lower-right of VSCode click on the file type and select "Configure file assocations for .dsa" and then select in JavaScript.
# // JzSense now includes v3 Documentation to fill in missing classes from v4 documentation.
# // Do not select TS as the interpreted language. Use JS.
# // There will be more adjustments to this script but i'm in school...so yeah.
# // To check and see if there are any updates, please go here: https://github.com/siblount/JzSense
# // Happy Coding!"""
#             file.write(HEADER.encode("utf-8"))
#         totalStr = bytes()
#         results.extend(processedClasses) # Add  v3 documentation.
#         for JsClass in results:
#             if JsClass is not None or JsClass != None:
#                 # Update implments one more time. Only needed if used multi-processing.
#                 CreateImplements(JsClass.dzObj)
#                 totalStr += JsClass.__str__().encode("utf-8") + b"\n"
#         file.write(b"\n" + totalStr)
#         file.close()
#     # Print a victory message!
#     print("JzIntellisense.js complete!\n=================================================\n=================================================\n\n")
#     print("ERRORED ENUMS\n")
#     for error in ERRORED_ENUMS:
#         print(error,end="\n")
#     print("\nSKIPPED DZOBJS\n")
#     for obj in SKIPPED_DZOBJS:
#         print(obj,end="\n")

# # The default cube, ctrl + a, ctrl + c, wombo combo.
# if __name__ == "__main__":
#     main()