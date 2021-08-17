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

print(parser.parse("2 + 2").pretty())