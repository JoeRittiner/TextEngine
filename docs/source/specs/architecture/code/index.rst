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
* **API Reference:** :doc:`../../../reference/index` - auto-generated from docstrings;
  the runtime truth of what is implemented. If this document and the reference diverge,
  the reference is correct and this document must be updated.
* **Requirements:** :doc:`../../requirements/index` - the behavioural contracts that the
  classes below must satisfy.

Document Conventions
~~~~~~~~~~~~~~~~~~~~~

* Class diagrams use PlantUML and follow the color convention defined in
  :doc:`../index` (Logical: blue, Visual: green, Display: orange, Facade: grey).
* Method signatures are written in Python 3 type-annotated style.

.. * ``# TODO`` markers indicate interface decisions that are not yet finalised.

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

.. _code_public_api:

Public API
----------

``TextEditor``
~~~~~~~~~~~~~~

The sole public entry point. All host-application interaction passes through this class.
(:need:`NFREQ-DEPLOY-201`)

Initialisation
..............

.. code-block:: python

   class TextEditor:
       def __init__(
           self,
           width: int,
           height: int,
           scrolloff: int,
           text: str = "",
           cursor_index: int | None = None,
       ) -> None:
           """
           Initialise the engine with the given display geometry and optional seed state.

           Parameters
           ----------
           width:
               Maximum number of characters per visual line. Must be a positive integer.
           height:
               Maximum number of visual lines the window can show simultaneously.
               Must be a positive integer.
           scrolloff:
               Number of visual lines kept visible above and below the cursor.
               Must be a non-negative integer satisfying ``2 * scrolloff < display_height``.
           text:
               Initial buffer content. Defaults to an empty string.
           cursor_index:
               Initial cursor position as an absolute index into ``text``.
               Defaults to ``len(text)`` (end of buffer).

           Raises
           ------
           TypeError
               If any required parameter is of the wrong type.
           ValueError
               If any parameter has an invalid value or the scrolloff–height constraint is violated.
           IndexError
               If ``cursor_index`` is outside ``[0, len(text)]``.
           """


Mutation Commands
.................

.. code-block:: python

       def insert(self, text: str) -> None:
           """Insert ``text`` at the current cursor position. Cursor moves to end of inserted text."""

       def delete(self) -> None:
           """Delete the character immediately right of the cursor. No-op at end of buffer."""

       def backspace(self) -> None:
           """Delete the character immediately left of the cursor. Cursor Moves left. No-op at start of buffer."""

Cursor Movement
...............

.. code-block:: python

       def move_up(self) -> None:
           """Move cursor up one visual line. Jumps to absolute start if on first visual line."""

       def move_down(self) -> None:
           """Move cursor down one visual line. Jumps to absolute end if on last visual line."""

       def move_left(self) -> None:
           """Move cursor one character left. No-op at start of buffer."""

       def move_right(self) -> None:
           """Move cursor one character right. No-op at end of buffer."""

       def move_home(self) -> None:
           """Move cursor to the absolute start of the buffer (index 0)."""

       def move_end(self) -> None:
           """Move cursor to the absolute end of the buffer (index len(buffer))."""

Cursor Query
............

Intended: Display data through ``get_cursor``. Other methods are supplementary. (see :ref:`req_output_modes`)

.. code-block:: python

       def get_cursor(self) -> WindowPosition:
           """Return cursor position as a window position ``[x, y]``."""

       def visual_cursor(self) -> VisualPosition:
           """Return cursor position as a visual coordinate ``(v_row, v_col)``."""

       def logical_cursor(self) -> LogicalPosition:
           """Return cursor position as a logical coordinate ``(row, col)``."""

       def raw_cursor(self) -> int:
           """Return cursor position as an absolute index."""

Content Query
.............

Intended: Display data through ``get_lines``. Other methods are supplementary. (see :ref:`req_output_modes`)

.. code-block:: python

       def get_lines(self) -> list[VisualLineGroup]:
           """Return the subset of visual lines in the current window."""

       def visual_lines(self) -> list[VisualLineGroup]:
           """Return all visual lines."""

       def logical_lines(self) -> list[str]:
           """Return the buffer split at newline boundaries."""

       def raw_text(self) -> str:
           """Return the buffer contents as a single string, including all newline characters."""


Magic Methods
.............

.. code-block:: python

    def __str__(self) -> str:
        """Return a string representation of the buffer. Including all newline characters."""

    def __repr__(self) -> str:
        """..."""


Excluded magic methods:

- ``__len__``: Length of the text? number of visual lines? logic lines?
- ``__iter__``: display lines? logic lines?
- ``__eq__``:  Just text? Or cursor position? geometry?
- ...

Public Return Types
-------------------

.. code-block:: python

    @dataclass
    class VisualLineGroup:
        """
        A group of visual lines, that form a logical line.
        """
        segments: list[str]

        def __iter__(): Iterator[str]
        def __len__(): int
        def __getitem__(index: int): str

    class WindowPosition(NamedTuple):
        x: int
        y: int

    class VisualPosition(NamedTuple):
        row: int
        col: int

    class LogicalPosition(NamedTuple):
        row: int
        col: int

.. _code_internal_interfaces:
