# """ Scraps through the DAZ Documentation Files and outputting `JSObject`s. This is used in conjuction with `DAZtoJSv4`. Main function to call is: `BeginWork(ignoreList[]: list[Str])`. """

# from bs4 import BeautifulSoup as bs
# from urllib.request import urlopen
# import re
# import os
# import multiprocessing
# import time
# import re
# import urllib
# import bs4
# from datetime import datetime

# # This is so damn messy, but good luck.

# # Methods need to check to see if they return themselves.

# print("Initializing")
# # Global variables
# OBJECT_INDEX_PAGE = R"file:D:\Python Test Folder\DAZScriptV3\classes.html"
# CLASS_HIERARCHY_PAGE = urlopen(R"file:D:\Python Test Folder\DAZScriptV3\hierarchy.html").read()
# JS_NAME = "JzSense.js"
# HTML_RETRIES = 3
# HTML_PARSER = "html5lib"
# HTML_LVL1_NAMES = ["level1", "level1 node"]
# IGNORE_OBJECTS = "Dz3DViewport , Dz3DViewRenderHandler , DzAbstractAssetContainer , DzAbstractNodeEditorPane , DzAction , DzActionMenu , DzActionMenuItem , DzActionMgr , DzActivityLayout , DzAddBlend , DzAlembicExporter , DzAlphaBlend , DzApp , DzAppSettings , Array , DzArrayHelper , DzAsset , DzAssetFileOutFilter , DzAssetIOFilter , DzAssetIOMgr , DzAssetMgr , DzAudioClip , DzAudioImporter , DzAuthenticationMgr , DzAuthor , DzBackdrop , DzBase , DzBasicCamera , DzBasicDialog , DzBone , Boolean , DzBoolProperty , DzBox3 , DzBoxLayout , DzBrickMaterial , DzButton , DzButtonGroup , ByteArray , DzCallBack , DzCallBackMgr , DzCamera , DzCameraAssetFilter , DzCategoryAssetContainer , DzCharacterAssetFilter , DzCheckBox , DzCheckListItem , DzCircle3 , Color , DzColorDialog , DzColorProperty , DzColorWgt , DzComboBox , DzComboEdit , DzCompatibilityBaseAssetContainer , DzContentFile , DzContentFolder , DzContentMgr , DzContentReplaceMgr , DzController , DzCr2Exporter , DzCustomData , Date , DzDateEdit , DzDateTimeEdit , DzDefaultMaterial , DzDelightRenderer , QDesktopWidget , DzDevice , DzDeviceMgr , DzDForm , DzDFormAssetFilter , DzDFormBase , DzDFormZone , DzDial , DzDialog , DzDir , DzDistantLight , DzDockArea , DzDockAreaColumn , DzDockBar , DzDockWindow , DzDomAttr , DzDomBasicNode , DzDomCDATASection , DzDomCharacterData , DzDomComment , DzDomDocument , DzDomDocumentFragment , DzDomDocumentType , DzDomElement , DzDomEntity , DzDomEntityReference , DzDomNode , DzDomNotation , DzDomProcessingInstruction , DzDomText , DzDrawStyle , DzDynamicDividerWgt , DzEdge , DzElement , DzElementData , DzElementPostLoadFileData , DzEnumProperty , DzEnumSlider , DzERCBake , DzERCFreeze , DzERCLink , Error , DzError , EvalError , DzExporter , DzExportMgr , DzFacet , DzFbxExporter , DzFbxImporter , DzFile , DzFileDialog , DzFileFilter , DzFileInfo , DzFileIO , DzFileIOPresetMgr , DzFileIOSettings , DzFileProperty , DzFlipManip , DzFloat2Property , DzFloat3Property , DzFloatColor , DzFloatColorProperty , DzFloatProperty , DzFloatSlider , DzFolderAssetContainer , Font , Function , DzGeometryImporter , DzGeometryShellNode , DzGeometryUtil , DzGeomSourceFileData , Global , DzGridLayout , DzGroupBox , DzGroupNode , DzGuidePage , DzGZFile , DzHBoxLayout , DzHButtonGroup , DzHeader , DzHelpMgr , DzHGroupBox , DzHierarchicalMaterialAssetFilter , DzHierarchicalPoseAssetFilter , Image , DzImageBlend , DzImageColorLayer , DzImageComponent , DzImageFileLayer , DzImageLayer , DzImageManip , DzImageMask , DzImageMgr , DzImageProperty , DzImageRenderHandler , DzImageTexture , DzImporter , DzImportMgr , DzInfoDivider , DzInfoTabs , DzInstanceGroupItem , DzInstanceGroupNode , DzInstanceNode , DzInt2 , DzInt2Property , DzInteractiveInstructionObject , DzInteractiveLessonMgr , DzInteractiveLessonObject , DzIntProperty , DzIntSlider , DzInvertManip , DzIrayRenderer , JSON , DzLabel , DzLayerAssetFilter , DzLayeredImage , DzLayeredTexture , DzLayout , DzLCDNumber , DzLight , DzLightAssetFilter , DzLine3 , DzLinearPointLight , DzLineEdit , DzListBox , DzListView , DzListViewItem , DzMainWindow , DzMaterial , DzMaterialAssetFilter , Math , DzMatrix3 , DzMatrix4 , DzMenu , DzMessageBox , DzModifier , DzMorphLoader , DzMorphLoaderBatch , DzMorphSupportAssetFilter , DzMultiMediaMgr , DzMultiplyBlend , NativeError , DzNode , DzNodeAligner , DzNodeProperty , DzNodeSelectionComboBox , DzNodeSupportAssetFilter , Number , DzNumericController , DzNumericNodeProperty , DzNumericProperty , Object , DzObject , QObject , DzObjExporter , DzObjImporter , DzOffsetManip , DzOpacityManip , DzOpenGL , DzOrientedBox3 , Palette , DzPane , DzPaneGroup , DzPaneMgr , DzPaneSettings , DzParentProductContainer , DzPathComboBox , DzPersistentMenu , Pixmap , DzPlugin , DzPluginMgr , Point , DzPointLight , DzPopupMenu , DzPoseAssetFilter , DzPresentation , DzProcess , DzProductAssetContainer , DzProductHolderContainer , DzPropertiesAssetFilter , DzProperty , DzPropertyGroup , DzPropertyGroupTree , DzPropertySelectionComboBox , DzPropertySettings , DzPuppeteerAssetFilter , DzPushButton , DzPZ3Importer , DzQuat , DzRadioButton , RangeError , Rect , DzRefCountedItem , ReferenceError , RegExp , DzRenderer , DzRendererMode , DzRenderHandler , DzRenderMgr , DzRenderOptions , DzRenderSettingsAssetFilter , DzRotateManip , DzRotationOrder , DzRSLShader , DzSaveFilter , DzSaveFilterMgr , DzScaleManip , DzScene , DzSceneAssetFilter , DzSceneData , DzSceneHelper , DzSceneSubsetAssetFilter , DzSceneSupportAssetFilter , DzScript , DzScriptContext , DzScriptedRenderer , DzScrollArea , DzScrollView , DzSearchContainer , DzSelectionMap , DzSettings , DzSettingsHelper , DzShaderAssetFilter , DzShaderCamera , DzShaderDescription , DzShaderLight , DzShaderMaterial , DzShaderParameter , DzShaderSupportAssetFilter , DzShapeRiggingAdjuster , DzShapingAssetFilter , DzSimpleElementData , DzSimpleElementScriptData , DzSimpleSceneData , DzSimpleSceneScriptData , DzSimulationSettingsAssetFilter , Size , DzSkeleton , DzSkeletonProperty , DzSourceFileData , DzSplitter , DzSpotLight , String , DzStringHelper , DzStringProperty , DzStyle , DzSubtractBlend , SyntaxError , DzSystem , DzTabWidget , DzTextBrowser , DzTextEdit , DzTexture , DzTextureComponent , DzTextureLayer , DzTextureMask , DzTime , DzTimeEdit , DzTimer , DzTimeRange , DzToolBar , DzToolBarItem , DzTopLevelAssetContainer , DzTransferUtility , DzTypeAssetContainer , TypeError , DzU3DExporter , DzUiLoader , DzUIPopUpWgt , DzUiWidget , DzUndoStack , DzUri , URIError , DzUserDrawStyle , DzUVSet , DzUVSupportAssetFilter , DzVBoxLayout , DzVButtonGroup , DzVec2 , DzVec3 , DzVersion , DzVGroupBox , DzVideoClip , DzVideoExporter , DzView , DzViewport , DzViewportMgr , DzViewRenderHandler , DzViewTool , DzWearablesAssetFilter , DzWeld , DzWidget , QWidget , DzZipFile".split(" , ")
# DELETED_V3_OBJECTS = "DzMRMMesh , DzMRMShape , DzActivityActionItem , DzFace , DzShaderPane , DzPaneLayout , DzCategoriesDBEntry , DzSubDBase , DzSubDFigure , DzSubDFigureObject , DzHalfEdge , DzSubDGroup , DzSubDMesh , DzSubDProp , DzSubDShape , ColorGroup , DzPolygon , DzPolyMesh , DzPolyShape , DzContentDBEntry , DzPoserBendParam , DzPoserCurve , DzPoserIKChain , DzPoserIKChains , DzPoserJoint , DzPoserJointParam , DzPoserJointSphere , DzPoserSmoothScale , DzPoserTwistParam , DzTriangle , DzQuad , DzLibraryPane , DzMacAudioClip , DzMath".split(" , ")
# IGNORE_OBJECTS.extend(DELETED_V3_OBJECTS)
# COMMENT_TEMPLATE_BEGINNING = "/**"
# COMMENT_TEMPLATE_ENDING = "*/"
# COMMENT_TEMPLATE_NEWLINE = " * "
# COMMENT_TEMPLATE_PARAM = "@param {} {}}"
# COMMENT_TEMPLATE_CONSTRUCTOR = "@constructor {}"
# COMMENT_UNICODE_REPLACEMENTS = {"“".encode("UTF-8") : b'"', "”".encode("UTF-8") : b'"'}
# TYPE_CONVERSION = {"QString" : "String", "int" : "Number", "float" : "Number", "decimal" : "Number", "double" : "Number"}
# ERRORED_ENUMS = []
# SKIPPED_DZOBJS = []


