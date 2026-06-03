.. _req_initialization:

4.1 System Initialization
=========================

4.1.1 Description and Priority
------------------------------
**Priority: High**

Initialization is the process by which the :term:`TextEditor` is created/ brought into a valid, operational state.
During initialization, the host application supplies all parameters required to configure the system, and
the :term:`TextEditor` constructs a self-consistent internal state from them.

No text manipulation, cursor movement, or output operations can be performed until the system is
successfully initialized. A failed initialization must not produce a :term:`TextEditor` instance.

Initialization is a one-time operation per :term:`TextEditor` instance. To change any
configuration parameter (e.g., :term:`Display Width`, :term:`Display Height`, or :term:`ScrollOff`),
the host application must discard the current instance and initialize a new one.

4.1.2 State Invariants
----------------------

.. inv:: Immutable Configuration
   :id: INV-INIT-001
   :tags: initialization, configuration
   :links: INV-WRAP-001, INV-WRAP-002, INV-VIEW-001

   Once the :term:`TextEditor` is successfully initialized, the values of :term:`Display Width`,
   :term:`Display Height`, and :term:`ScrollOff` must remain constant for the lifetime of that instance.
   They may not be mutated by any operation after initialization.

.. inv:: Post-Initialization Validity
   :id: INV-INIT-002
   :tags: initialization, state
   :links: INV-CURSOR-001, INV-VIEW-002, INV-VIEW-003, INV-VIEW-004

   Upon successful initialization, all system invariants must be satisfied simultaneously. The resulting
   state must be indistinguishable from a state reached by the normal operation of the system.

   Specifically, the following must hold:

   * The :term:`Text Buffer` contains the provided initial text (or is empty).
   * The :term:`Cursor` :term:`Absolute Index` is within ``[0, len(text_buffer)]``.
   * All coordinate representations of the :term:`Cursor` are consistent with each other and with the
     :term:`Text Buffer` contents (:need:`INV-CURSOR-003`).
   * ``0 <= window_start <= max(0, num_visual_lines - display_height)`` (:need:`INV-VIEW-003`).
   * The :term:`Cursor` is positioned within the :term:`Viewport` or within a :term:`ScrollOff` margin,
     as permitted by :need:`FR-VIEW-001`.

4.1.3 Preconditions
-------------------

None. Initialization is the entry point of the system and has no preconditions beyond the parameters
supplied by the host application.

4.1.4 Stimulus/Response Sequences
----------------------------------

* **Stimulus:** The host application requests initialization of a :term:`TextEditor` with a valid set
  of parameters (``display_width``, ``display_height``, ``scrolloff``, and optionally ``text`` and
  ``cursor_index``).

  **Response:** The system validates all parameters, constructs the internal :term:`Text Buffer`,
  computes all :term:`visual lines <Visual Line>`, places the :term:`Cursor` at the specified or default
  position, and sets the :term:`Window Start` to the minimal value that satisfies :need:`FR-VIEW-001`.
  The :term:`TextEditor` enters an operational state and is ready to accept further commands.

* **Stimulus:** The host application requests initialization with one or more invalid parameters (e.g.,
  ``display_width = 0``, ``scrolloff`` violating :need:`INV-VIEW-002`, a ``cursor_index`` out of range,
  or a type mismatch).

  **Response:** The system raises an exception describing the violated constraint. No internal state is
  constructed or mutated. The :term:`TextEditor` remains inert.

4.1.5 Functional Requirements
------------------------------

Happy Path
~~~~~~~~~~

.. freq:: System Initialization
   :status: Open
   :id: FR-INIT-001
   :tags: initialization
   :links: INV-INIT-001, INV-INIT-002

   The :term:`TextEditor` must be initialized by the host application by supplying the following
   parameters:

   * **Initial text** - optional; defaults to an empty string (see :need:`FR-INIT-002`).
   * :term:`Display Width` (``display_width``) - required (see :need:`FR-INIT-003`).
   * :term:`Display Height` (``display_height``) - required (see :need:`FR-INIT-004`).
   * :term:`ScrollOff` (``scrolloff``) - required (see :need:`FR-INIT-005`).
   * **Initial cursor position** - optional; defaults to the end of the :term:`Text Buffer`
     (see :need:`FR-INIT-006`).

   :term:`Window Start` is not a host-supplied parameter. It is computed by the system during
   initialization (see :need:`INV-INIT-002`, :need:`FR-INIT-007`).

   The system must not expose any observable state until initialization completes successfully.

.. freq:: Text Initialization
   :status: Open
   :id: FR-INIT-002
   :tags: initialization
   :links: FR-TEXT-017

   The host application may supply an initial text string at initialization.

   If initial text is provided, the resulting :term:`Text Buffer` state must be identical to that
   produced by initializing the system with no text and then inserting the provided string in full,
   as per :need:`FR-TEXT-017`.

   If no text is provided, the system must initialize the :term:`Text Buffer` to an empty string,
   equivalent to a single empty :term:`logical line`.

.. freq:: Display Width Initialization
   :status: Open
   :id: FR-INIT-003
   :tags: initialization
   :links: INV-WRAP-001, INV-WRAP-002

   The host application must supply a positive integer value for :term:`Display Width` at initialization.

   If the value is zero, negative, or not an integer, the system must raise an exception and
   halt initialization (see :need:`FR-INIT-011`, :need:`FR-INIT-013`).

