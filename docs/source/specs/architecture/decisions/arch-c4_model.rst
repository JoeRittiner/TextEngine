C4 Model
~~~~~~~~

Context
.......

The engine's layered domain structure was already decided (see :doc:`arch-layers`): three
additive domains, Logical, Visual, and Display, stacked with strict unidirectional
dependencies. That decision produced a natural hierarchy of abstraction: the engine as a
whole, the domains within it, and the modules within each domain.

What remained was a documentation decision: how to describe and communicate that hierarchy
consistently. Without a shared model, there is no principled way to answer questions such
as: what counts as a component? what is the boundary of a domain? what level of detail
belongs in which diagram? Inventing answers ad-hoc risks inconsistency across diagrams and
requires every term to be defined before it can be used.

Decision
........

The architecture of the Text Editor Engine is described using the **C4 model**
(https://c4model.com/).

The C4 hierarchy is applied as follows:

* **System:** The Text Editor Engine and Host application.
* **Container:** Each of the three domains: Logical, Visual, and Display. These are not
  separately deployable processes; they are bounded, cohesive units of responsibility
  within a single Python module.
* **Component:** The individual modules within each domain (e.g. ``TextBuffer``,
  ``WrapEngine``, ``ViewportState``).
* **Code:** The classes, functions, and data structures that implement each component.

Rationale
.........

The C4 model's four-level hierarchy maps directly onto the engine's existing structure,
with no forcing required. The engine is in the System; its three domains are Containers; the
modules within each domain are Components. C4 therefore gives the hierarchy names it would
have needed regardless. It does not impose a structure, it labels one that already exists.

C4 also scales with the reader. The Context and Container diagrams communicate the
high-level structure to anyone reading the architecture document for the first time.
Component diagrams provide the detail needed during implementation. The model does not
require all four levels to be diagrammed — levels can be omitted where they add no
clarity — which keeps documentation proportionate to the engine's actual complexity.

Finally, C4 is tooling-agnostic and widely understood. Using it means the diagrams and
vocabulary in this document are immediately legible to anyone familiar with the model,
without requiring project-specific conventions to be explained first.

Alternatives Considered
.......................

**An ad-hoc structural vocabulary.**
  Rather than adopting C4, the architecture document could have invented its own terms and
  diagram conventions. This was rejected because it would require every diagram and every
  use of terms like "domain" or "component" to be accompanied by a definition. C4 provides
  those definitions for free, and its conventions are already understood by practitioners.

Consequences
............

**Easier:**

* Diagrams at different levels of detail (Context, Container, Component) can be produced
  and read independently. A reader who only needs the high-level picture reads the
  Container diagram; a reader implementing a component reads the Component diagram. Neither
  diagram needs to carry the detail of the other.
* The model's vocabulary resolves naming questions without discussion. Whether a given
  unit is a Container or a Component is answered by C4's definitions, not by negotiation
  each time a new diagram is drawn.
* The Container boundary makes violations of single responsibility visible in the
  documentation itself: if a Container's responsibility cannot be stated in one sentence,
  the diagram signals a problem before the code is written.

**Constrained or made harder:**

* The C4 Container level implies a degree of autonomy and replaceability that does not
  fully apply here: the three domains are co-located in a single Python module and share a
  process. Using "Container" for a bounded unit within a module is a deliberate adaptation
  of the model, not a strict application of it. This must be noted explicitly to avoid
  misleading readers who expect Containers to be separately deployable services.
* Maintaining consistency across four levels of documentation adds overhead. Decisions
  about what belongs at the Component level versus the Container level must be made
  deliberately and may require revisiting as the implementation evolves.
* For a project of this scale, the full C4 apparatus — four levels, multiple diagram
  types, explicit interface contracts — is more structure than the complexity of the
  problem strictly demands. The overhead is accepted in exchange for the learning value
  and the consistency it enforces.