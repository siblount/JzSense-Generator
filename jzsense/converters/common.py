class Comment():
    COMMENT_TEMPLATE_BEGINNING = "/**"
    COMMENT_TEMPLATE_NEWLINE = " * "
    COMMENT_TEMPLATE_ENDING = " */"

    def __init__(self, msg:str="", indent="") -> None:
        self.__indent = indent
        self.__raw_msg = msg
        self.__msg = self._construct_comment()
    
    def _construct_comment(self):
        current_indent = self.__indent
        working_str = current_indent + Comment.COMMENT_TEMPLATE_BEGINNING + '\n'
        return working_str + \
            "\n".join([current_indent + Comment.COMMENT_TEMPLATE_NEWLINE + line for line in self.__raw_msg.split("\n")]) + \
            f"\n{current_indent}" + Comment.COMMENT_TEMPLATE_ENDING
    
    def update_comment(self, updated_msg:str):
        self.__raw_msg = updated_msg
        self.__msg = self._construct_comment()

    def __str__(self) -> str:
        return self.__msg

    def __repr__(self) -> str:
        return f"Comment: {self.__raw_msg[:40]}"
        