# def TryReconnect(link) -> bs:
#     for _ in range(HTML_RETRIES):
#         try:
#             return bs(urlopen(link),features=HTML_PARSER)
#         except:
#             print("Retry failed...trying again in 3 seconds.")
#             time.sleep(3)
#             continue
#     print("Couldn't reconnect.")
# def GenerateRE(msg:str) -> str:
#     words = msg.strip().split(" ")
#     for word in words:
#         if word.strip() == "":
#             words.remove(word)
#         else:
#             words[words.index(word)] = "(" + word + ")"
#     return "|".join(words)
# def FetchNextSibling(s) -> bs:
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
# def IsFriend(element1: bs, element2: bs):
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
#     return number in range(nRange[0],nRange[1])
# def GetReturnType(tableRowBS:bs) -> str:
#     """Requires the `<tr>` bs object. Returns a string of the return type."""
#     returnType = tableRowBS.find("td", {"class" : "memItemLeft"}) # type: bs
#     if returnType is not None or returnType != None:
#         return returnType.text
#     else:
#         print("WARNING: returnType returned None.")
# def GetSymbolArgs(tableRowBS:bs) -> str:
#     """ Requires the `<tr>` bs object. Returns a string of the property, parameters, and function/signal name."""
#     value = tableRowBS.find("td", {"class" : "memItemRight"}) # type: bs
#     if value is not None or value != None:
#         return value.get_text()
#     else:
#         print("WARNING: value returned None.")
# def FindMaxSourceLineGivenContextTable(tableRowBS:bs, strict:bool) -> int:
#     """Returns the maximum source line for a given context, such as: Methods, Static Methods, Properties, etc."""
#     trRange = GetParentSourceLineRange(tableRowBS.parent)
#     def GetLast(context:bs) -> bs:
#         """Recursive function to chop down `tr` elements until the very last one. Also checks if it is in the parent sourceline range."""
#         if not strict:
#             possibleTR = context.find_next("tr") # type: bs
#             headerTR = possibleTR.find("h2")
#         else:
#             someObj = context.find_next_sibling()
#             if (someObj is not None or someObj != None) and someObj.name == "tr":
#                 possibleTR = someObj
#                 headerTR = possibleTR.find("h2")
#             else:
#                 possibleTR = None
#                 headerTR = None
#         if (possibleTR != None or possibleTR is not None) and possibleTR.sourceline in range(trRange[0], trRange[1]+1) and (headerTR == None or headerTR is None):
#             return GetLast(possibleTR)
#         else:
#             return context
    
