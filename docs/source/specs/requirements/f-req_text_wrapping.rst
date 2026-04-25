4.3 Text Wrapping
=================

4.3.1 Description and Priority
------------------------------
**Priority: Medium**

:term:`Logical lines <logical line>` that exceed the :term:`display width` are not truncated or hidden.
Instead, they are segmented into multiple :term:`visual lines <visual line>`.

Wrapping is a purely visual transformation and does not modify the underlying :term:`text buffer`.
No "soft" or "hard" newline characters are inserted into the buffer to facilitate wrapping.
This mechanism determines the mapping between the Absolute Index and Visual Coordinates as described in the
:doc:`Cursor Specification <f-req_cursor_movement>`.

.. note::
   The current implementation uses "Character Wrapping" (breaking at the exact :term:`display width` boundary).
   Future iterations may introduce "Word Wrapping" logic.

4.3.2 State Invariants
----------------------

.. inv:: Defined Display Width
   :id: INV-WRAP-001
   :tags: wrap

   A positive integer :term:`display width` (representing the maximum number of :term:`characters <character>`
   per :term:`visual line`) must be defined at system initialization.

.. inv:: Static Display Width
   :id: INV-WRAP-002
   :tags: wrap

   The :term:`display width` must remain constant during the lifetime of the system instance.

   .. note::
      To simulate a responsive or dynamic width, the environment must re-initialize the system component with the
      updated width value.

.. inv:: Visual Line Integrity
   :id: INV-WRAP-003
   :tags: wrap

   The sum of the lengths of all :term:`visual lines <visual line>` associated with a :term:`logical line`
   must equal the length of that :term:`logical line`.

4.3.3 Preconditions
-------------------

All wrapping logic assumes a valid :term:`text buffer` as defined in
:doc:`Text Buffer Specification <f-req_text_manipulation>`. Wrapping is applied automatically whenever the
:term:`text buffer` state changes or the system is initialized.

4.3.4 Stimulus/Response Sequences
---------------------------------

* **Stimulus:** The :term:`text buffer` is modified (insertion, deletion, or initialization).

  **Response:** The system recalculates the break points for all affected :term:`logical lines <logical line>`
  and updates the total visual line count and :term:`cursor` Visual Coordinates.

4.3.5 Functional Requirements
-----------------------------

.. freq:: Non-Destructive Wrapping
   :id: FR-WRAP-001
   :tags: wrap

   Wrapping operations must not alter the contents of the :term:`text buffer`.

   Joining all :term:`visual lines <visual line>` (excluding the implicit visual break) must perfectly reconstruct the
   original :term:`logical line`.

.. freq:: Full Content Visibility
   :id: FR-WRAP-002
   :tags: wrap

   The system must not truncate or omit characters from the :term:`visual lines <visual line>`.
   Every character in the :term:`text buffer` must be assigned to exactly one :term:`visual line`.

.. freq:: Break Logic (Character-Based)
   :id: FR-WRAP-003
   :tags: wrap

   A :term:`logical line` must be split into :term:`visual lines <visual line>` such that:
      * Each :term:`visual line` (except potentially the last one) has a length exactly equal to the :term:`display width`.
      * The final :term:`visual line` of a :term:`logical line` has a length of ``logical_line_length % display_width``.

.. freq:: Line Isolation
   :id: FR-WRAP-004
   :tags: wrap

   Wrapping must be performed on a per-line basis. The system must never combine characters from two different
   :term:`logical lines <logical line>` into a single :term:`visual line`.

.. freq:: Empty Line Handling
   :id: FR-WRAP-005
   :tags: wrap

   A :term:`logical line` with zero characters (including and excluding newlines) must still result in exactly one
   :term:`visual line` with a length of zero to provide a valid :term:`cursor` position.


Out of Scope
~~~~~~~~~~~~

.. freq:: Character Boundary Flexibility
   :id: NR-WRAP-101
   :tags: wrap, out-of-scope

   Wrapping may occur at any character boundary. Word boundaries do not need to be preserved.
