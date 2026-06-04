Cursor Belongs to the Visual Domain
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Context
.......

The editor architecture is divided into three domain layers. Data flows upward through these layers
(Logical → Visual → Display), while requests flow downward.

A design question emerged regarding ownership of the cursor. At first glance, the cursor appears to
belong naturally to the Logical Domain because its position can be represented fundamentally as an
absolute index into the text buffer. Because this absolute index must remain valid relative to the text
buffer, the cursor is tightly coupled to logical text mutations.

However, cursor movement requirements (such as moving vertically across wrapped lines
(:need:`FR-CURSOR-030`)) are primarily visual in nature. This creates architectural tension between:

* Keeping cursor state close to the underlying text buffer source of truth.
* Preserving strict, unidirectional dependencies between domains.
* Avoiding unnecessary layout translation responsibilities within lower-level components.

Decision
........

The cursor belongs in the **Visual Domain**.

The Logical Domain remains responsible only for text storage and mutation through absolute indices;
it does not require or expose a cursor abstraction. Text mutation operations require only an absolute
index, meaning a cursor is not fundamental to logical text storage.

The cursor stores its position as a visual coordinate; any translation to an absolute index for mutation
purposes is performed by the ``VisualLogicalAdapter``.

The cursor is not placed in the Display Domain because the Visual Domain already defines the editor-wide
visual coordinate system. The Display Domain merely presents a truncated window of that visual
representation.

Rationale
.........

Vertical and horizontal cursor movements depend entirely on visual layout information that the Logical Domain
has no awareness of. If the cursor were placed in the Logical Domain, calculating a simple upward or downward
movement would incur a heavy translation cost:

1. Reading the current position as an absolute index from the Logical Domain.
2. Translating that absolute index into a visual coordinate via the Visual Domain.
3. Calculating the target visual position.
4. Validating the target visual position against wrapped visual lines.
5. Translating the resulting visual position back into an absolute index.
6. Updating the logical position back in the Logical Domain.

This flow is highly inefficient and breaks domain isolation. Because the Visual Domain already owns the
wrapped line structures and visual coordinate systems, keeping both the cursor state and the movement
calculation logic within the Visual Domain removes the need for index translation during live movement.

The actual, streamlined movement flow operates entirely within visual space:

1. **Read** the current visual coordinate from ``CursorState`` (enforcing lazy clamping;
   see :doc:`arch-position_validation`).
2. **Pass** the coordinate along with the direction and current visual lines to the ``MovementResolver``.
3. **Compute** the new valid visual coordinate inside the ``MovementResolver``.
4. **Update** the result back onto ``CursorState`` via the orchestration of the ``VisualDomainService``.

Placing the cursor in the Logical Domain instead would require the Logical Domain to become aware of visual
line concepts, force a lower-layer component to depend on a higher-layer service, or necessitate a complex
coordination layer solely to bridge the two domains.

The cursor is better understood as a visual interaction construct that references logical text positions
rather than as a fundamental property of the logical text model itself.

Alternatives Considered
.......................

**Cursor in the Logical Domain**
  The cursor could have been represented purely as an absolute index alongside the text buffer. Vertical
  movement across visual lines would be calculated on demand based on line lengths and display width.
  This was rejected because cursor movement semantics depend on visual layout information (e.g., wrapped
  lines and visual coordinates). Implementing movement logic in the Logical Domain would either violate
  the dependency direction rule or require additional translation logic to leak downwards.

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

* Keeps visual movement logic and coordinate translation encapsulated within a single domain layer.
* Preserves a strict, unidirectional dependency direction: Display → Visual → Logical. The Logical Domain
  remains completely independent of visual layout and wrapping concerns.
* Keeps the text mutation engine flexible and clean, as text operations are not coupled to the existence
  of a cursor abstraction.
* Enhances testability by isolating state from calculation; ``CursorState`` and ``MovementResolver`` exist
  as distinct, specialized components within the same domain.

**Harder:**

* The Visual Domain must maintain translation logic between visual coordinates and logical indices for when
  mutations occur.
* Any buffer mutation that changes the wrapping map may silently invalidate the stored visual coordinate,
  requiring revalidation on the next cursor read.
* Operations that appear logically simple, such as cursor movement, now require coordination with visual
  layout structures even when the underlying text buffer remains entirely unchanged.
