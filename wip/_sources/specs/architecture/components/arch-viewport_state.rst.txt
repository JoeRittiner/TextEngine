Viewport State
~~~~~~~~~~~~~~

Responsibility
..............

``ViewportState`` determines which visual lines are currently displayable by maintaining
the window's position over the full visual line sequence and scrolling when the cursor
moves outside the viewport.

Owned State
...........

``ViewportState`` owns three pieces of state, all fixed at initialisation except
``window_start``:

* **Display height:** A positive integer defining the maximum number of visual lines the
  display can show simultaneously. (:need:`FR-INIT-004`, :need:`INV-VIEW-001`)
* **ScrollOff:** A non-negative integer defining the number of lines at the top and bottom
  of the display that are visible but outside the viewport. The condition
  ``2 * scrolloff < display_height`` must hold; violations are rejected at initialisation.
  (:need:`FR-INIT-005`, :need:`FR-INIT-011`, :need:`INV-VIEW-002`)
* **Window start:** The index of the first visual line currently in the display window.
  This is the only piece of state that changes during normal operation. It is not
  supplied by the host application; it is derived during initialisation as the smallest
  non-negative value that satisfies :need:`INV-VIEW-003` and :need:`FR-VIEW-001` given
  the initial cursor position. (:need:`FR-INIT-007`)

Viewport height (the subset of the display window excluding the scrolloff margins) is
an invariant derived from ``display_height`` and ``scrolloff``, not independently owned
state. (:need:`INV-VIEW-004`)

**Initialisation validation.** All three host-supplied parameters are validated on
initialisation. A null or incorrectly-typed value raises an exception and halts
initialisation. (:need:`FR-INIT-012`, :need:`FR-INIT-013`) The scrolloff–height conflict
is checked after both individual values have passed their own validation.
(:need:`FR-INIT-011`)

Behaviour
.........

Given the current visual line count, the current cursor's visual coordinate, and the
existing ``window_start``, ``ViewportState`` determines whether ``window_start`` requires
adjustment and returns the displayable range ``[window_start, window_start +
display_height - 1]``.

The scroll decision follows from two constraints. First, the cursor must always be within
the display window. (:need:`FR-VIEW-001`) Second, whenever mathematically possible, the
cursor must be within the viewport (the inner region excluding the scrolloff margins.)
(:need:`FR-VIEW-002`) When the cursor falls outside the viewport, ``window_start`` is
adjusted by the minimum amount needed to bring the cursor back inside.
(:need:`FR-VIEW-003`) The scrolloff constraint is relaxed only when the window has
reached the absolute start or end of the visual line sequence and cannot scroll further.
(:need:`FR-VIEW-002`)

Scrolling is non-destructive: adjusting ``window_start`` does not modify the text buffer,
the cursor's Absolute Index, Logical coordinate, or Visual coordinate.
(:need:`FR-VIEW-004`)

The returned range is always contiguous. Display output is a function of both the buffer
state and the current ``window_start``; the same range returns the same lines for a given
buffer state. (:need:`INV-MODE-003`)

Dependencies
............

**Depends on:** Its inputs only: the visual line count, the cursor's visual coordinate,
and its own owned state. ``ViewportState`` holds no references to any other component.

**Depended on by:** The ``DisplayDomainService``, which owns ``ViewportState``, supplies
it with the current visual line count and cursor position after every operation, and uses
the returned range to slice the displayable lines.

Key Invariants
..............

* **Window bounds.** ``window_start`` is always within the range
  ``0 <= window_start <= max(0, num_visual_lines - display_height)``. This holds at
  initialisation and is maintained after every update. (:need:`INV-VIEW-003`)

* **Cursor within display.** The cursor's visual row is always within the display window.
  That is, within ``[window_start, window_start + display_height - 1]``. This invariant
  is never relaxed. (:need:`FR-VIEW-001`)

* **Cursor within viewport when possible.** The cursor's visual row is within the viewport
  ``[window_start + scrolloff, window_start + display_height - scrolloff - 1]``
  unless the window is near the absolute start or end of the visual line sequence.
  (:need:`FR-VIEW-002`)

* **Immutable configuration.** ``display_height`` and ``scrolloff`` do not change after
  initialisation. A change to either requires re-initialisation. (:need:`INV-INIT-001`)

* **Read-only operations are non-destructive.** Querying the displayable range does not
  modify ``window_start``, the text buffer, or the cursor. (:need:`INV-MODE-001`)
