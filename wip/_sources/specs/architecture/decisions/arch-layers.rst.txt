Layered Domains
~~~~~~~~~~~~~~~

Context
.......

The Text Editor Engine must transform raw text into a form suitable for display. This
involves at least three distinct concerns: storing and mutating text, wrapping it into
visual lines, and clipping those lines to a fixed-height window. Each concern operates on
a different representation of the same underlying data, and each has a natural boundary
where it stops and the next begins.

A structural decision was required: should these concerns be handled by a single flat
module, or should the engine be divided into explicit layers, each owning one concern?

Decision
........

The engine is structured as three **additive, unidirectional layers**: the Logical,
Visual, and Display Domains, stacked from the bottom up. Each layer is fully functional
independently of any layer above it. Higher layers add abstraction; they do not replace
lower ones.

Rationale
.........

The additive property is the key design principle. The Logical Domain is a complete,
working system on its own: it stores text. The Visual Domain adds wrapping, making the
engine useful for any host that needs soft line breaks; the Logical Domain beneath it
is unaffected. The Display Domain adds viewport management on top of that; the Visual
Domain beneath it is unaffected.

This means the decision to add each layer was independent. The Display Domain was added
because viewport management is a feature worth having inside the engine rather than
delegating to the host application. But it was added to a fully functional Visual Domain,
not woven into it. If the Display Domain were removed tomorrow, the Visual Domain would
still work correctly. The same holds for the Visual Domain relative to the Logical.

This independence has direct consequences for testability: each layer can be exercised in
isolation, without instantiating the layers above it. It also has consequences for
reasoning: a bug in wrapping is a Visual Domain bug; a bug in scrolling is a Display
Domain bug. The layers give errors a natural home.

The unidirectional dependency rule (lower layers are unaware of higher ones) follows
from the same principle. A lower layer that depends on a higher layer is no longer
independent; it cannot be tested or understood without the layer above it.

Alternatives Considered
.......................

**Flat module with no explicit domain boundaries.**
  All concerns, text storage, wrapping, viewport management, could be implemented in a
  single module with no internal structure. This is the simplest approach and would be
  functionally sufficient for a project of this scale. It was rejected for two reasons:

  * it provides no separation of concerns, making it harder to test each behaviour in
    isolation
  * it offers no learning value in designing and reasoning about a structured architecture,
    which is an explicit goal of this project.

**Two layers: Logical and a combined Visual/Display.**
  Wrapping and viewport management could be merged into a single layer above the Logical
  Domain. This reduces the number of moving parts and is a reasonable structure if the
  two concerns are always configured and changed together. It was rejected because wrapping
  is a function of display width and viewport management is a function of display height
  and cursor position, they are distinct concerns that change for distinct reasons. Merging
  them would make it harder to test wrapping independently of scrolling, and would obscure
  the boundary where each concern begins. (See :doc:`arch-display_domain` for the detailed
  reasoning on that specific boundary.)

Consequences
............

**Easier:**

* Each layer can be instantiated and tested without the layers above it. Unit tests for
  wrapping do not require a configured viewport; unit tests for text mutation do not
  require wrapping at all.
* Bugs and responsibilities have a natural home. A concern that does not fit cleanly into
  one layer is a signal that either the layer boundaries are wrong or the concern has not
  been fully analysed.
* Adding a new layer of abstraction in the future (e.g. syntax highlighting as a
  transformation above the Visual layer) follows the same pattern without requiring
  changes to existing layers.

**Constrained or made harder:**

* Operations that cross layer boundaries, such as inserting a character, which affects
  the text buffer, the wrap layout, and potentially the viewport, must be coordinated
  explicitly. This coordination is distributed across the domain service chain, with
  each service responsible for propagating the operation to the layer below it and updating
  its own state before returning.
* Each layer boundary is a contract that must be defined and maintained. As the
  implementation evolves, keeping those contracts stable requires discipline.
* The layered structure requires a vocabulary to describe it consistently. This decision
  was the direct motivation for adopting a formal structural model.
  (See :doc:`arch-c4_model`.)
