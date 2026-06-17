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
updated in tandem with the code, not after the fact. It is hand-authored and design-first:
the signatures here are the contract; the auto-generated API Reference is the verification.

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
               If any parameter has an invalid value, or the scrolloff–height constraint
               is violated.
           IndexError
               If ``cursor_index`` is outside ``[0, len(text)]``.
           """


.. :need:`FR-INIT-013` :need:`FR-INIT-011` :need:`FR-INIT-006`

Mutation Commands
.................

.. code-block:: python

       def insert(self, text: str) -> None:
           """Insert ``text`` at the current cursor position. Cursor moves to end of inserted text."""

       def delete(self) -> None:
           """Delete the character immediately right of the cursor. No-op at end of buffer."""

       def backspace(self) -> None:
           """Delete the character immediately left of the cursor. Cursor moves left. No-op at start of buffer."""

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
           """Move cursor to the absolute start of the buffer (index ``0``)."""

       def move_end(self) -> None:
           """Move cursor to the absolute end of the buffer (index ``len(buffer)``)."""

Cursor Query
............

.. note::

   The primary interface for host applications is the ``cursor`` property, which returns the cursor
   in Window coordinates. The remaining methods expose the cursor in other coordinate spaces
   for advanced integrations. See :ref:`req_output_modes`.

.. code-block:: python

       @property
       def cursor(self) -> WindowPosition:
           """Return cursor position as a window coordinate ``[x, y]``."""

       def visual_cursor(self) -> VisualPosition:
           """Return cursor position as a visual coordinate ``(v_row, v_col)``."""

       def logical_cursor(self) -> LogicalPosition:
           """Return cursor position as a logical coordinate ``(row, col)``."""

       def raw_cursor(self) -> int:
           """Return cursor position as an absolute index."""

Content Query
.............

.. note::

   The primary interface for host applications is the ``lines`` property, which returns the
   viewport-clipped display lines. The remaining methods expose the full buffer in other
   representations for advanced integrations. See :ref:`req_output_modes`.

.. code-block:: python

       @property
       def lines(self) -> list[VisualLineGroup]:
           """Return the subset of visual lines currently visible within the window."""

       def visual_lines(self) -> list[VisualLineGroup]:
           """Return all visual lines across the entire buffer."""

       def logical_lines(self) -> list[str]:
           """Return the buffer split at newline boundaries, newline characters excluded."""

       def raw_text(self) -> str:
           """Return the buffer contents as a single string, including all newline characters."""

Magic Methods
.............

.. code-block:: python

       def __str__(self) -> str:
           """Return the buffer contents as a string. Equivalent to ``raw_text()``."""

       def __repr__(self) -> str:
           """Return a developer-readable representation of the editor state.
           Including all initialization parameters."""

.. rubric:: Excluded Magic Methods

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - Method
     - Rationale
   * - ``__hash__``
     - ``__eq__`` is excluded, so Python retains the default identity-based hash.
       No action required; noted here to prevent a future ``__eq__`` addition from
       silently breaking hashing.
   * - ``__len__``
     - Ambiguous: length of the raw text vs. number of logical lines vs. number of
       visual lines. Callers must use ``len(editor.raw_text())`` or equivalent explicitly.
   * - ``__iter__``
     - Ambiguous: iterate characters, logical lines, or visual lines. No single
       interpretation is obviously correct.
   * - ``__eq__``
     - Ambiguous: equality of buffer content alone vs. full state including cursor
       position and display geometry.
   * - ``__bool__``
     - Misleading: ``INV-TEXT-001`` guarantees the buffer always contains at least one
       logical line, so an "empty" editor would still be truthy. The result would
       surprise callers.
   * - ``__copy__`` / ``__deepcopy__``
     - The prescribed way to clone state is re-initialisation via the output interfaces
       (:need:`NR-INIT-101`, :need:`NR-INIT-102`). A shallow copy would produce a second
       instance sharing internal component references, breaking the ownership model.
   * - ``__getstate__`` / ``__setstate__``
     - State serialisation is explicitly out of scope (:need:`NR-INIT-102`). Allowing
       pickling would produce silent success with undefined behaviour on restore.

Public Return Types
-------------------

These types form the public data contract between the engine and host applications.
They are defined here rather than inferred from the class diagrams, as they cross the
public API boundary and must remain stable independently of internal implementation changes.

.. code-block:: python

   @dataclass(frozen=True)
   class VisualLineGroup:
       """All visual segments that belong to one logical line."""

       segments: list[str]

       def __iter__(self) -> Iterator[str]:
           return iter(self.segments)

       def __len__(self) -> int:
           return len(self.segments)

       def __getitem__(self, index: int) -> str:
           return self.segments[index]


   class WindowPosition(NamedTuple):
       """Cursor position within the visible window. ``x`` is column, ``y`` is display row."""
       x: int
       y: int


   class VisualPosition(NamedTuple):
       """Cursor position across all wrapped visual lines."""
       row: int
       col: int


   class LogicalPosition(NamedTuple):
       """Cursor position in logical line and column space."""
       row: int
       col: int

.. _code_internal_interfaces:

Internal Component Interfaces
-----------------------------

.. note::

   These are internal contracts between components. They are not part of the public API and
   may change without notice to host applications. They are recorded here to support
   implementation and isolated unit testing of individual components.

``TextBuffer``
~~~~~~~~~~~~~~

.. code-block:: python

   def insert(self, text: str, index: int) -> None:
       """Insert ``text`` at ``index``. No-op if ``text`` is empty."""

   def delete(self, index: int) -> None:
       """Delete the character immediately right of ``index``.
       No-op if ``index == len(buffer)``."""

   def get_text(self) -> str:
       """Return the buffer contents as a single string."""

``CursorState``
~~~~~~~~~~~~~~~

.. code-block:: python

   def get_position(self) -> int:
       """Return the current cursor position as an absolute index."""

   def set_position(self, position: int) -> None:
       """Set the cursor position. Caller is responsible for bounds validation."""

   def move_left(self) -> None:
       """Decrement position by 1. Caller is responsible for bounds validation."""

   def move_right(self) -> None:
       """Increment position by 1. Caller is responsible for bounds validation."""

   def move_home(self) -> None:
       """Set position to 0."""

   def move_end(self, text_len: int) -> None:
       """Set position to ``text_len``."""

``LogicalDomainService``
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def get_lines(self) -> list[str]:
       """Return the buffer split at newline boundaries, newline characters excluded."""

   def get_logical_cursor(self) -> LogicalPosition:
       """Return cursor position as a logical coordinate ``(row, col)``."""

   def _to_logical(self, position: int) -> LogicalPosition:
       """Convert absolute index to logical coordinate."""

   def _to_abs(self, position: LogicalPosition) -> int:
       """Convert logical coordinate to absolute index."""

``VisualLogicalAdapter``
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def insert(self, text: str) -> None:
       """Insert ``text`` at the current cursor position. Cursor moves to end of inserted text."""

   def delete(self) -> None:
       """Delete the character immediately right of the cursor. No-op at end of buffer."""

   def backspace(self) -> None:
       """Delete the character immediately left of the cursor. Cursor moves left. No-op at start of buffer."""

   def get_lines(self) -> list[VisualLineGroup]:
       """Return all visual lines across the entire buffer."""

   def get_cursor(self) -> VisualPosition:
       """Return cursor position as a visual coordinate ``(v_row, v_col)``."""

   def set_cursor(self, position: VisualPosition) -> None:
       """Set the cursor position."""

   def move_left(self) -> None:
       """Move cursor one character left. No-op at start of buffer."""

   def move_right(self) -> None:
       """Move cursor one character right. No-op at end of buffer."""

   def move_home(self) -> None:
       """Move cursor to the absolute start of the buffer (index ``0``)."""

   def move_end(self) -> None:
       """Move cursor to the absolute end of the buffer (index ``len(buffer)``)."""

   def _to_visual(self, abs_index: int) -> VisualPosition:
       """Convert absolute index to visual coordinate."""

   def _to_abs(self, position: VisualPosition) -> int:
       """Convert visual coordinate to absolute index."""

   def _rebuild_wrap_map(self) -> List[List[Span]]:
       """Recompute and store the internal wrapping map from the current buffer state.
       Must be called after every mutation before any read or coordinate translation
       is served. (`INV-WRAP-003`)"""

``MovementResolver``
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   @staticmethod
   def move_up(line_lengths: list[int], cursor: VisualPosition) -> VisualPosition:
       """Return new cursor position after moving up one visual line.
       Jumps to ``(0, 0)`` if already on the first visual line. (`FR-CURSOR-050`)
       Truncates column to target line length if necessary. (`FR-CURSOR-031`)"""

   @staticmethod
   def move_down(line_lengths: list[int], cursor: VisualPosition) -> VisualPosition:
       """Return new cursor position after moving down one visual line.
       Jumps to end of last line if already on the last visual line. (`FR-CURSOR-050`)
       Truncates column to target line length if necessary. (`FR-CURSOR-031`)"""

``ViewportState``
~~~~~~~~~~~~~~~~~

.. code-block:: python

   def get_range(self) -> tuple[int, int]:
       """Return ``(window_start, window_start + display_height - 1)``."""

   def update(self, cursor: VisualPosition, num_visual_lines: int) -> int:
       """Update ``window_start`` to satisfy cursor visibility and scrolloff constraints.
       Adjusts by the minimum amount required. (:need:`FR-VIEW-003`)"""
