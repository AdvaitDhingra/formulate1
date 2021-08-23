import lark

expression_grammer = """
arith:   term   | term "+" arith  -> add | term "-" arith      -> sub
term:    factor | factor "*" term -> mul | factor "/" term     -> div
factor:  pow    | "+" factor      -> pos | "-" factor          -> neg
pow:     call ["**" factor]
call:    atom   | call trailer
atom:    "(" expression ")" | CNAME -> symbol | NUMBER -> literal
trailer: "(" arglist ")"
arglist: expression ("," expression)*

%import common.CNAME
%import common.NUMBER
%import common.WS
"""
grammer = "\n".join(["start: expression", "expression: arith", "%ignore WS"]) + expression_grammer

parser = lark.Lark(grammer)

class AST: # Abstract syntax tree maker 
    _fields = ()
    def __init__(self, *args, line=None):
        self.line = line
        for n, x in zip(self._fields, args):
            setattr(self, n, x)
            if self.line is None: self.line = x.line 

class Literal(AST):
    _fields = ("value",)
    def __str__(self):
        return str(self.value)

class Symbol(AST):
    _fields = ("symbol",)
    def __str__(self):
        return self.symbol 

class Call(AST):
    _fields = ("function", "arguments")
    def __str__(self):
        return "{0}({1})".format(str(self.function), ", ".join(str(x) for x in self.arguments))

def toast(ptnode):  # Recursively convert parsing tree (PT) into abstract syntax tree (AST).
    if ptnode.data in ("add", "sub", "mul", "div", "pos", "neg"):
        arguments = [toast(x) for x in ptnode.children]
        return Call(Symbol(str(ptnode.data), line=arguments[0].line), arguments)
    elif ptnode.data == "pow" and len(ptnode.children) == 2:
        arguments = [toast(ptnode.children[0]), toast(ptnode.children[1])]
        return Call(Symbol("pow", line=arguments[0].line), arguments)
    elif ptnode.data == "call" and len(ptnode.children) == 2:
        return Call(toast(ptnode.children[0]), toast(ptnode.children[1]))
    elif ptnode.data == "symbol":
        return Symbol(str(ptnode.children[0]), line=ptnode.children[0].line)
    elif ptnode.data == "literal":
        return Literal(float(ptnode.children[0]), line=ptnode.children[0].line)
    elif ptnode.data == "arglist":
        return [toast(x) for x in ptnode.children]
    else:
        return toast(ptnode.children[0])    # many other cases, all of them simple pass-throughs

print(toast(parser.parse("2 + 2")))

