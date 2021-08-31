from lark import Lark, Transformer

# The Grammer

grammer = Lark(r"""

?value: list -> list
      | SIGNED_NUMBER

list: "[" [value ("," value)*] "]" 

sum: "SUM(" list ")" -> sum


%import common.SIGNED_NUMBER 
%import common.WS
%ignore WS
""", start='value')

text = "SUM([2, 2])"

class OptimusPrime(Transformer):
    def list(self, items):
        return list(items);

class Magic(Transformer):
    def SIGNED_NUMBER(self, n):
        (n,) = n
        return float(n)
    def sum(self, s):
        iterator = 0
        for i in s:
            iterator += i 
        return iterator

    list = list
tree = grammer.parse(text)
print(Magic().transform(tree))

# parser = lark.Lark(grammer)

# class AST: # Abstract syntax tree maker 
#     _fields = ()
#     def __init__(self, *args, line=None):
#         self.line = line
#         for n, x in zip(self._fields, args):
#             setattr(self, n, x)
#             if self.line is None: self.line = x.line 

# class Literal(AST):
#     _fields = ("value",)
#     def __str__(self):
#         return str(self.value)

# class Symbol(AST):
#     _fields = ("symbol",)
#     def __str__(self):
#         return self.symbol 

# class Call(AST):
#     _fields = ("function", "arguments")
#     def __str__(self):
#         return "{0}({1})".format(str(self.function), ", ".join(str(x) for x in self.arguments))

# def toast(ptnode):  # Recursively convert parsing tree (PT) into abstract syntax tree (AST).
#     if ptnode.data in ("add", "sub", "mul", "div", "pos", "neg"):
#         arguments = [toast(x) for x in ptnode.children]
#         return Call(Symbol(str(ptnode.data), line=arguments[0].line), arguments)
#     elif ptnode.data == "pow" and len(ptnode.children) == 2:
#         arguments = [toast(ptnode.children[0]), toast(ptnode.children[1])]
#         return Call(Symbol("pow", line=arguments[0].line), arguments)
#     elif ptnode.data == "call" and len(ptnode.children) == 2:
#         return Call(toast(ptnode.children[0]), toast(ptnode.children[1]))
#     elif ptnode.data == "symbol":
#         return Symbol(str(ptnode.children[0]), line=ptnode.children[0].line)
#     elif ptnode.data == "literal":
#         return Literal(float(ptnode.children[0]), line=ptnode.children[0].line)
#     elif ptnode.data == "arglist":
#         return [toast(x) for x in ptnode.children]
#     else:
#         return toast(ptnode.children[0])    # many other cases, all of them simple pass-throughs

# # run the operation
# def run(astnode, symbols):
#     if isinstance(astnode, Literal):
#         return astnode.value

#     elif isinstance(astnode, Symbol):
#         return symbols[astnode.symbol]

#     elif isinstance(astnode, Call):
#         function = run(astnode.function, symbols)
#         arguments = [run(x, symbols) for x in astnode.arguments]
#         return function(*arguments)

# import math, operator
# # Here we define what symbol does what
# symbols = {"add": operator.add, "sub": operator.sub, "mul": operator.mul, "div": operator.truediv,
#            "pos": operator.pos, "neg": operator.neg, "pow": math.pow, "sqrt": math.sqrt, "x": 5}

# #run(toast(parser.parse("2 + 2")), symbols)
# print(parser.parse("sqrt(2)"))
