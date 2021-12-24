from typing_extensions import Self

from jzsense.common.constants import *
from jzsense.common.ds4 import *

import os
# Classes used to hold parsed info.
class DazObject():
    """ An object that is found via the object index and it's parsed information."""
    DazObjects = [] #type: list[DazObject]
    def __init__(self, name:str, link:str, dzPage:bs=None, ds_version:int=4):
        self.enums = [] # type: list[JSEnum]
        self.functions = [] # type: list[JSFunction]
        self.properties = [] # type: list[JSProperty]
        self.constructors = [] # type: list[JSConstructor]
        self.signals = [] # type: list[JSSignal]
        self.implements = [] # type: list[str]
        self.jsclass = None # type: JSClass
        self.name = name
        self.lowered_name = name.lower()
        self.link = link
        self.ds_version = ds_version
        self.classinfo = ""
        self.dzPage = dzPage
        self.local_location = ""
        DazObject.DazObjects.append(self)

    @classmethod
    def ExistsAll(cls, strObj):
        foundIt = False
        for obj in cls.DazObjects:
            if strObj in obj.enums or strObj in obj.functions or strObj in obj.properties or strObj in obj.constructors or strObj in obj.signals or strObj in obj.implements or strObj in obj.link or strObj in obj.name:
                foundIt = True
                break
        return foundIt

    @classmethod
    def FindObjAll(cls, strObj):
        for obj in cls.DazObjects:
            if strObj in obj.enums or strObj in obj.functions or strObj in obj.properties or strObj in obj.constructors or strObj in obj.signals or strObj in obj.implements or strObj in obj.link or strObj in obj.name:
                return obj
        return None

    def __str__(self):
        return f"DazObject: {self.name}"
class JSType():
    """ Used for capturing the type of an parameter, return value, or property. """
    types = {}

    def __init__(self, name:str) -> None:
        self.name = name
        self.lowered_name = name.lower()
        self.is_temp = "_" in name
        self.was_updated = False
        JSType.types[self.lowered_name] = self
        
    def update(self, new_name:str):
        if self.was_updated:
            return
        self.name = new_name
        self.lowered_name = new_name.lower()
        self.was_updated = True

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

    @staticmethod
    def cleanse_name(name:str) -> str:
        """ Removes "deprecated" bullshit from the name."""
        if "deprecated" in name:
            return name[:name.index("(")].strip()
        else:
            return name
    @classmethod
    def get_type(cls, type:str) -> Self:
        type_name = JSType.cleanse_name(type)
        type_name_lower = type_name.lower()
        if type_name_lower in cls.types:
            return cls.types[type_name_lower]
        else:
            return JSType(type_name)
class JSProperty():
    def __init__(self, name: str, jstype: JSType, description:str = "", dzObj:DazObject = None):
        self.name = name
        self.description = str(description.encode("UTF-8"),"UTF-8").strip()
        self.jstype = jstype
        # self.type = str(vType.encode("UTF-8"),"UTF-8")
        self.dzObj = dzObj

    def __str__(self):
        return f"{self.name}"
    def __repr__(self) -> str:
        return f"{self.name}:{self.jstype};"

    def GetMethodVersion(self) -> str:
        return f"{self.name}:{self.jstype};"

    def GetRegularVersion(self) -> str:
        return f"var {self.name}:{self.jstype};"

    def GetJSDocDescription(self) -> str:
        totalMsg = COMMENT_TEMPLATE_BEGINNING + "\n"
        totalMsg += COMMENT_TEMPLATE_NEWLINE + f"@description {self.description}\n"
        totalMsg += "\t" + COMMENT_TEMPLATE_ENDING
        return totalMsg
