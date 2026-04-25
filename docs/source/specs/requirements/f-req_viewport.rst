4.4 Viewport & Scrolling
========================

4.4.1 Description and Priority
------------------------------
**Priority: Low**

The window defines the total visible height, limiting the maximum number of :term:`visual lines <visual line>` that
can be displayed at once.

The :term:`viewport` acts as a virtual boundary within that window. It constraints where the :term:`cursor` can move
before triggering a scroll.

:term:`ScrollOff` defines the margin: the number of :term:`visual lines <visual line>` that must remain visible above
and below the :term:`cursor`. The :term:`cursor` is only allowed to enter the scrollOff margins if it is near the
absolute start or end of the document where scrolling further is impossible.

The visible window range is automatically updated in response to :term:`cursor` movement and text manipulation.

4.4.2 State Invariants
----------------------

.. inv:: Display Dimensions
   :id: INV-VIEW-001
   :tags: viewport, state

   A positive integer ``display_height`` must be defined at system initialization. It dictates the maximum number of
   :term:`visual lines <visual line>` the system can render at any given time.

   **Note:** If dynamic resizing is needed by a user, the system must be re-initialized with a new ``display_height``.

.. inv:: ScrollOff Constraint
   :id: INV-VIEW-002
   :tags: viewport, scrolloff

   A non-negative integer ``scrolloff`` must be defined. To ensure a valid :term:`viewport` exists,
   the condition ``2 * scrolloff < display_height`` must strictly hold true.

.. inv:: Window Bounds
   :id: INV-VIEW-003
   :tags: viewport, boundaries

   The visible window is defined by a ``window_start`` index (representing the first visible :term:`visual line` index).
   The window must always be contained within the available :term:`visual lines <visual line>`.
   The valid range is:

      ``0 <= window_start <= max(0, num_visual_lines - display_height)``.

.. inv:: Viewport Subset
   :id: INV-VIEW-004
   :tags: viewport, boundaries

   The :term:`viewport` is the subset of the window excluding the top and bottom ``scrolloff`` lines.

   The :term:`viewport height` is strictly ``display_height - (2 * scrolloff)``.

   The :term:`viewport` must always be fully contained within the window.

4.4.3 Preconditions
-------------------

The system requires an initialized :term:`text buffer` that has been successfully mapped into
:term:`visual lines <visual line>` according to the :doc:`Wrapping Specification <f-req_text_wrapping>`.

4.4.4 Stimulus/Response Sequences
---------------------------------

* **Stimulus:** The :term:`cursor` is moved to a new position within the bounds of the current :term:`viewport`.

  **Response:** The system requires no scrolling action; the window remains unchanged.

* **Stimulus:** The :term:`cursor` is moved to a position outside the current :term:`viewport`
  (into the scrolloff region or beyond).

  **Response:** The system adjusts ``window_start`` by the minimal amount required to include the new :term:`cursor`
  position within the :term:`viewport` (respecting document boundaries).

* **Stimulus:** Text is deleted, reducing the total number of :term:`visual lines <visual line>` such that the current
  ``window_start`` violates :need:`INV-VIEW-003`.

  **Response:** The system automatically shifts ``window_start`` upwards (decreasing the value) until the window bounds
  are valid again.

4.4.5 Functional Requirements
-----------------------------

.. freq:: Cursor Constraint & Scrolloff
   :id: FR-VIEW-001
   :tags: viewport, scrolloff

   The system must enforce that the :term:`cursor` remains within the :term:`viewport` whenever mathematically possible.
   This constraint must only be relaxed (allowing the :term:`cursor` into the scrolloff region) when the document
   boundaries prevent the window from scrolling further
   (i.e., when ``window_start == 0`` or ``window_start == total_visual_lines - display_height``).

.. freq:: Minimal Scroll Adjustment
   :id: FR-VIEW-002
   :tags: viewport, scrolling

   When adjusting the window to satisfy :need:`FR-VIEW-001`, the system must change the ``window_start`` index by the
   absolute minimum amount required to bring the target :term:`visual line` back into the :term:`viewport`.

.. freq:: Non-Destructive Scrolling
   :id: FR-VIEW-003
   :tags: viewport, scrolling
   :links: FR-CURSOR-004

   Scrolling operations must strictly adjust the ``window_start`` index. They must be a purely visual mechanism and
   must not change the Absolute Index, Logical or Visual Coordinates of the :term:`cursor`,
   nor modify the :term:`text buffer`.

   Scrolling operations may adjust the Window Coordinate ``[x, y]`` of the :term:`cursor`.