.. freq:: Display Height Initialization
   :status: Open
   :id: FR-INIT-004
   :tags: initialization
   :links: INV-VIEW-001

   The host application must supply a positive integer value for :term:`Display Height` at initialization.

   If the value is zero, negative, or not an integer, the system must raise an exception and
   halt initialization (see :need:`FR-INIT-011`, :need:`FR-INIT-013`).

.. freq:: ScrollOff Initialization
   :status: Open
   :id: FR-INIT-005
   :tags: initialization
   :links: INV-VIEW-002

   The host application must supply a non-negative integer value for :term:`ScrollOff` at initialization.
   A value of ``0`` is valid and disables the scroll margin entirely.

   If the value is negative or not an integer, the system must raise an exception and halt initialization
   (see :need:`FR-INIT-011`, :need:`FR-INIT-013`).

   .. note::
      A ``scrolloff`` value that violates the cross-parameter constraint
      ``2 * scrolloff < display_height`` is rejected by :need:`FR-INIT-012`, even if
      the individual value is otherwise a valid non-negative integer.

.. freq:: Cursor Initialization
   :status: Open
   :id: FR-INIT-006
   :tags: initialization
   :links: INV-CURSOR-001

   The host application may supply an :term:`Absolute Index` to set the initial :term:`Cursor` position.
   The value must satisfy ``0 <= cursor_index <= len(text_buffer)`` after the :term:`Text Buffer` has
   been constructed per :need:`FR-INIT-002`.

   If no cursor position is provided, the system must default to ``len(text_buffer)``, placing the
   :term:`Cursor` immediately right of the last :term:`character` in the :term:`Text Buffer`.

   If a value outside the valid range (negative, or greater than ``len(text_buffer)``) or a non-integer is provided,
   the system must raise an exception and halt initialization (see :need:`FR-INIT-011`).

   .. note::
      :term:`Logical Coordinate`, :term:`Visual Coordinate`, and :term:`Window Coordinate` are not host-supplied
      parameters. There is currently no support for setting this values by the host application, even after
      initialization. Changing the :term:`Cursor` position must be done via movement commands.

.. freq:: Window Start Initialization
   :status: Open
   :id: FR-INIT-007
   :tags: initialization
   :links: FR-VIEW-001, FR-INIT-006, INV-VIEW-003

   The :term:`Window Start` is not supplied by the host application. The system must derive it
   automatically during initialization.

   The system must set :term:`Window Start` to the smallest non-negative integer value that satisfies
   both :need:`INV-VIEW-003` and :need:`FR-VIEW-001` given the initial :term:`Cursor` position.

   If the initial :term:`Cursor` position falls within the :term:`Viewport` at ``window_start = 0``,
   the system must set ``window_start = 0``.

Conflicts and Error Conditions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. freq:: ScrollOff–Height Conflict
   :status: Open
   :id: FR-INIT-011
   :tags: initialization, conflict
   :links: INV-VIEW-002

   If the condition ``2 * scrolloff >= display_height`` holds after both :term:`ScrollOff` and
   :term:`Display Height` have been validated individually, the system must raise an exception and halt
   initialization. No partial state must be constructed.

   This constraint is checked after :need:`FR-INIT-004` and :need:`FR-INIT-005` have each passed their
   individual validations, as it requires both values to be present.

.. freq:: Null Parameter
   :status: Open
   :id: FR-INIT-012
   :tags: initialization, conflict

   If a ``null`` (or language-equivalent absent) value is passed to any required parameter
   (``display_width``, ``display_height``, or ``scrolloff``), the system must raise an exception and
   halt initialization.

   .. note::
      Optional parameters (``text``, ``cursor_index``) have defined default behaviors when absent and
      must not raise an exception when omitted or null.

.. freq:: Type Conflict
   :status: Open
   :id: FR-INIT-013
   :tags: initialization, conflict

   If a value of an incorrect type is passed to any parameter, the system must raise an exception and
   halt initialization.

   Examples of invalid types:

   * A float (e.g., ``1.5``) in place of an integer for ``display_width``, ``display_height``,
     ``scrolloff``, or ``cursor_index``.
   * A non-string value in place of a string for the initial text.
   * **Exception** ``null`` (or language-equivalent absent) values for the optional parameters
     (``text``, ``cursor_index``) are allowed.

4.1.6 Out of Scope
-------------------

.. nreq:: Re-Initialization
   :id: NR-INIT-101
   :tags: out-of-scope, initialization

   The system does not support in-place re-initialization or mutation of configuration parameters
   (``display_width``, ``display_height``, ``scrolloff``) after successful initialization.
   To change these values, the host application must instantiate a new :term:`TextEditor` instance.

.. nreq:: State Persistence
   :id: NR-INIT-102
   :tags: out-of-scope, initialization

   The system does not provide mechanisms for serializing or deserializing its internal state.
   Saving and restoring editor state (e.g., for crash recovery or session resumption) is the
   responsibility of the host application, which may serialize the :term:`Text Buffer` contents and
   cursor position via the output interfaces and supply them as initialization parameters to a new
   instance.