.. _arch_error_contract_page:

Error Contract
==============

The engine uses (three) standard Python exception types. No custom exception hierarchy is defined.
The ``TextEditor`` facade is the sole exception boundary visible to the host application; internal
components raise the exceptions below when they detect a contract violation, and the facade either
resolves them (where a violation can be corrected at the boundary) or re-raises them with sufficient
context for the host to act on.

The host application never receives a raw exception from an internal component directly.

Exception Types
---------------

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Exception
     - When raised
   * - ``TypeError``
     - A parameter is of the wrong Python type: a float in place of an integer for ``display_width``,
       ``display_height``, ``scrolloff``, or ``cursor_index``; a non-string argument to ``insert``.
       (:need:`FR-INIT-013`)
   * - ``ValueError``
     - A parameter has the correct type but an invalid value: ``display_width`` or ``display_height``
       is zero or negative; ``scrolloff`` is negative; the cross-parameter constraint
       ``2 * scrolloff < display_height`` is violated; ``cursor_index`` is negative or greater than
       ``len(text_buffer)``.
       (:need:`FR-INIT-011`, :need:`FR-INIT-012`, :need:`FR-INIT-003`, :need:`FR-INIT-004`,
       :need:`FR-INIT-005`)
   * - ``IndexError``
     - A cursor or index position is outside the valid range for the current buffer state.
       (:need:`FR-INIT-006`, :need:`INV-CURSOR-001`)

Null / Absent Parameters
------------------------

Required parameters (``width``, ``height``, ``scrolloff``) raise ``TypeError``
when ``null`` or absent, since ``None`` is of the wrong type for an integer parameter.
Optional parameters (``text``, ``cursor_index``) have defined defaults and must not raise when
omitted or ``null``. (:need:`FR-INIT-012`)

Per-Operation Failure Modes
----------------------------

.. rubric:: Initialisation

.. list-table::
   :widths: 40 20 40
   :header-rows: 1

   * - Condition
     - Exception
     - Requirement
   * - ``width`` is zero, negative, or non-integer
     - ``TypeError`` / ``ValueError``
     - :need:`FR-INIT-003`, :need:`FR-INIT-013`
   * - ``height`` is zero, negative, or non-integer
     - ``TypeError`` / ``ValueError``
     - :need:`FR-INIT-004`, :need:`FR-INIT-013`
   * - ``scrolloff`` is negative or non-integer
     - ``TypeError`` / ``ValueError``
     - :need:`FR-INIT-005`, :need:`FR-INIT-013`
   * - ``2 * scrolloff >= display_height``
     - ``ValueError``
     - :need:`FR-INIT-011`
   * - Any required parameter is ``null``
     - ``TypeError``
     - :need:`FR-INIT-012`
   * - ``cursor_index`` out of range or non-integer
     - ``IndexError`` / ``TypeError``
     - :need:`FR-INIT-006`, :need:`FR-INIT-013`
   * - ``text`` is non-string
     - ``TypeError``
     - :need:`FR-INIT-013`

.. rubric:: Text Mutations (insert, delete, backspace)

.. list-table::
   :widths: 10 30 20 40
   :header-rows: 1

   * - Method
     - Condition
     - Result
     - Requirement
   * - ``insert(text)``
     - ``text`` is non-string
     - ``TypeError``
     - :need:`FR-INIT-013`
   * - ``insert(text)``
     - ``text`` is empty.
     - No-op
     - :need:`FR-TEXT-013`
   * - ``insert(text)``
     - length of ``text`` > 1 characters
     - All are inserted
     - :need:`FR-TEXT-017`
   * - ``delete()``
     - No character to the right of the cursor
     - No-op
     - :need:`FR-TEXT-024`
   * - ``backspace()``
     - No character to the left of the cursor
     - No-op
     - :need:`FR-TEXT-034`

.. rubric:: Cursor Movement

Attempts to move the cursor into an invalid position are a silent no-op. (e.g. Moving left from the
start of the buffer, or right from the end of the buffer.)

Propagation Rules
-----------------

All exceptions escape the ``TextEditor`` facade unchanged in type. The facade adds a descriptive
message to any exception it re-raises, sufficient for the host application to identify the violated
constraint without consulting internal component source.

No partial state is constructed on a failed initialisation. If any validation step raises, the
``TextEditor`` instance is not created and no internal component is initialised.
(:need:`FR-INIT-001`, :need:`INV-INIT-002`)

Test Obligations
----------------

Every entry in the per-operation table above must have a corresponding test that:

* Supplies the invalid input.
* Asserts the correct exception type is raised.
* Asserts the engine produces no observable side-effects (no partial state, no mutated buffer).
