Layer Reads
~~~~~~~~~~~~~~~~~~~~~

Context
.......

:ref:`req_software_interfaces` requires the Facade to expose read interfaces in all four
representations of the editor state:

* **Display representation.** Content as currently visible within the window.
* **Wrapped representation.** Content after line wrapping has been applied.
* **Logical representation.** Content expressed in logical coordinates.
* **Raw representation.** The underlying text buffer contents.

The architecture is organised into three domains: Logical, Visual, and Display. The
Display Domain depends on the Visual Domain, which depends on the Logical Domain. A
design decision is required regarding whether read operations must follow this hierarchy
strictly, or whether the Facade may query lower layers directly when exposing state to
the host application.

Decision
........

The Facade holds direct references to the Logical, Visual, and Display domain services.
It queries the appropriate domain directly for read operations.

The Visual Domain also exposes interfaces for absolute-index and logical-coordinate
representations, because it holds both the cursor state and the translation machinery
between visual and logical coordinate spaces.

The bypass is limited to read operations. Write operations (insert, delete, backspace,
and cursor movement) must flow through the full domain hierarchy. Each layer in the write
path owns derived state that must be updated as part of the operation. Buffer mutations
require the wrapping map to be refreshed, and cursor movements require viewport state to
be updated. Bypassing any layer would leave the derived state stale.

Rationale
.........

Allowing the Facade to read directly from the appropriate domain preserves the
responsibilities of each layer. If all reads were forced through the Display Domain, the
Display Domain would need to expose capabilities that are not part of its purpose, such
as raw text access and logical-coordinate queries. This would blur domain boundaries and
make higher layers responsible for concepts they neither own nor use.

The Visual Domain is the correct source for cursor-based representations. The Logical
Domain owns the text buffer but does not own cursor state. Absolute-index and
logical-coordinate queries require both the current cursor position and coordinate
translation logic, both of which reside in the Visual Domain.

A potential concern with bypassing layers for reads is whether different read paths could
observe inconsistent or stale state. This architecture avoids that risk because all
persistent state is owned by the components that are the source of truth for their
respective domains. The ``TextBuffer`` owns the logical text state, and the
``CursorState`` owns the cursor state. Mutating operations update these components
in-place before returning. Consequently, a read performed through any domain service
observes the current state regardless of which layer is queried. Read-path bypassing
therefore does not create a synchronisation problem.

.. note::
   In normal operation, hosts are expected to interact primarily with the display representation
   exposed by the editor. Access to wrapped, logical, and raw representations is a specialised
   capability intended for advanced integrations, diagnostics, testing, future features, or
   unforeseen requirements. The software requirements mandate access to all representations for
   these reasons. Their presence therefore reflects an intentional extensibility decision rather
   than an expectation of frequent use.

Alternatives Considered
.......................

**Strict Sequential Delegation**
  The Facade could interact exclusively with the Display Domain, with every read request
  delegated through Display → Visual → Logical as necessary. This was rejected because it
  would require the Domains to expose and effectively own capabilities unrelated to their
  concerns. This violates single responsibility and weakens the separation between
  architectural layers.

Consequences
............

**Easier:**

* Each domain exposes only the information it owns. Intermediate layers do not need
  forwarding interfaces for unrelated concepts.
* The Facade can obtain information directly from the authoritative source of truth
  for that representation, reducing unnecessary delegation chains.
* Domain boundaries remain aligned with domain responsibilities, improving clarity and
  maintainability

**Constrained or made harder:**

* The architecture permits layer bypassing for reads, so the distinction between read and
  write operations must remain explicit and consistently enforced.
* Write operations cannot use the same shortcut. All mutations must continue to flow
  through the full domain hierarchy so that derived state, such as wrapping and viewport
  information, remains consistent.
* Future contributors must preserve the invariant that direct access is read-only. If a
  write path bypasses the hierarchy, derived state can become stale even though the
  underlying source-of-truth state remains correct.
* The Facade exposes capabilities that many hosts may never use. This slightly increases
  the public API surface in exchange for flexibility and future extensibility.
