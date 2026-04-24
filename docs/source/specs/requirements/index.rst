Requirements
============

Introduction
------------

Purpose
~~~~~~~

This document specifies the functional and non-functional requirements for the :term:`TextEditor` component.
The primary objective is to define the external behavior and state logic of the component as a discrete unit,
rather than its internal implementation or architectural patterns.

This specification serves as the foundational "contract" for developers integrating the :term:`TextEditor` into larger
applications. It ensures that text manipulation, cursor tracking, and visual wrapping remain deterministic and testable
across any runtime environment.

Scope
~~~~~

The :term:`TextEditor` is defined as a pure logic component. It maintains internal state regarding text content and
positioning but produces no side effects beyond its own data structures.

The scope of this specification includes:

* ...

The scope of this specification does NOT include:

* ...

The system is defined as a pure logic component with no side effects beyond its internal state.
It provides a structured representation of text and cursor position that can be consumed by external systems.

The requirements focus on precise, testable behavior of text manipulation, cursor movement, etc. independent of any
specific runtime environment or application context.

Definitions
~~~~~~~~~~~
The following terminology is used throughout this document to ensure clarity.

.. include:: req_glossary.rst

System Overview
---------------

The :term:`TextEditor` is a stateful, pure-logic component designed to provide deterministic text storage,
cursor tracking, and visual layout calculations. The name "Text Editor" may be slightly misleading:
it is not a full-featured desktop GUI application, but rather the underlying "engine" that models text editing behavior.

The component operates by maintaining an internal state. External applications programmatically push commands
(e.g., insert text, move cursor) to mutate this state, and subsequently request the resulting layout or cursor position.

**Core Responsibilities:**

* Storage and manipulation of text in a deterministic manner.
* Tracking of cursor position relative to the text layout.
* Calculation of :term:`visual lines <visual line>` based on a predefined maximum :term:`display width`.
* Calculation of the visible :term:`viewport` based on a predefined :term:`display height`.

**Explicit Non-Responsibilities:**

* **User Input:** Does not capture keyboard or mouse events. All "typing" or "clicking" must be translated into API
  calls by the host application.
* **Rendering & I/O:** Does not draw to the screen, manage windows, or perform file reading/writing.
* **Selection & Clipboard:** Does not handle text highlighting, selection, or copy/cut/paste operations
  (these must be simulated by the host application if required).

State Model
-----------

The internal state of the :term:`TextEditor` consists of the text content, the cursor position, and the parameters
defining the display boundaries.

Text Buffer
~~~~~~~~~~~
The component acts as the source of truth for the document's content. It exclusively supports **UTF-8** character
encoding.

Cursor
~~~~~~
The cursor operates strictly as a "pipe" or "insert" cursor, meaning it mathematically resides *between* characters,
rather than *on* a character.

For example, in the string "ab", the cursor can be at position 0 (before 'a'), position 1 (between 'a' and 'b'), or
position 2 (after 'b').

Display Model
~~~~~~~~~~~~~
The layout state is governed by two core parameters:

* **Display Width:** A maximum width threshold. Text is not truncated; instead, :term:`logical lines <logical line>`
  are wrapped into :term:`visual lines <visual line>` when they exceed this width. (Specific visual wrapping rules
  are defined separately).
* **Display Height (Window):** A maximum vertical threshold. When the total number of
  :term:`visual lines <visual line>` exceeds this height, the component tracks a vertical offset to represent the
  currently visible subset of text.

Invariants
~~~~~~~~~~
The component guarantees the following state invariants at all times:

* **Minimum Content:** There is always at least one :term:`logical line <logical line>`.
  An "empty" editor contains exactly one empty line.
* **Cursor Bounds:** The cursor is strictly bound to existing text. It can never move into negative indices or
  beyond the absolute end of the text buffer.
* **Cursor Default State:** In an empty editor, the cursor is invariably positioned at origin coordinates:
  window ``(0,0)``, visual ``[0,0]``, and logical index ``0``.

Behavioral Model
----------------

This section outlines how the component's state mutates in response to external commands and how it yields data.

Editing Operations
~~~~~~~~~~~~~~~~~~
The text buffer can be manipulated exclusively at the current cursor location.
The primary operations are text insertion and text deletion. These operations permanently mutate the internal state.

Cursor Movement
~~~~~~~~~~~~~~~
The cursor can be commanded to move incrementally (Left, Right, Up, Down) or jump to boundaries (Home, End).

Crucially, vertical cursor movement (Up/Down) operates entirely on the wrapped :term:`visual lines <visual line>`,
rather than the underlying :term:`logical lines <logical line>`.

Scrolling Behavior
~~~~~~~~~~~~~~~~~~
The display window's vertical offset updates *only* to keep the cursor visible. If a cursor movement would cause the
cursor to exit the bounds of the current :term:`display height`, the window offset is recalculated to bring the cursor
back into view with minimal scrolling. Scrolling is strictly cursor-driven.

Output Behavior / Modes
~~~~~~~~~~~~~~~~~~~~~~~
Because the component does not render text itself, it provides a retrieval interface to output the text state in four
distinct modes:

* **Display Mode:** Returns only the :term:`visual lines <visual line>` that currently fit within the
  :term:`display height` window.
* **Wrapped Mode:** Returns all :term:`visual lines <visual line>` from the entire document, ignoring the display height
  constraint.
* **Logical Mode:** Returns all :term:`logical lines <logical line>` from the entire document.
* **Raw Mode:** Returns the raw, unformatted text string as a continuous string.

*Note: Newline characters (`\n`) are stripped and not returned in Display or Wrapped modes.
They are only retained in Raw mode.*

Cursor Reporting
~~~~~~~~~~~~~~~~
The component provides methods to retrieve the exact location of the cursor in different contextual coordinate systems:

* **Display Position:** Returned as ``(x, y)``, representing the cursor's coordinates relative to the visible window.
* **Visual Position:** Returned as ``[row, char]``, representing the cursor's location within the completely wrapped
  text layout (absolute visual row).
* **Logical Position:** Returned as an ``index`` integer, representing the absolute character offset in the raw
  underlying string.

