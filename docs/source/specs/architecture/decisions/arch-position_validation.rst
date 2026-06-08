Cursor Position Validation
~~~~~~~~~~~~~~~~~~~~~~~~~~

Context
.......

The system must guarantee that the cursor always refers to a valid position within the bounds of the text buffer.
(:need:`INV-CURSOR-001` ) There are two distinct events that can invalidate a previously valid cursor position:

* **Cursor movement.** A movement or set command alters the coordinate, which could potentially push it past the
  boundaries of the text.
* **Buffer mutation.** Insertions, or backspaces modify the text length and move the cursor. Buffer modification
  and cursor movement must be synchronized for these events.

Because the cursor is tracked as a stable absolute index, (``abs_index``) a valid cursor position is strictly bounded
by the linear sequence of characters: ``0 <= k <= len(text)``. The system needs a predictable strategy to enforce this
boundary during state reads and writes.

Decision
........

Cursor position validation is the exclusive responsibility of the **``LogicalDomainService``**. The ``CursorState``
component itself is completely decoupled from validation logic and functions as a raw data store.

The ``LogicalDomainService`` intercepts all operations to enforce the boundary check ``0 <= k <= len(text)`` at the
service boundary under two strict modes of execution:

1. **On Set / Move:** The ``LogicalDomainService`` intercepts all position modifications and branches its validation
   behavior based on the command type:

   * *Explicit Sets:* An explicit ``set(k)`` command validates the index. If ``k`` falls outside
     ``0 <= k <= len(text)``, the service strictly throws an exception (e.g., ``ValueError`` or ``IndexError``)
     and rejects the write.
   * *Movement Commands:* Relative or structural logical adjustments (``move_*``) evaluate the target index before
     committing. If the target falls out of bounds, the service intercepts it and processes the command as a safe
     **no-op**, leaving the cursor state unchanged.
2. **On Get:** Whenever the cursor position is read, the ``LogicalDomainService`` checks the stored absolute index
   against the current text length. Under normal conditions, mutations and sets keep this index completely
   synchronized. If an out-of-bounds index is detected during a read operation, it indicates a critical state anomaly,
   and the service immediately raises a specific exception (e.g., ``ValueError`` or ``IndexError``).

Rationale
.........

Moving validation logic out of ``CursorState`` and into the service layer aligns perfectly with a stateless,
absolute-index-centric model. Because validation has been reduced to a trivial length check (``len(text)``), it can be
executed eagerly with virtually zero performance overhead.

* **Symmetric Service Enforcement:** Centralizing validation inside the ``LogicalDomainService`` creates a highly
  predictable boundary. The domain guarantees that bad inputs are normalized before hitting the state layer on writes,
  while treating un-normalized data on reads as an exceptional breach of domain logic rather than a normal operational
  condition.
* **Decoupling State from Context:** ``CursorState`` no longer needs access to the buffer contents or layout maps to
  evaluate its own position. It remains an isolated primitive container that depends on nothing, making it highly
  robust and trivial to maintain.

Alternatives Considered
.......................

**Lazy Validation on Read via Visual Lines (Previous Architecture)**
  The system previously treated cursor validation as a lazy operation deferred until ``get_position()`` was called.
  Under that model, ``CursorState`` held a raw, transiently invalid visual coordinate ``(row, col)`` and dynamically
  verified it by querying visual lines from the ``VisualLogicalAdapter`` on every read. This was rejected because it
  introduced a heavy circular dependency from the lowest state layer back up to layout components, resulting in
  unnecessary complexity for a rule that is fundamentally a basic text boundary constraint.

Consequences
............

**Easier:**

* **O(1) Boundary Evaluation:** Validating against a flat buffer sequence length bypasses line wrapping maps entirely.
* **Isolated Component Testing:** ``CursorState`` contains zero branching logic or dependencies, allowing it to be
  tested or swapped effortlessly.
* **Fail-Fast Explicit Integration:** Forcing ``set(k)`` to throw an exception ensures that external domains or
  coordinate adapters cannot accidentally supply corrupt or miscalculated indices without triggering an immediate,
  visible error.
* **Safe Relative Navigation:** Treating out-of-bounds ``move_*`` commands as no-ops simplifies client code in higher
  layers, eliminating the need for callers to constantly check boundary conditions before issuing a step command.

**Harder:**

* **Service Responsibility Load:** The ``LogicalDomainService`` must carefully handle every text mutation path to
  ensure that the matching cursor index changes are applied atomically, preventing valid read paths from accidentally
  triggering an out-of-bounds exception.