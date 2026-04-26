4.2 Cursor & Movement
=====================

4.2.1 Description and Priority
------------------------------
**Priority: High**

The :term:`cursor` is a position in the :term:`text buffer` that determines where text manipulation operations
occur.

The :term:`cursor` can be represented in multiple coordinate systems to serve different functional layers,
corresponding to the four :doc:`output modes <f-req_output_modes>`:

1. **Absolute Index** (``index``) - Source of truth for text manipulation.
2. **Logical Coordinate** (``[row, col]``) - Relevant for distinguishing :term:`logical lines <logical line>`
   (e.g., line numbers).
3. **Visual Coordinate** (``[v_row, v_col]``) - Relevant for text layout, rendering, and visual navigation.
4. **Window Coordinate** (``[x, y]``) - Relevant for displaying text within a :term:`viewport`.
   **Note:** ``[x, y]`` are not pixel coordinates. The system does not operate with pixels. ``y`` denotes the visible
   line index within the :term:`viewport` (where ``y=0`` is the first visible line, not necessarily the first document
   line). ``x`` denotes the column/character index.

4.2.2 State Invariants
----------------------

.. inv:: Valid Coordinate Ranges
   :id: INV-CURSOR-001
   :links: INV-WRAP-001, INV-VIEW-001

   The :term:`cursor` must always refer to a valid logical and visual position within the bounds of the
   :term:`text buffer`.

   The valid ranges for the respective coordinate systems are:

   * **Absolute Index**:
        * ``0 <= index <= len(text)``
   * **Logical Coordinate**
        * ``0 <= row < num_logical_lines``
        * ``0 <= col <= len(logical_line)``
   * **Visual Coordinate**:
        * ``0 <= v_row < num_visual_lines``
        * ``0 <= v_col <= len(visual_line)``
   * **Window Coordinate**:
        * ``0 <= y < display_height``
        * ``0 <= x <= display_width``

.. inv:: Inter-Character Positioning
   :id: INV-CURSOR-002

   The :term:`cursor` must always refer to a position *between* characters, not *on* a character itself.

.. inv:: Coordinate Synchronization
   :id: INV-CURSOR-003
   :links: INV-CURSOR-001

   The Absolute Index, Logical Coordinate, Visual Coordinate, and Window Coordinate must bijectively map
   to the exact same underlying position in the :term:`text buffer`. A change in one representation must be
   perfectly reflected in the others.

4.2.3 Preconditions
-------------------

All operations in this section assume a valid, initialized :term:`text buffer` as defined in
:doc:`Text Buffer Specification <f-req_text_manipulation>`.

Operations relying on visual representations (Visual Coordinates, Window Coordinates, Cursor Movement) assume valid,
initialized :term:`viewport`, :term:`display height` and :term:`display width`.

4.2.4 Stimulus/Response Sequences
---------------------------------

* **Stimulus:** An external system or user triggers a horizontal :term:`cursor` movement (e.g., left, right).

  **Response:** The system adjusts the :term:`cursor`, implicitly wrapping across
  :term:`visual lines <visual line>` if necessary, and updates all coordinate representations.

* **Stimulus:** An external system or user triggers a vertical :term:`cursor` movement (e.g., up, down).

  **Response:** The system calculates the new Visual Coordinate relative to the :term:`visual lines <visual line>`,
  truncating the visual column if the target line is shorter, and applies the update.

* **Stimulus:** An external system or user triggers a boundary :term:`cursor` movement (e.g., home, end).

  **Response:** The system updates the :term:`cursor` to the absolute start (index ``0``)
  or absolute end (index ``len(text)``) of the :term:`text buffer`.

* **Stimulus:** Text is inserted or deleted at the current :term:`cursor`.

  **Response:** The text is manipulated, and the :term:`cursor` implicitly updates its coordinates to remain logically
  consistent with the surrounding text boundary.

4.2.5 Functional Requirements
-----------------------------

Cursor Position & Coordinates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. freq:: Mutable Cursor Position
   :status: Open
   :id: FR-CURSOR-001
   :tags: cursor, state

   The system must maintain a mutable :term:`cursor`. No text manipulation operation may bypass the :term:`cursor`.

.. freq:: Logical Coordinate Representation
   :status: Open
   :id: FR-CURSOR-002
   :tags: cursor, coordinates

   The system must provide an interface to return the :term:`cursor` as a Logical Coordinate ``[row, col]``.
   A ``col`` value equal to the :term:`logical line` length represents the position immediately after the last
   character (before the newline delimiter).

.. freq:: Visual Coordinate Representation
   :status: Open
   :id: FR-CURSOR-003
   :tags: cursor, coordinates

   The system must provide an interface to return the :term:`cursor` as a Visual Coordinate ``[v_row, v_col]``
   representing its location across all wrapped :term:`visual lines <visual line>`.
   A ``v_col`` value equal to the :term:`visual line` length represents the position immediately after the last
   character on that visual segment.

.. freq:: Window Coordinate Representation
   :status: Open
   :id: FR-CURSOR-004
   :tags: cursor, coordinates

   The system must provide an interface to return the :term:`cursor` as a Window Coordinate ``[x, y]`` representing its
   location within the visible :term:`viewport`.
   An ``x`` value equal to ``display_width`` represents a position resting at the extreme right edge of the window.

