Architecture Specification
==========================

Introduction
------------

Purpose
~~~~~~~

.. Describe the purpose of this document. An architecture document is distinct from a requirements document:
   where the SRS defines *what* the system must do, this document defines *how* the system is internally
   structured to fulfil those requirements. State that this document records deliberate structural decisions
   and their rationale, so that they can be understood, reviewed, and revisited as the project evolves.

This document describes the internal structure of the Text Editor Engine. Where the
:doc:`Software Requirements Specification (SRS) <../requirements/index>` defines *what* the system must do from the
outside, this document defines how the system is *structured* internally to fulfil those requirements.

Specifically, this document records: the domain decomposition of the system, the responsibilities and
boundaries of each component, the contracts between components, and the rationale behind significant
structural decisions. It does not restate requirements, it references them.

Scope
~~~~~

.. Identify which parts of the system this document covers. For a project with a single top-level component
   (e.g. TextEditor), this is straightforward. If the architecture document covers only a subset of the
   system, say so explicitly and reference the documents that cover the remainder.

This document covers the entire Text Editor Engine: the public-facing ``TextEditor`` facade and all
internal components. It does not cover host application concerns such as rendering, input handling,
or file I/O. These are explicitly outside the engine's boundary (see :ref:`arch_out_of_scope`).

Intended Audience
~~~~~~~~~~~~~~~~~

The primary audience is the author, both as engine implementer and as future host application
integrator. The engine implementer should read the document in full. The host application integrator
should focus on the public API (:ref:`arch_public_api`) and the out-of-scope boundary
(:ref:`arch_out_of_scope`).

Relationship to Other Documents
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Software Requirements Specification (SRS):** :doc:`../requirements/index` -
  defines the behavioural contract this architecture must satisfy. This document references
  requirements but does not reproduce them.
* **Component Descriptions:** individual component pages under :ref:`arch_components`.
* **Architectural Decisions:** individual decision pages under :ref:`arch_decisions`.
* **Glossary:** :doc:`arch_glossary`: shared terminology for all architecture documents.

References
~~~~~~~~~~

* Facade Pattern: https://refactoring.guru/design-patterns/facade
* C4 Model (context/container/component diagrams): https://c4model.com/
* UML 2.5.1 Specification: https://www.omg.org/spec/UML/2.5.1/PDF/
* SOLID Principles: https://en.wikipedia.org/wiki/SOLID

Document Conventions
~~~~~~~~~~~~~~~~~~~~

* **Diagram color-coding:** Architectural diagrams use a consistent color scheme to distinguish
  domains: Logical Domain (blue), Visual Domain (green), Display Domain (orange), Facade (grey).

* **Naming convention:** Component names use ``PascalCase``. Internal functions and variables
  follow Python's ``snake_case``.

* **Dependency arrows:** In all component diagrams, arrows point in the direction of dependency
  (from the dependent toward the thing it depends on), not in the direction of data flow.

* **"Component" vs. "class":** This document uses *component* to mean a named unit of
  architectural responsibility. Whether a component is realised as a class, a module, or a set of
  pure functions is an implementation not assumed here.

.. note:: **C4 Model:**

   The :ref:`Text Editor <arch_system>` is made up of three :ref:`Domains/ Layers/ Containers <arch_containers>`
   (applications and data stores), each of which contains one or more :ref:`components <arch_components>`,
   which in turn are implemented by one or more "code" elements (classes, interfaces, objects, functions, etc).

.. _arch_goals_and_constraints:

Architectural Goals and Constraints
-----------------------------------

.. All goals below are pursued within the standard engineering constraints of SOLID, DRY, and KISS.
   These are assumed, not repeated under each point.

Goals
~~~~~

.. State the qualities this architecture is explicitly designed to achieve. These should be derived from
   the non-functional requirements in the SRS. Examples for this kind of project:
   - Testability: all logic must be exercisable without a host application.
   - Separation of concerns: each component owns one well-defined responsibility.
   - Replaceability: internal components should be replaceable without changing the public API.
   Write each goal as a short labelled statement, not a vague aspiration.

