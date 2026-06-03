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

The Logical Domain Service owns one piece of state: the TextBuffer instance. Ownership
here means the service is the only component that holds a reference to the TextBuffer and
the only component through which the TextBuffer is mutated or queried.

The service owns no independent data of its own. It is not a pure calculator. It holds
the TextBuffer, but all persistent state lives inside that instance.

Behaviour
.........

**Text representations.** The service exposes two read interfaces derived from the
TextBuffer's raw string:

* **Raw output:** the buffer contents returned as a single unmodified string, including
  all ``\n`` characters. (:need:`FR-MODE-001`)
* **Logical line output:** the buffer contents split at ``\n`` boundaries, with the
  newline characters themselves excluded from the returned strings.
  (:need:`FR-MODE-011`, :need:`FR-TEXT-016`, :need:`FR-TEXT-025`, :need:`FR-TEXT-035`)

**Coordinate translation.** The service translates between absolute indices and logical
coordinates ``(line, col)`` for all mutation operations. Neither the TextBuffer nor the
Visual Domain performs this translation. This translation is also the mechanism through
which the system satisfies its cursor representation interfaces: returning the cursor as
an absolute index (:need:`FR-CURSOR-002`) or as a logical coordinate
(:need:`FR-CURSOR-003`) both depend on the Logical Domain Service's ability to convert
between these two spaces on demand. The cursor itself is not a Logical Domain concept;
the service provides the coordinate machinery, not the cursor state.

**Mutation delegation.** Insert, delete and backspace operations are validated at the
service boundary.Inputs are type-checked, and values of incorrect types are rejected with an exception
(:need:`FR-INIT-013`). The operation is then delegated to the TextBuffer, which applies its own
normalisation rules before modifying the buffer. The service does not duplicate or
override those rules.

Dependencies
............

**Depends on:** The TextBuffer component for all text storage and mutation. The service
has no other engine dependencies.

**Depended on by:** The Visual Domain. The Visual Domain calls the Logical Domain Service
for all text reads and writes. It never accesses the TextBuffer directly.

Key Invariants
..............

* **Strict encapsulation.** The TextBuffer instance must never be exposed outside the
  Logical Domain. All reads and mutations from the Visual Domain pass through this
  service's interface. If this invariant is broken, the coordinate-consistency and
  output-stability guarantees below become unenforceable.

* **Output stability.** Raw and logical line output are pure functions of the TextBuffer's
  current state. Repeated queries with no intervening mutation return identical results.
  (:need:`INV-MODE-002`)

* **Coordinate consistency.** For any buffer position, the Absolute Index and ``(line, col)``
  returned by the service always refer to the same character.  (:need:`INV-CURSOR-003`)