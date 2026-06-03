Layer Reads
~~~~~~~~~~~~~~~~~~~~~

.. TODO Finish

Context
.......

.. What situation or question forced this decision? What were the competing pressures?

The Facade must expose read interfaces to the host application in all four output modes:
Display, Wrapped, Logical, and Raw (see :ref:`req_software_interfaces`).

The domain architecture is layered. The Display Domain depends on the Visual Domain, and
the Visual Domain depends on the Logical Domain. A straightforward interpretation of this
layering would allow the Facade to communicate only with the Display Domain, requiring all
read requests to flow through each intermediate layer.

However, not all information belongs naturally to every layer. For example, logical
coordinates and absolute buffer indices are concepts used by the Visual and Logical
Domains but are not required by the Display Domain itself. Requiring all reads to pass
through every layer would force intermediate domains to expose and forward information
that is outside their responsibilities.

The design must balance architectural layering against clear ownership of read
responsibilities.

Decision
........

.. What did you decide? State it plainly and unambiguously.

The Facade holds direct references to the Display, Visual, and Logical Domain Services
and may query each service directly for read operations.

Each domain service exposes the read interfaces that correspond to the concepts it owns:

* The Display Domain exposes display-oriented representations.
* The Visual Domain exposes wrapped-line representations and visual cursor information.
* The Logical Domain exposes logical text representations.

The Visual Domain also exposes absolute buffer indices and logical coordinates derived
from the current visual cursor position. These values are provided by the Visual Domain
because it owns the cursor state and the translation between visual and logical
coordinate spaces.

Direct access from the Facade to lower layers is permitted only for read operations.
Write operations must continue to follow the normal domain-service boundaries so that all
required state updates and invariants are enforced.

Rationale
.........

.. Why did you make this choice? What properties does it give you?

Allowing the Facade to read directly from the domain that owns a piece of information
keeps responsibilities localized and avoids creating pass-through interfaces whose only
purpose is to forward data upward through the architecture.

For example, if the Facade could access only the Display Domain, obtaining an absolute
buffer index would require the request to pass through the Display Domain to the Visual
Domain and potentially onward to the Logical Domain before returning the result. The
Display Domain would become responsible for exposing concepts it neither owns nor uses.

Direct reads preserve separation of concerns. Each domain remains responsible only for
the concepts within its own scope, while the Facade serves as the aggregation point that
presents those concepts to external callers.

Restricting the bypass to read operations preserves the integrity of the layered
architecture. Reads observe state; writes modify state. Allowing writes to bypass
intermediate layers would risk skipping coordination logic, state synchronization, or
invariant enforcement that those layers are responsible for.

Alternatives Considered
.......................

.. What other options did you evaluate and why did you reject them?

**All reads pass through the domain layers.**

The Facade could communicate exclusively with the Display Domain, with each lower layer
exposing pass-through interfaces for information owned by deeper layers.

This was rejected because it forces domains to expose concepts outside their
responsibilities. The Display Domain would need to provide access to logical positions,
absolute indices, and other information that it does not use itself. The resulting
interfaces would primarily exist to relay data rather than to encapsulate domain
behavior.

The approach does have one advantage: all access follows the same architectural path,
making it impossible for callers to accidentally bypass a layer. However, this benefit
was judged less important than maintaining clear ownership of read responsibilities.

Consequences
............

.. What does this decision make easier? What does it constrain or make harder?
   Every architectural decision is a trade-off — if you cannot think of a consequence,
   you have not thought about it hard enough.

**Easier:**

* Each domain exposes only the information it owns. Intermediate layers do not need
  forwarding interfaces for unrelated concepts.
* The Facade can obtain information directly from the source of truth rather than through
  multiple layers of delegation.
* Domain boundaries remain aligned with domain responsibilities, improving clarity and
  maintainability.

**Constrained or made harder:**

* The Facade is aware of multiple domain services rather than only the topmost layer,
  increasing its coupling to the overall architecture.
* Architectural layering is no longer enforced uniformly for reads. Developers must
  understand that direct access is permitted only for observation, not modification.
* Write operations require discipline. If future code bypasses layers for writes, state
  synchronization and invariant enforcement may be broken. The distinction between
  permitted read bypasses and prohibited write bypasses must therefore remain explicit.
