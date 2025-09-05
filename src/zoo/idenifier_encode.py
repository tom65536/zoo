

import bootstring


def asciify(ident: str) -> str:
   """Convert Unicode identifier to ASCII."""
   return (
      bootstring.encode(ident.replace('_', '-').replace('.', '__'))
      .replace('-', '_')
   )

def deasciify(ascid: str) -> str:
   """Recover Unicode identifier from ASCII."""
   return (
      bootstring.decode(ascid.replace('_', '-'))
      .replace('-', '_').replace('__', '.')
   )
  
test_idents = (
   'x',
   'alpha_1',
   'γ_i',
   '_priv',
   'System.IO.print',
)

for _ident in test_idents:
   _ascid = asciify(_ident)
   roundtrip = deasciify(_ascid)
   print(f'{_ident} -> {_ascid} -> {roundtrip}')
   