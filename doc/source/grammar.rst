.. DO NOT EDIT THE RST FILE
   Modify zoo.lark instead

.. _title:

"""""""""""""""""""""
ZOO Grammar Reference
"""""""""""""""""""""

.. _intro:

Introduction
============

ZOO is an object-oriented
general-purpose language
designed with program quality
in mind. It is strongly typed
and garbage-collected.

ZOO serves also as a proof of concept
for a class-based language where
classes use automated delegation
instead of inheritance as described
in [Viega1998]_ .

.. _packages:

Packages and Programs
=====================

ZOO libraries are distributed as
packages. A package consists of

- a directory with a package descriptor
  in a ``cage.yaml``
  file and one or more ZOO module
  files, optionally organized in
  subdirectories, or
- a single self-contained ZOO module
  file. Instead of an additional YAML
  file the package descriptor is
  embedded as YAML front matter
  (see below).

.. _lexical:

Lexical Structure
=================

Encoding
--------

Program code is expected to be
encoded using UTF-8.

Indentation
-----------

Program code is structured using
indentation. This means that
white space at the beginning of a
line is meaningful.

Notation of indentation in this
grammer comprises the ``_INDENT``
token for an increase of indentation
and ``_DEDENT`` for a decrease of
indentation.

::

   %declare _INDENT _DEDENT

White Space
-----------

All characters (outside literals)
belonging to the Unicode general
category *Space Separator* (Zs)
and the horizontal tabulator (U+0009)
account for white space.
White space separtes tokens and defines
indentation but is otherwise ignored.

::

   WS_INLINE: /(\p{Zs}|\t)+/
   %ignore WS_INLINE

.. important:: Indentation is computed
   by the number of space characters
   (U+0020) plus three times the
   number of horizontal tabulators
   (U+0009) only. All other white
   space characters are ignored for
   counting.

   In order to keep the visual and the
   logical layout consistent you should
   not mix spaces, tabs and other
   white space for indentation.

.. _comments:
Comments
--------

