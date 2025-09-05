""" ZOO  Programming Language Parser.

An experimental language.
"""
import json
import unicodedata
from dataclasses import dataclass, field
from functools import cache
from pathlib import Path
from typing import Any

from emoji import emojize

from lark import Lark, ParseTree, Transformer
from lark.exceptions import UnexpectedCharacters
from lark.indenter import Indenter
from lark import Token

import regex

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

BACKSLASH_ESC = {
   '\\': '\\',
   '"': '"',
   'a': '\x07',
   'b': '\x08',
   'e': '\x1B',
   'f': '\x0C',
   'n': '\x0A',
   'r': '\x0D',
   't': '\x09',
   'v': '\x0B',    
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

      
   def DECIMAL_FLOAT_LITERAL(self, token: Token) -> Token:
      """Normalize decimal float literal."""
      result = ''
      suffix = ''
      for ch in token:
         if ch in ('-', '+', '.'):
            result += ch
         elif ch == '_':
            continue
         elif ch >= 'A' and ch <= 'z':
            suffix += ch
         else:
            result += chr(
               ord('0') + unicodedata.decimal(ch)
            )
      
      fres = float(result)
      if suffix:
         _, fsuff = DECIMAL_SUFFIXES.get(suffix, (1, 1.0))
         fres *= fsuff
      return Token.new_borrow_pos(
         token.type,
         fres,
         token,
      )

   def CHAR_LITERAL(self, token: Token) -> Token:
      """Normalize character literals."""
      return Token.new_borrow_pos(
         token.type,
         normalize_char_literal(str(token)),
         token,
      )
   
   def RAW_STRING_LITERAL(self, token: Token) -> Token:
      """Normalize raw string literals."""
      data = str(token.value)[1:-1]
      lines = regex.split(r'\p{Zs}*(?:\r\n|[\p{Zl}\p{Zp}\r\n])\p{Zs}*&?', data)
      return Token.new_borrow_pos(
         token.type,
         '\n'.join(lines),
         token,
      )
      
   def STRING_LITERAL_QQ(self, token: Token) -> Token:
     """Normalize string literals."""
     return Token.new_borrow_pos(
        token.type,
        normalize_string_literal(str(token[1:-1])),
        token,
     )
     
   def STRING_LITERAL_QB(self, token: Token) -> Token:
     """Normalize string literals."""
     return Token.new_borrow_pos(
        token.type,
        normalize_string_literal(str(token[1:-2])),
        token,
     )

     
   def STRING_LITERAL_BQ(self, token: Token) -> Token:
     """Normalize string literals."""
     return Token.new_borrow_pos(
        token.type,
        normalize_string_literal(str(token[2:-1])),
        token,
     )

   
   def STRING_LITERAL_BB(self, token: Token) -> Token:
     """Normalize string literals."""
     return Token.new_borrow_pos(
        token.type,
        normalize_string_literal(str(token[2:-2])),
        token,
     )

     
   def get_module(self) -> ZooModule:
      return self._module

STRING_PARSER = regex.compile(
   r"(?P<txt>[^\\\"\n\r\p{Zl}\p{Zp}]+)"
   + r"|(?P<esc>\\[" +(''.join(BACKSLASH_ESC.keys()))+'])'
   + r"|(?P<chr>\\'.[^']*')"
   + r"|(?P<lbr>\\?\p{Zs}*(\r\n|[\p{Zl}\p{Zp}\r\n])\p{Zs}*&?)"
)

def normalize_string_literal(value: str) -> str:
   """Normalize string literals."""
   result = ''
   for m in STRING_PARSER.finditer(value):
      kind = m.lastgroup
      chunk = m.group()
      if kind == 'txt':
         result += chunk
      elif kind == 'esc':
         result += BACKSLASH_ESC[chunk[1]]
      elif kind == 'chr':
         result += normalize_char_literal(chunk[1:])
      elif '\\' not in chunk:
         result += '\n'
   return result

def normalize_char_literal(value: str) -> str:
   """Normalize character literal."""
   data: str = value[1:-1]
   if data.startswith('\\'):
      data = BACKSLASH_ESC.get(data[1:], '')
   elif data.startswith('U+'):
      try:
         code_point = int(data[2:], 16)
         data = chr(code_point)
      except ValueError:
         data = ''
   elif data.startswith(':') and data.endswith(':') and len(data) > 2:
      data = emojize(data)
   else:
      try:
         data = unicodedata.lookup(data)
      except KeyError:
         data = get_mnemonics().get(data, data)
   data = unicodedata.normalize('NFC', data)
   if len(data) != 1:
      raise ValueError(f'Illegal character literal: {value}')
   return data
         
class ZooIndenter(Indenter):
    """Indenter for the ZOO language."""
    NL_type = '_NL'
    OPEN_PAREN_types = [
       'LPAR',
       'LSQB',
       'LBRACE',
       'STRING_LITERAL_QB',
    ]
    CLOSE_PAREN_types = [
       'RPAR',
       'RSQB',
       'RBRACE',
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

@cache
def get_mnemonics() -> dict[str, str]:
   with (Path(__file__).parent / "mnemonics.json").open('r', encoding="utf-8") as jsf:
      return {
         key: value['char']
         for key, value in json.load(jsf).items()
      }
