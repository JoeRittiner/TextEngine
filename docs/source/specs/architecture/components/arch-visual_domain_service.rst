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

The ``VisualDomainService`` owns the ``VisualLogicalAdapter`` and ``CursorState``
instances. These are the two stateful components of the Visual Domain; all persistent
state in the domain lives inside them. ``MovementResolver`` is stateless and is not owned
in any meaningful sense, it has no lifecycle that the service needs to manage.

Behaviour
.........

**Pass-through operations.** Read operations for wrapped visual output, and visual-to-logical
mapping are delegated without modification to the ``VisualLogicalAdapter``. The service's only
obligation for these is to ensure that no read operation modifies any state.
(:need:`INV-MODE-001`, :need:`FR-CURSOR-001`)

**Cursor representations.** The ``VisualDomainService`` is the owner of three cursor
representation interfaces, because it holds both the cursor state and the translation
machinery needed to fulfil them:

* *Visual coordinate:* retrieved directly from ``CursorState``. (:need:`FR-CURSOR-004`)
* *Absolute index:* retrieved from ``CursorState`` and translated via the
  ``VisualLogicalAdapter``. (:need:`FR-CURSOR-002`)
* *Logical coordinate:* retrieved from ``CursorState`` and translated via the
  ``VisualLogicalAdapter``. (:need:`FR-CURSOR-003`)

All three are read-only operations and must not modify any state. (:need:`INV-MODE-001`)

**Cursor movement.** Movement commands are orchestrated across three steps: retrieve the
current valid position from ``CursorState``; pass it along with the command and the
current visual lines to ``MovementResolver``; set the result back on ``CursorState``.
(:need:`FR-CURSOR-020`) The service does not perform movement logic or position validation
itself.

**Text mutation and cursor update.** Mutation operations require post-mutation cursor
management, and the rule differs per operation, making this the service's primary
non-trivial orchestration responsibility:

* *Insert:* pass the current cursor position and the text to the ``VisualLogicalAdapter``,
  which delegates the mutation and refreshes the wrapping map; then advance the cursor to
  immediately after the inserted characters.
  (:need:`FR-TEXT-012`, :need:`FR-TEXT-015`, :need:`FR-TEXT-017`)
* *Delete:* pass the current cursor position to the ``VisualLogicalAdapter`` for
  delegation; the cursor position is unchanged.
  (:need:`FR-TEXT-022`, :need:`FR-TEXT-023`)
* *Backspace:* pass the current cursor position to the ``VisualLogicalAdapter`` for
  delegation; then move the cursor one position to the left.
  (:need:`FR-TEXT-031`, :need:`FR-TEXT-032`, :need:`FR-TEXT-033`)

In all three cases, the ``VisualLogicalAdapter`` is responsible for translating the visual
coordinate, issuing the mutation to the Logical Domain, and refreshing the wrapping map
before returning. The service does not manage map consistency directly.

**Newline insertion and deletion at wrapped boundaries.** :need:`FR-CURSOR-011` and
:need:`FR-CURSOR-012` require specific cursor behaviour when newlines are inserted or
deleted at visual line boundaries. These cases require no additional logic in the service
beyond the standard mutation-and-update sequence described above: the
``VisualLogicalAdapter``'s coordinate recalculation after the mutation produces the
correct cursor position as a natural consequence. This is a deliberate architectural
reliance, not an omission.

Dependencies
............

**Depends on:** ``VisualLogicalAdapter``, ``CursorState``, and ``MovementResolver``. The
service does not depend on the ``LogicalDomainService`` directly. All Logical Domain
contact passes through the ``VisualLogicalAdapter``.

**Depended on by:** The Display Domain, which calls the ``VisualDomainService`` for all
text reads, text mutations, and cursor movement. No component in the Display Domain
interacts with any Visual Domain component directly.

Key Invariants
..............

* **Coordinate synchronisation.** At every point where the service returns a value to its
  caller, all coordinate representations (Absolute Index, Logical, Visual) must
  bijectively map to the same underlying buffer position. The service is the only
  component where a violation of this invariant could go undetected, because it is the
  only component with access to all coordinate spaces simultaneously.
  (:need:`INV-CURSOR-003`)

* **Cursor not bypassed.** No text mutation operation may be performed without the service
  first retrieving the current cursor position and using it as the target. A mutation
  issued at an arbitrary position, bypassing ``CursorState``, violates the contract of
  the public API and breaks coordinate synchronisation. (:need:`FR-CURSOR-001`)

* **Read-only operations are non-destructive.** No read operation, output in any mode,
  cursor representation in any coordinate space, may modify the text buffer, cursor
  position, or wrapping map. (:need:`INV-MODE-001`)