class JSConstructor():
    def __init__(self, name:str, params:str="", documentation:str = None):
        self.name = str(name.encode("UTF-8"),"UTF-8")
        self.params = JSParameter.parse_params(params)
        # self.message = self.ConvertToJS(self)
        self.dzObj = DazObject.FindObjAll(name)
        self.documentation = self.GetJSDocDescription(documentation)
        self.raw_doc = documentation
    #     /**
	#  * @description /
	#  * @returns *
	#  * @since *
	#  * @param 
	#  * 
	#  * @attention  
	#  */
    # What.
    
    def __repr__(self):
        params = ", ".join(str(param) for param in self.params)
        return f"{self.name} ({params})"
    # DEPRECRATED: ONLY USED FOR DS3
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
            #print(obj.params, obj.name, type(obj.params))
            if type(obj.params) is tuple:
                if len(obj.params) != 1:
                    if "=" in obj.params[1]:
                            # Get = index.
                            equalIndex = obj.params[1].index("=")
                            beforeEqualStr = obj.params[1][:equalIndex] # type: str
                            nameParams = f"{fix_str(beforeEqualStr)}:{obj.params[0]}"
                    else:
                        nameParams = f"{fix_str(obj.params[1])}:{obj.params[0]}"
                else:
                    nameParams = obj.params[0]
            else:
                # nameParams = [name.strip().split(" ") for name in obj.params if name not in PARAM_IGNORE]
                nameParams = [name for name in obj.params if name not in PARAM_IGNORE]
                finalParam = []
                # for param in nameParams:
                #     if "=" in param[1]:
                #         # Get = index.
                #         equalIndex = param[1].index("=")
                #         beforeEqualStr = param[1][:equalIndex]
                #         paramVal = f"{fix_str(beforeEqualStr)}:{param[0]}"
                #     else:
                #         paramVal = f"{param[1]}:{param[0]}"
                #     finalParam.append(paramVal)
                
            if type(nameParams) is str:
                totalMsg += f"constructor({nameParams})" + " {\n\t"
            else:
                totalMsg += f"constructor({SEPERATOR.join(finalParam)})" +" {\n\t"
        # End it.
        totalMsg += "\n\t};"
        return totalMsg

    # DEPRECRATED: ONLY USED FOR DS3
    @staticmethod
    def GetJSDocDescription(msg) -> str:
        # [0] - textDesc [1] - returnDesc [2] - sinceDesc [3] - paramsDesc [4] - attentionDesc
        totalMsg = COMMENT_TEMPLATE_BEGINNING + "\n"
        if msg[0] != None:
            totalMsg += COMMENT_TEMPLATE_NEWLINE + f"@description {msg[0]}\n"
        if msg[1] != None:
            totalMsg += COMMENT_TEMPLATE_NEWLINE + f"@returns {msg[1]}\n"
        if msg[2] != None:
            totalMsg += COMMENT_TEMPLATE_NEWLINE + f"@since {msg[2]}\n"
        if msg[3] != None:
            listOfParams = msg[3].split("|!|") #list[str]
            for param in listOfParams:
                totalMsg += COMMENT_TEMPLATE_NEWLINE + f"@param {param}\n"
        if msg[4] != None:
            totalMsg += COMMENT_TEMPLATE_NEWLINE + f"@attention {msg[4]}\n"
        totalMsg += COMMENT_TEMPLATE_NEWLINE + "@constructor\n"
        totalMsg += COMMENT_TEMPLATE_ENDING + "\n"
        return str(totalMsg.encode("utf-8"),"utf-8")