* **Strict Unidirectional Dependencies:**
  Dependencies flow in one direction only: from higher domains toward lower domains. No component
  in the Logical Domain may depend on anything in the Visual or Display Domain. This is an absolute
  rule, not a guideline.

  *Rationale:* Enforces testability (each domain can be tested in isolation and mocked),
  replaceability (a domain can be rewritten without affecting domains below it), and prevents
  circular coupling.

* **Pure Logic and Determinism:**
  The engine is a pure-logic system. Given the same initial state and the same sequence of
  operations, it always produces the same output. It has no side effects beyond its own internal
  state: no I/O, no randomness, no time-dependence.

  *Rationale:* Makes all behaviour unit-testable and all bugs reproducible.

* **Single Responsibility per Component:**
  Each component within a domain  owns one clearly statable concern. If a component's responsibility cannot be
  described in one sentence without the word "and", it is doing too much.

  *Rationale:* The multi-coordinate cursor system creates natural pressure toward coupling. Strict
  single responsibility keeps coordinate translation localised and prevents it from spreading across
  components.

* **Testability Without a Host:**
  Every component and every code path must be exercisable by a unit test that does not instantiate
  any GUI framework, terminal library, or external dependency.

  *Rationale:* See :ref:`req_software_quality_attributes`.

* **Performance:**
  Text manipulation, cursor tracking, and visual wrapping must remain performant during rapid
  host-application input loops. See :ref:`req_performance_requirements`.

.. :ref:`req_software_quality_attributes`

Constraints
~~~~~~~~~~~

* **Language:** Implemented entirely in Python.
* **Threading:** Single-threaded. No concurrency model is defined or supported.
* **Deployment unit:** The engine is provided as a single importable module. ``TextEditor`` is the
  sole public entry point. :need:`NFREQ-DEPLOY-201`
* **Dependencies:** Python Standard Library only. No third-party packages. (Test dependencies
  such as ``pytest`` and ``hypothesis`` are exempt from this constraint.)
* **UI/IO independence:** The engine must not depend on any GUI framework, terminal library, or
  ``stdin``/``stdout``. All rendering and input capture are the host application's responsibility.
  See :need:`NR-CURSOR-102`, :need:`NR-MODE-101`.
* **No state persistence:** The engine does not read from or write to disk. See :need:`NR-INIT-102`.

.. _arch_asr:

Architecturally Significant Requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These requirements have a disproportionate influence on structure and are highlighted here because
they constrain or directly motivate specific architectural decisions.

* **Four-Coordinate Cursor System** (:need:`INV-CURSOR-001`):
  The cursor must be tracked consistently across Absolute Index, Logical, Visual, and Window
  coordinate spaces. This is the most structurally complex requirement in the system and is the
  primary reason the domain boundary between Visual and Display exists.
  (See :doc:`decisions/arch-display_domain`.)

* **Non-Destructive Visual Wrapping** (:need:`FR-WRAP-001`):
  Line wrapping is a visual transformation and must never mutate the underlying text buffer.
  This requirement mandates that the Logical Domain is unaware of wrap state.

* **Configurable Display Geometry** (:need:`INV-WRAP-001`, :need:`INV-VIEW-001`, :need:`INV-VIEW-002`):
  Width, height, and scrolloff must be runtime-configurable. The Display Domain must hold no
  hardcoded geometry assumptions, and the engine must be re-queryable after a resize without
  re-initialising text or cursor state.

.. _arch_out_of_scope:

Explicitly Out of Scope
~~~~~~~~~~~~~~~~~~~~~~~

The following concerns are deliberately excluded from the engine. The host application is
responsible for all of the below. (If/ When required.)

* Rendering and display output
* Keyboard and mouse input capture
* File I/O and state persistence
* Clipboard operations
* Undo/redo history
* Syntax highlighting

.. _arch_system:

System Context
--------------

System Context Diagram
~~~~~~~~~~~~~~~~~~~~~~

.. plantuml:: diagrams/system_context.puml

.. _arch_public_api:

Public API (Facade Interface)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``TextEditor`` class is the sole public surface of the engine. All host application interaction
passes through it. Internal components are not part of the public API and may change without notice.