Edge Case: Boundary wrapping
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. freq:: Virtual Position at Display Width
   :status: Open
   :id: FR-CURSOR-010
   :tags: cursor, boundary, rendering
   :links: FR-WRAP-003

   When a :term:`cursor` is positioned at the exact boundary of a wrapped :term:`logical line` (where the logical
   column is a multiple of ``display_width``), the valid Visual Coordinate must be represented as resting at the end of
   the current :term:`visual line` (``[v_row, display_width]``), rather than the start of the next line
   (``[v_row + 1, 0]``).
   The system must normalize any programmatic input of ``[v_row + 1, 0]`` for a wrapped boundary to
   ``[v_row, display_width]``.

.. freq:: Newline Insertion at Boundary
   :status: Open
   :id: FR-CURSOR-011
   :tags: cursor, boundary, insert

   Inserting a newline character when the :term:`cursor` is at a wrapped boundary (``[v_row, display_width]``) must move
   the :term:`cursor` to the start of the newly created :term:`logical line` (``[row + 1, 0]``, ``[v_row + 1, 0]``).

.. freq:: Newline Deletion at Boundary
   :status: Open
   :id: FR-CURSOR-012
   :tags: cursor, boundary, delete
   :links: FR-TEXT-025, FR-TEXT-035

   Deleting a newline character (via delete) must keep the :term:`cursor` indices unchanged.

   Deleting a newline character (via backspace) when the :term:`cursor` is at the start of a :term:`logical line`
   (``[v_row, 0]``) must move the :term:`cursor` to the end of the previous :term:`logical line`. (Now merged into
   one :term:`logical line`.)

Cursor Movement
~~~~~~~~~~~~~~~

.. freq:: Movement Operations
   :status: Open
   :id: FR-CURSOR-020
   :tags: movement

   The :term:`cursor` must support basic movement: ``up``, ``down``, (see :ref:`vertical-movement`)
   ``left``, and ``right``, (see :ref:`horizontal-movement`) as well as boundary jumps to the ``home`` and ``end`` of
   the :term:`text buffer`. (See :ref:`boundary-behaviors`)

.. freq:: Non-Destructive Movement
   :status: Open
   :id: FR-CURSOR-021
   :tags: movement

   Changing the :term:`cursor` must strictly be a navigation operation and must not modify the :term:`text buffer`.

.. _vertical-movement:

Vertical Movement
~~~~~~~~~~~~~~~~~

.. freq:: Visual Line Basis
   :status: Open
   :id: FR-CURSOR-030
   :tags: movement, vertical

   Vertical movements (``up`` or ``down``) must be evaluated relative to the :term:`visual lines <visual line>`,
   transparently crossing wrapped boundaries without requiring distinct logic for :term:`logical lines <logical line>`.

.. freq:: Target Visual Line Truncation
   :status: Open
   :id: FR-CURSOR-031
   :tags: movement, vertical
   :links: NR-CURSOR-101

   When moving vertically, the system must attempt to preserve the current visual column (``v_col``).
   If the target :term:`visual line` is shorter than the current ``v_col``, the system must truncate the new position
   to the end of the target :term:`visual line` (its maximum valid ``v_col``).

.. _horizontal-movement:

Horizontal Movement
~~~~~~~~~~~~~~~~~~~

.. freq:: Horizontal Absolute Shifting
   :status: Open
   :id: FR-CURSOR-040
   :tags: movement, horizontal
   :links: INV-CURSOR-003

   Moving the :term:`cursor` ``left`` or ``right`` must strictly decrement or increment the :term:`Absolute Index`
   by exactly 1, respectively. By definition of :need:`INV-CURSOR-003`, this inherently handles all appropriate
   wrapping across :term:`visual lines <visual line>` and :term:`logical lines <logical line>`.

.. _boundary-behaviors:

Boundary Behaviors
~~~~~~~~~~~~~~~~~~

.. freq:: Vertical Boundary Extremes
   :status: Open
   :id: FR-CURSOR-050
   :tags: movement, boundary

   Moving ``up`` from any valid position on the first :term:`visual line` must relocate the :term:`cursor` to the
   absolute start of the text.
   Moving ``down`` from any valid position on the last :term:`visual line` must relocate the :term:`cursor` to the
   absolute end of the text.

.. freq:: Inoperative Extents
   :status: Open
   :id: FR-CURSOR-051
   :tags: movement, boundary, no-op

   Moving ``left`` at the absolute start of the text, or moving ``right`` at the absolute end of the text,
   must not alter the :term:`cursor` (No-Op).

.. freq:: Move Home
   :status: Open
   :id: FR-CURSOR-052
   :tags: movement, boundary

   Moving ``home`` must relocate the :term:`cursor` to the start of the :term:`text buffer`.

   Equivalent to setting the :term:`absolute index` to 0.

.. freq:: Move End
   :status: Open
   :id: FR-CURSOR-053
   :tags: movement, boundary

   Moving ``end`` must relocate the :term:`cursor` to the end of the :term:`text buffer`.

   Equivalent to setting the :term:`absolute index` to the length of the :term:`text buffer`.

4.2.6 Out of Scope
------------------

.. nreq:: Desired Column Retention
   :id: NR-CURSOR-101
   :tags: out-of-scope, movement

   The system is currently not required to support a "Desired Column" or "Sticky Ghost Cursor" feature (the ability to
   memorize the furthest ``v_col`` position when navigating vertically across shorter intermediate lines).

.. nreq:: User Input
   :id: NR-CURSOR-102
   :tags: out-of-scope, movement

   The system does not capture keyboard or mouse events
   All "typing" or "clicking" must be translated into API calls by the host application.