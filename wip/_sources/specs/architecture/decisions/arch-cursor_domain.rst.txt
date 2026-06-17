Cursor Belongs to the Logical Domain
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Context
.......

The editor architecture is divided into three domain layers. Data flows upward through these layers
(Logical → Visual → Display), while requests flow downward.

A design question emerged regarding ownership of the cursor. The cursor's position can be fundamentally
tracked as an absolute index into the text buffer, making it deeply tied to logical text mutations
(such as insertions and deletions). However, vertical cursor movement across wrapped lines requirements
(:need:`FR-CURSOR-030`), depend entirely on layout information managed by the Visual Domain.

This creates an architectural tension between:

* Keeping cursor state close to the text buffer source of truth to ensure state stability during mutations.
* Preserving strict, unidirectional dependencies between domain layers.
* Mitigating translation overhead during directional movement operations.

Decision
........

The cursor belongs in the **Logical Domain**.

The ``CursorState`` component is owned and managed entirely by the ``LogicalDomainService``. It stores the
cursor position using a single primitive value: an absolute index (``abs_index``) into the text buffer.

The Visual Domain contains no persistent cursor state. It borrows the cursor position on demand from the
Logical Domain when executing visual calculations.

Movement operations are split by axis:

1. **Horizontal Movement:** The Visual Domain acts as a pure pass-through, delegating horizontal adjustments
   directly to the Logical Domain to evaluate as absolute index changes.
2. **Vertical Movement:** The ``VisualDomainService`` orchestrates visual adjustments via a multi-step
   translation flow utilizing the ``VisualLogicalAdapter`` and the stateless ``MovementResolver``.

Rationale
.........

Storing the cursor as a visual coordinate ``(row, col)`` in the Visual Domain introduces "lazy validation".
Because a visual coordinate is a derived value dependent on a shifting wrapping map, text mutations can silently
invalidate the cursor's coordinate, forcing a permanent and messy dependency from ``CursorState``
back onto the ``VisualLogicalAdapter``.

Moving the cursor to the Logical Domain as an absolute index provides several structural advantages:

* **State Stability:** An absolute index is a stable primitive. It does not become corrupt or invalid
  when wrapping maps or display widths change.
* **Atomic Mutations:** Text modifications (insertions and deletions) can update both the text buffer and the
  cursor position simultaneously within the same domain layer, eliminating complex cross-domain synchronization
  hooks.
* **Simplified Horizontal Movement:** Because horizontal movement does not inherently require structural layout
  lines, delegating it straight to the Logical Domain bypasses unnecessary layout processing.

While vertical movement now requires an explicit read-translate-resolve-write orchestration flow across domain
boundaries, this overhead is accepted. The reliability of a stable, mutation-safe absolute index outweighs the
cost of performing coordinate translation during live vertical steps.

The vertical movement flow operates cleanly without storing state in the Visual Domain:

1. **Read** the current absolute index from the Logical Domain via the ``VisualLogicalAdapter``.
2. **Translate** the absolute index into a transient visual coordinate using the adapter's wrapping map.
3. **Resolve** the target visual coordinate by passing the position and direction to the stateless ``MovementResolver``.
4. **Translate Back** the calculated target visual coordinate into an absolute index.
5. **Write** the final absolute index back to the ``CursorState`` in the Logical Domain.

Alternatives Considered
.......................

**Cursor in the Visual Domain (Previous Architecture)**
  The cursor was previously modeled as a visual coordinate stored in the Visual Domain to avoid translation
  overhead during directional movements. This was rejected because visual coordinates are derived values.
  Buffer mutations constantly threatened to break the coordinate, requiring a complex lazy validation pattern
  and forcing the state layer to depend heavily on layout components.

**Movement Controller in the Visual Domain, Cursor in the Logical Domain**
  A dedicated movement controller component could have been introduced in the Visual Domain while leaving
  the cursor state itself in the Logical Domain. This was rejected because it violates architectural dependency
  rules: the Logical Domain would be exposed to Visual Domain concepts to reconcile state, or an active
  bidirectional coordination path would be required. The resolution is to place both the state and the resolver
  in the Visual Domain, while maintaining them as separate components to ensure testability.

**Cursor in the Display Domain**
  The cursor could have been modeled relative to window or display coordinates. This was rejected because it
  introduces unnecessary layout abstraction. Lower domains are generally preferred when satisfying an
  architectural invariant, and the Visual Domain already accurately defines the editor-wide coordinate system.

Consequences
............

**Easier:**

* **Stable Truth:** The cursor position is never transiently invalid or desynchronized during text mutations.
* **Clean Visual Domain:** The Visual Domain is entirely stateless regarding the cursor, behaving as a functional
  layout calculator.
* **Encapsulated Mutations:** Core editor operations like text insertion and backspacing process cleanly within a
  single domain block.

**Harder:**

* **Boundary Orchestration:** Vertical movement requires a strict, multi-step orchestration sequence by the
  ``VisualDomainService`` to safely map across the boundary.
* **Adapter Workload:** The ``VisualLogicalAdapter`` must maintain highly accurate, bidirectional translation
  logic (index-to-visual and visual-to-index) to prevent layout drifts during vertical steps.