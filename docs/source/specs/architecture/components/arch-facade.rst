TextEditor
~~~~~~~~~~

Responsibility
..............

The ``TextEditor`` is the sole public entry point to the system, exposing a unified
interface over the domain services to the host application. (:need:`NFREQ-DEPLOY-201`)

Owned State
...........

The ``TextEditor`` owns three domain service instances: the ``LogicalDomainService``,
the ``VisualDomainService``, and the ``DisplayDomainService``. The internal components
of each domain are not visible to the facade.

No observable state is exposed before initialisation completes successfully.
(:need:`FR-INIT-001`)

Behaviour
.........

**Initialisation.** The ``TextEditor`` is initialised by the host application with the
full set of configuration parameters: initial text, cursor position, display width,
display height, and scrolloff. (:need:`FR-INIT-001`) If no cursor position is provided,
the cursor defaults to the position immediately after the last character in the buffer.
(:need:`FR-INIT-006`) The ``TextEditor`` initialises the domain services in dependency
order (Logical first, then Visual, then Display) and verifies that all initialization
invariants hold simultaneously before returning. (:need:`INV-INIT-002`) Else it must
throw an exception. (:need:`FR-INIT-011`, :need:`FR-INIT-012`, :need:`FR-INIT-013`)

**Output interfaces.** The facade exposes output grouped by which service handles it:

* *Text reads,* delegated to the ``LogicalDomainService``: raw text (:need:`FR-MODE-001`)
  and logical lines (:need:`FR-MODE-011`).
* *Visual reads and non-window cursor representations,* delegated to the
  ``VisualDomainService``: wrapped visual output (:need:`FR-MODE-021`), visual-to-logical
  mapping (:need:`FR-MODE-022`), cursor as Visual Coordinate (:need:`FR-CURSOR-004`),
  cursor as Absolute Index (:need:`FR-CURSOR-002`), and cursor as Logical Coordinate
  (:need:`FR-CURSOR-003`). The ``VisualDomainService`` fulfils all three non-window cursor
  representations because it holds both ``CursorState`` and the translation machinery of
  the ``VisualLogicalAdapter``. These do not pass through the Display Domain.
* *Display reads and window cursor representation,* delegated to the
  ``DisplayDomainService``: viewport-truncated output (:need:`FR-MODE-031`),
  display-to-logical mapping (:need:`FR-MODE-032`), and cursor as Window Coordinate
  (:need:`FR-CURSOR-005`).

All output operations are read-only. (:need:`INV-MODE-001`) This is a deliberate bypass of
the layering. (See :doc:`../decisions/arch-layer_reads`)

**Mutations and movement.** Insert, delete, backspace, and cursor movement operations
are delegated to the ``DisplayDomainService``, which propagates them through the Visual
and Logical Domains in turn. The facade adds no logic of its own to these operations.
(:need:`FR-CURSOR-020`)

**No logic beyond delegation.** The facade does not implement business logic, coordinate
translation, or domain-specific behaviour. If the facade contains anything other than
delegation and initialisation sequencing, that logic belongs in a domain service.

Dependencies
............

**Depends on:** All three domain services directly: ``LogicalDomainService`` for raw
and logical text output; ``VisualDomainService`` for wrapped visual output, visual-to-logical
mapping, and all non-window cursor representations;
``DisplayDomainService`` for display-mode output, window cursor representation, mutations,
and movement. The facade does not depend on any component inside a domain.

**Depended on by:** The host application exclusively. No internal component depends on
the ``TextEditor``.

Scope Boundary
..............

The following are explicitly outside the system's scope. The facade must not expose
interfaces for any of them, and the host application is responsible for implementing
them where needed:

* **User input.** The system does not capture keyboard or mouse events. The host
  application translates input into API calls. (:need:`NR-CURSOR-102`)
* **Re-initialisation.** Configuration parameters cannot be changed after successful
  initialisation. To change them, the host application instantiates a new ``TextEditor``.
  (:need:`NR-INIT-101`)
* **State persistence.** The system provides no serialisation or deserialisation. The
  host application may read the text buffer and cursor position via the output interfaces
  and supply them as initialisation parameters to a new instance. (:need:`NR-INIT-102`)
* **Rendering and I/O.** The system does not handle rendering or GUI operations.
  (:need:`NR-MODE-101`)
* **Text selection, clipboard, undo/redo.** These operations are not supported.
  (:need:`NR-TEXT-101`, :need:`NR-TEXT-102`, :need:`NR-TEXT-103`)

Key Invariants
..............

* **Post-initialisation validity.** Upon successful initialisation, all system invariants
  hold simultaneously: the buffer contains the supplied initial text; the cursor is within
  valid bounds in all four coordinate spaces; all coordinate representations are mutually
  consistent; and ``window_start`` satisfies the window bounds and cursor visibility
  constraints. The initial state is indistinguishable from one reached through normal
  operation. (:need:`INV-INIT-002`)

* **Coordinate synchronisation.** At every point where the facade returns a value to the
  host application, all four cursor representations (Absolute Index, Logical Coordinate,
  Visual Coordinate, Window Coordinate) bijectively map to the same underlying buffer
  position. (:need:`INV-CURSOR-003`)

* **Sole public entry point.** No domain service, component, or internal interface is
  accessible to the host application except through the ``TextEditor``. This is a
  deployment constraint, not merely a design preference. (:need:`NFREQ-DEPLOY-201`)
