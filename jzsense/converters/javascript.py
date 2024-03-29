from jzsense.common.ds4 import fix_str
from jzsense.js import *
from jzsense.converters.common import Comment

# JavaScript Format
# Class Documentation
    # Class (implements)
# Constructors
# Properties
# Enum
# Function
# Signal
def _write_class_documentation(class_:JSClass) -> str:
    def BeautifyText(text:str):
        # TODO: Use regex for exact search.
        # Ex: beautify 'index' not 'indexs'
        lineList = text.split("\n")
        for i, line in enumerate(lineList):
            wordList = line.split()
            for j, word in enumerate(wordList):
                for property in class_.properties:
                    if re.match(f"({property.name})",word):
                        wordList[j] = f"`{word}`"
            lineList[i] = " ".join(wordList)
        return "\n".join(lineList)
    if class_.dzObj.ds_version == 3:
        return BeautifyText("**WARNING: This information comes from DAZ Studio version 3 documentation and MAY NOT be available or is deprecated.**\n" + class_.classinfo)
    else:
        return BeautifyText(class_.classinfo + f"\nFor more information, go to: {{@link {class_.link}}}")
def _write_constructor_documentation(constructor:JSConstructor) -> str:
    working_strs = []
    constructor_msgs = constructor.raw_doc
    if constructor_msgs[0] is not None:
        working_strs.append(f"@description {constructor_msgs[0]}")
    if constructor_msgs[1] is not None:
        working_strs.append(f"@returns {constructor_msgs[1]}")
    if constructor_msgs[2] is not None:
        working_strs.append(f"@since {constructor_msgs[2]}")
    if constructor_msgs[3] is not None:
        params = constructor_msgs[3].split("|!|") #type: list[str]
        for param in params:
            type = None
            for _param in constructor.params:
                if _param.parameter_name in param:
                    type = _param.parameter_type
            if type is not None:
                working_strs.append(f"@param {{{type}}} {param}")
            else:
                working_strs.append(f"@param {param}")
    if constructor_msgs[4] is not None:
        working_strs.append(f"@attention {constructor_msgs[4]}")
    # TODO: If deprepcated, add deprecated.
    return str("\n".join(working_strs).encode("utf-8",errors="replace"),"utf-8")
def _write_property_documentation(property:JSProperty) -> str:
    return f"@description {property.description}\n@type {{{property.jstype}}}"
def _write_function_documentation(func:JSFunction) -> str:
    if func.other_info is None:
        return ""
    working_strs = []
    func_msgs = func.other_info
    if func_msgs[0] is not None:
        working_strs.append(f"@description {func_msgs[0]}")
    if func_msgs[1] is not None:
        if func.returnObj == "void":
            working_strs.append(f"@returns {func_msgs[1]}")
        else:
            working_strs.append(f"@returns {{{func.returnObj}}} {func_msgs[1]}")
    else:
        if func.returnObj != "void":
            working_strs.append(f"@returns {func.returnObj}")
    if func_msgs[2] is not None:
        working_strs.append(f"@since {func_msgs[2]}")
    if func_msgs[3] is not None:
        params = func_msgs[3].split("|!|") #type: list[str]
        for param in params:
            # Find parameter type.
            type = None
            for _param in func.params:
                if _param.parameter_name in param:
                    type = _param.parameter_type
            if type is not None:
                working_strs.append(f"@param {{{type}}} {param}")
            else:
                working_strs.append(f"@param {param}")
    if func_msgs[4] is not None:
        working_strs.append(f"@attention {func_msgs[4]}")
    # TODO: If deprepcated, add deprecated.
    return str("\n".join(working_strs).encode("utf-8",errors="replace"),"utf-8")
def _write_enum_documentation(enum:JSEnum) -> str:
    return f"@description ENUM: {enum.raw_doc}"
def _write_signal_documentation(signal:JSSignal) -> str:
    working_strs = []
    working_strs.append("**THIS IS A SIGNAL!**")
    working_strs.append(f"@description {signal.raw_doc}")
    working_strs.append(f"@signature `{signal.signature}`")
    working_strs.append(f"@event")
    return str("\n".join(working_strs).encode("utf-8",errors="replace"),"utf-8")

