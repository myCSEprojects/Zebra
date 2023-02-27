from dataclasses import dataclass

@dataclass
class Error:
    type_:str
    message_:str
    lineNumber: int

    def report(self):
        print(f"{self.type_}:{self.lineNumber}\n{self.message}")
        global isError
        isError = True

@dataclass
class RuntimeException:
    type_:str
    message_:str
    lineNumber: int

    def raise_(self):
        raise Exception(f"{(self.type_ + ': ') if (self.type_) else ' '}{self.lineNumber}\n{self.message}")
        