Display Domain
~~~~~~~~~~~~~~

Context
.......

The Text Editor Engine must track the cursor consistently across four coordinate spaces:
Absolute Index, Logical, Visual, and Window. (:need:`INV-CURSOR-001`)

The Visual Domain already provides a fully functional layer: it wraps the raw text into
visual lines and tracks the cursor in Visual coordinates ``(row, col)``. If the display
were infinitely tall, the Visual Domain alone would suffice.

The problem is that real displays are not infinitely tall. The engine must also:

* Constrain the visible output to a fixed-height window.
* Keep the cursor within that window as it moves (scrolling when necessary).
* Translate the cursor's Visual coordinate into a Window coordinate ``[x, y]`` that is
  relative to the visible portion of the wrapped output.

A design decision was required: where does height-management and Window-coordinate
tracking belong in the domain structure?

Decision
........

An additional Display Domain is placed **above** the Visual Domain in the dependency stack.
It does not replace the Visual Domain; it extends it. The Display Domain consumes the Visual
Domain's output (the full list of wrapped visual lines and the Visual cursor position) and
applies a second transformation: truncating that list to the visible window and translating
the Visual cursor into Window coordinates.

The Display Domain is the Visual Domain with one additional responsibility: deciding
which visual lines are currently visible.

Rationale
.........

The Visual Domain already produces the correct logical structure: lines wrapped to the
configured display width, with the cursor tracked in Visual space. Height-management is
a strictly additive concern: it does not change how lines are wrapped or how the cursor
moves; it only selects a subset of what the Visual Domain has already computed.

Placing the Display Domain above the Visual Domain reflects this dependency accurately.
The Display Domain depends on Visual output; the Visual Domain is unaware of the window
height. This preserves the unidirectional dependency rule (:ref:`arch_goals_and_constraints`)
and ensures that neither domain's behaviour bleeds into the other's responsibility.

The alternative placement, adjacent to or below the Visual Domain, would require the
Display Domain to replicate wrapping logic or to operate on unwrapped logical lines. This
would violate single responsibility, increase complexity, and break the clean coordinate
ownership model.

Alternatives Considered
.......................

**Display Domain operating directly above the Logical Domain (bypassing Visual).**
  The Display Domain could truncate *logical* lines rather than visual lines, making it
  independent of the Visual Domain entirely. This is structurally simpler, but it is
  less useful: logical lines are not wrapped, so the host application would always receive
  raw, unwrapped text regardless of the configured display width. The wrapping
  invariant (:need:`FR-WRAP-001`) would be unenforceable at the display boundary.

**Merging Display and Visual into a single domain.**
  A single domain could handle both wrapping and viewport management. This reduces the
  number of moving parts, but conflates two distinct concerns; line wrapping (a function
  of width) and viewport scrolling (a function of height and cursor position), into one
  component. The combined domain would be harder to test in isolation and would violate
  single responsibility.

**Host application manages viewport.**
  The engine could expose all wrapped visual lines and leave height-clipping and
  Window-coordinate translation to the host. This simplifies the engine but pushes
  non-trivial coordinate logic into every host implementation.

Consequences
............

**Easier:**

* The Visual Domain can be developed, tested, and reasoned about independently of window
  geometry. All wrapping behaviour is fully exercisable without a window height.
* The Display Domain's responsibility is narrow and precisely stated: given visual lines
  and a visual cursor, return the visible subset and the Window cursor. It can be unit-tested
  with a mock of the Visual Domain's output.
* The coordinate ownership model is clean: each domain owns exactly one coordinate space,
  and translation is always localised to the domain boundary where the spaces meet.

**Constrained or made harder:**

* The engine has three layers where two might seem sufficient for simple use cases. This
  adds cognitive overhead when first reading the architecture.
* A resize operation (change to ``display_height`` or ``display_width``) must propagate
  through two domain boundaries. The Visual Domain must recompute wrapping for a new
  width; the Display Domain must recompute the viewport for a new height. These are
  currently treated as re-initialisation events. (:need:`INV-VIEW-001`, :need:`INV-WRAP-001`)
* Raw text does not cross the Display Domain boundary. Any host that needs both the
  visible text and the Window cursor position must issue two separate queries.
  The Facade resolves this by holding direct references to all three domain services,
  allowing it to serve each output mode from its owning layer without passing concerns
  upward.
