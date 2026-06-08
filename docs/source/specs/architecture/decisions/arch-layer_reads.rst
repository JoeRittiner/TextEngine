Layer Reads
~~~~~~~~~~~

Context
.......

:ref:`req_software_interfaces` requires the Facade to expose read interfaces in all four
representations of the editor state:

* **Display representation.** Content and cursor position as currently visible within the viewport window.
* **Wrapped representation.** Content and cursor position after line wrapping has been applied.
* **Logical representation.** Content and cursor position expressed in logical coordinates.
* **Raw representation.** The underlying text buffer contents and absolute inex of the cursor position.

The architecture is organised into three domains: Logical, Visual, and Display. The
Display Domain depends on the Visual Domain, which depends on the Logical Domain. A
design decision is required regarding whether read operations must follow this hierarchy
strictly, or whether the Facade may query lower layers directly when exposing state to
the host application.

Decision
........

The Facade holds direct references to the Logical, Visual, and Display domain services.
It queries the appropriate domain service directly for read operations, aligning each
query type with the domain that natively owns that representation:

1. **Raw and Logical Reads:** Queried directly from the ``LogicalDomainService``.
   Because the Logical Domain owns both the text buffer and the ``CursorState``, it is the sole authority for
   evaluating raw text strings, logical line blocks, absolute indices, and logical ``(line, col)`` coordinates.
2. **Wrapped Reads:** Queried directly from the ``VisualDomainService``.
   The Visual Domain provides wrapped text lines and visual ``(v_row, v_col)`` coordinates by projecting the
   logical state onto its internal wrapping map layout.
3. **Display Reads:** Queried directly from the ``DisplayDomainService``.
   The Display Domain provides viewport-truncated text arrays and window-relative coordinates based on its
    active scrolling offset.

The bypass is strictly limited to read operations. Write operations (insert, delete, backspace,
and cursor movement) must continue to flow sequentially through the domain hierarchy. Each layer in the write
path acts as an orchestrator or contains derived state that must be refreshed dynamically as part of the transaction.

Rationale
.........

Allowing the Facade to read directly from the appropriate domain preserves the clean, single-responsibility separation
of each layer. If all reads were forced to traverse upward through the Display Domain, intermediate layers would be
cluttered with pass-through forwarding interfaces for data they do not use, care about, or conceptually understand.

A potential concern with bypassing layers for reads is whether different read paths could
observe inconsistent or stale state. This architecture avoids that risk because all
persistent state is eagerly updated in-place during write transactions. Text modifications instantly update both
the text buffer and the absolute cursor index within the Logical Domain. The write path ensures that the Visual
Domain's wrapping map and the Display Domain's viewport boundary are updated synchronously before the write
transaction yields control back to the caller. Consequently, a read performed through any domain service immediately
observes an internally consistent, up-to-date state snapshot regardless of which layer is targeted.

.. note::
   In normal operation, hosts are expected to interact primarily with the display representation
   exposed by the editor. Access to wrapped, logical, and raw representations is a specialised
   capability intended for advanced integrations, diagnostics, testing, or custom host plugins.
   The software requirements mandate access to all representations for these reasons.
   Their presence therefore reflects an intentional extensibility decision rather than an expectation of frequent use.

Alternatives Considered
.......................

**Strict Sequential Delegation**
  The Facade could interact exclusively with the Display Domain, with every read request
  delegated through Display → Visual → Logical as necessary. This was rejected because it
  would require the upper domains to expose and effectively forward capabilities completely unrelated to their
  concerns (such as raw buffer access). This violates single responsibility and weakens the modularity of the
  architectural layers.

Consequences
............

**Easier:**

* **Strict Domain Coherence:** Each domain exposes only the information it owns. Intermediate layers do not need
  forwarding interfaces for unrelated concepts.
* **Clear Domain Boundaries:** Domain boundaries remain aligned with domain responsibilities, improving clarity and
  maintainability
* **No Unnecessary Delegation Chains:** The Facade obtains information directly from the authoritative source of truth
  for that representation, reducing boilerplate forwarding methods across boundaries.

**Constrained or made harder:**

* **Explicit Architecture Discipline:** Because the architecture permits layer bypassing for reads, the functional
  distinction between read and write operations must remain explicit and consistently enforced by future developers.
* **No Write Path Shortcuts:** Write operations cannot use the same direct shortcut. All mutations must continue to
  flow sequentially through the full domain hierarchy to ensure that layout caches, wrapping maps, and viewport window
  offsets remain strictly synchronized and aligned.
* **Future Contributors:** Future contributors must preserve the invariant that direct access is read-only. If a
  write path bypasses the hierarchy, derived state can become stale even though the
  underlying source-of-truth state remains correct.
* **Public API Surface:** The Facade exposes capabilities that many hosts may never use. This slightly increases
  the public API surface in exchange for flexibility and future extensibility.
