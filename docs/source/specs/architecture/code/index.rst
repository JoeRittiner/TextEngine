.. _arch_code_index:

Code (C4 Level 4)
=================

Introduction
------------

Purpose
~~~~~~~

This document is the C4 Level 4 layer of the architecture. Where the Component level
(:doc:`../index`) describes the *responsibilities* and *contracts* of each component,
this document describes their *implementation structure*: class diagrams, method signatures,
parameter types, return types, and the precise interface contracts that components publish to
one another.

This is the authoritative reference for anyone writing or reviewing implementation code. It is
updated in tandem with the code, not after the fact. It is hand-authored, design-first,
specifies intent and contracts.

Relationship to Other Documents
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Architecture Components (C4 Level 3):** :doc:`../index` - the layer above; describes
  responsibilities and ownership without prescribing class structure.
* **Requirements:** :doc:`../../requirements/index` - the behavioural contracts that the
  classes below must satisfy.

Document Conventions
~~~~~~~~~~~~~~~~~~~~~

* Class diagrams use PlantUML and follow the color convention defined in
  :doc:`../index` (Logical: blue, Visual: green, Display: orange, Facade: grey).
* Method signatures are written in Python 3 type-annotated style.

.. _code_class_diagrams:

Class Diagrams
--------------

Logical Domain
~~~~~~~~~~~~~~

.. plantuml::  ../diagrams/class-logical_domain.puml

Visual Domain
~~~~~~~~~~~~~

.. plantuml::  ../diagrams/class-visual_domain.puml

Display Domain
~~~~~~~~~~~~~~

.. plantuml::  ../diagrams/class-display_domain.puml

Full System
~~~~~~~~~~~

.. plantuml::  ../diagrams/class-facade.puml


.. _code_internal_interfaces:
