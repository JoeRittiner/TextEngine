Cursor Belongs to the Visual Domain
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Context
.......

The editor architecture is divided into three domain layers:

1. Logical Domain
2. Visual Domain
3. Display Domain

Data flows upward through the layers, while requests flow downward.

The Logical Domain owns the text buffer and operates on absolute indices.
The Visual Domain is responsible for visual line construction (wrapping).
The Display Domain truncates and presents the visible window.

A design question emerged regarding ownership of the cursor construct.

At first glance, the cursor appears to belong naturally to the Logical Domain because it can be represented as an
absolute index into the text buffer. A source of truth for the cursor position.
Since the absolute index must remain valid relative to the text buffer, the cursor is tightly coupled to logical
text state.

However, cursor movement requirements are primarily visual in nature. For example, vertical cursor movement operates
across visual lines rather than logical lines (:need:`FR-XXX-XX`).

This creates tension between:

* Keeping cursor state close to the text buffer.
* Preserving strict unidirectional dependencies between domains.
* Avoiding unnecessary responsibilities in translation components.

Decision
........

The cursor construct is belongs in the Visual Domain.

The Logical Domain remains responsible only for text storage and mutation through absolute indices.

The cursor may internally reference an absolute index, but cursor behavior, movement, and coordinate semantics are
considered visual concerns.

Rationale
.........

Vertical cursor movement depends on visual layout information.

**Example:** Moving the cursor upward requires:

#. Reading the current position (e.g. as absolute index).
#. Translating the absolute index into visual coordinates.
#. Calculating the target visual position.
#. Validating the target visual position.
#. Translating the resulting visual position back into an absolute index.
#. Updating the logical position.

The required translation logic must exist within the Visual Domain because that domain owns wrapped line structure
and visual coordinate systems.

Placing the cursor in the Logical Domain would require one of the following:

* The Logical Domain becoming aware of visual line concepts.
* A Logical Domain component depending on Visual Domain services.
* A separate coordination component being introduced solely to bridge the domains.

Additionally, the text buffer itself does not require a cursor abstraction. Text mutation operations only require an
insertion or replacement index. The existence of a cursor is therefore not fundamental to logical text storage.

The cursor is better understood as a visual interaction construct that references logical text positions rather than
as part of the logical text model itself.

The cursor is not placed in the Display Domain because the Visual Domain already defines the editor-wide visual
coordinate system. The Display Domain only presents a truncated viewport of that visual representation.

Alternatives Considered
.......................

**Cursor in the Logical Domain**

The cursor could have been represented purely as an absolute index alongside the text buffer.
Vertical movement across visual lines would be calculated based on line lengths and display width.

This was rejected because cursor movement semantics depend on visual layout information such as wrapped lines and
visual coordinates. Implementing movement logic in the Logical Domain would either violate dependency direction or
require additional translation logic.

**Movement Controller in the Visual Domain**

A dedicated movement controller component could have been introduced in the Visual Domain while leaving the cursor
itself in the Logical Domain.

This was rejected because the cursor would simply be a state with little to no logic. It would simply verify that it is
within the bounds of the buffer. The movement controller would be the primary logic component. Combining the cursor
state and movement controller into a single component is the proposed solution.

Cursor in the Display Domain

The cursor could have been modeled relative to window/ display coordinates.

This was rejected because it introduces unnecessary abstraction. (Lower domain is generally preferred)

Consequences
............

This decision keeps visual movement logic and coordinate translation within a single domain.

It preserves strict dependency direction:

* Display → Visual → Logical

The Logical Domain remains independent of visual and wrapping concerns.

The architecture also remains flexible because text mutation operations are not coupled to the existence of a cursor
abstraction.

However, this decision means the Visual Domain must maintain translation logic between visual coordinates and logical
indices. The cursor therefore depends on wrapping state and visual layout recalculation.

Additionally, some operations that appear logically simple, such as cursor movement, now require coordination with
visual layout structures even when the underlying text buffer is unchanged.
