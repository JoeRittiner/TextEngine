Logical Domain Service
~~~~~~~~~~~~~~~~~~~~~~

Responsibility
..............

The Logical Domain Service is the sole external interface of the Logical Domain. It
exposes the domain's two canonical text representations: raw string and logical lines,
and translates between absolute indices and logical coordinates for mutation operations.
No component outside the Logical Domain interacts with the TextBuffer directly.

Owned State
...........

The Logical Domain Service owns two pieces of state: the ``TextBuffer`` instance and ``CursorState``.
Ownership here means the service is the only component that holds a reference to them and
the only component through which the they are mutated or queried.

The service owns no independent data of its own. It is not a pure calculator. It holds
the ``TextBuffer`` and ``CursorState``, but all persistent states live inside those instances.

Behaviour
.........

**Text representations.** The service exposes two read interfaces derived from the
TextBuffer's raw string:

* **Raw output:** the buffer contents returned as a single unmodified string, including
  all ``\n`` characters. (:need:`FR-MODE-001`)
* **Logical line output:** the buffer contents split at ``\n`` boundaries, with the
  newline characters themselves excluded from the returned strings.
  (:need:`FR-MODE-011`, :need:`FR-TEXT-016`, :need:`FR-TEXT-025`, :need:`FR-TEXT-035`)

**Cursor state.** The service provides read and write interfaces to the ``CursorState`` instance:

* **Get & Set:** Before setting and before returning, the Service validates the cursor's
  position in the buffer. (:need:`INV-CURSOR-001`)
* **Move:** Horizontal movement is validated and clamped to the buffer's bounds.
  (:need:`FR-CURSOR-020`, :need:`FR-CURSOR-052`, :need:`FR-CURSOR-053`)

**Coordinate translation.** The service translates between absolute indices and logical
coordinates ``(row, col)`` for all mutation operations. Neither the ``TextBuffer`` nor the
Visual Domain performs this translation. This translation is also the mechanism through
which the system satisfies its cursor representation interfaces: returning the cursor as
an absolute index (:need:`FR-CURSOR-002`) or as a logical coordinate
(:need:`FR-CURSOR-003`) both depend on the Logical Domain Service's ability to convert
between these two spaces on demand.

The Logical Domain is a cursor-centric model and only supports text manipulation at the cursor
position. (:need:`FR-CURSOR-001`)

**Mutation delegation.** ``insert``, ``delete``, ``backspace`` and ``move_*`` operations are
validated at the service boundary. Inputs are type-checked, and values of incorrect types are
rejected with an exception (:need:`FR-INIT-013`). The operation is then delegated to the
``TextBuffer`` or ``CursorState``.

Dependencies
............

**Depends on:** The ``TextBuffer`` and ``CursorState`` components for all text storage and
mutation and cursor state management. The service has no other engine dependencies.

**Depended on by:** The Visual Domain. The Visual Domain calls the ``LogicalDomainService``
for all text reads and writes and horizontal cursor movement. It never accesses the
``TextBuffer`` or ``CursorState`` directly.

Key Invariants
..............

* **Strict encapsulation.** The internal components must never be exposed outside the
  Logical Domain. All reads and mutations from a higher Domain pass through this
  service's interface. If this invariant is broken, the coordinate-consistency and
  output-stability guarantees below become unenforceable.

* **Output stability.** Raw and logical line output are pure functions of the TextBuffer's
  current state. Repeated queries with no intervening mutation return identical results.
  (:need:`INV-MODE-002`)

* **Coordinate consistency.** For any buffer position, the Absolute Index and ``(line, col)``
  returned by the service always refer to the same position between characters.
  (:need:`INV-CURSOR-003`)