#     lastTR = GetLast(tableRowBS)
#     return lastTR.sourceline
# def FindMaxSourceLineGivenContext(divBS:bs) -> int:
#     """Returns the maximum source line for a given context, such as: Methods, Static Methods, Properties, etc."""
#     divRange = GetParentSourceLineRange(divBS.parent)
#     h2 = divBS.find_next("h2")
#     if h2 is not None or h2 != None:
#         max = h2.sourceline
#     else:
#         max = divRange[1]
#     # def GetLast(context:bs) -> bs:
#     #     """Recursive function to chop down `div` elements until the very last one. Also checks if it is in the parent sourceline range."""
#     #     possibleDiv = context.find_next(context.name) # type: bs
#     #     if possibleDiv != None or possibleDiv is not None and possibleDiv.sourceline in range(divRange[0], divRange[1]+1) and possibleDiv.sourceline < max:
#     #         return GetLast(possibleDiv)
#     #     else:
#     #         return context
#     # lastTR = GetLast(divBS)
#     # return lastTR.sourceline
#     return max
# def GetNextSiblingBS(context: bs, attrs:dict, min: int, max: int) -> bs:
#                 nextTr = context.find_next_sibling(context.name, attrs)
#                 if (nextTr is not None or nextTr != None) and nextTr.sourceline in range(min, max):
#                     return nextTr
# def GetNextBS(context: bs, attrs:dict, min: int, max: int) -> bs:
#                 nextTr = context.find_next(context.name, attrs)
#                 if (nextTr is not None or nextTr != None) and nextTr.sourceline in range(min, max):
#                     return nextTr
# def GetDetailedInfo(workingTr: bs, name: str, headerText="Member Data Documentation", params=None) -> tuple[str, str, str, str, str]:
#     def GetParamsInfo(context:bs) -> str:
#         """`context` is the `dl` object. Returns a string of parameter information. If multiple params, split text by `|!|`"""
#         paramsInfo = []
#         # Get the tbody.
#         tbody = context.find("tbody") # type: bs
#         if tbody is not None or tbody != None:
#             # Get all trs.
#             for x in tbody.find_all("tr"):
#                 tr = x # type: bs
#                 paramName = None
#                 paramDesc = None
#                 for y in tr.find_all("td"):
#                     td = y # type: bs
#                     potentialEm = td.find("em")
#                     if potentialEm is None or potentialEm == None:
#                         if td.text != (None or ""):
#                             paramDesc = td.text
#                         else:
#                             continue
#                     else:
#                         paramName = potentialEm.text
#                 paramsInfo.append(f"{paramName} - {paramDesc.strip()}")
#         if len(paramsInfo) == 0:
#             return None
#         else:
#             return "|!|".join(paramsInfo)
#     def GetReturnsInfo(context:bs) -> str:
#         """`context` is the `dl` object. Returns a string of parameter information. If multiple params, split text by `|!|`"""
#         # Get the tbody.
#         dd = context.find("dd") # type: bs
#         if dd != None or dd is not None:
#             return dd.text.strip()
#     def GetAttentionInfo(context:bs) -> str:
#         """`context` is the `dl` object. Returns a string of parameter information. If multiple params, split text by `|!|`"""
#         # Get the tbody.
#         dd = context.find("dd") # type: bs
#         if dd != None or dd is not None:
#             return dd.text.strip()
        