The engine guarantees that after every public method call, all internal state is consistent.
The caller never observes a partially-updated state.

**Initialisation**
  The engine is configured at construction time with display geometry (width, height, scrolloff).
  Text content and cursor position may optionally be seeded. After construction the engine is in a
  fully valid state.
  (:doc:`../requirements/f-req_initialization`)

**Mutation Commands**
  Operations that modify the text buffer (``insert``, ``delete``, ``backspace``). The cursor may be updated as a
  consequence. The engine does not expose partial results mid-mutation.

  *Error contract (TBD):* Behaviour on invalid operations (e.g. ``backspace`` at position 0) is
  unresolved. See :ref:`arch_error_contract`.

**Cursor Movement**
  Operations that reposition the cursor without modifying text (``move_up``, ``move_down``,
  ``move_left``, ``move_right``, ``move_home``, ``move_end``). Movement at a boundary is a no-op.
  (:doc:`../requirements/f-req_cursor_movement`)

**Cursor Query**
  Returns the current cursor position in a caller-specified coordinate space (see :ref:`arch_coordinate_spaces`).

**Content Query**
  Returns the current text content in a caller-specified form (:term:`logical lines`, :term:`visual lines`,
  or :term:`display lines`).

.. _arch_containers:

Containers
----------

Domain Layer Model
~~~~~~~~~~~~~~~~~~

The engine is divided into three layered domains. Each domain depends only on the one domain directly
below it and is completely independent of the domains above it.

.. note:: **C4 Model:**
   In this architecture, the domains/ layers aren't necessarily "real". They're more conceptual. There might not
   be a literal "LogicalLayer" or "DisplayLayer" that exists, the same way an actual database or UI might exist in other
   C4 models. Nonetheless, the components will be grouped into these conceptual domains for the purposes of this
   architecture. I.e. they will not overlap.

Data flows *up* through the layers in response to queries. Commands flow *down*: the caller
instructs a domain, which delegates further down as needed. No domain notifies the domain above it
of a change. It is the caller's responsibility (ultimately the ``TextEditor`` facade) to re-query
after a mutating operation.

Within each domain, components are either **stateful** (they own and mutate data) or **stateless
calculators** (pure functions with no owned state).

A single public-facing class, ``TextEditor``, acts as the Facade: it is the only entry point for
host applications, owns references to all internal components, and is responsible for coordinating
cross-domain operations.

**Domain responsibilities:**

* **LogicalDomain:** Owns the raw text string and its line index. All mutations to text content
  occur here. This is the single source of truth for text.

* **VisualDomain:** Requests raw text from the Logical Domain and applies visual transformations
  (line wrapping). Does not mutate text directly, it passes mutation requests down to the Logical Domain.
  Tracks the cursor in Visual coordinates. Translates between Visual and Logical coordinates.

* **DisplayDomain:** Manages window geometry and tracks the cursor in Window coordinates.
  Determines which subset of visual lines is returned to the host. If cursor movement causes the
  viewport to scroll, the Visual Domain is unaffected. Does not mutate cursor or text directly; it
  passes mutation requests down to the Visual Domain.

**Important:** Domains have no responsibility to notify the Domain above them when it changes.
Synchronisation is the Facade's responsibility.

.. **Why is Cursor in the Visual Domain, not the Logical Domain?**
   See :doc:`decisions/arch-cursor_domain`.

.. _arch_coordinate_spaces:

Coordinate Systems & Output Modes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The cursor exists simultaneously in four coordinate spaces. Each domain is responsible for
translating between the spaces it owns. The four spaces map directly onto the domain structure and
onto the output modes exposed by the public API (See :doc:`../requirements/f-req_output_modes`).

.. _arch_coordinate_ownership:

======= ======= ============== ======================================
Mode    Domain  Coordinate     Meaning
======= ======= ============== ======================================
Raw     Logical Absolute Index ...
Logical Logical Logical        ...
Wrapped Visual  Visual         ...
Display Display Window         ...
======= ======= ============== ======================================

