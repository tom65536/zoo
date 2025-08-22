""" ZOO  Programming Language Parser.

An experimental language.
"""
from functools import cache

from lark import Lark, ParseTree
from lark.indenter import Indenter


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
   parser = zoo_parser(**opts)
   if not src.endswith('\n'):
      src = src + '\n'
   return parser.parse(src)


def test():
   """Test."""

   
      
   test_module = r"""
#! zoo
#
# Test Module
#
" Doc. \'"'
& defines \(foo\) and \(bah\). \
& more lines.
"
---
author: me
version: 1.2.3
---

use ξ = foo.bar from "the library"
namespace foo.bar
   pass
"""
   tree = parse_module(test_module)
   print(tree.pretty())

if __name__ == '__main__':
   test()
    