#     ###############################################
    
#     # Find `h2` Member Data Documentation
#     h2 = workingTr.find_next('h2', text=headerText)
#     if h2 != None or h2 is not None:
#         minSourceline = h2.find_next("div", {"class" : "memitem"}).sourceline
#         maxSourceline = FindMaxSourceLineGivenContext(h2)
#         lastDiv = None
#         while True:
#             if lastDiv is None or lastDiv == None:
#                 workingDiv = h2.find_next("div", {"class" : "memproto"})
#             else:
#                 workingDiv = GetNextBS(lastDiv, {"class" : "memproto"}, minSourceline, maxSourceline)
#             if workingDiv is None or workingDiv == None:
#                 break
#             text = workingDiv.find("td", {"class" : "memname"}).parent.text # type: str
#             if params != None:
#                 if (text is not None or text != None) and name in text and re.search(GenerateRE(params), text, re.ASCII) != None:
#                     # We got our working Div.
#                     lastDiv = workingDiv
#                     break
#                 else:
#                     lastDiv = workingDiv
#             else:
#                 if (text is not None or text != None) and name in text:
#                     # We got our working Div.
#                     lastDiv = workingDiv
#                     break
#                 else:
#                     lastDiv = workingDiv
#         workingDoc = lastDiv.find_next("div", {"class" : "memdoc"}) # type: bs
#         # Do we need to chop down the workingDoc?
#         if workingDoc.find("dl") == None:
#             # If not, return only text info.
#             return (workingDoc.text.strip(), None, None, None, None)
#         else:
#             # We got some work to do.
#             # First find regular description.
#             potentialP = workingDoc.findNext() # type: bs
#             if (potentialP is not None or potentialP != None) and potentialP.name == "p":
#                 regularDesc = potentialP.text.strip()
#             else:
#                 regularDesc = None
#             parametersDesc = None
#             returnsDesc = None
#             attentionDesc = None
#             for d in workingDoc.find_all("dl"): # was lastDiv
#                 dl = d # type: bs
#                 boldType = dl.find("dt") # type: bs
#                 if boldType != None or boldType is not None:
#                     workingBold = boldType.text
#                     if "Parameters" in workingBold:
#                         parametersDesc = GetParamsInfo(dl)
#                     if "Returns" in workingBold:
#                         returnsDesc = GetReturnsInfo(dl)
#                     if "Attention" in workingBold:
#                         attentionDesc = GetAttentionInfo(dl)
#         return (regularDesc, returnsDesc, parametersDesc, attentionDesc, None)
#     else:
#         print("WARNING: Got properties but didn't find Member Data Documentation.")

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
#     def __init__(self, name, params, returnObj, desc, static = False, dzObj:DzObject=None):
#         # Order of these are important. Some need to be intialized before the others.
#         self.name = name
#         self.params = self.ParseParams(params)
#         self.returnObj = returnObj
#         if desc != None or desc is not None:
#             self.desc = self.GetJSDocDescription(desc)
#         else:
#             self.desc = self.GetJSDocDescription(("Daz Studio V3 documentation missing.", None, None, None, None))
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
#         if desc != None or desc is not None:
#             self.desc = self.GetJSDocDescription(desc)
#         else:
#             self.desc = self.GetJSDocDescription(("Daz Studio V3 documentation missing.", None, None, None, None))
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
#     # [0] - Type [1] - var Name
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
    
    
#     @staticmethod
#     def WriteJSClass(jsObj) -> str:
#         jsClass = jsObj # type: JSClass
#         implementMsg = ""
#         """Returns a JS Class with required variables, functions, enums, etc."""
#         totalMsg = ""
#         # Start with class info.
#         fileName = os.path.basename(jsClass.link)
#         totalMsg += COMMENT_TEMPLATE_BEGINNING + "\n" + COMMENT_TEMPLATE_NEWLINE + "@classdesc " + "### **This class is from v3 documentation and may be outdated.** ###" + jsObj.classinfo + "\n" + COMMENT_TEMPLATE_NEWLINE + " For more information, go to: " + f"<DAZ_SCRIPT_V3_API>/{fileName} "  + COMMENT_TEMPLATE_ENDING + "\n"
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