class JSFunction():
    def __init__(self, name:str, params:str, returnObj:str|JSType, desc:str, static:bool = False, dzObj:DazObject=None, otherInfo:tuple[str,str,str,str,str]=tuple()):
        # Order of these are important. Some need to be intialized before the others.
        self.name = name
        self.params = JSParameter.parse_params(params)
        self.returnObj = returnObj # "void" or JSType.
        if desc is not None:
            self.desc = self.GetJSDocDescription(desc)
        else:
            if dzObj.ds_version == 3:
                self.GetJSDocDescription(("DAZ Studio V3 - Missing documentation.", None, None, None, None))
            else:
                self.GetJSDocDescription(("DAZ Studio 4 - Missing documentation.", None, None, None, None))
            
        self.dzObj = dzObj
        self.static = static
        # if dzObj.name == "Global":
        #     self.message = self.ConvertToJSGlobal(self)
        # else:
        #     self.message = self.ConvertToJS(self)
        self.other_info = desc
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return f"{self.name} -> {self.returnObj} | {len(self.params)}"

    # DEPRECATED: BELOW FUNCS ONLY AVAILABLE FOR DS3

    @classmethod
    def ConvertToJS(cls,j) -> str:
        SEPERATOR = ", "
        PARAM_IGNORE = ["…"]
        totalMsg = ""
        obj = j # type: cls
        # Get the length of params.
        if (obj.params is None or len(obj.params) == 0):
            totalMsg += f"{obj.name}():{j.returnObj.strip()}" + " {\n\t"
        else:
            #print(obj.params, obj.name, type(obj.params))
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
        totalMsg += "\n\t};"
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
            #print(obj.params, obj.name, type(obj.params))
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
        totalMsg += "\n\t};"
        return totalMsg
    @staticmethod
    def GetJSDocDescription(msg:tuple[str,str,str,str,str]) -> str:
        # [0] - textDesc [1] - returnDesc [2] - sinceDesc [3] - paramsDesc [4] - attentionDesc
        totalMsg = COMMENT_TEMPLATE_BEGINNING + "\n"
        if msg[0] != None:
            totalMsg += COMMENT_TEMPLATE_NEWLINE + f"@description {msg[0]}\n"
        if msg[1] != None:
            totalMsg += COMMENT_TEMPLATE_NEWLINE + f"@returns {msg[1]}\n"
        if msg[2] != None:
            totalMsg += COMMENT_TEMPLATE_NEWLINE + f"@since {msg[2]}\n"
        if msg[3] != None:
            listOfParams = msg[3].split("|!|") #list[str]
            for param in listOfParams:
                totalMsg += COMMENT_TEMPLATE_NEWLINE + f"@param {param}\n"
        if msg[4] != None:
            totalMsg += COMMENT_TEMPLATE_NEWLINE + f"@attention {msg[4]}\n"
        totalMsg += COMMENT_TEMPLATE_ENDING + "\n"
        return str(totalMsg.encode("utf-8"),"utf-8")
class JSEnum():
    def __init__(self, name:str, desc:str, dzObj:DazObject = None):
        self.name = name
        self.raw_doc = desc
        self.desc = self.GetJSDocDescription(desc)
        self.dzObj = dzObj
        self.message = self.GetMethodVersion(self)

    def __str__(self) -> str:
        return self.name
    @classmethod
    def GetJSDocDescription(cls, msg) -> str:
        totalMsg = COMMENT_TEMPLATE_BEGINNING + "\n"
        totalMsg += COMMENT_TEMPLATE_NEWLINE + f"@description ENUMERATOR: {msg}\n"
        #totalMsg += COMMENT_TEMPLATE_NEWLINE + "@constructor\n"
        totalMsg += COMMENT_TEMPLATE_ENDING + "\n"
        return str(totalMsg.encode("utf-8"),"utf-8")

    @classmethod
    def GetMethodVersion(cls,self) -> str:
        return f"static {self.name};"
class JSSignal():
    def __init__(self, name:str, params:str, signature:str, documentation:str, dzObj:DazObject):
        self.name = name
        self.params = JSParameter.parse_params(params)
        self.signature = signature
        self.raw_doc = documentation
        self.documentation = self.GetJSDocDescription(documentation, signature)
        # self.message = self.ConvertToJS(self)
        self.dzObj = dzObj

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"{self.name} ({self.params})"
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
            totalMsg += f"{obj.name}():void" + " {\n\t"
        else:
            #print(obj.params, obj.name, type(obj.params))
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
                    totalMsg += f"{obj.name}({nameParams}):void" + " {\n\t"
            else:
                    totalMsg += f"{obj.name}({SEPERATOR.join(finalParam)}):void" +" {\n\t"
        # End it.
        totalMsg += "\n\t};"
        return totalMsg

    @classmethod
    def GetJSDocDescription(cls, msg, signature) -> str:
        totalMsg = COMMENT_TEMPLATE_BEGINNING + "\n"
        totalMsg += COMMENT_TEMPLATE_NEWLINE+ "**THIS IS A NOT AN ACTUAL FUNCTION**, THIS IS A `signal`! USE ONLY THE `signature`.\n "
        totalMsg += COMMENT_TEMPLATE_NEWLINE + f"@description {msg}\n"
        totalMsg += COMMENT_TEMPLATE_NEWLINE + f"@signature `{signature}`\n"
        totalMsg += COMMENT_TEMPLATE_NEWLINE + f"@event\n"
        #totalMsg += COMMENT_TEMPLATE_NEWLINE + "@constructor\n"
        totalMsg += COMMENT_TEMPLATE_ENDING + "\n"
        return str(totalMsg.encode("utf-8"),"utf-8") 
