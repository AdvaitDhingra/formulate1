import lark

# The Grammer

grammer = lark.Lark(r'''

start: expression

expression: pow 
          | addition
          | subtraction
          | multiplication
          | division

pow: atom ["**" atom | "^" atom]
addition: (atom "+" atom)*
subtraction: (atom "-" atom)*
division : (atom "/" atom)*
multiplication: (atom "*" atom)*
atom: "(" expression ")" | NUMBER -> literal


%import common.CNAME
%import common.NUMBER
%import common.WS

%ignore WS
''')

def _to_python(node, out):
  if node.data == "start":
    assert len(node.children) == 1
    _to_python(node.children[0], out)

  elif node.data == "expression":
    assert len(node.children) == 1
    _to_python(node.children[0], out)

  elif node.data == "pow":
    assert len(node.children) == 2
    _to_python(node.children[0], out)
    out.append("**")
    _to_python(node.children[1], out)
  
  elif node.data == "addition":
    _to_python(node.children[0], out)
    out.append("+")
    _to_python(node.children[1], out)

  elif node.data == "literal":
    assert len(node.children) == 1
    assert isinstance(node.children[0], str)
    out.append(str(node.children[0]))

  else:
    raise NotImplementedError(node.data)

def to_python(parsing_tree):
  out = []
  _to_python(parsing_tree, out)
  return "".join(out)

print(grammer.parse("1+1").pretty())
  