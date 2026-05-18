.. The engine is within the *System*; its three domains are *Containers*; the modules within each domain are
  *Components*, which are made up of *Classes*, *Functions* and *Code*.

.. Though the domains are not separately deployable processes; they are bounded objects within a single Python module.
   See :doc:`decisions/arch-c4_model`.

C4 Model
~~~~~~~~

Context
.......

.. What situation or question forced this decision? What were the competing pressures?

The Text Editor Engine needed a vocabulary and a diagramming convention to describe and
communicate its internal structure. Without a shared model, there is no principled way to
answer questions such as: what counts as a component? what is the boundary of a domain?
what level of detail belongs in which diagram?

The engine is structured around three layered domains: Logical, Visual, and Display.
Each with distinct responsibilities and strict unidirectional dependencies
(:ref:`arch_goals_and_constraints`). This layered structure has a natural hierarchy of
abstraction: the engine as a whole, the domains within it, and the modules within each
domain. A structural model was needed that could express that hierarchy consistently and
support diagrams at each level of detail.

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

The C4 model's four-level hierarchy maps cleanly onto the engine's existing structure.
The three domains correspond naturally to Containers: each has a single statable
responsibility, a defined interface to adjacent domains, and internal components that are
hidden behind that interface. Adopting C4 gives these concepts standard names and a
standard set of diagram types, rather than inventing an ad-hoc notation.

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

**Monolithic architecture with no formal structural model.**
  The engine could have been implemented as a single flat module of functions and classes,
  with no explicit domain boundaries, no formal component model, and no architectural
  diagrams. This is the simplest possible approach and would have been sufficient for a
  project of this scale in purely functional terms. It was rejected for two reasons:

  1. it would provide no learning value in designing and reasoning about a layered
     architecture
  2. a flat structure actively works against the testability and single-responsibility
     goals (:ref:`arch_goals_and_constraints`) that are central to the project.

**An ad-hoc structural vocabulary.**
  Rather than adopting C4, the architecture document could have invented its own terms and
  diagram conventions. This was rejected because it would require every diagram and every
  use of terms like "domain" or "component" to be accompanied by a definition. C4 provides
  those definitions for free, and its conventions are already understood by practitioners.

Consequences
............

**Easier:**

* Each domain has a single statable responsibility (Container = one concern), enforced by
  the model's vocabulary. This directly supports the Single Responsibility Principle and
  makes violations visible: if a Container's responsibility requires "and", it is doing
  too much.
* Components within a domain can be tested in isolation, because the Container boundary
  defines a clear seam. Mocking a domain's interface for testing is a natural consequence
  of treating it as a Container.
* Diagrams at different levels of detail (Context, Container, Component) can be produced
  independently and read independently, which keeps each diagram focused.

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
  and the structural discipline it imposes.
