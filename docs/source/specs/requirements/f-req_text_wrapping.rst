.. _req_text_wrapping:

4.4 Text Wrapping
=================

4.4.1 Description and Priority
------------------------------
**Priority: Medium**

:term:`Logical lines <logical line>` that exceed the :term:`display width` are not truncated or hidden.
Instead, they are segmented into multiple :term:`visual lines <visual line>`.

Wrapping is a purely visual transformation and does not modify the underlying :term:`text buffer`.
No "soft" or "hard" newline characters are inserted into the :term:`text buffer` to facilitate wrapping.
This mechanism determines the mapping between the :term:`Absolute Index` and
:term:`Visual Coordinates <Visual Coordinate> as described in the :doc:`Cursor Specification <f-req_cursor_movement>`.

.. note::
   The current implementation uses "Character Wrapping" (breaking at the exact :term:`display width` boundary).
   Future iterations may introduce "Word Wrapping" logic.

4.4.2 State Invariants
----------------------

.. inv:: Defined Display Width
   :id: INV-WRAP-001
   :tags: wrap
   :links: FR-INIT-003

   A positive integer :term:`display width` (representing the maximum number of :term:`characters <character>`
   per :term:`visual line`) must be defined at system initialization.

.. inv:: Static Display Width
   :id: INV-WRAP-002
   :tags: wrap
   :links: FR-INIT-003

   The :term:`display width` must remain constant during the lifetime of the system instance.

   .. note::
      To simulate a responsive or dynamic width, the environment must re-initialize the system component with the
      updated width value.

.. inv:: Visual Line Integrity
   :id: INV-WRAP-003
   :tags: wrap

   The sum of the lengths of all :term:`visual lines <visual line>` associated with a :term:`logical line`
   must equal the length of that :term:`logical line`.

4.4.3 Preconditions
-------------------

All wrapping logic assumes a valid :term:`text buffer` as defined in
:doc:`Text Buffer Specification <f-req_text_manipulation>`. Wrapping is applied automatically whenever the
:term:`text buffer` state changes or the system is initialized.

4.4.4 Stimulus/Response Sequences
---------------------------------

* **Stimulus:** The :term:`text buffer` is modified (insertion, deletion, or initialization).

  **Response:** The system recalculates the break points for all affected :term:`logical lines <logical line>`
  and updates the total :term:`visual line`-count and :term:`cursor` :term:`Visual Coordinates <Visual Coordinate>`.

4.4.5 Functional Requirements
-----------------------------

.. freq:: Non-Destructive Wrapping
   :status: Open
   :id: FR-WRAP-001
   :tags: wrap

   Wrapping operations must not alter the contents of the :term:`text buffer`.

   Joining all :term:`visual lines <visual line>` (excluding the implicit visual break) must perfectly reconstruct the
   original :term:`logical line`.

.. freq:: Full Content Visibility
   :status: Open
   :id: FR-WRAP-002
   :tags: wrap

   The system must not truncate or omit :term:`characters <character>` from the :term:`visual lines <visual line>`.
   Every :term:`character` in the :term:`text buffer` must be assigned to exactly one :term:`visual line`.

.. freq:: Break Logic (Character-Based)
   :status: Open
   :id: FR-WRAP-003
   :tags: wrap

   A :term:`logical line` is split into :term:`visual lines <visual line>` of length ``display_width``, except the
   last, whose length is ``logical_line_length % display_width`` (or ``display_width`` if zero).

.. freq:: Line Isolation
   :status: Open
   :id: FR-WRAP-004
   :tags: wrap

   Wrapping must be performed on a per-line basis. The system must never combine :term:`characters <character>` from
   two different :term:`logical lines <logical line>` into a single :term:`visual line`.

.. freq:: Empty Line Handling
   :status: Open
   :id: FR-WRAP-005
   :tags: wrap

   A :term:`logical line` with zero :term:`characters <character>` must result in exactly one :term:`visual line` with
   a length of zero.


Out of Scope
~~~~~~~~~~~~

.. nreq:: Character Boundary Flexibility
   :id: NR-WRAP-101
   :tags: wrap, out-of-scope

   Wrapping may occur at any :term:`character` boundary. Word boundaries do not need to be preserved.