class JSClass():
    JsClasses = [] # type: list[JSClass]
    JS_CLASS_START = "class {}"
    def __init__(self, dzObj: DazObject):
        self.enums = dzObj.enums
        self.functions = dzObj.functions
        self.constructors = dzObj.constructors
        self.implements = dzObj.implements
        self.signals = dzObj.signals
        self.name = dzObj.name
        self.properties = dzObj.properties
        self.classinfo = dzObj.classinfo
        self.link = dzObj.link
        self.dzObj = dzObj
        self.JsClasses.append(self)
        dzObj.jsclass = self

    def __str__(self):
        if self.name != "Global":
            return self.WriteJSClass(self)
        else:
            return self.AddGlobals(self)

    def get_class_definition(self):
        """ Returns the class defintion with `{` at the end."""
        extends_msg = "extends " + ", ".join(set(str(jstype) for jstype in self.implements))
        if extends_msg == "extends ":
            return f"class {self.name} {{"
        else:
            return f"class {self.name} {extends_msg} {{"
    
    def get_class_documentation(self):
            # TODO: Remove classinfo from dazobject and move to JSClass.
            return self.BeautifyText(self.classinfo)

    def BeautifyText(self, text:str):
        # TODO: Use regex for exact search.
        # Ex: beautify 'index' not 'indexs'
        lineList = text.split("\n")
        for i, line in enumerate(lineList):
            wordList = line.split()
            for j, word in enumerate(wordList):
                for property in self.properties:
                    if re.match(f"({word})") in property.name:
                        wordList[j] = f"`{word}`"
            lineList[i] = " ".join(wordList)
        return "\n".join(lineList) 

    @staticmethod
    def WriteJSClass(jsObj:Self) -> str:
        """Returns a JS Class with required variables, functions, enums, etc."""
        jsClass = jsObj # type: JSClass
        
        implementMsg = ""
        totalMsg = ""
        # Start with class info.
        if jsClass.dzObj.ds_version == 3:
            fileName = os.path.basename(jsClass.link)
            totalMsg += COMMENT_TEMPLATE_BEGINNING + "\n" + COMMENT_TEMPLATE_NEWLINE + "@classdesc " + "### **This class is from v3 documentation and may be outdated.** ###" + jsObj.classinfo + "\n" + COMMENT_TEMPLATE_NEWLINE + " For more information, go to: " + f"<DAZ_SCRIPT_V3_API>/{fileName} "  + COMMENT_TEMPLATE_ENDING + "\n"
        else:
            totalMsg += COMMENT_TEMPLATE_BEGINNING + "\n" + COMMENT_TEMPLATE_NEWLINE + "@classdesc " + jsObj.classinfo + "\n" + COMMENT_TEMPLATE_NEWLINE + " For more information, go to: {@link " + f"{jsObj.link}" + "} " + COMMENT_TEMPLATE_ENDING + "\n"
        # Start with implements.
        if len(jsClass.implements) != 0:
            implementMsg = " extends " + ", ".join(set(str(jstype) for jstype in jsClass.implements))
        totalMsg += JSClass.JS_CLASS_START.format(jsClass.name) + implementMsg + " {\n"
        # Then variables.
        if len(jsClass.properties) !=0:
            for prop in jsClass.properties:
                totalMsg += "\t" + prop.GetJSDocDescription() + "\n"
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
        # Then signals
        if len(jsClass.signals) != 0:
            for signal in jsClass.signals:
                totalMsg += "\t" + signal.documentation + "\t" + signal.message + "\n"
        # We are done.
        # End curly brace.
        if jsClass.name == "Global":
            return fix_str(totalMsg)
        else:
            totalMsg += "\n}"
        return fix_str(totalMsg)

    @staticmethod
    def AddGlobals(jsObj) -> str:
        jsClass = jsObj # type: JSClass
        implementMsg = ""
        """Returns a JS Class with required variables, functions, enums, etc."""
        totalMsg = "\n////////////////////////////////////////GLOBALS/////////////////////////////////////////////\n"
        # Start with variables.
        if len(jsClass.properties) !=0:
            for prop in jsClass.properties:
                totalMsg += prop.GetRegularVersion() + "\n"
        # Then our functions/methods.
        if len(jsClass.functions) != 0:
            for function in jsClass.functions:
                totalMsg += function.desc + function.message + "\n"
        return fix_str(totalMsg)
