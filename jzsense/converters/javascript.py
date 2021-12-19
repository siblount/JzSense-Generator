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
    return BeautifyText(class_.classinfo)
def _write_constructor_documentation(constructor:JSConstructor) -> str:
    working_strs = []
    constructor_msgs = constructor.documentation
    if constructor_msgs[0] is not None:
        working_strs.append(f"@description {constructor_msgs[0]}")
    if constructor_msgs[1] is not None:
        working_strs.append(f"@returns {constructor_msgs[1]}")
    if constructor_msgs[2] is not None:
        working_strs.append(f"@since {constructor_msgs[2]}")
    if constructor_msgs[3] is not None:
        params = constructor_msgs.split("|!|") #type: list[str]
        for param in params:
            working_strs.append(f"@param {param}")
    if constructor_msgs[4] is not None:
        working_strs.append(f"@attention {constructor_msgs[4]}")
    # TODO: If deprepcated, add deprecated.
    return str("\n".join(working_strs).encode("utf-8"),"utf-8")
def _write_property_documentation(property:JSProperty) -> str:
    return f"@description {property.description}\n@type {{{property.jstype}}}"
def _write_function_documentation(func:JSFunction) -> str:
    working_strs = []
    func_msgs = func.other_info
    if func_msgs[0] is not None:
        working_strs.append(f"@description {func_msgs[0]}")
    if func_msgs[1] is not None:
        working_strs.append(f"@returns {func_msgs[1]}")
    if func_msgs[2] is not None:
        working_strs.append(f"@since {func_msgs[2]}")
    if func_msgs[3] is not None:
        params = func_msgs.split("|!|") #type: list[str]
        for param in params:
            working_strs.append(f"@param {param}")
    if func_msgs[4] is not None:
        working_strs.append(f"@attention {func_msgs[4]}")
    # TODO: If deprepcated, add deprecated.
    return str("\n".join(working_strs).encode("utf-8"),"utf-8")
def _write_enum_documentation(enum:JSEnum) -> str:
    return f"@description ENUM:{enum.raw_doc}"
def _write_signal_documentation(signal:JSSignal) -> str:
    working_strs = []
    working_strs.append("**THIS IS A SIGNAL!**")
    working_strs.append(f"@description {signal.raw_doc}")
    working_strs.append(f"@signature `{signal.signature}`")
    working_strs.append(f"@event")
    return str("\n".join(working_strs).encode("utf-8"),"utf-8")

def convert(dazObj:DazObject) -> str:
    """ Converts a DazObject into a representable JSDOC comment for JavaScript. """
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
            working_strs.append(str(Comment(_write_constructor_documentation(constructor)),"\t"))
            # Add constructor declaration.
            # If constructor has parameters...
            if len(constructor.params) != 0:
                params = ", ".join([f"{name} {val}" for (name, val) in constructor.params])
                working_strs.append(f"\tconstructor({params}) {{}};")
            else:
                working_strs.append(f"\tconstructor() {{}};")
        except Exception:
            pass
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
            params = []
            for name, val in func.params:
                params.append(name, val)
            params = ", ".join(params)
            if func.static:
                working_strs.append(f"\tstatic function {func}({params}) {{}};")
            else:
                working_strs.append(f"\function {func}({params}) {{}};")
        except Exception:
            pass
    # Signals (basically the same thing as funcs)
    for signal in dazObj.signals:
        try:
            # Write signaltion description.
            working_strs.append(str(Comment(_write_signal_documentation(signal),"\t")))
            params = []
            for name, val in signal.params:
                params.append(name, val)
            params = ", ".join(params)
            working_strs.append(f"\tfunction {signal}({params}) {{}};")
        except Exception as e:
            print(e)
    # We are done.
    working_strs.append("\n}\n")
    return fix_str("\n".join(working_strs))