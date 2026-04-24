Requirements
============

Purpose & Scope
---------------

This document describes the requirements for the :term:`TextEditor` component.
It defines how the :term:`TextEditor` should behave as a unit to the outside world. Obviously, not how the component
works internally.

The scope of this specification includes:
   * ...

The scope of this specification does NOT include:
   * ...

The system is defined as a pure logic component with no side effects beyond its internal state.
It provides a structured representation of text and cursor position that can be consumed by external systems.

The requirements focus on precise, testable behavior of text manipulation and cursor movement, independent of any
specific runtime environment or application context.


Project Results
---------------

.. note::
   The project results as a whole differ from the results of the :term:`TextEditor` component.
   This document describes the results of the :term:`TextEditor` component. Not any personal goals this project is
   meant to facilitate.

The end result of the project is a text :term:`editor <TextEditor>` component. The name "Text Editor" may
be slightly misleading, as the project is not intended to be a full-featured :term:`editor <TextEditor>`. Instead, it
provides text storage and cursor tracking with deterministic editing behavior.

Supports UTF-8 only. (Maybe)

The component stores text and maintains a cursor position. The text can be manipulated at the cursor location, including
insertion and deletion operations. The cursor can be moved left, right, up, and down (and "home" and "end").

The cursor lies _between_ characters, not on them. (e.g. "a|b" is between the characters 'a' and 'b'). And is bound to
existing characters. It cannot move beyond the start or end of the text. (e.g. "\|ab" cannot move left, "ab|" cannot move right)

The editor defines a maximum display width. Lines are not truncated; instead, they are wrapped into
:term:`visual lines <visual line>`. Vertical cursor movement operates on these wrapped
:term:`visual lines <visual line>` rather than on :term:`logical lines <logical line>`.

The editor also defines a :term:`display height` (window). When the number of :term:`visual lines <visual line>`
exceeds the :term:`display height`, only a subset is considered visible. The window offset updates only when the cursor
would otherwise move outside the visible area. (i.e., scrolling with the cursor)

The editor is capable of outputting the text in various "modes".
   * Display: :term:`visual lines <visual line>` clamped to the :term:`display height`
   * Wrapped: :term:`visual lines <visual line>` (not clamped)
   * Logic: :term:`logical lines <logical line>` (not wrapped)
   * Raw: raw text (not split into lines)
Newline characters (`\n`) are not returned (except in raw text mode).

The editor is also capable of outputting the cursor position.
   * display position in the window ``(row, col)``
   * visual position in the wrapped text ``[row, char]``
   * maybe: logical position in the original text ``index``

Visual Wrapping Rules: I'll define these requirements later

There is always at least one empty line. The cursor would be at (``(0,0)``, ``[0,0]``, ``0``).

----

The :term:`editor <TextEditor>` will not handle text selection. (e.g. with a mouse, or Shift+Arrow)

The :term:`editor <TextEditor>` will not handle copy, cut or paste operations. (e.g. Ctrl+C, Ctrl+X, Ctrl+V) This could
maybe be simulated by the application that uses the :term:`editor <TextEditor>`.

The editor does not perform file I/O and is not responsible for rendering. Instead, it acts as a pure logic component
that provides the text and cursor state representing what would be visible. It may maintain an internal state. I.e.
movements and changes to the text won't return the new state. It will be kept internally and must be requested.

The :term:`editor <TextEditor>` does not handle user input (e.g., keyboard or mouse events). I.e. "typing" needs to be
handled programmatically by the application that uses the :term:`editor <TextEditor>`. Any mouse movements and clicks
to move the cursor are also handled by the application.
