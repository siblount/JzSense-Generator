from jzsense.js import *
from jzsense.converters.common import Comment
# Format:
# Object Name | Symbol Type | Symbol Name | Documentation | Additonal Info
# (DzObject,  | (Property,  | x           | "Gets x value"| (getValue,
#   DzMesh,      Function,                                   -> False)
#   ...)         ...)
def wrap_string(*args) -> str:
    workingstr = ""
    for arg in args:
        workingstr += f'"{str(arg)}",' # Wrap args in quote.
    workingstr = workingstr[:-1] # get rid of last comma
    return workingstr
def unescape_string(str_) -> str:
    return str_.replace("\n","\\n")
def remove_empty_lines(arr:list[str]):
    for i in range(len(arr)-1,0,-1):
        if len(arr[i]) == 0:
            del arr[i]
def _write_class(class_:JSClass) -> str:
    return unescape_string(wrap_string(class_.dzObj.name, "", class_.dzObj.name, class_.classinfo, ""))
def _write_constructors(dzObj:DazObject) -> str:
    strs = []
    for constructor in dzObj.constructors:
        working_strs = []
        constructor_msgs = constructor.raw_doc
        if constructor_msgs[0] is not None:
            working_strs.append(unescape_string(wrap_string(dzObj.name, "Function", constructor.name, f"@description {constructor_msgs[0]}", "")))
        if constructor_msgs[1] is not None:
            working_strs.append(unescape_string(wrap_string(dzObj.name, "Function", constructor.name, f"@returns {constructor_msgs[1]}", "")))
        if constructor_msgs[2] is not None:
            working_strs.append(unescape_string(wrap_string(dzObj.name, "Function", constructor.name, f"@since {constructor_msgs[2]}", "")))
        if constructor_msgs[3] is not None:
            params = constructor_msgs[3].split("|!|") #type: list[str]
            for param in params:
                type = None
                for _param in constructor.params:
                    if _param.parameter_name in param:
                        type = _param.parameter_type
                if type is not None:
                    working_strs.append(unescape_string(wrap_string(dzObj.name, "Function", constructor.name, f"@param {{{type}}} {param}", "")))
                else:
                    working_strs.append(unescape_string(wrap_string(dzObj.name, "Function", constructor.name, f"@param {param}", "")))
        if constructor_msgs[4] is not None:
            working_strs.append(unescape_string(wrap_string(dzObj.name, "Function", constructor.name, f"@attention {constructor_msgs[4]}", "")))
        # TODO: If deprepcated, add deprecated.
        strs.append(str("\n".join(working_strs).encode("utf-8",errors="replace"),"utf-8"))
    remove_empty_lines(strs)
    return "\n".join(strs) if len(strs) != 0 else ""
def _write_properties(dzObj:DazObject) -> str:
    strs = []
    for prop in dzObj.properties:
        strs.append(unescape_string(wrap_string(dzObj.name, "Property", prop.name, prop.description, "")))
    return "\n".join(strs) if len(strs) != 0 else ""
def _write_functions(dzObj:DazObject) -> str:
    strs = []
    for func in dzObj.functions:
        strs.append(unescape_string(wrap_string(dzObj.name, "Function", func.name, func.other_info, func.returnObj)))
        strs.append(_write_parameters(func))
    remove_empty_lines(strs)
    return "\n".join(strs) if len(strs) != 0 else ""
def _write_enums(dzObj:DazObject) -> str:
    strs = []
    for enum in dzObj.enums:
        strs.append(unescape_string(wrap_string(dzObj.name, "Variable", enum.name, enum.desc, "")))
    return "\n".join(strs) if len(strs) != 0 else ""
def _write_parameters(func:JSFunction) -> str:
    strs = []
    for param in func.params:
        strs.append(unescape_string(wrap_string(func.dzObj.name, "Variable", param.parameter_name, param.parameter_type, func.name)))
    return "\n".join(strs) if len(strs) != 0 else ""
def _write_signals(dzObj:DazObject) -> str:
    strs = []
    for signal in dzObj.signals:
        strs.append(unescape_string(wrap_string(dzObj.name, "Function", signal.name, signal.raw_doc, signal.signature)))
    return "\n".join(strs) if len(strs) != 0 else ""
def convert(dazObj:DazObject) -> str:
    strs = [_write_class(dazObj.jsclass),
            _write_constructors(dazObj),
            _write_properties(dazObj),
            _write_functions(dazObj),
            _write_enums(dazObj),
            _write_signals(dazObj)]

    remove_empty_lines(strs)

    return "\n".join(strs) if len(strs) != 0 else ""
