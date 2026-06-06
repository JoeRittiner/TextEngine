CursorState
~~~~~~~~~~~

Responsibility
..............

``CursorState`` is the authoritative store for the cursor's position, expressed in visual
coordinates. It guarantees that the position it returns is always valid, clamping its
stored value against the current visual line structure on every read.
(:need:`FR-CURSOR-001`)

Owned State
...........

``CursorState`` owns one piece of state: the cursor's visual coordinate
``(v_row, v_col)``. This is the ground truth for cursor position within the Visual Domain.
The stored value may be transiently invalid between a buffer mutation and the next read;
the valid, corrected value is only guaranteed at the point of retrieval via
``get_position``. The raw stored coordinate must never be exposed directly.

Behaviour
.........

**On set.** ``CursorState`` accepts a new visual coordinate and stores it without
validation. The caller is responsible for passing a position that is correct given the
current buffer state; ``MovementResolver`` provides this guarantee for movement commands.
The stored value may become stale if the buffer is subsequently mutated before the next
read.

**On get.** Before returning the stored coordinate, ``CursorState`` queries the
``VisualLogicalAdapter`` to check whether the stored position is valid. If not, the
``CursorState`` clamps to the nearest valid position per :need:`INV-CURSOR-001` and
:need:`FR-CURSOR-031`, updates the stored value, and returns the corrected coordinate.
Validity is defined by the requirements; the clamping behaviour is architecturally
significant only in that it is *lazy*. Deferred to read time rather than enforced eagerly
after every buffer change. (See: :doc:`../decisions/arch-position_validation`)

**Boundary normalisation.** One position constraint is enforced on both set and get:
:need:`FR-CURSOR-010`, where a cursor at the end of a wrapped line is normalised to
the start of the next line. This normalisation is not a clamping concern. It is a
representational invariant that must hold at all times, not only when the buffer has
changed.

**Initialisation.** The initial cursor position is supplied as an Absolute Index by the
host application and translated to a visual coordinate during initialisation
(:need:`FR-INIT-001`, :need:`FR-INIT-006`). An out-of-range value or incorrect type
raises an exception and halts initialisation (:need:`FR-INIT-013`).

Dependencies
............

**Depends on:** The ``VisualLogicalAdapter``, to retrieve the current visual line structure for
coordinate validation on read. ``CursorState`` does **not** depend on ``MovementResolver``
or the ``VisualDomainService``.

**Depended on by:** The ``VisualDomainService``, which is the only component that calls
``get_position`` or sets a new position on ``CursorState``.

Key Invariants
..............

* **Valid on read.** The coordinate returned by ``get_position`` always satisfies the
  valid visual coordinate ranges defined in :need:`INV-CURSOR-001`. The stored coordinate
  may be transiently outside these ranges, but this is never visible to callers.

* **Inter-character positioning.** The cursor always refers to a position between
  characters, never on a character. (:need:`INV-CURSOR-002`)

* **Non-destructive.** Reading or updating the cursor position never modifies the text
  buffer. (:need:`FR-CURSOR-021`)

* **No direct state exposure.** The raw stored coordinate must only ever be accessed
  through ``get_position``. Any path that exposes it directly bypasses the validity
  guarantee and breaks :need:`INV-CURSOR-001`.