class JSParameter():
    #TODO: Use parameters for all placements of ParseParams
    def __init__(self, parameter_name:str, parameter_type:JSType, value:str="") -> None:
        if parameter_name == "function":
            parameter_name = "func"
        self.parameter_name = parameter_name
        self.parameter_type = parameter_type
        self.value = value


    def __str__(self) -> str:
        if self.value != "":
            return f"{self.parameter_name} = {self.value}"
        else:
            return f"{self.parameter_name}"

    def __repr__(self) -> str:
        return f"{self.parameter_name}:{self.parameter_type} = {self.value}"

    @staticmethod
    def parse_params(params:str) -> tuple["JSParameter"]:
        """ Given a string `params` will be converted to (return) a tuple of `JSParamter`s."""
        def _handle_param(param:str) -> JSParameter | JSRestParameter:
            """ Converts the param in any format (incluing incomplete). Must not have () at beginning or end. `param` should be stripped.
            
            Returns:

                `JSParameter` if the parameter has a name and/or a type.

                `JSRestParameter` if it is an any argument (...args)
            """
            # Not sure if this gets called anymore.
            if "…" in param:
                return JSRestParameter()
            # addManipulator((deprecated) manip) 
            if "( deprecated )" in param or "(deprecated)" in param:
                closing_parenthesis_index = param.find(")") + 1 # includes closing parenthesis
                type = JSType.get_type(param[:closing_parenthesis_index])
                param = param[closing_parenthesis_index:]
                if "=" in param:
                    name, val = param.split("=",1)
                    name = name.strip()
                    val = val.strip()
                    return JSParameter(name, type, val)
                else:
                    return JSParameter(param.strip(),type)
            else:
                if " " in param:
                    type, param = param.split(" ",1)
                    type = JSType.get_type(type)
                    if "=" in param:
                        name, val = param.split("=",1)
                        name = name.strip()
                        val = val.strip()
                        return JSParameter(name, type, val)
                    else:
                        return JSParameter(param.strip(),type)
                else:
                    # someFunc ( DzTexture ) <-- wtf; else statement handles this.
                    if "=" in param:
                        type, val = param.split("=",1)
                        type = type.strip()
                        name = type.lower()
                        val = val.strip()
                        return JSParameter(name, type, val)
                    else:
                        type = param.strip()
                        name = type.lower()
                        return JSParameter(name, type)

            
        # concat ( Object element1, … )
        # create special JSParameter - rest parameter. --> ...args
        properties = []
        #[0] - Type [1] - var Name
        # If comma in param string it means we have multiple params.
        if "," in params:
            # Constructor has multiple parameters.
            _params = params.split(",")
            for p in _params:
                properties.append(_handle_param(p.strip()))
        else:
            # Constructor has one or none parameter.
            if params == "":
                return tuple()
            else:
                properties.append(_handle_param(params.strip()))

        return tuple(properties)

class JSRestParameter():
    """ A parameter in which accepts any number of arguments."""
    def __init__(self) -> None:
        pass
    def __str__(self) -> str:
        return "...args"
    def __repr__(self) -> str:
        return str(self)