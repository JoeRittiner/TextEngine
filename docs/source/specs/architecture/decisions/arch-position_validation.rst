Cursor Position Validation
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. Aim for one record per non-obvious choice.
   Examples of decisions worth recording for this project:
   - Why a Facade pattern rather than a flat module of functions.
   - Whether Cursor is a class with its own state or a value computed from TextBuffer's state.
   - Whether WrapEngine is stateful (caches results) or stateless (recalculates on every call).
   - Whether components may call each other directly or only through the Facade.

Context
.......

:need:`INV-CURSOR-001` requires that the cursor always refers to a valid position within
the bounds of the text buffer. There are two distinct events that can invalidate a
previously valid cursor position:

* **Cursor movement.** A movement command produces a new target position that may be
  out of bounds. For example, moving up from a longer visual line to a shorter one, or
  moving right at the last column of a visual line.
* **Buffer mutation.** An insert, delete or backspace operation changes the visual line
  structure. The cursor position is not updated by the mutation itself; it may now refer
  to a column that no longer exists on its line, or a line that no longer exists at all.

These two triggers are independent: a movement command does not change the buffer, and a
buffer mutation does not necessarily change the cursor's intended position. Any design that
assigns validation responsibility to a single component must handle both cases cleanly,
without splitting the invariant or requiring the cursor to be notified of buffer changes
it did not cause.

Decision
........

Cursor position validation is the responsibility of the ``CursorState`` component,
enforced lazily on read. ``CursorState`` holds a raw stored position that may be
transiently invalid between operations. When ``get_position`` is called, ``CursorState``
retrieves the current visual line structure from the ``WrapEngine``, clamps its stored
position to the nearest valid coordinate, and returns the corrected value. The internal
state is updated to the clamped value at the same time.

The ``WrapEngine`` does not perform clamping. If a caller passes an out-of-bounds position
to the ``WrapEngine`` for translation, the ``WrapEngine`` raises an exception. It is a
pure coordinate translator, not a position corrector.

The ``MovementResolver`` is a stateless calculator that computes a new visual coordinate
given a direction and the current visual line structure. It produces positions that are
correct by construction. It applies line-boundary wrapping and line-length checks as part
of movement computation. It does not set ``CursorState`` directly. The
``VisualDomainService`` orchestrates: it retrieves the clamped current position from
``CursorState``, passes it to ``MovementResolver``, and sets the result back on
``CursorState``.

Rationale
.........

Enforcing the invariant lazily on read concentrates the validity guarantee in one place
without requiring any component to be notified of changes it did not cause. When the
buffer mutates, the ``CursorState``'s stored position becomes transiently stale, but no
notification or coordination is needed. The next read corrects it automatically. This is
the structural property that resolves the two-trigger problem: both cursor movement and
buffer mutation are handled by the same mechanism, at the same point, without special
cases.

Keeping the ``WrapEngine`` as a pure translator (throwing on invalid input rather than
correcting it) preserves its single responsibility and prevents cursor semantics from
leaking into the coordinate translation layer. The ``WrapEngine`` does not need to know
what a valid cursor position is; it only needs to know how to translate between coordinate
spaces.

Making ``MovementResolver`` a pure calculator, with no reference to ``CursorState``,
means movement logic can be tested entirely independently of cursor state management.
A movement test needs only a position, a direction, and a set of visual lines. Having the
``VisualDomainService`` orchestrate the handoff between the two components keeps the
coupling explicit and unidirectional.

Alternatives Considered
.......................

**WrapEngine clamps rather than throws.**
  The ``WrapEngine`` could expose a clamp operation, accepting any position and returning
  the nearest valid one. This was rejected because it would give the ``WrapEngine``
  knowledge of cursor semantics, what "nearest valid" means for a cursor is a
  cursor-level concept, not a coordinate-translation concept. It also would not resolve
  the two-trigger problem on its own: the ``WrapEngine`` is unaware of cursor movement,
  so it could not enforce the invariant after a movement command without additional
  orchestration.

**VisualDomainService clamps after every operation.**
  The ``VisualDomainService`` could call a clamp function after every mutation and every
  movement, guaranteeing the cursor is valid immediately after each operation rather than
  lazily on read. This was rejected because it makes the validity guarantee dependent on
  the service remembering to clamp after every operation. Adding a new operation type that
  forgets the clamp step would silently break the invariant. The lazy approach makes the
  guarantee self-enforcing within ``CursorState`` itself.

**CursorState is notified of buffer changes by VisualDomainService.**
  The ``VisualDomainService`` could explicitly notify ``CursorState`` whenever the buffer
  mutates, triggering an immediate revalidation. This was rejected because it requires an
  active notification path that can be missed. The lazy approach achieves the same
  outcome (the cursor is valid when read) without requiring a notification contract.

**Split validation: WrapEngine validates movement, CursorState validates on read.**
  Validation could be split between two components, each handling one trigger. This was
  rejected because split responsibility means the invariant is only fully enforced when
  both halves work correctly together. The single lazy-read mechanism in ``CursorState``
  handles both triggers without coordination.

Consequences
............

**Easier:**

* The validity guarantee is self-enforcing. ``CursorState`` does not depend on being
  notified of external changes; it corrects itself on the next read regardless of what
  caused the staleness.
* ``MovementResolver`` is a pure calculator and can be tested in complete isolation from
  cursor state. Movement logic is fully exercisable with a position, a direction, and a
  series of line lengths.
* The ``WrapEngine`` remains a pure translator. No cursor concepts enter the coordinate
  translation layer.

**Constrained or made harder:**

* ``CursorState``'s stored position may be transiently invalid between a buffer mutation
  and the next ``get_position`` call. This is acceptable as long as the stored position is
  never exposed directly. All access must go through ``get_position``. If this access
  discipline is ever broken, the invariant fails silently.
* Every ``get_position`` call incurs the cost of retrieving visual lines from the
  ``WrapEngine`` and checking the stored position against them. For the expected usage
  pattern of reading the cursor position infrequently relative to the number of operations,
  this is acceptable. If ``get_position`` were called in a tight loop, the repeated
  retrieval would be unnecessary overhead.
* The ``VisualDomainService`` must coordinate the ``MovementResolver`` → ``CursorState``
  handoff correctly. The two components do not know each other; the service is the only
  place where a programming error in the handoff could corrupt the cursor state.