Container Diagram
~~~~~~~~~~~~~~~~~

.. plantuml:: diagrams/domain_layers.puml

Data Flow: Representative Examples
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. TODO: Sequence diagram for insert() and move_right() — one mutation, one movement.
   Both should illustrate the downward command / upward data pattern.

**Example:** ``insert("a")``

#. The host application calls ``TextEditor.insert("a")``.
#. The Facade delegates to the Visual Domain, passing the current Visual cursor position.
#. The Visual Domain converts the Visual position to an Absolute Index and passes the insert
   request down to the Logical Domain.
#. The Logical Domain mutates the text buffer and returns the updated text.
#. The Visual Domain recomputes the wrapped line layout from the updated text.
#. The Facade queries the Display Domain to determine whether the viewport needs to scroll to keep
   the cursor visible, and updates Window coordinates accordingly.
#. Control returns to the host application. No output is pushed. The host must get the updated  text
   and display position manually.

.. plantuml:: diagrams/seq_insert.puml

**Example:** ``move_right()``

.. TODO

.. plantuml:: diagrams/seq_move_right.puml

.. _arch_components:

Components
----------

.. _arch_component_descriptions:

Component Descriptions
~~~~~~~~~~~~~~~~~~~~~~

.. toctree::
   :maxdepth: 2

   arch-text_buffer

Internal Interfaces
~~~~~~~~~~~~~~~~~~~

Key contracts between internal components are recorded here. Full per-component interface details
are in :ref:`arch_component_descriptions`.

* **Visual → Logical:** The Visual Domain queries the Logical Domain for the raw text string.
  It does not instruct the Logical Domain on how to store or represent text.

* **Display → Visual:** The Display Domain queries the Visual Domain for the total number of
  wrapped visual lines and the current cursor visual position. It receives counts and indices,
  never raw text. Raw text does not cross the Display domain boundary.

* **Intra-domain:** Components within the same domain follow the same unidirectional rule. A
  component may depend on another component in the same domain, but not the reverse. For example,
  within the Visual Domain, ``Cursor`` may request data from and depend on ``LineWrapper``, but
  ``LineWrapper`` must not depend on ``Cursor``.

* **No cross-domain direct calls:** Components do not call components in non-adjacent domains. (The Display Domain is
  unaware of the Logical Domain.)
  Each domain exposes a single internal interface (a domain service).
  Internal coordination within a domain is the domain service's responsibility.

Component Diagram
~~~~~~~~~~~~~~~~~

.. plantuml:: diagrams/display_components.puml
.. plantuml:: diagrams/visual_components.puml
.. plantuml:: diagrams/logical_components.puml

.. _arch_decisions:

Architectural Decisions
-----------------------

.. toctree::
   :maxdepth: 1
   :glob:

   decisions/*

Open Questions
--------------

.. _arch_error_contract:

Unresolved Questions
~~~~~~~~~~~~~~~~~~~~~

* **Error handling contract:** What is the engine's behaviour on invalid operations?
  Options: raise an exception, return a status code, or silently no-op with state unchanged.
  This affects the public API contract in [...] and must be decided before the facade is implemented.

* **Logging:** Should the engine emit structured logs? If so, at which layer. Only the facade,
  or also internal components? Using the standard library ``logging`` module is consistent with
  the library constraint, but the scope is unresolved.

* **Resize behaviour:** The configurable geometry constraint (:need:`INV-VIEW-001`) implies the
  display can be resized at runtime. Is this a re-initialisation (new engine instance) or a
  mutation operation on an existing instance? The current API does not expose a resize method.


Known Limitations
~~~~~~~~~~~~~~~~~

* **Single-threaded only.** No concurrency primitives are used. The engine is not safe to call
  from multiple threads simultaneously.
* **In-memory only.** The entire text buffer is held in memory. There is no streaming or paging
  for large documents.

.. Future Evolution
   ~~~~~~~~~~~~~~~~

Appendix A: Glossary
--------------------

.. include:: arch_glossary

Appendix B: Revision History
-----------------------------

.. include:: arch_history.rst

Indices and tables
------------------
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
