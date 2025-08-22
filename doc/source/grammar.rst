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
  in a ``package.yaml``
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

::

   int_literal: DECIMAL_INT_LITERAL

   DECIMAL_INT_LITERAL: /[-+]?\p{Nd}+(_\p{Nd}+)*/



Floating Point Literals
~~~~~~~~~~~~~~~~~~~~~~~

TODO

Character Literals
~~~~~~~~~~~~~~~~~~

::

   CHAR_LITERAL: /'([^'\\\n\r\p{Zl}\p{Zp}]+|\\[^\n\r\p{Zl}\p{Zp}])'/


String Literals
~~~~~~~~~~~~~~~

::

   STRING_LITERAL_QQ: "\"" ( /[^\\\"\n\r\p{Zl}\p{Zp}]/ | /\\[Nbfnrtv]/ | "\\" CHAR_LITERAL | /\\?\p{Zs}*(\r\n|[\p{Zl}\p{Zp}\r\n])\p{Zs}*&/ )* (/\\?\p{Zs}*(\r\n|[\p{Zl}\p{Zp}\r\n])\p{Zs}*/)? "\""
   STRING_LITERAL_BQ: "\\)" ( /[^\\\"\n\r\p{Zl}\p{Zp}]/ | /\\[Nbfnrtv]/ | "\\" CHAR_LITERAL | /\\?\p{Zs}*(\r\n|[\p{Zl}\p{Zp}\r\n])\p{Zs}*&/ )* (/\\?\p{Zs}*(\r\n|[\p{Zl}\p{Zp}\r\n])\p{Zs}*/)? "\""
   STRING_LITERAL_BB: "\\)" ( /[^\\\"\n\r\p{Zl}\p{Zp}]/ | /\\[Nbfnrtv]/ | "\\" CHAR_LITERAL | /\\?\p{Zs}*(\r\n|[\p{Zl}\p{Zp}\r\n])\p{Zs}*&/ )* (/\\?\p{Zs}*(\r\n|[\p{Zl}\p{Zp}\r\n])\p{Zs}*/)? "\\("
   STRING_LITERAL_QB: "\"" ( /[^\\\"\n\r\p{Zl}\p{Zp}]/ | /\\[Nbfnrtv]/ | "\\" CHAR_LITERAL | /\\?\p{Zs}*(\r\n|[\p{Zl}\p{Zp}\r\n])\p{Zs}*&/ )* (/\\?\p{Zs}*(\r\n|[\p{Zl}\p{Zp}\r\n])\p{Zs}*/)? "\\("


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
be placed in a separate ``package.yaml``
file) or other tool specific sections
(e.g. Citation File Format (`CFF`_)
or `publiccode.yml`_)

YFM sections start and end with
a line consisting of at least three
consecutive hyphens.

  >>> # Here comes meta data
  ... ---
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



::

   doc: "doc" STRING_LITERAL_QQ _NL
      | "doc" STRING_LITERAL_QB symbol_ref _doc_tail

   _doc_tail: STRING_LITERAL_BQ _NL
      | STRING_LITERAL_BB symbol_ref _doc_tail 

   symbol_ref: NAME | PNAME


Modules
=======
The code is organized in modules.
A module should correspond to a file.
Module file names are expected to have
the suffix ``.zoo``.

   >>> use system.io
   ... use system.net.http

::

   ?start: module

   module: _NL? _module_unit constructor? _NL*

   _module_unit: module_head _unit

   _common_unit: _common_head _unit

   ?module_head:
      | _module_head_doc
      | _module_head_yfm

   _module_head_doc: doc
      | _module_head_yfm doc
   _module_head_yfm: yfm
      | _module_head_doc yfm

   _common_head: doc?


   _unit: use_directive+ _unit_feature*
      | _unit_feature+


   use_directive: "use" ns_alias? ns_id ("from" library_name)? _NL

   library_name: NAME | STRING_LITERAL_QQ

   ns_alias: ns_id "="

   namespace_decl: "namespace" ns_id _NL _INDENT _common_unit _DEDENT

   ns_id: PNAME
      | JOKER
      | NAME
      | ns_id "." NAME


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
      | _pass

   class_def: "class" class_name type_params? _cons_param_list? _NL _INDENT _class_body _DEDENT
   interface_def: "interface" interface_name type_params? _NL _INDENT _iface_body _DEDENT

   class_name: NAME | PNAME
   interface_name: NAME | PNAME

   _cons_param_list: param_list
      | default_param_list

A default parameter list ``(*)``
specifies that the list of parameters
should be generated from all field
variables

::

   default_param_list: "(" AST ")"

   _class_body: _class_head _class_feature* constructor?
      | _class_feature+ constructor?
      | constructor

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

   inherits_clause: "inherits" type_expr ("," type_expr)* _NL

   class_is_clause: "is" _class_attrib ("," _class_attrib)* _NL
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

   iface_is_clause: "is" _iface_attr ("," _iface_attr)* _NL
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

   where_clause: "where" NAME _generic_constraint _NL

   _generic_constraint: generic_implements
      | generic_permits
      | generic_is

   generic_implements: "implements" type_expr
   generic_permits: "permits" type_expr
   generic_is: "is" _generic_class_attrib

   _generic_class_attrib: pure
      | immutable
      | singleton
      | attribute_expr

   _implements_clauses: "implements" implements_clause ("," implements_clause)* _NL
   implements_clause: type_expr _per_clause?

   forwarder_clause: "forwarder" _generic_constraint _NL

   permits_clause: "permits" symbol_ref ("," symbol_ref)* _NL

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

   abstract_full_pro: "pro" pro_name type_annotation _NL (_INDENT _ap_head _DEDENT)?
   abstract_getter: "get" pro_name type_annotation _NL (_INDENT _ap_head _DEDENT)?
   abstract_setter: "set" pro_name type_annotation _NL (_INDENT _ap_head _DEDENT)?

   _ap_head: ap_is_clause+ _abstract_body?
      | _abstract_body
   ap_is_clause: "is" _ap_attr ("," _ap_attr)* _NL
   _ap_attr: obsolete
      | stable
      | unstable
      | pure
      | immutable
      | attr_expr

   abstract_method: "def" method_name type_params? param_list? type_annotation? _NL (_INDENT _am_head _DEDENT)?
   _am_head: am_is_clause+ _abstract_body?
      | _abstract_body
   am_is_clause: "is" _am_attr ("," _am_attr)* _NL
   _am_attr: obsolete
      | stable
      | unstable
      | pure
      | immutable
      | attr_expr


   abstract_cue: "cue" cue_name type_params? param_list? type_annotation? _NL (_INDENT _ac_head _DEDENT)?
   _ac_head: ac_is_clause+ _abstract_body?
      | _abstract_body
   ac_is_clause: "is" _ac_attr ("," _ac_attr)* _NL
   _ac_attr: obsolete
      | stable
      | unstable
      | pure
      | immutable
      | attr_expr 

   abstract_event: "event" event_name type_params? param_list? _NL (_INDENT _ae_head _DEDENT)?
   _ae_head: ae_is_clause+ _abstract_body?
      | _abstract_body
   ae_is_clause: "is" _ae_attr ("," _ae_attr)* _NL
   _ae_attr: obsolete
      | stable
      | unstable
      | pure
      | immutable
      | attr_expr

   var_field_decl: "var" var_name type_annotation? initializer? _NL (_INDENT _var_head _DEDENT)?

   _var_head: doc
      | _var_head_element+ doc?

   _var_head_element: var_is_clause

   var_is_clause: "is" _var_attr ("," _var_attr)* _NL

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

   _full_property_decl: "pro" pro_name type_annotation? _pro_impl
   _getter_only_decl: "get" pro_name type_annotation? _xet_impl
   _setter_only_decl: "set" pro_name type_annotation? _xet_impl
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

   pro_is_clause: "is" _pro_attr ("," _pro_attr)* _NL
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

   setter_impl: "set" _NL _INDENT _xet_impl_body _DEDENT

   getter_impl: "get" _NL _INDENT _xet_impl_body _DEDENT

   _per_clause: "per" ("var" | var_name)

   test_decl: "test" (doc | _NL) _INDENT _test_contents _DEDENT
   _test_contents: _test_head_element+ block?
       | block

   _test_head_element: test_is_clause
      | test_param_spec

   test_is_clause: "is" _test_attr ("," _test_attr)* _NL
   _test_attr: attr_expr

   test_param_spec: "var" test_param ("," test_param)* _test_param_initializer
   test_param: var_name type_annotation?
      | JOKER
   _test_param_initializer: test_param_generator
      | test_param_setter
      | _NL _INDENT block _DEDENT
   test_param_setter: "=" inline_expr _NL
   test_param_generator: "in" inline_expr _NL

   cue_decl: "cue" cue_name type_params? param_list? type_annotation? _NL _INDENT _cue_contents _DEDENT
   _cue_contents: _cue_head block?
      | block

   _cue_head: _cue_head_element+ doc? _method_contracts* test_decl*
      | doc _method_contracts* test_decl*
      | _method_contracts+ test_decl*
      | test_decl+

   _cue_head_element: cue_is_clause

   cue_is_clause: "is" _cue_attrib ("," _cue_attrib)*
   _cue_attrib: pure
      | attribute_expr
      | obsolete
      | stable
      | unstable
      | cached

   cue_name: NAME

   event_decl: "event" event_name type_params? param_list? _NL (_INDENT _event_head _DEDENT)?

   event_name: NAME | PNAME
   _event_head: event_is_clause+ doc?
      | doc
   event_is_clause: "is" _event_attrib ("," _event_attrib)* _NL
   _event_attrib: obsolete
      | stable
      | unstable
      | public
      | private
      | internal
      | attribute_expr


   method_decl: "def" method_name type_params? param_list? type_annotation? _NL _INDENT _method_contents _DEDENT
   method_name: NAME | PNAME
   _method_contents: _method_head _method_contracts* test_decl* block?
      | _method_contracts+ test_decl* block?
      | test_decl+ block?
      | block
   _method_head: _method_head_element+ doc?
      | doc
   _method_head_element: method_is_clause
      | where_clause
   method_is_clause: "is" _method_attrib ("," _method_attrib)* _NL
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

   requires_contract: "requires" _contract_impl
   ensures_contract: "ensures" _contract_impl
   invariant: "invariant" _contract_impl
   decreases: "decreases" _contract_impl

   _contract_impl: expr_stmt
      | _NL _INDENT _expr_block _DEDENT
   _expr_block: doc expr_stmt*
      | expr_stmt+
      | _pass

   param_list: "(" formal_args? ")"

   formal_args: formal_arg ("," formal_arg)* ","?
   formal_arg: arg_name type_annotation? initializer?
   arg_name: NAME | PNAME | JOKER

   constructor: block

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

   assertion: "assert" inline_expr _NL (_INDENT doc _DEDENT)?
   break_stmt: _jump_cond? "break" (rhs |_NL)
   continue_stmt: _jump_cond? "continue" _NL
   return_stmt: _jump_cond? "return_stmt" (rhs | _NL)

   _jump_cond: when_clause
      | unless_clause

   when_clause: "when" inline_expr
   unless_clause: "unless" inline_expr

   defer_stmt: _jump_cond? "defer" _NL (_INDENT block _DEDENT)?

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
      | "new" var_name

   expr_with_body: inline_expr lambda_args? _NL (_INDENT body_block _DEDENT)?
   object_init: inline_expr "but" _NL _INDENT body_block _DEDENT   
   if_expr: "if" inline_expr _NL _INDENT block _DEDENT elif_clause* else_clause?
   while_expr: "while" inline_expr _NL _INDENT body_block _DEDENT else_clause?
   match_expr: "match" inline_expr ("," inline_expr)* ","? _NL _INDENT case_clause+ else_clause? _DEDENT
   elif_clause: "elif" inline_expr _NL _INDENT body_block _DEDENT
   else_clause: "else"  _NL _INDENT body_block _DEDENT
   case_clause: "case" pattern guard? _NL _INDENT body_block _DEDENT

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

   try_expr: "try" _atomic_expr

   catch_expr: _atomic_expr "catch" _atomic_expr

   _atomic_expr: never
      | todo
      | ref_expr
      | call_expr
      | old_expr

   ?call_expr: subscript_expr
      | call_expr "?"? actual_params

   ref_expr: "ref" subscript_expr
   old_expr: "old" subscript_expr

   ?subscript_expr: subscript_expr subscript_operator method_name
      | _subscribable_expr

   _subscribable_expr: "(" inline_expr ")"
      | tuple_expr
      | map_expr
      | list_expr
      | string_interpolation
      | string_literal
      | named_ref

   subscript_operator: SUBS
      | SUBS_MAYBE

   named_ref: NAME
      | PNAME
      | JOKER
      | value

   value: "value"

   never: "never"
   todo: "todo"

   string_literal: STRING_LITERAL_QQ
   string_interpolation: STRING_LITERAL_QB inline_expr (STRING_LITERAL_BB inline_expr)* STRING_LITERAL_BQ
   list_expr: "[" (_simple_entry ("," _simple_entry)* ","?)? "]"
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
      | string_pattern

   string_pattern: STRING_LITERAL_QQ
      | STRING_LITERAL_QB pattern_name string_pattern_tail
   string_pattern_tail: STRING_LITERAL_BQ
      | STRING_LITERAL_BB pattern_name string_pattern_tail

   stream_pattern: "[" (_stream_pat_entry ("," _stream_pat_entry)* ","?)? "]"

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

   type_def: "type" type_name type_params? formal_args? type_annotation _NL (_INDENT _type_head _DEDENT)?
   type_name: NAME | PNAME
   _type_head: doc
      | _type_head_element+ doc?

   _type_head_element: type_is_clause
      | where_clause
      | requires_contract
      | ensures_contract

   type_is_clause: "is" _type_attr ("," _type_attr)*

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

   type_annotation: "as" type_expr

   _pass: "pass" _NL?

   attribute_expr: NAME

   unstable: "unstable"
   stable: "stable"
   obsolete: "obsolete" STRING_LITERAL_QQ?
   public: "public"
   private: "private"
   internal: "internal"
   singleton: "singleton"
   pure: "pure" AST?
   immutable: "immutable" AST?
   cached: "cached"



   AST: "*"
   OPT: "?"
   NAME: /(?!_)(?=\p{L}|\p{Nl}|\p{Other_ID_Start})[\p{L}\p{Nl}\p{Other_ID_Start}\p{Mn}\p{Mc}\p{Nd}\p{Pc}\p{Other_ID_Continue}_]+/
   PNAME: JOKER NAME
   JOKER: "_"


   ASSIGN: "="
   ALTER: "+=" | "-=" | "*=" | "/=" | "^="

   AND: "and"
   OR: "or"
   XOR: "xor"
   IMPLIES: "implies"
   NOT: "not"
   DIV: "div"
   MOD: "mod"
   PLUS_OP: "+"
   MINUS_OP: "-"
   SLASH: "/"
   EQ: "=="
   NEQ: "<>"
   LT: "<"
   LEQ: "<="
   GT: ">"
   GEQ: ">="
   IN: "in"
   PIPE: "|>"
   EPIP: "<|"

   SUBS: "."
   SUBS_MAYBE: "?."

   EXCLAM: "!"

.. rubric:: Citations

.. [Viega1998] John Viega, Bill Tutt, and Reimer Behrends.
   1998. Automated Delegation is a Viable Alternative to Multiple Inheritance in Class Based Languages.
   Technical Report. University of Virginia, USA.

.. _YAML: https://yaml.org
.. _CFF: https://citation-file-format.github.io/
.. _publiccode.yml: https://yml.publiccode.tools/