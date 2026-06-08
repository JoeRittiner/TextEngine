Movement Resolver
~~~~~~~~~~~~~~~~~

Responsibility
..............

``MovementResolver`` translates movement commands into valid visual coordinates, given a
current position and the current visual line structure.

Owned State
...........

``MovementResolver`` is a pure calculator. It owns no state. Every call is fully
determined by its input parameters: a visual coordinate, the movement command,
and visual lines.

Behaviour
.........

``MovementResolver`` accepts a visual coordinate, a direction (:need:`FR-CURSOR-020`),
and the current sequence of visual lines. It returns a visual coordinate that is valid
per :need:`INV-CURSOR-001`. The returned position is correct by construction.
``MovementResolver`` applies all relevant boundary and truncation logic internally, so
the caller receives a position that can be passed directly to the ``VisualLogicalAdapter``
without further validation.

The movement rules are defined in :need:`FR-CURSOR-020`, :need:`FR-CURSOR-030`,
:need:`FR-CURSOR-031`, :need:`FR-CURSOR-040`, :need:`FR-CURSOR-050`,
:need:`FR-CURSOR-051`, :need:`FR-CURSOR-052`, and :need:`FR-CURSOR-053`.

Movement is strictly non-destructive. :need:`FR-CURSOR-021`.

Two aspects are architecturally significant and worth stating explicitly:

**``MovementResolver`` does not implement desired-column retention.**
:need:`NR-CURSOR-101` explicitly excludes this feature. Vertical movement always uses
the current ``v_col``, truncated to the target line's length if necessary. This is stated
here to prevent a future implementor from adding sticky-column logic without a corresponding
requirements change. Should this section contradict updated requirements, assume the
requirements are correct and update this section to align with them.

Dependencies
............

**Depends on:** Its input parameters only. ``MovementResolver`` holds no references to
any other component. The visual lines it requires are passed in by the
``VisualDomainService`` at call time.

**Depended on by:** The ``VisualDomainService``, which supplies the current position and
visual lines, calls ``MovementResolver``, and sets the result via ``VisualLogicalAdapter``.

Key Invariants
..............

* **Output validity.** The coordinate returned by ``MovementResolver`` always satisfies
  :need:`INV-CURSOR-001`.

* **Non-destructive.** ``MovementResolver`` does not modify any component state. It
  computes and returns; nothing else. (:need:`FR-CURSOR-021`)
