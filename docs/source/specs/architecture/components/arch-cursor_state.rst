CursorState
~~~~~~~~~~~

Responsibility
..............

``CursorState`` is the authoritative store for the cursor's position, expressed as an Absolute Index.
(:need:`FR-CURSOR-001`)

Owned State
...........

``CursorState`` owns one piece of state: the cursor's position ``abs_index``.
This is the ground truth for cursor position within the Logical Domain.

This state is updated upon ``move_*`` commands, as well when the buffer is mutated by
``insert`` or ``backspace``. (:need:`FR-CURSOR-020`, :need:`FR-TEXT-011`, :need:`FR-TEXT-021`)

Though it holds no reference to the buffer. It must be informed of buffer mutations for ``insert``
and ``backspace`` commands.

Behaviour
.........

**On set.** ``CursorState`` accepts a new absolute index and stores it. It operates under the invariant
that the ``LogicalDomainService`` pre-validates explicit sets, throwing an error before invalid indices
reach this component.

**On get.** The ``CursorState`` returns the stored absolute index without validation.
The caller is responsible for ensuring the position is valid given the current buffer state.

**Move.** ``CursorState`` offers an interface for moving horizontally and to ends. (``move_home``
and ``move_end``) These are coordinated by the ``LogicalDomainService``, which treats out-of-bounds results
as no-ops to ensure this state component never holds an invalid absolute index.

**Initialisation.** The initial cursor position is supplied as an Absolute Index by the
host application (:need:`FR-INIT-001`, :need:`FR-INIT-006`). An out-of-range value or incorrect type
raises an exception and halts initialisation (:need:`FR-INIT-013`).

Dependencies
............

**Depends on:** Nothing.

**Depended on by:** The ``LogicalDomainService``, which is the only component that calls
``get_position`` or sets a new position on ``CursorState``.

Key Invariants
..............

* **Inter-character positioning.** The cursor always refers to a position between
  characters, never on a character. (:need:`INV-CURSOR-002`)

* **Non-destructive.** Reading or updating the cursor position never modifies the text
  buffer. (:need:`FR-CURSOR-021`)
