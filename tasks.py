
import os
import sys


from doctest import DocTestParser
from pathlib import Path

from invoke import task, Collection, Program

# import pylit

from lark.exceptions import LarkError

# Add src path to Python path
sys.path.insert(0,
   os.path.abspath(
      os.path.join(
         os.path.dirname(__file__),
         'src',
      )
   )
)

from zoo.parser import parse_module


@task
def literate(_):
   """Run PyLit on the grammar file.
   
   Produces an RST file.
   """
   in_file = Path('src/zoo/zoo.lark')
   out_file = Path('doc/source/grammar.rst')
   #pylit.main(args=[
   #   'src/zoo/zoo.lark',
   #   'doc/source/grammar.rst',
   #   '--overwrite=yes',
   #])
   out_file.write_text(
      unlit(
         in_file.read_text(
            encoding='utf-8',
         )
      ),
      encoding='utf-8',
   )

@task(pre=[literate])
def docparse(_):
   """Run Doc-Test ZOO Examples."""
   parser = DocTestParser()

   examples = parser.get_examples(
      Path('doc/source/grammar.rst')
      .read_text(encoding='utf-8')
   )

   for example in examples:
      print('~' * 30)
      print(example.source)
      print('-' * 30)
      try:
         ast = parse_module(example.source)
         print(ast.pretty())
      except LarkError as err:
         print('! ' + str(err))

@task(pre=[literate])
def sphinx(c):
   """Run sphinx to generate documentation."""
   c.run('sphinx-build doc/source doc/build')


@task(pre=[sphinx])
def serve(c):
   """Run HTTP server on sphinx output."""
   c.run('python -m http.server -d doc/build')


def unlit(
   src: str,
   comment: str='# ',
   code_indent: str=' '*3,
) -> str:
   """Convert code fie to RST."""
   result = []
   blank_comment = comment.rstrip()
   for line in src.splitlines():
      if line.startswith(comment):
         result.append(
            line[len(comment):]
         )
      elif line.rstrip() == blank_comment:
         result.append('')
      elif not line.strip():
         result.append('')
      else:
         result.append(code_indent+line)
   return '\n'.join(result)


namespace = Collection(
   literate,
   docparse,
   sphinx,
   serve,
)

if __name__ == "__main__":
   program = Program(namespace=namespace)
   program.run(['make', "docparse", "serve"])
