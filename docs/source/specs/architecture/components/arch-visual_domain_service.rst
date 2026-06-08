Visual Domain Service
~~~~~~~~~~~~~~~~~~~~~

Responsibility
..............

The ``VisualDomainService`` is the sole external interface of the Visual Domain. It
exposes the domain's text representations and cursor position, and orchestrates all text
mutation and cursor movement operations, supplying the current cursor position so that
callers never need to manage it directly. (:need:`FR-CURSOR-001`)

Owned State
...........

The ``VisualDomainService`` owns the ``VisualLogicalAdapter`` instance. It is the sole
stateful components of the Visual Domain; all persistent state in the domain lives inside it.
``MovementResolver`` is stateless and is not owned in any meaningful sense, it has no
lifecycle that the service needs to manage.

Behaviour
.........

**Pass-through operations.** The service delegates horizontal movement, and text mutation commands
to the ``VisualLogicalAdapter``. The service's only obligation for these is to ensure that no read
operation modifies any state.

**Vertical movement.** Vertical movement commands are orchestrated across three steps: retrieve the
current visual position from ``VisualLogicalAdapter``; pass it, along with the direction and the
current visual lines, to ``MovementResolver``; set the result back through ``VisualLogicalAdapter``.
(:need:`FR-CURSOR-020`) The service does not perform movement logic or position validation
itself.

Dependencies
............

**Depends on:** ``VisualLogicalAdapter``, and ``MovementResolver``. The
service does not depend on the ``LogicalDomainService`` directly. All Logical Domain
contact passes through the ``VisualLogicalAdapter``.

**Depended on by:** The Display Domain, which calls the ``VisualDomainService`` for all
text reads, text mutations, and cursor movement. No component in the Display Domain
interacts with any Visual Domain component directly.

Key Invariants
..............

* **Read-only operations are non-destructive.** No read operation, output in any mode,
  cursor representation in any coordinate space, may modify the text buffer, cursor
  position, or wrapping map. (:need:`INV-MODE-001`)