# def GetClassDescription(DzObj:DzObject):
#     soup = bs(DzObj.dzPage, features=HTML_PARSER)
#     h2 = soup.find("h2",text="Detailed Description") # type: bs
#     if h2 is not None or h2 != None:
#         DzObj.classinfo = str(h2.nextSibling)
#     else:
#         DzObj.classinfo = ""
# def CreateImplements(x:DzObject):
#     global CLASS_HIERARCHY_PAGE
#     soup = bs(CLASS_HIERARCHY_PAGE,features="html5lib")
#     us = soup.find('a', {"class" : "el"}, text=x.name)
#     aParent = us.parent
#     liParent = aParent.parent
#     # If we don't inherit from anything...
#     if liParent.name == "ul" and liParent.parent.name != "body":
#         parentClass = liParent.parent.find('a', {"class" : "el"})
#         x.implements.append(parentClass.text)
#         print(x.name, "implements", parentClass.text)
#     else:
#         print(x.name, "does not implement anything.")
#         return
# def CreateProperties(DzObj:DzObject):
#     link = DzObj.dzPage
#     soup = bs(link,features="html5lib")
#     # Find all "level 3" class that is a div.
#     tableData = soup.find_all("td", {"colspan" : "2"}) # type: list[bs]
#     for x in tableData:
#         tD = x # type: bs
#         possibleTDtext = tD.text == "Properties"
#         if possibleTDtext:
#             # We got the properties h2. Now to chop down the table rows below it.
#             minSourceLine = tD.parent.sourceline # td parent is tr.
#             maxSourceLine = FindMaxSourceLineGivenContextTable(tD.parent, True)+1
#             lastTr = None
#             while True:
#                 #rV = Return Value | pN = Property Name
#                 if lastTr == None:
#                     workingTr = tD.parent.find_next("tr")
#                 else:
#                     workingTr = GetNextSiblingBS(lastTr, {}, minSourceLine, maxSourceLine)
#                 # Now find detailed information.
#                 if workingTr is None or workingTr == None:
#                     break # We are done.
#                 tdReturnValue = workingTr.find("td", {"class" : "memItemLeft"})
#                 rV = tdReturnValue.find("a").text
#                 tdName = workingTr.find("td", {"class" : "memItemRight"})
#                 pN = tdName.find("a").text
#                 desc = GetDetailedInfo(workingTr, pN)
#                 JsProperty = JSProperty(pN, rV, desc[0], DzObj)
#                 DzObj.properties.append(JsProperty)
#                 lastTr = workingTr
# def CreateConstuctors(x):
#     DzObj = x # type: DzObject
#     soup = bs(DzObj.dzPage,features=HTML_PARSER)
#     tableData = soup.find_all("td", {"colspan" : "2"}) # type: list[bs]
#     for x in tableData:
#         tD = x # type: bs
#         possibleTDtext = tD.text == "Constructors"
#         if possibleTDtext:
#             minSourceLine = tD.parent.sourceline # td parent is tr.
#             maxSourceLine = FindMaxSourceLineGivenContextTable(tD.parent, True)+1
#             lastTr = None
#             while True:
#                 #rV = Return Value | pN = Property Name
#                 if lastTr == None:
#                     workingTr = tD.parent.find_next("tr")
#                 else:
#                     workingTr = GetNextSiblingBS(lastTr, {}, minSourceLine, maxSourceLine)
#                 # Now find detailed information.
#                 if workingTr is None or workingTr == None:
#                     break # We are done.
#                 # Make sure we didn't get a fucking <br>
#                 possibleBr = workingTr.find("br")
#                 textAvailable = workingTr.text == None
#                 if (possibleBr != None or possibleBr is not None) and not textAvailable:
#                     # Don't go any fruther, do next iteration.
#                     lastTr = workingTr
#                     continue
#                 cN = GetSymbolArgs(workingTr)
#                 pA = cN[cN.index("(")+1:cN.index(")")].strip()
#                 cN = cN[:cN.index("(")].strip()
#                 desc = GetDetailedInfo(workingTr, cN, "Constructor & Destructor Documentation", pA)
#                 JsConstructor = JSConstructor(cN, pA, documentation=desc)
#                 DzObj.constructors.append(JsConstructor)
#                 print(desc,"|", cN)
#                 lastTr = workingTr   
# def CreateStaticMethods(DzObj:DzObject):
#     soup = bs(DzObj.dzPage,features=HTML_PARSER)
#     tableData = soup.find_all("td", {"colspan" : "2"}) # type: list[bs]
#     for x in tableData:
#         tD = x # type: bs
#         possibleTDtext = tD.text == "Methods (Static)"
#         if possibleTDtext:
#             minSourceLine = tD.parent.sourceline # td parent is tr.
#             maxSourceLine = FindMaxSourceLineGivenContextTable(tD.parent, True)+1
#             lastTr = None
#             while True:
#                 #rV = Return Value | pN = Property Name
#                 if lastTr == None:
#                     workingTr = tD.parent.find_next("tr")
#                 else:
#                     workingTr = GetNextSiblingBS(lastTr, {}, minSourceLine, maxSourceLine)
#                 # Now find detailed information.
#                 if workingTr is None or workingTr == None:
#                     break # We are done.
#                 # Make sure we didn't get a fucking <br>
#                 possibleBr = workingTr.find("br")
#                 textAvailable = workingTr.text == None
#                 if (possibleBr != None or possibleBr is not None) and not textAvailable:
#                     # Don't go any fruther, do next iteration.
#                     lastTr = workingTr
#                     continue
#                 mN = GetSymbolArgs(workingTr)
#                 pA = mN[mN.index("(")+1:mN.index(")")].strip()
#                 mN = mN[:mN.index("(")].strip()
#                 rV = GetReturnType(workingTr)
#                 desc = GetDetailedInfo(workingTr, mN, "Member Function Documentation", pA)
#                 JsStaticMethod = JSFunction(mN, pA, rV, desc, True, DzObj)
#                 DzObj.functions.append(JsStaticMethod)
#                 print(desc,"|", mN)
#                 lastTr = workingTr   
# def CreateMethods(DzObj:DzObject):
#     soup = bs(DzObj.dzPage,features=HTML_PARSER)
#     tableData = soup.find_all("td", {"colspan" : "2"}) # type: list[bs]
#     for x in tableData:
#         tD = x # type: bs
#         possibleTDtext = tD.text == "Methods"
#         if possibleTDtext:
#             minSourceLine = tD.parent.sourceline # td parent is tr.
#             maxSourceLine = FindMaxSourceLineGivenContextTable(tD.parent, True)+1
#             lastTr = None
#             while True:
#                 #rV = Return Value | pN = Property Name
#                 if lastTr == None:
#                     workingTr = tD.parent.find_next("tr")
#                 else:
#                     workingTr = GetNextSiblingBS(lastTr, {}, minSourceLine, maxSourceLine)
#                 # Now find detailed information.
#                 if workingTr is None or workingTr == None:
#                     break # We are done.
#                 # Make sure we didn't get a fucking <br>
#                 possibleBr = workingTr.find("br")
#                 textAvailable = workingTr.text == None
#                 if (possibleBr != None or possibleBr is not None) and not textAvailable:
#                     # Don't go any fruther, do next iteration.
#                     lastTr = workingTr
#                     continue
#                 mN = GetSymbolArgs(workingTr)
#                 pA = mN[mN.index("(")+1:mN.index(")")].strip()
#                 mN = mN[:mN.index("(")].strip()
#                 rV = GetReturnType(workingTr).strip() # wtf is char(180)
#                 desc = GetDetailedInfo(workingTr, mN, "Member Function Documentation", pA)
#                 JsStaticMethod = JSFunction(mN, pA, rV, desc, False, DzObj)
#                 DzObj.functions.append(JsStaticMethod)
#                 print(desc,"|", mN)
#                 lastTr = workingTr
# def CreateEnums(DzObj:DzObject):
#     soup = bs(DzObj.dzPage,features="html5lib")
#     tableData = soup.find_all("td", {"colspan" : "2"}) # type: list[bs]
#     for x in tableData:
#         tD = x # type: bs
#         possibleTDtext = tD.text == "Enumerations"
#         if possibleTDtext:
#             h2 = tD.parent.find_next('h2', text="Member Enumeration Documentation") # type: bs
#             if h2 != None or h2 is not None:
#                 minSourceline = h2.find_next("div", {"class" : "memitem"}).sourceline
#                 maxSourceline = FindMaxSourceLineGivenContext(h2)
#                 # Find a tbody within memitem.
#                 fTBody = h2.find_next("tbody") #type: bs
#                 lastfTBody = None
#                 while True:
#                     if lastfTBody is None or lastfTBody == None:
#                         workingfT = fTBody
#                     else:
#                         workingfT = GetNextBS(lastfTBody, {}, minSourceline, maxSourceline)
#                     # If none, we are done.
#                     if workingfT is None or workingfT == None:
#                         break
#                     # Get all trs
#                     listOfTrs = workingfT.find_all("tr")
#                     # For each tr, append enum. 
#                     for t in listOfTrs:
#                         tr = t # type: bs
#                         # Get enum name in em.
#                         try:
#                             eN = tr.find("em").text.strip()
#                         except:
#                             print("Fucking parser.")
#                             continue
#                         # Get enum description.
#                         eD = tr.find("em").parent.find_next("td").text.strip()
#                         # Create enum and append to DzObj enum list.
#                         JsEnum = JSEnum(eN, eD, DzObj)
#                         DzObj.enums.append(JsEnum)
#                         print("ENUM:", eN, "DESC:",  eD, "Class:", DzObj.name)
#                     lastfTBody = workingfT
# def CreateSignals(DzObj:DzObject):
#     soup = bs(DzObj.dzPage,features="html5lib")
#     tableData = soup.find_all("td", {"colspan" : "2"}) # type: list[bs]
#     for x in tableData:
#         # Confirm if we have enumerations.
#         tD = x # type: bs
#         possibleTDtext = tD.text == "Signals"
#         # If so, do work.
#         if possibleTDtext:
#             h2 = tD.parent.parent.find_next('h2', text="Member Function Documentation") # type: bs
#             if h2 != None or h2 is not None:
#                 minSourceline = h2.find_next("div", {"class" : "memitem"}).sourceline
#                 maxSourceline = FindMaxSourceLineGivenContext(h2)
#                 lastMemItem = None
#                 while True:
#                     if lastMemItem is None or lastMemItem == None:
#                         workingMemItem = h2.find_next("div", {"class" : "memitem"}) # type: bs
#                         if workingMemItem is not None:
#                             workingMemName = workingMemItem.find("table", {"class" : "memname"})
#                     else:
#                         workingMemItem = GetNextBS(lastMemItem, {"class" : "memitem"}, minSourceline, maxSourceline)
#                         if workingMemItem is not None:
#                             workingMemName = workingMemItem.find("table", {"class" : "memname"})
#                     if workingMemItem is None or workingMemItem == None:
#                         break
#                     if re.search(GenerateRE("\[signal\]"), workingMemItem.text) == None:
#                         lastMemItem = workingMemItem
#                         continue
#                     memdoc = workingMemItem.find("div", {"class" : "memdoc"}) # type: bs
#                     try:
#                         signatureBS = memdoc.find("code")
#                         signature = signatureBS.text.strip()
#                         desc = signatureBS.parent.find_next("p").text.strip()
#                     except:
#                         print("WARNING: No signature found and no desc found.")
#                         desc = memdoc.text
#                         signature = None
#                     tdName = workingMemName.find("td", {"class" : "memname"}).text # type: str
#                     if signature == None:
#                         signature = f"{tdName}()"
#                     lastColonIndex = tdName.rindex(":")
#                     sName = tdName[lastColonIndex+1:].strip()
#                     # Create the object.
#                     JsSignal = JSSignal(sName, "", signature, desc, DzObj)
#                     DzObj.signals.append(JsSignal)
#                     print("JsSignal for", DzObj.name, ":", sName, ":", signature, ":" , desc)
#                     lastMemItem = workingMemItem

