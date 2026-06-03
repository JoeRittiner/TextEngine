Display Domain Service
~~~~~~~~~~~~~~~~~~~~~~

Responsibility
..............

The ``DisplayDomainService`` is the sole external interface of the Display Domain. It
exposes the displayable subset of visual lines and the cursor in Window coordinates, and
propagates all text mutation and cursor movement operations from the host application to
the Visual Domain, updating the viewport after every operation that changes the cursor
position.

Owned State
...........

The ``DisplayDomainService`` owns the ``ViewportState`` instance. All persistent state in
the Display Domain lives inside it.

Behaviour
.........

**Pass-through operations.** Text mutation and cursor movement operations are delegated
directly to the ``VisualDomainService`` without modification. After any operation that
could change the cursor's visual row, the service updates ``ViewportState`` before
returning. This update is eager, not lazy. (See :ref:`below <eager-viewport-update>`)
(See :doc:`../decisions/arch-eager_viewport_update`) even
when the row did not change.

**Viewport-truncated output.** The service exposes the subset of visual lines currently
within the display window (:need:`FR-MODE-031`) together with metadata indicating which
display lines belong to which logical line. (:need:`FR-MODE-032`) The slicing is
performed by the service using the range returned by ``ViewportState``; the service does
not delegate this to the Visual Domain.

**Window coordinate translation.** The service translates the cursor's Visual coordinate
to a Window coordinate for the cursor representation interface. (:need:`FR-CURSOR-005`,
:need:`INV-CURSOR-001`, :need:`INV-CURSOR-003`) This translation is performed inline:
``window_y = visual_row - window_start`` and ``visual_row = window_y + window_start``.

Dependencies
............

**Depends on:** The ``VisualDomainService``, for all text reads, mutations, and cursor
operations. ``ViewportState``, which it owns.

**Depended on by:** The ``TextEditor`` facade, which is the sole caller of the
``DisplayDomainService``.

Key Invariants
..............

* **Viewport current after every operation.** After any operation that changes the cursor
  position, ``window_start`` is updated before any value is returned to the caller.
  The viewport is never stale at the service boundary. (:need:`INV-VIEW-003`,
  :need:`FR-VIEW-001`)

* **Window output bounded by display height.** The number of lines returned by the
  viewport-truncated output interface never exceeds ``display_height``, and the content
  always corresponds to the range ``[window_start, window_start + display_height]``.
  (:need:`FR-MODE-031`)

* **Coordinate synchronisation.** The Window coordinate returned for the cursor
  bijectively maps to the same underlying buffer position as the Absolute Index, Logical,
  and Visual representations. (:need:`INV-CURSOR-003`)

* **Read-only operations are non-destructive.** No read — display output, cursor
  representation, coordinate translation — modifies the text buffer, cursor position, or
  ``window_start``. (:need:`INV-MODE-001`)
