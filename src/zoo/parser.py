""" ZOO  Programming Language Parser.

An experimental language.
"""

import unicodedata
from dataclasses import dataclass, field
from functools import cache
from typing import Any


from lark import Lark, ParseTree, Transformer
from lark.indenter import Indenter
from lark import Token

from ruamel.yaml import YAML

DECIMAL_SUFFIXES = {
   'q': (0, 1.0E-30),
   'r': (0, 1.0E-27),
   'y': (0, 1.0E-24),
   'z': (0, 1.0E-21),
   'a': (0, 1.0E-18),
   'f': (0, 1.0E-15),
   'p': (0, 1.0E-12),
   'n': (0, 1.0E-09),
   'μ': (0, 1.0E-06),
   'u': (0, 1.0E-06),
   'm': (0, 1.0E-03),
   'c': (0, 1.0E-02),
   'd': (0, 0.1),
   'da': (10, 1.0E+01),
   'h': (100, 1.0E+02),
   'k': (1000, 1.0E+03),
   'K': (1000, 1.0E+03),
   'ki': (1024, 1.024E+03),
   'Ki': (1024, 1.024E+03),
   'M': (1000**2, 1.0E+06),
   'Mi': (1024**2, 1.024E+03**2),
   'G': (1000**3, 1.0E+09),
   'Gi': (1024**3, 1.024E+03**3),
   'T': (1000**4, 1.0E+12),
   'Ti': (1024**4, 1.024E+03**4),
   'P': (1000**5, 1.0E+15),
   'Pi': (1024**5, 1.024E+03**5),
   'E': (1000**6, 1.0E+03**6),
   'Ei': (1024**6, 1.024E+03**6),
   'Z': (1000**7, 1.0E+03**7),
   'Zi': (1024**7, 1.024E+03**7),
   'Y': (1000**8, 1.0E+03**8),
   'Yi': (1024**8, 1.024E+03**8),
   'R': (1000**9, 1.0E+03**9),
   'Ri': (1024**9, 1.024E+03**9),
   'Q': (1000**10, 1.0E+03**10),
   'Qi': (1024**10, 1.024E+03**10),
   
   
}


@dataclass
class ZooModule:
   """Wrapper around literal tokens.
   
   Stores additional validated value.
   """
   package_info: dict[str, Any] = field(default_factory=dict)
   

class ZooTransformer(Transformer):
   """Transform the AST."""
   
   def __init__(self) -> None:
      super().__init__()
      self._module: ZooModule = ZooModule()
   
   def YFM(self, token: Token) -> Token:
      """Validate YAML Front Matter."""
      lines = '\n'.join(token.splitlines()[1:-1])
      yaml = YAML(typ='safe')
      data = yaml.load(lines)
      self._module.package_info.update(data)
      return token
      
   def DECIMAL_INT_LITERAL(self, token: Token) -> Token:
      """Normalize decimal integer literal."""
      result = ''
      suffix = ''
      for ch in token:
         if ch in ('-', '+'):
            result += ch
         elif ch == '_':
            continue
         elif ch >= 'A' and ch <= 'z':
            suffix += ch
         else:
            result += chr(
               ord('0') + unicodedata.decimal(ch)
            )
      
      ires = int(result)
      if suffix:
         isuff, _ = DECIMAL_SUFFIXES.get(suffix, (1, 1.0))
         ires *= isuff
      return Token.new_borrow_pos(
         token.type,
         ires,
         token,
      )

   def get_module(self) -> ZooModule:
      return self._module

class ZooIndenter(Indenter):
    """Indenter for the ZOO language."""
    NL_type = '_NL'
    OPEN_PAREN_types = [
       '(',
       '[',
       '{',
       'STRING_LITERAL_QB',
    ]
    CLOSE_PAREN_types = [
       ')',
       ']',
       '}',
       'STRING_LITERAL_BQ'
    ]
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 3

@cache
def zoo_parser(**opts) -> Lark:
   """Create a new parser."""   
   return Lark.open(
      'zoo.lark',
   	parser='lalr',
   	postlex=ZooIndenter(),
   	rel_to=__file__,
   	regex=True,
   	debug=True,
   	**opts,
   )
   
def parse_module(src: str, **opts) -> ParseTree:
   """Parse the contents of a module file."""
   transformer = ZooTransformer()
   parser = zoo_parser(**opts)
   if not src.endswith('\n'):
      src = src + '\n'
   ast = parser.parse(src)
   ast = transformer.transform(ast)
   print(transformer.get_module())
   return ast
