4.5 Window & Scrolling
======================

4.5.1 Description and Priority
------------------------------
**Priority: Low**

The :term:`window` defines the total visible height, limiting the maximum number of :term:`visual lines <visual line>`
that can be "displayed" at once. A ``window_height = 10`` means that no more than 10 :term:`visual lines <visual line>`/
:term:`display lines <display line>` are returned.

The :term:`viewport` acts as a virtual boundary within the :term:`window`. It constraints where the :term:`cursor` can
move before triggering a scroll. A ``viewport_height = window_height`` means there are no restrictions on where the
:term:`cursor` is displayed (:term:`window coordinate`) withing the :term:`window`.

:term:`ScrollOff` defines the margin: the number of :term:`visual lines <visual line>` that must remain visible above
and below the :term:`cursor`. The :term:`cursor` is only allowed to enter the :term:`scrollOff` margins if it is near
the absolute start or end of the :term:`text buffer` where scrolling further is impossible.

The visible :term:`window` range/ the :term:`window start` is automatically updated in response to :term:`cursor`
movement and text manipulation.

4.5.2 State Invariants
----------------------

.. inv:: Display Dimensions
   :id: INV-VIEW-001
   :tags: viewport, state
   :links: FR-INIT-004

   A positive integer :term:`display height` must be defined at system initialization. It dictates the maximum number of
   :term:`visual lines <visual line>` the system can return as :term:`display lines <display line>`.

   **Note:** If dynamic resizing is needed by a user, the system must be re-initialized with a new
   :term:`display height`.

.. inv:: ScrollOff Constraint
   :id: INV-VIEW-002
   :tags: viewport, scrolloff
   :links: FR-INIT-005

   A non-negative integer :term:`scrollOff` must be defined. To ensure a valid :term:`viewport height` exists,
   the condition ``2 * scrolloff < display_height`` must strictly hold true.

.. inv:: Window Bounds
   :id: INV-VIEW-003
   :tags: viewport, boundaries

   The visible :term:`window` is defined by a :term:`window start` index (representing the first visible
   :term:`visual line` index).

   The :term:`window` must always be contained within the available :term:`visual lines <visual line>`.
   The valid range is:

      ``0 <= window_start <= max(0, num_visual_lines - display_height)``.

.. inv:: Viewport Subset
   :id: INV-VIEW-004
   :tags: viewport, boundaries

   The :term:`viewport` is the subset of the :term:`display lines <display line>` excluding the top and bottom :term:`scrollOff` lines:
   ``[scroloff, viewport_height + scrolloff]``.

   The :term:`viewport height` is strictly ``display_height - (2 * scrolloff)`` and positive.

4.5.3 Preconditions
-------------------

The system requires an initialized :term:`text buffer` that has been successfully mapped into
:term:`visual lines <visual line>` according to the :doc:`Wrapping Specification <f-req_text_wrapping>`.

4.5.4 Stimulus/Response Sequences
---------------------------------

* **Stimulus:** The :term:`cursor` is moved to a new position within the bounds of the current :term:`viewport`.

  **Response:** The system requires no scrolling action; the :term:`window` remains unchanged.

* **Stimulus:** The :term:`cursor` is moved to a position outside the current :term:`viewport`
  (into the :term:`scrollOff` region or beyond).

  **Response:** The system adjusts the :term:`window start` by the minimal amount required to include the new
  :term:`cursor` position within the :term:`viewport`.

* **Stimulus:** Text is deleted, reducing the total number of :term:`visual lines <visual line>` such that the current
  :term:`window start` violates :need:`INV-VIEW-003`.

  **Response:** The system automatically shifts the :term:`window start` upwards (decreasing the value) until the
  :term:`window` bounds are valid again.

4.5.5 Functional Requirements
-----------------------------

.. freq:: Cursor Window Constraint
   :status: Open
   :id: FR-VIEW-001
   :tags: viewport, scrolloff

   The system must enforce that the :term:`cursor` remains within the :term:`window`/
   :term:`display lines <display line>` at all times.

   In other words: the ``y`` value of the :term:`window coordinate` must be within the range
   ``[0, num_display_lines-1]``. (Together with :need:`INV-CURSOR-003`)
   (Since there is always at least one :term:`logical line` (:need:`INV-TEXT-001`), ``num_display_lines`` will always be at least ``1``.)

.. freq:: Cursor Constraint & Scrolloff
   :status: Open
   :id: FR-VIEW-002
   :tags: viewport, scrolloff

   The system must enforce that the :term:`cursor` remains within the :term:`viewport` whenever mathematically possible.

   This constraint must only be relaxed (allowing the :term:`cursor` into the :term:`scrollOff` region) when the
   :term:`window start` has reached the absolute start or end of the :term:`text buffer` and prevent the :term:`window`
   from scrolling further
   (i.e., when ``window_start == 0`` or ``window_start == max(0, len(visual_lines) - display_height)``).

.. freq:: Minimal Scroll Adjustment
   :status: Open
   :id: FR-VIEW-003
   :tags: viewport, scrolling
   :links: FR-VIEW-002

   When adjusting the :term:`window`, the system must change the :term:`window start` index by the absolute minimum
   amount required to satisfy :need:`FR-VIEW-002`.

.. freq:: Non-Destructive Scrolling
   :status: Open
   :id: FR-VIEW-004
   :tags: viewport, scrolling
   :links: FR-CURSOR-005

   Scrolling operations must adjust only the :term:`window start` index, :term:`window coordinate` and the
   :term:`display lines <display line>`. They are a purely visual mechanism and must not change the
   :term:`Absolute Index`, :term:`Logical <Logical Coordinate>`, or :term:`Visual Coordinates <Visual Coordinate>` of
   the :term:`cursor`, nor modify the :term:`text buffer`.

   Scrolling operations may adjust the :term:`Window Coordinate` ``[x, y]`` of the :term:`cursor` only in some cases.