Comments add information for the
(human) reader which is ignored
by the compiler. Comments start with
a number sign (``#``), also known as
hash sign, and extend to the end of
the line.

The following Unicode variants are
treated equalky as number signs:

- NUMBER SIGN (U+0023)
- SMALL NUMBER SIGN (U+FE5F)
- FULLWIDTH NUMBER SIGN (U+FF03)

::

   SH_COMMENT: /[#\uFE5F\uFF03][^\r\n\p{Zp}\p{Zl}]*/
   %ignore SH_COMMENT

There is no multiline comment
notation in ZOO. Although it involves
a bit more typing, a series of single
line comments is visually more
pronounced and therefore easier to
distinguish.

.. note:: Having said that comments
   carry information for the human
   reader it may as well provide
   information for external tools,
   as in shebang (``#!``) or editor
   specific lines.

.. note:: If the information should
   be part of the delivered documentation
   you should prefer `doc`_ over
   comments. If the information should
   be machine readable you may want
   to place it in a `yfm`_ section.

::

   >>> #! /usr/bin/zoo run
   ... # vim: ts=3:sw=3:syntax=zoo
   ... #
   ... # NOTE to myself: This module is empty.
   ...
   ... pass

Lines
-----

Lines are separated by a line feed
(U+000A) optionally preceeded by
a carriage return (U+000D) or
by any Unicode character in the
general categories Line Separator (Zl)
or Paragraph Separator (Zp).

.. note:: The extended Unicode characters
   are not accounted for in indentation
   computation and should therefore be
   avoided.

::

   _NL: (/\r\n|[\p{Zl}\p{Zp}\r\n]/ WS_INLINE? | SH_COMMENT)+

.. _names:
Names and Identifiers
---------------------

The rules for names correspond to
`UAX31`_ with the following restrictions:

- Names are case sensitive.
- No consecutive underscores are allowed.
- A leading underscore alters the default accessibility:
  * internal for namespaces
  * positional only for arguments
  * private in any other context
- Names must not coincide with any
  of the reversed words.

A name that consists of a single underscore
only has a special meaning depending on the
context:

- an anonymous symbol in a defining context,
- a wildcard in structural pattern matching,
- the argument in an abonymous function context.

It is recommended - though not enforced -
to stick to the following naming conventions:

- Use lower-case words separated by
  underscores (snake-case) for function, method,
  property, variable and argument names
  (e.g. ``first_element``).
- Use capitalized words with no
  underscores (Pascal-style) for
  class, interface, type, type parameter
  and namespace identifiers
  (e.g. ``MutableCollection``).
  Acronyms should be written with
  only the first letter capitalized
  (i.e. ``HttpSocket`` rather than
  ``HTTPSocket``).
- Use single letter identifiers only
  if the meaning is clear from the context
  (e.g. a mathematical formula, as loop variable, etc.).
- Exported (public) names should be in
  English and ASCII only.
- Whenever applicable, use the appropriate
  grammatical form:

  * Prefer nouns for classes.
    When implementing a pattern use the
    pattern name as part of the identifier.
  * Interfaces may be named by nouns
    or capabilities (Enumerable, Collapsible).
  * Pedicates should be preceeded by an
    auxilliary verb, such as: is, has, can, etc.
  * methods/functions characterized
    by their effect should be in
    imperative mood.
  * methods, functions, properties
    characterized by their result
    should either be named after the
    result (e.g. ``length``) or by
    a transformation (such as ``reversed``)
  * Avoid noisy prefixes such as ``get_``,
    ``compute_`` ans suffixes (e.g. ``Type``)
    if possible.

     >>> var first_entry = work_list.first
     ... class CustomerFactory
     ...    def create_customer as Customer
     ...       pass
     ...    def has_generated(customer as Customer) as Boolean
     ...       customer.creator == this

.. definitions

::

   NAME: /(\p{L}|\p{Nl}|\p{Other_ID_Start})(_?[\p{L}\p{Nl}\p{Other_ID_Start}\p{Mn}\p{Mc}\p{Nd}\p{Pc}\p{Other_ID_Continue}]+)*_?/
   PNAME: JOKER NAME
   JOKER: "_"

.. _reserved:
Reserved Words
--------------

::

   AND: "and"
   AS: "as"
   ASSERT: "assert"
   BREAK: "break"
   BUT: "but"
   BY: "by"
   CACHED: "cached"
   CASE: "case"
   CATCH: "catch"
   CLASS: "class"
   CONTINUE: "continue"
   CUE: "cue"
   DECREASING: "decreasing"
   DEF: "def"
   DEFER: "defer"
   DIV: "div"
   DOC: "doc"
   ELIF: "elif"
   ELSE: "else"
   ENSURES: "ensures"
   EVENT: "event"
   FORWARDER: "forwarder"
   GET: "get"
   IF: "if"
   IMMUTABLE: "immutable"
   IMPLEMENTS: "implements"
   IMPLIES: "implies"
   IN: "in"
   INHERITS: "inherits"
   INTERFACE: "interface"
   INTERNAL: "internal"
   INVARIANT: "invariant"
   IS: "is"
   MATCH: "match"
   MOD: "mod"
   NAMESPACE: "namespace"
   NEVER: "never"
   NEW: "new"
   NOT: "not"
   OBSOLETE: "obsolete"
   OLD: "old"
   OR: "or"
   PASS: "pass"
   PERMITS: "permits"
   PRIVATE: "private"
   PRO: "pro"
   PURE: "pure"
   PUBLIC: "public"
   REF: "ref"
   REQUIRES: "requires"
   RETURN: "return"
   SET: "set"
   SINGLETON: "singleton"
   STABLE: "stable"
   TEST: "test"
   THIS: "this"
   TODO: "todo"
   TRY: "try"
   TYPE: "type"
   UNLESS: "unless"
   UNSTABLE: "unstable"
   USE: "use"
   USING: "using"
   VALUE: "value"
   VAR: "var"
   WHERE: "where"
   WHEN: "when"
   WHILE: "while"
   XOR: "xor"

.. _literals:

Literals
--------

Integer Literals
~~~~~~~~~~~~~~~~

Currently, only decimal integer literals
are implemented. Underscores may be
inserted as separators for readability.

Furthermore, decimal digits in any
alphabet may be used.

   >>> var number = 1_000_000
   ... var thirty_nine = ೩೯

An optional metric or binary prefix
may be added to the literal:

   >>> assert 15k == 15_000
   ... assert 12Ki == 12_288 # == 12*1024

::

   int_literal: DECIMAL_INT_LITERAL

   DECIMAL_INT_LITERAL: /[-+]?\p{Nd}+(_\p{Nd}+)*(da|h|[kKMGTPEZYRQ]i?)?/



Floating Point Literals
~~~~~~~~~~~~~~~~~~~~~~~

Floating point literals must contain
a decimal point; an optional exponent
and a metric or binary prefix may be added.

   >>> var pi = 3.14_15
   ... var floppy_sizy = 1.44Mi

::

   float_literal: DECIMAL_FLOAT_LITERAL

   DECIMAL_FLOAT_LITERAL: /[-+]?\p{Nd}+(_\p{Nd}+)*\.(\p{Nd}+(_\p{Nd}+)*)?([eE][-+]?\p{Nd}+(_\p{Nd}+)*)?([qryzafpnμumcd]|da|h|[kKMGTPEZYRQ]i?)?/


Character Literals
~~~~~~~~~~~~~~~~~~

A character represents a `Unicode Scalar Value`_,
which is any Unicode code point except
high-surrogate and low-surrogate code points.
In other words, the ranges of integers
0 to D7FF<sub>16</sub> and
E000<sub>16</sub> to 10FFFF<sub>16</sub>
inclusive.

Character literals are delimited by
single quotes/apostrophes (``'``) and may be
represented by:

- the character itself (e.g. ``'Ē'``),
- the apostroph itself (``'''``)
- a backslash escape, i.e. one of
   * ``'\"'`` (double quote)
   * ``'\\'`` (literal backslash)
   * ``'\a'`` (audible bell, U+0007)
   * ``'\b'`` (backspace, U+0008)
   * ``'\e'`` (escape, U+001B)
   * ``'\f'`` (form feed, U+000C)
   * ``'\n'`` (line feed, U+000A)
   * ``'\r'`` (carriage return , U+000D)
   * ``'\t'`` (horizontal tab, U+0009)
   * ``'\v'`` (vertical tab, U+000B)   
- a mnemonic according to `RFC 1345`_ (e.g.``'E-'``),
- the hexadecimal codepoint value (e.g. ``'U+0112'),
- an emoji code (``':thumbsup:'``),
- a full unicode name (``'LATIN CAPITAL LETTER A WITH MACRON'``).

Character literals are normalized to
NFC if necessary.

  >>> var characters = [
  ...    'ß',
  ...    'ss',
  ...    'U+00DF',
  ...    'LATIN SMALL LETTER SHARP S',
  ...    ':croissant:',
  ...    '\\',
  ... ]

::

   char_literal: CHAR_LITERAL
   CHAR_LITERAL: /'([^'\\\n\r\p{Zl}\p{Zp}]+|\\['"\\abefnrtv]|')'/


String Literals
~~~~~~~~~~~~~~~

String literals are delimited by double
quotes and may be multiline literals.

If a line break is introduced in a string
literal the first non-space character
of the next line must be an ampersand
(``&``) or the closing delimiter. A
backslash (``\\``) as last character in
the line tells the compiler to ignore
the line break.

String interpolation is delimited by
``\\(`` and ``\\)``.

Backslash escapes are supported as
two letter escapes (e.g. ``"\\n"``)
and as character literal escapes.

   >>> var story = "
   ...    &Intro
   ...    &=====
   ...    &Bj\'o/'rn brought \
   ...    &a \':croissant:', said \(author\).
   ...    &\n\'HORIZONTAL ELLIPSIS'"

::

   STRING_LITERAL_QQ: "\"" ( /[^\\\"\n\r\p{Zl}\p{Zp}]/ | /\\[abefnrtv]/ | "\\" CHAR_LITERAL | /\\?\p{Zs}*(\r\n|[\p{Zl}\p{Zp}\r\n])\p{Zs}*&/ )* (/\\?\p{Zs}*(\r\n|[\p{Zl}\p{Zp}\r\n])\p{Zs}*/)? "\""
   STRING_LITERAL_BQ: "\\)" ( /[^\\\"\n\r\p{Zl}\p{Zp}]/ | /\\[abefnrtv]/ | "\\" CHAR_LITERAL | /\\?\p{Zs}*(\r\n|[\p{Zl}\p{Zp}\r\n])\p{Zs}*&/ )* (/\\?\p{Zs}*(\r\n|[\p{Zl}\p{Zp}\r\n])\p{Zs}*/)? "\""
   STRING_LITERAL_BB: "\\)" ( /[^\\\"\n\r\p{Zl}\p{Zp}]/ | /\\[abefnrtv]/ | "\\" CHAR_LITERAL | /\\?\p{Zs}*(\r\n|[\p{Zl}\p{Zp}\r\n])\p{Zs}*&/ )* (/\\?\p{Zs}*(\r\n|[\p{Zl}\p{Zp}\r\n])\p{Zs}*/)? "\\("
   STRING_LITERAL_QB: "\"" ( /[^\\\"\n\r\p{Zl}\p{Zp}]/ | /\\[abefnrtv]/ | "\\" CHAR_LITERAL | /\\?\p{Zs}*(\r\n|[\p{Zl}\p{Zp}\r\n])\p{Zs}*&/ )* (/\\?\p{Zs}*(\r\n|[\p{Zl}\p{Zp}\r\n])\p{Zs}*/)? "\\("

Raw String Literals
~~~~~~~~~~~~~~~~~~~

Raw string literals are delimited by
backticks (grave). A double backtick
must be used to produce a literal backtick
inside a raw string.
There are no further escapes defined inside
a raw string.

  >>> raw_stings = {
  ...    "regex": `3\.14\d*`,
  ...    "path": `C:\System\xyz.dll`,
  ...    "empty": ``,
  ...    "backticks": `see ``x```,
  ...    "multiline": `Shopping List:
  ...       & - milk
  ...       & - bread
  ...       & - flour
  ...       `
  ... }

::

   RAW_STRING_LITERAL: "`" ( /[^`\n\r\p{Zl}\p{Zp}]/ | "``" | /\p{Zs}*(\r\n|[\p{Zl}\p{Zp}\r\n])\p{Zs}*&/ )* (/\p{Zs}*(\r\n|[\p{Zl}\p{Zp}\r\n])\p{Zs}*/)? "`"

.. _yfm:

YAML Front Matter (YFM)
-----------------------

`YAML`_ Front Matter (YFM) should
be used to include program metadata,
such as version, license and authorship
information in a machine- and
human-readable way.

The YFM sections may also include
package manager data such as
dependencies (which would otherwise
be placed in a separate ``cage.yaml``
file) or other tool specific sections
(e.g. Citation File Format (`CFF`_)
or `publiccode.yml`_)

YFM sections start and end with
a line consisting of at least three
consecutive hyphens.

  >>> # Here comes meta data
  ... --------------------
  ... version: 1.0.6
  ... license-spdx: MIT
  ... ---
  ... pass

::

   YFM: /^-{3,}\s*\n[\s\S]*?^-{3,}\s*$/m

   yfm: YFM _NL

.. _doc:

Doc-Strings
-----------

While `comments`_ are ignored completely
by the compiler, doc-strings add explanations
to the ource code which are extracted into
developer documentation (alongside with
declarations, doc-tests and contracts).

Doc-strings look like normal string literals
preceded by the keyword ``doc``.

String interpolations may comprise
symbols only (``\(Symbol\)``) which are
converted to cross-references.

The doc-strings are interpreted as
markdown documents (CommonMark)
with some extensions. Issue numbers
(by hash-tag), pull-/merge-requests
(by exclamation mark), at-mentions
are resolved if the issue-tracker
and SCM are configured.

::

   doc: DOC STRING_LITERAL_QQ _NL
      | DOC STRING_LITERAL_QB symbol_ref _doc_tail

   _doc_tail: STRING_LITERAL_BQ _NL
      | STRING_LITERAL_BB symbol_ref _doc_tail 

   symbol: NAME | PNAME
   symbol_ref: symbol
      | symbol_ref "." symbol


Modules
=======
The source code in ZOO is organized
in module files. One or more module files
in a common directory structure build
a package which may comprise a library
and/or one or more executable programs.
(You may also have a package defining
only tests, e.g. for integration testing
for multiple packages.)

Module file names are expected to have
the suffix ``.zoo``.

::

   ?start: module

Module Structure
----------------

Modules may consist of up to three
sections, each of which may be missing.
The sections must appear in the given
order:

 1. A module header comprising
    module `doc-strings<doc>`_ and/or
    YAML Front Matter (`YFM<yfm>`_),
 2. Definitions and declarations,
 3. A main `program`_ script.

An empty file is a valid module.

::

   module: _NL? _module_unit executable? _NL*
      | _NL? executable _NL*


   _module_unit: module_head _unit?
      | _unit

Module Head
-----------

The module head may comprise
an alternating series of doc-strings
and YFM. Any YFM section following a
doc-string becomes part of the documentation.

   >>> # Comments at the beginning
   ... # may provide a shebang line,
   ... # license headers and editor
   ... # settings.
   ... ---
   ... boring_hash: 0x14af5b7033bb9c
   ... ---
   ... doc "# The ACME Library."
   ... ---
   ... keywords:
   ... - GUI
   ... - reactive
   ... ---
   ... pass

In the above example, the keywords
would be part of the documentation
while ``boring_hash`` won't.

::

   ?module_head:
      | _module_head_doc
      | _module_head_yfm

   _module_head_doc: doc
      | _module_head_yfm doc
   _module_head_yfm: yfm
      | _module_head_doc yfm

Accessibility Rules
-------------------

ZOO distinguishes three levels of
access to defined entities:

public
   accessible without any restriction
   from any package, corresponds
   to a package export

internal
   accessible from all module files
   within the same package but not
   from other packages

private
   accessible only from within
   the same module file

The accessibility level is determined
by the accessibility of the surrounding
scope (namespace or class), the name
and explicit attributes:

- The accessibility can never be higher
  and by default is equal to the accessibility
  of the containing scope.
- If the accessibility is declared by an
  annotation, and not wider than the
  accessibility of the scope,
  no further rules apply.
- If the definition is not contained
  in any namespace or in a namespace
  containing a name part starting with
  an underscore, the maximum accessibility
  is internal.
- If the definition is contained in
  the (pseudo-)namespace called ``_``
  the accessibility is private.
- If the definition is not
  a namespace declaration and the defined
  name starts with an underscore the
  accessibility is set to private
  by defult (may be altered by an
  annotation). 

::

   public: PUBLIC
   internal: INTERNAL
   private: PRIVATE


Module Definitions and Declarations
-----------------------------------

Modules may access external definitions
and add new definitions to different
namespaces. Possible declarations
and definitions comprise:

- namespaces (new or existing),
- class declarations,
- interface declarations,
- type aliases
- (global) variables/fields
- property declarations
- test definitions
- cue definitions
- event declarations
- function declarations.

::

   _unit: use_directive+ _unit_feature*
      | _unit_feature+

   _unit_feature: namespace_decl
      | class_def
      | interface_def
      | type_def
      | var_field_decl
      | property_decl
      | test_decl
      | cue_decl
      | event_decl
      | method_decl


Namespaces
----------

Namespaces are used to avoid name collissions
and to structure groups of definitions
into logically and semantically coherent
hierarchies.

Namespaces have dotted names, e.g.
``System.Net.Http``, and may be nested;
The effective fully qualified name
is computed by concatenating the
name of the outer namespace with the
name of the inner namespace separated
by a dot.

   >>> namespace Extra.Net.Http
   ...    class Server
   ...       pass
   ...
   ... namespace Extra.Net
   ...    namespace Http
   ...       class Client
   ...          pass

In the above example both classes
exist in the same namespace
``Extra.Net.Http``; their fully
qualified names are
``Extra.Net.Http.Server`` and
``Extra.Net.Http.Client``.

Multiple packages may define symbols
in the same namespace. Redefining a
symbol with the same fully qualified
name within the same range of visibility
will, however, result in an error.


::

   namespace_decl: NAMESPACE ns_id _NL _INDENT _unit _DEDENT

   ns_id: PNAME
      | JOKER
      | NAME
      | ns_id "." NAME

Use Directive
-------------

Having to use the fully qualified name
everywhere would lead to quite verbous
source code. Therefore the ``use``
directive allows to make the contents
of a namespace visible without the need
to prefix each symbol by the namespace
id.

   >>> use Extra.Net.Http
   ... server = Server(8080)

In its second form the use statement
locally introduces an abbreviation for
the given namespace:

   >>> use xhttp = Extra.Net.Http
   ... server = xhttp.Server(8080)

This form is especially useful if simply
using several namespaces would lead to
name clashes.

::

   use_directive: USE ns_alias? ns_id _NL

   ns_alias: ns_id "="

.. _program:
Programs
--------

Programs can be defined in several
ways:

- as executable code block at the end
  of a module,
- as a `cue`_ called ``main`` at
  the module level,
- as a `cue`_ called ``main``
  inside a class.

To run or compile a program the corresponding
module (file name) or class (fully qualified class name)
must be specified.

::

   executable: block


Features
========

.. _contract:
Contracts
---------

ZOO defines four kinds of contracts:

Preconditions
   denote predicates that are
   *required* to be true immediately
   before a method, function, property
   or cue is run. Overwriting may
   weaken preconditions but never
   enforce stronger constraints.
   A failing precondition is blamed
   to the caller (i.e. indicates a bug
   in the calling code). Every statement
   in a precondition must evaluate to a
   Boolean value.
Postconditions
   denote predicates that are
   *ensured* to be true immediately
   before a method, function, property
   or cue returns. Overwriting may only
   add constraints, postconditions are
   never weakened. A failing postcondition
   is blamed to the invoked code.
   Every statement in a postconditon
   must evaluate to a Boolean value
   or to a function mapping the result
   of the enclosing function to a
   Boolean value. Postconditions my use
   old-expressions to refer to values
   before the function evaluation
Invariants
   denote expressions that must
   evaluate to the same value before
   and at the end of an invokation.
   Invariants may be declared at the
   class or interface level applying
   to all methods, properties and cues
   of the class or all implementations
   of the interface.
   Invariants may be declared in a loop
   in which case they must hold before
   and after each iteration.
Variants
   denote expressions that must
   be *decreasing*, i.e. whose type
   ensures an ordering, a lower bound
   and is inductively generated
   (currently only non-negative integers).
   Variants are checked at every recursion step
   if attached to a recursive function,
   and at each iteration if attached to a
   loop.

Contracts are lways run inside tests
but can be turned off in production
runs for performance reasons.

   >>> def factorial(x as Integer) as Integer
   ...    is pure, immutable, cached
   ...    doc "Compute the factorial of \(x\)."
   ...    requires x >= 0
   ...    ensures
   ...       doc "the factorial of \(x\)
   ...       & is never smaller than \(x\)."
   ...       _ >= x
   ...    decreasing x
   ...    return if x > 1
   ...       x * factorial(x - 1)
   ...    else
   ...       1
   ...

.. end
::

   requires_contract: REQUIRES _contract_impl
   ensures_contract: ENSURES _contract_impl
   invariant: INVARIANT _contract_impl
   decreases: DECREASING _contract_impl

   _contract_impl: expr_stmt
      | _NL _INDENT _expr_block _DEDENT

   _expr_block: doc expr_stmt*
      | expr_stmt+
      | _pass


.. _mutability:
Mutability and Side-Effects
---------------------------

::


.. _maturity:
Maturity
--------

.. _class:
Classes
-------

.. _interface:
Interfaces
----------

.. _alias:
Type Aliases
------------

.. _field:
Fields and Global Variables
---------------------------

.. _function:
Functions
---------

.. _cue:
Cues
----

.. _property:
Properties
----------

.. _event:
Events
------

.. _test:
Tests
-----


::


   class_def: CLASS class_name type_params? _cons_param_list? _NL _INDENT _class_body _DEDENT
   interface_def: INTERFACE interface_name type_params? _NL _INDENT _iface_body _DEDENT

   class_name: NAME | PNAME
   interface_name: NAME | PNAME

   _cons_param_list: param_list

   _class_body: _class_head _class_feature* executable?
      | _class_feature+ executable?
      | executable

   _iface_body: _iface_head _iface_feature*
      | _iface_feature+ 

   _class_head: doc
      | _class_head_element+ doc?

   _iface_head: doc
      | _iface_head_element+ doc?

   _class_head_element: class_is_clause
      | where_clause
      | _implements_clauses
      | forwarder_clause
      | requires_contract
      | ensures_contract

   _iface_head_element: iface_is_clause
      | where_clause
      | inherits_clause

   inherits_clause: INHERITS type_expr ("," type_expr)* _NL

   class_is_clause: IS _class_attrib ("," _class_attrib)* _NL
   _class_attrib: obsolete
      | stable
      | unstable
      | public
      | private
      | internal
      | singleton
      | pure
      | immutable
      | attribute_expr

   iface_is_clause: IS _iface_attr ("," _iface_attr)* _NL
   _iface_attr: obsolete
      | stable
      | unstable
      | public
      | private
      | internal
      | pure
      | attribute_expr
      | type_def

   type_params: "[" NAME ("," NAME)* "]"

   where_clause: WHERE NAME _generic_constraint _NL

   _generic_constraint: generic_implements
      | generic_permits
      | generic_is

   generic_implements: IMPLEMENTS type_expr
   generic_permits: PERMITS type_expr
   generic_is: IS _generic_class_attrib

   _generic_class_attrib: pure
      | immutable
      | singleton
      | attribute_expr

   _implements_clauses: IMPLEMENTS implements_clause ("," implements_clause)* _NL
   implements_clause: type_expr _per_clause?

   forwarder_clause: FORWARDER _generic_constraint _NL

   permits_clause: PERMITS symbol_ref ("," symbol_ref)* _NL

   _class_feature: invariant
      | var_field_decl
      | property_decl
      | test_decl
      | cue_decl
      | event_decl
      | method_decl
      | type_def

   _iface_feature: _abstract_property
      | abstract_method
      | abstract_cue
      | abstract_event
      | _pass

   _abstract_property: abstract_full_pro
      | abstract_getter
      | abstract_setter

   _abstract_body: _method_contracts+
      | doc _method_contracts*

   abstract_full_pro: PRO pro_name type_annotation _NL (_INDENT _ap_head _DEDENT)?
   abstract_getter: GET pro_name type_annotation _NL (_INDENT _ap_head _DEDENT)?
   abstract_setter: SET pro_name type_annotation _NL (_INDENT _ap_head _DEDENT)?

   _ap_head: ap_is_clause+ _abstract_body?
      | _abstract_body
   ap_is_clause: IS _ap_attr ("," _ap_attr)* _NL
   _ap_attr: obsolete
      | stable
      | unstable
      | pure
      | immutable
      | attr_expr

   abstract_method: DEF method_name type_params? param_list? type_annotation? _NL (_INDENT _am_head _DEDENT)?
   _am_head: am_is_clause+ _abstract_body?
      | _abstract_body
   am_is_clause: IS _am_attr ("," _am_attr)* _NL
   _am_attr: obsolete
      | stable
      | unstable
      | pure
      | immutable
      | attr_expr


   abstract_cue: CUE cue_name type_params? param_list? type_annotation? _NL (_INDENT _ac_head _DEDENT)?
   _ac_head: ac_is_clause+ _abstract_body?
      | _abstract_body
   ac_is_clause: IS _ac_attr ("," _ac_attr)* _NL
   _ac_attr: obsolete
      | stable
      | unstable
      | pure
      | immutable
      | attr_expr 

   abstract_event: EVENT event_name type_params? param_list? _NL (_INDENT _ae_head _DEDENT)?
   _ae_head: ae_is_clause+ _abstract_body?
      | _abstract_body
   ae_is_clause: IS _ae_attr ("," _ae_attr)* _NL
   _ae_attr: obsolete
      | stable
      | unstable
      | pure
      | immutable
      | attr_expr

   var_field_decl: VAR var_name type_annotation? initializer? _NL (_INDENT _var_head _DEDENT)?

   _var_head: doc
      | _var_head_element+ doc?

   _var_head_element: var_is_clause

   var_is_clause: IS _var_attr ("," _var_attr)* _NL

   _var_attr: private
      | public
      | internal
      | immutable
      | attribute_expr
      | obsolete
      | stable
      | unstable

   var_name: NAME | PNAME

   initializer: "=" inline_expr

   property_decl: _full_property_decl
      | _getter_only_decl
      | _setter_only_decl

   _full_property_decl: PRO pro_name type_annotation? _pro_impl
   _getter_only_decl: GET pro_name type_annotation? _xet_impl
   _setter_only_decl: SET pro_name type_annotation? _xet_impl
   pro_name: NAME
      | PNAME
      | param_list
   _pro_impl: _per_clause _NL (_INDENT _pro_head _DEDENT)?
      | _NL _INDENT _pro_body _DEDENT
   _xet_impl: _per_clause _NL (_INDENT _pro_head _DEDENT)?
      | _NL _INDENT _xet_body _DEDENT
   _pro_head: _pro_head_element+ doc? test_decl*
      | doc test_decl*
      | test_decl+
   _pro_head_element: pro_is_clause

   pro_is_clause: IS _pro_attr ("," _pro_attr)* _NL
   _pro_attr: obsolete
      | stable
      | unstable
      | private
      | public
      | internal
      | pure
      | immutable
      | cached
      | attr_expr

   _pro_body: _pro_head? getter_impl? setter_impl
      | _pro_head setter_impl? getter_impl
   _xet_body: _pro_head? _xet_impl_body
   _xet_impl_body: _method_contracts+ block?
      | block

   setter_impl: SET _NL _INDENT _xet_impl_body _DEDENT

   getter_impl: GET _NL _INDENT _xet_impl_body _DEDENT

   _per_clause: BY (VAR | var_name)

   test_decl: TEST (doc | _NL) _INDENT _test_contents _DEDENT
   _test_contents: _test_head_element+ block?
       | block

   _test_head_element: test_is_clause
      | test_param_spec

   test_is_clause: IS _test_attr ("," _test_attr)* _NL
   _test_attr: attr_expr

   test_param_spec: VAR test_param ("," test_param)* _test_param_initializer
   test_param: var_name type_annotation?
      | JOKER
   _test_param_initializer: test_param_generator
      | test_param_setter
      | _NL _INDENT block _DEDENT
   test_param_setter: "=" inline_expr _NL
   test_param_generator: IN inline_expr _NL

   cue_decl: CUE cue_name type_params? param_list? type_annotation? _NL _INDENT _cue_contents _DEDENT
   _cue_contents: _cue_head block?
      | block

   _cue_head: _cue_head_element+ doc? _method_contracts* test_decl*
      | doc _method_contracts* test_decl*
      | _method_contracts+ test_decl*
      | test_decl+

   _cue_head_element: cue_is_clause

   cue_is_clause: IS _cue_attrib ("," _cue_attrib)*
   _cue_attrib: pure
      | attribute_expr
      | obsolete
      | stable
      | unstable
      | cached

   cue_name: NAME

   event_decl: EVENT event_name type_params? param_list? _NL (_INDENT _event_head _DEDENT)?

   event_name: NAME | PNAME
   _event_head: event_is_clause+ doc?
      | doc
   event_is_clause: IS _event_attrib ("," _event_attrib)* _NL
   _event_attrib: obsolete
      | stable
      | unstable
      | public
      | private
      | internal
      | attribute_expr


   method_decl: DEF method_name type_params? param_list? type_annotation? _NL _INDENT _method_contents _DEDENT
   method_name: NAME | PNAME
   _method_contents: _method_head _method_contracts* test_decl* block?
      | _method_contracts+ test_decl* block?
      | test_decl+ block?
      | block
   _method_head: _method_head_element+ doc?
      | doc
   _method_head_element: method_is_clause
      | where_clause
   method_is_clause: IS _method_attrib ("," _method_attrib)* _NL
   _method_attrib: pure
      | immutable
      | obsolete
      | stable
      | unstable
      | public
      | private
      | internal
      | cached
      | attribute_expr

   _method_contracts: requires_contract
      | ensures_contract
      | invariant
      | decreases


   param_list: "(" formal_args? ")"

   formal_args: formal_arg ("," formal_arg)* ","?
   formal_arg: arg_name type_annotation? initializer?
   arg_name: NAME | PNAME | JOKER

   block: statement+

   body_block: body_contract* statement+

   body_contract: decreases
      | invariant
      | requires_contract
      | ensures_contract

   statement: _pass
      | expr_stmt
      | assertion
      | defer_stmt
      | break_stmt
      | continue_stmt
      | return_stmt

   assertion: ASSERT inline_expr _NL (_INDENT doc _DEDENT)?
   break_stmt: _jump_cond? BREAK (rhs |_NL)
   continue_stmt: _jump_cond? CONTINUE _NL
   return_stmt: _jump_cond? RETURN (rhs | _NL)

   _jump_cond: when_clause
      | unless_clause

   when_clause: WHEN inline_expr
   unless_clause: UNLESS inline_expr

   defer_stmt: _jump_cond? DEFER _NL (_INDENT block _DEDENT)?

   expr_stmt: (lhs assign_op)* rhs

   rhs: (inline_expr ",")* _last_expr
   _last_expr: expr_with_body
      | object_init
      | if_expr
      | while_expr
      | match_expr

   lhs: (assignable ",")* assignable
   assignable: inline_expr
      | var_name type_annotation
      | NEW var_name

   expr_with_body: inline_expr lambda_args? _NL (_INDENT body_block _DEDENT)?
   object_init: inline_expr BUT _NL _INDENT body_block _DEDENT   
   if_expr: IF inline_expr _NL _INDENT block _DEDENT elif_clause* else_clause?
   while_expr: WHILE inline_expr _NL _INDENT body_block _DEDENT else_clause?
   match_expr: MATCH inline_expr ("," inline_expr)* ","? _NL _INDENT case_clause+ else_clause? _DEDENT
   elif_clause: ELIF inline_expr _NL _INDENT body_block _DEDENT
   else_clause: ELSE  _NL _INDENT body_block _DEDENT
   case_clause: CASE pattern guard? _NL _INDENT body_block _DEDENT

   guard: _jump_cond
   lambda_args: "|" formal_args? "|"
   inline_args: ("|" formal_args?)? PIPE

Operator Precedence
-------------------

- assignment
- tuple composition: ``,``
- pipe ``|>`` (infix)
- bind parameter ``<|`` (infix)
- function context ``| ... |>`` (prefix)
- logic: ``and``, ``or``, ``or else``, ``xor``, ``not``
- membership: ``in``
- comparison: ``==``, ``<=``, ``>=``, ``<>``
- additive ``+``, ``-``
- multiplicative ``*``, ``/``, ``div``, ``mod``; prefix sign ``+``, ``-``
- power ``^``
- ``try``, ``catch``
- ``ref``, ``old``
- subscription ``.``, ``?.`` and call ``()``

::

   inline_expr: pipe_expr

   ?pipe_expr: bind_expr
      | pipe_expr PIPE bind_expr

   ?bind_expr: lambda_expr
      | bind_expr EPIP lambda_expr

   ?lambda_expr: implies_expr
      | inline_args implies_expr

   ?implies_expr: logic_expr (IMPLIES logic_expr)*

   ?logic_expr: logic_prefix_expr
      | logic_expr logic_op logic_prefix_expr

   ?logic_prefix_expr: membership_expr
      | logic_op logic_prefix_expr

   logic_op: AND
      | OR
      | XOR
      | NOT

   ?membership_expr: comparison_expr (NOT? IN comparison_expr)?

   ?comparison_expr: additive_expr (comp_op additive_expr)*
   comp_op: EQ | NEQ | LT | LEQ | GT | GEQ

   ?additive_expr: multiplicative_expr
      | additive_expr additive_op multiplicative_expr
   additive_op: PLUS_OP
      | MINUS_OP

   ?multiplicative_expr: factor_expr
      | multiplicative_expr multiplicative_op factor_expr
   multiplicative_op: AST
      | SLASH
      | DIV
      | MOD

   ?factor_expr: sign? _error_handler_expr exponent?

   sign: PLUS_OP | MINUS_OP

   exponent: "^" sign? _error_handler_expr  

   _error_handler_expr: _atomic_expr
      | try_expr
      | catch_expr

   try_expr: TRY _atomic_expr

   catch_expr: _atomic_expr CATCH _atomic_expr

   _atomic_expr: never
      | todo
      | ref_expr
      | call_expr
      | old_expr

   ?call_expr: subscript_expr
      | call_expr "?"? actual_params

   ref_expr: REF subscript_expr
   old_expr: OLD subscript_expr

   ?subscript_expr: subscript_expr subscript_operator method_name
      | _subscribable_expr

   _subscribable_expr: "(" inline_expr ")"
      | tuple_expr
      | map_expr
      | list_expr
      | string_interpolation
      | string_literal
      | int_literal
      | float_literal
      | char_literal
      | named_ref

   subscript_operator: SUBS
      | SUBS_MAYBE

   named_ref: NAME
      | PNAME
      | JOKER
      | value
      | THIS

   value: VALUE

   never: NEVER
   todo: TODO

   string_literal: STRING_LITERAL_QQ
      | RAW_STRING_LITERAL

   string_interpolation: STRING_LITERAL_QB inline_expr (STRING_LITERAL_BB inline_expr)* STRING_LITERAL_BQ
   list_expr: LSQB (_simple_entry ("," _simple_entry)* ","?)? RSQB
   map_expr: "{" (_map_entry ("," _map_entry)* ","?)? "}"
   tuple_expr: "(" (inline_expr "," (inline_expr ",")* inline_expr?)? ")"

   _simple_entry: inline_expr _jump_cond?
      | flatten_simple _jump_cond?
   flatten_simple: AST _simple_entry

   _map_entry: dict_entry _jump_cond?
      | flatten_simple _jump_cond?
   dict_entry: inline_expr ":" inline_expr

   assign_op: (AND | OR | DIV | MOD )? ASSIGN
      | ALTER

   pattern: open_sequence_pattern
      | comb_pattern

   open_sequence_pattern: (comb_pattern ",")+ comb_pattern?

   ?comb_pattern: binding_pattern
      | comb_pattern logic_op binding_pattern
   ?binding_pattern: _closed_pattern ("as" pattern_name)?
      | pattern_name pattern_limits?
      | pattern_limits
   _closed_pattern: object_pattern
      | literal_pattern
      | stream_pattern
      | mapping_pattern
      | any_pattern
      | "(" pattern ")"

   pattern_limits: pattern_limit_op inline_expr
   pattern_limit_op: EQ
      | NEQ
      | LT
      | GT
      | LEQ
      | GEQ
      | IN
      | NOT IN

   literal_pattern: int_literal
      | float_literal
      | char_literal
      | string_pattern

   string_pattern: STRING_LITERAL_QQ
      | STRING_LITERAL_QB pattern_name string_pattern_tail
   string_pattern_tail: STRING_LITERAL_BQ
      | STRING_LITERAL_BB pattern_name string_pattern_tail

   stream_pattern: LSQB (_stream_pat_entry ("," _stream_pat_entry)* ","?)? RSQB

   _stream_pat_entry: comb_pattern
      | ast_pattern

   ast_pattern: AST comb_pattern

   mapping_pattern: "{" (_map_pattern_entry ("," _map_pattern_entry)* ","?)? "}"
   _map_pattern_entry: key_value_pattern
      | ast_pattern
   key_value_pattern: inline_expr ":" comb_pattern

   object_pattern: class_denoter "(" pattern? ")"

   class_denoter: NAME
      | PNAME SUBS (NAME | PNAME) 
      | class_denoter "." (NAME | PNAME)

   any_pattern: JOKER

   pattern_name: PNAME

   type_def: TYPE type_name type_params? formal_args? type_annotation _NL (_INDENT _type_head _DEDENT)?
   type_name: NAME | PNAME
   _type_head: doc
      | _type_head_element+ doc?

   _type_head_element: type_is_clause
      | where_clause
      | requires_contract
      | ensures_contract

   type_is_clause: IS _type_attr ("," _type_attr)*

   _type_attr: public
      | private
      | internal
      | stable
      | unstable
      | obsolete
      | pure
      | immutable

   type_expr: type_combination

   ?type_combination: type_product
      | type_combination type_com type_product

   type_com: AND
      | OR

   ?type_product: type_factor
      | type_product type_op type_factor

   type_op: AST | SLASH

   ?type_factor: result_type type_exponent?

   type_exponent: "^" sign? int_literal (SLASH int_literal)?

   ?result_type: postfix_type EXCLAM postfix_type
      | EXCLAM postfix_type
      | postfix_type
   ?postfix_type: _simple_type
      | postfix_type type_postfix

   type_postfix: AST | OPT

   _simple_type: named_type
      | tuple_type

   named_type: symbol_ref actual_type_params?

   actual_type_params: "[" type_param ("," type_param)* ","? "]"
   type_param: AST
      | variance_spec? type_expr
   variance_spec: PLUS_OP | MINUS_OP

   tuple_type: "(" type_expr "," (type_expr ",")* type_expr? ")"

   actual_params: "(" (actual_param ("," actual_param)* ","?)? ")"
   actual_param: inline_expr
      | NAME "=" inline_expr

   attr_expr: attr_name actual_params?
   attr_name: NAME | PNAME

   type_annotation: AS type_expr

   _pass: PASS _NL?

   attribute_expr: NAME

   unstable: UNSTABLE
   stable: STABLE
   obsolete: OBSOLETE STRING_LITERAL_QQ?

   singleton: SINGLETON
   pure: PURE AST?
   immutable: IMMUTABLE AST?
   cached: CACHED



   AST: "*"
   OPT: "?"


   ASSIGN: "="
   ALTER: "+=" | "-=" | "*=" | "/=" | "^="


   PLUS_OP: "+"
   MINUS_OP: "-"
   SLASH: "/"
   EQ: "=="
   NEQ: "<>"
   LT: "<"
   LEQ: "<="
   GT: ">"
   GEQ: ">="
   PIPE: "|>"
   EPIP: "<|"

   SUBS: "."
   SUBS_MAYBE: "?."

   EXCLAM: "!"

   LSQB: "["
   RSQB: "]"

.. rubric:: Citations

.. [Viega1998] John Viega, Bill Tutt, and Reimer Behrends.
   1998. Automated Delegation is a Viable Alternative to Multiple Inheritance in Class Based Languages.
   Technical Report. University of Virginia, USA.

.. _YAML: https://yaml.org
.. _CFF: https://citation-file-format.github.io/
.. _publiccode.yml: https://yml.publiccode.tools/
.. _Unicode Scalar Value: https://www.unicode.org/glossary/#unicode_scalar_value
.. _RFC 1345: https://datatracker.ietf.org/doc/html/rfc1345
.. _UAX31: https://www.unicode.org/reports/tr31/