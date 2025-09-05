
Credits
=======

* Most of the syntax is based on the
  meanwhile deprecated `Cobra`_ language.
* From `Ceylon`_ we adopted SI/decimal
  prefixes for numeric literal,
  extending the concept by binary
  prefixes. Furthermore, `Ceylon`_
  (and probably many others) provide
  - named character references,
  - union and intersection types
  - sealed interfaces, whereas ZOO
    is closer along the lines of
    Java using a ``permits`` clause.
* `Crystal`_ inspired
  - decentralized package management,
  - Rubyesque iterators
* `Dafny`_ provides a loop-variant
  like ``decreases`` assertion which
  ensures termination of recursive
  functions.
* From `ZIG`_ we adopted
  - compile time function evaluation
    (planned) for pure immutable
    terminating (via ``decreasing`` if
    recursive) functions,
  - integrated unit tests,
  - ``defer`` and ``unreachable``
    statement,
  - result types, ``try`` and ``catch``
    expressions.
* `NIM`_ inspired the function
  overloading resolution
  strategy (planned). It also features
  Uniform Function Call Syntax (`UFCS`_).
* life cycle annotations ``stable`` and
  ``unstable`` (on top of ``obsolete``)
  are similar to ``@incubating``
  annotation in `Gradle`_ .
* singleton support by annotation is
  similar to Eiffel's ``once``
* ZOO implements most of Automated
  Delegation s specified in [Viega1998]_,
  side-effect free methods [Ierusalimschy1995]_,
  and variant parametric types [Igarashi2006]_.
* Probably new features, which at least
  I haven't
  seen before in other languages:
  - Character mnemonics according to
    `RFC 1345`_ in character and string
    literals,
  - `YAML`_ Front Matter (YFM) in source
    files for package and dependency
    information,
  - immutability for functions,
    meaning that the result varies only
    with the function arguments,
  - distinction between coverage from
    dedicated tests and accidental
    coverage,
  - dedicated ``todo`` statement,
  - singleton classes for dimensionful
    quantities.

.. rubric:: Citations

.. [Viega1998] John Viega, Bill Tutt, and Reimer Behrends.
   1998. Automated Delegation is a Viable Alternative to Multiple Inheritance in Class Based Languages.
   Technical Report. University of Virginia, USA.
   
.. [Ierusalimschy1995] Roberto Ierusalimschy, Noemi Rodriguez.
   1995. Side-effect free functions in object-oriented languages.
   Computer Languages, Volume 21, Issues 3–4, 1995, Pages 129-146, ISSN 0096-0551.
   
.. [Igarashi2006] Atsushi Igarashi and Mirko Viroli. 2006.
   Variant parametric types: A flexible subtyping scheme for generics.
   ACM Trans. Program. Lang. Syst. 28, 5 (September 2006), 795–847.

.. _YAML: https://yaml.org
.. _RFC 1345: https://datatracker.ietf.org/doc/html/rfc1345
.. _Cobra: https://web.archive.org/web/20170325001050/http://cobra-language.com/
.. _Ceylon: https://projects.eclipse.org/projects/technology.ceylon
.. _Crystal: https://crystal-lang.org/
.. _Gradle: https://docs.gradle.org/current/userguide/userguide.html
.. _Dafny: https://dafny.org/
.. _NIM: https://nim-lang.org/
.. _UFCS: https://en.m.wikipedia.org/wiki/Uniform_function_call_syntax
.. _ZIG: https://ziglang.org/