# def DetermineIfEligible(x: DzObject):
#     """ Checks if the class is a ECMAScript. If it is, we will return false. Otherwise true."""
#     soup = bs(urlopen(x.dzPage),features=HTML_PARSER)
#     results = soup.find_next("h2", text="Detailed Description")
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
#     # if not DetermineIfEligible(DzObj) or DzObj in IGNORE_OBJECTS:
#     #     print(DzObj.name + " is not eligble. Deleting.")
#     #     return None
#     GetClassDescription(DzObj)
#     CreateImplements(DzObj)
#     CreateConstuctors(DzObj)
#     CreateEnums(DzObj)
#     CreateProperties(DzObj)
#     CreateStaticMethods(DzObj)
#     CreateMethods(DzObj)
#     CreateSignals(DzObj)
#     return JSClass(DzObj)

# def ClassStillExists(DzObj:DzObject) -> bool:
#     # Create a .dsa file.
#     fileName = f"CLASS_STILL_EXIST-{DzObj.name}.dsa"
#     with open(fileName, "w") as file:
#         tryStatement = "var failed = false;\ntry {\n\t" + DzObj.name + "\n} catch (e) {\n\tvar newFile = new DzFile(\"D:/Python Test Folder/New folder/" + DzObj.name + ".txt\");\n\tnewFile.open(DzFile.WriteOnly);\n\tnewFile.write(\"Failed\");\n\tnewFile.close();\n\tfailed=true;\n} finally {\n\tif (!failed) {\n\t\tvar newFile = new DzFile(\"D:/Python Test Folder/New folder/" + DzObj.name + ".txt\");\n\t\tnewFile.open(DzFile.WriteOnly);\n\t\tnewFile.write(\"Success\");\n\t\tnewFile.close();\n\t}\n}"
#         file.write(tryStatement)
#         file.close()
#     time.sleep(1)
#     os.popen("\"C:\Program Files\DAZ 3D\DAZStudio4\DAZStudio.exe\" " + f"\"{os.path.abspath(fileName)}\"")
#     time.sleep(1)
#     # Find the result.
#     expectedFile = DzObj.name
#     count = 0
#     while not os.path.isfile(f"D:/Python Test Folder/New folder/{expectedFile}.txt"):
#         time.sleep(0.25)
#         count += 1
#         if count >= 8:
#             print(f"Something didn't work out for {DzObj.name}")
#             return False
#     with open(f"D:/Python Test Folder/New folder/{expectedFile}.txt") as outputFile:
#         if "Success" in outputFile.read():
#             return True
#         else:
#             return False

# def BeginWork(ignoreList = []):
#     listOfLinks = []
#     soup = bs(urlopen(OBJECT_INDEX_PAGE),features=HTML_PARSER)
#     tds = soup.find_all("td")
#     for x in tds:
#         td = x # type: bs
#         possibleLink = td.find_next("a",{"class" : "el"})
#         if possibleLink:
#             listOfLinks.append((os.path.join("D:\\Python Test Folder\\DAZScriptV3\\", possibleLink["href"]), possibleLink.text))
#     for link in listOfLinks:
#         if not DzObject.ExistsAll(link[1]) and link[1] not in ignoreList and link[1] not in IGNORE_OBJECTS:
#             DzObject(link[1], link[0], urlopen("file:" + link[0]).read())
#             print(f"Created DzObject for {link[1]}.")
#     # Print working classes.
#     for object in DzObject.DzObjects:
#        ProcessObject(object)
#     # with multiprocessing.Pool(4) as p:
#     #     results = p.map(ProcessObject, DzObject.DzObjects)
#     return JSClass.JsClasses
# if __name__ == "__main__":
#     BeginWork()