# Global vs non-global
def _write_non_global(dazObj:DazObject) -> str:
    """ Returns a string that contains the `dazObj`'s symbols wrapped inside a class along with it's documentation. """
    working_strs = []
    # Write class documentation comment.
    working_strs.append(str(Comment(_write_class_documentation(dazObj.jsclass))))
    # Write the class name, implements.
    working_strs.append(dazObj.jsclass.get_class_definition())
    # Indent is now 1 tab level.
    # Constructors
    for constructor in dazObj.constructors:
        try:
            # Add constructor description.
            working_strs.append(str(Comment(_write_constructor_documentation(constructor),"\t")))
            # Add constructor declaration.
            # If constructor has parameters...
            if len(constructor.params) != 0:
                params = ""
                if constructor.params is not None:
                    params = ", ".join([str(param) for param in constructor.params])
                working_strs.append(f"\tconstructor({params}) {{}};")
            else:
                working_strs.append(f"\tconstructor() {{}};")
        except Exception as e:
            print(f"Constructor error: {e}")
    # Properties
    for property in dazObj.properties:
        try:
            # Add property description.
            working_strs.append(str(Comment(_write_property_documentation(property), "\t")))
            # Add property definition.
            working_strs.append(f"\t{property};")
        except Exception:
            pass
    # Enums
    for enum in dazObj.enums:
        try:
            # Add enum description.
            working_strs.append(str(Comment(_write_enum_documentation(enum),"\t")))
            # Add enum definition.
            working_strs.append(f"\t{enum};")
        except Exception:
            pass
    # Functions
    for func in dazObj.functions:
        # Write function description.
        try:
            working_strs.append(str(Comment(_write_function_documentation(func),"\t")))
            params = ""
            if func.params is not None:
                params = ", ".join([str(param) for param in func.params])
            if func.static:
                working_strs.append(f"\tstatic {func}({params}) {{}};")
            else:
                working_strs.append(f"\t{func}({params}) {{}};") # Weird cases when ) is
        except Exception as e:
            print(f"function error: {e}")
    # Signals (basically the same thing as funcs)
    for signal in dazObj.signals:
        try:
            # Write signaltion description.
            working_strs.append(str(Comment(_write_signal_documentation(signal),"\t")))
            params = ""
            if signal.params is not None:
                params = ", ".join([str(param) for param in signal.params])
            working_strs.append(f"\t{signal}({params}) {{}};")
        except Exception as e:
            print(e)
    # We are done.
    working_strs.append("\n}\n")
    return fix_str("\n".join(working_strs))
def _write_global(dazObj:DazObject) -> str:
    """ Returns a string that contains global symbols and its documentation. """
    working_strs = []
    # Write class documentation comment.
    working_strs.append(str(Comment(_write_class_documentation(dazObj.jsclass))))
    # Indent is now 1 tab level.
    # Properties
    for property in dazObj.properties:
        try:
            # Add property description.
            working_strs.append(str(Comment(_write_property_documentation(property))))
            # Add property definition.
            working_strs.append(f"var {property};")
        except Exception:
            pass
    # Enums
    for enum in dazObj.enums:
        try:
            # Add enum description.
            working_strs.append(str(Comment(_write_enum_documentation(enum))))
            # Add enum definition.
            working_strs.append(f"var {enum};")
        except Exception:
            pass
    # Functions
    for func in dazObj.functions:
        # Write function description.
        try:
            working_strs.append(str(Comment(_write_function_documentation(func))))
            params = ""
            if func.params is not None:
                params = ", ".join([str(param) for param in func.params])
            if func.static:
                working_strs.append(f"static function {func}({params}) {{}};")
            else:
                working_strs.append(f"function {func}({params}) {{}};")
        except Exception:
            pass
    # Signals (basically the same thing as funcs)
    for signal in dazObj.signals:
        try:
            # Write signaltion description.
            working_strs.append(str(Comment(_write_signal_documentation(signal))))
            params = ""
            if signal.params is not None:
                params = ", ".join([str(param) for param in signal.params])
            working_strs.append(f"function {signal}({params}) {{}};")
        except Exception as e:
            print(e)
    # We are done.
    working_strs.append("\n")
    return fix_str("\n".join(working_strs))

def convert(dazObj:DazObject) -> str:
    """ Converts a DazObject into a representable JSDOC comment for JavaScript. """
    if dazObj.name != "Global":
        return _write_non_global(dazObj)
    else:
        return _write_global(dazObj)