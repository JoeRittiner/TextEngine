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
* **Glossary:** shared terminology for all architecture documents. (:doc:`arch_glossary`)

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

* **C4 levels:** This document follows the C4 model hierarchy. The engine is within the *System*; its
  three domains are *Containers*; the modules within each domain are *Components*, which are made up of *Classes*,
  *Functions* and *Code*.
  See :doc:`decisions/arch-c4_model` for the rationale for adopting this model.

* **Coordinate Notation:** Coordinates that are relative to lines (logical or visual) are written with brackets
  ``(line, col)``. Coordinates that are relative to the window are written as with square brackets ``[x, y]``.
  This is to distinguish between coordinate systems.

.. _arch_goals_and_constraints:

Architectural Goals and Constraints
-----------------------------------

.. All goals below are pursued within the standard engineering constraints of SOLID, DRY, and KISS.
   These are assumed, not repeated under each point.

Goals
~~~~~

* **Single Responsibility per Container:**
  Each domain has a single responsibility. If a container's responsibility cannot be described in
  one sentence without the word "and", it is doing too much.

  *Rationale:* Prevents the spread of concerns and makes the architecture easier to understand and maintain.

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
  Each component within a domain owns one clearly statable concern. If a component's responsibility cannot be
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
  Width, height, and scrolloff must be runtime-configurable. The Domains must hold no
  hardcoded geometry assumptions.

.. _arch_out_of_scope:

Explicitly Out of Scope
~~~~~~~~~~~~~~~~~~~~~~~

The following concerns are deliberately excluded from the engine. The host application is
responsible for all of the below.

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
  Operations that modify the text buffer (``insert``, ``delete``, ``backspace``). The cursor may be
  updated as a consequence. The engine does not expose partial results mid-mutation.
  (:doc:`../requirements/f-req_text_manipulation`)

**Cursor Movement**
  Operations that reposition the cursor without modifying text (``move_up``, ``move_down``,
  ``move_left``, ``move_right``, ``move_home``, ``move_end``). Movement at a boundary is a no-op.
  (:doc:`../requirements/f-req_cursor_movement`)

**Cursor Query**
  Returns the current cursor position in a caller-specified coordinate space.
  See :ref:`arch_coordinate_spaces`.
  (:doc:`../requirements/f-req_cursor_movement`)

**Content Query**
  Returns the current text content in a caller-specified form (logical lines, visual lines, or display lines).
  (:doc:`../requirements/f-req_output_modes`)

.. _arch_containers:

Containers
----------

Domain Layer Model
~~~~~~~~~~~~~~~~~~

The engine is divided into three layered domains. Each domain depends only on the one domain directly
below it and is completely independent of the domains above it.

.. note::

   Each domain is represented at runtime by a domain service (e.g. ``VisualDomainService``), which owns the domain's
   internal components and is the sole point of contact for the layer above. This makes each domain independently
   instantiable and unit-testable in isolation. The C4 *container* level is used here because it accurately captures
   this boundary structure.

   The domains are not separately deployable processes; they are bounded objects within a single Python module.
   See :doc:`decisions/arch-c4_model`.

.. Domain Services could be "interfaced" and therefore mocked for unit testing.

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
  viewport to scroll, the Visual Domain is unaffected. Does not mutate cursor or text directly,
  it passes movement requests down to the Visual Domain. Translates between Window and Visual coordinates.

.. _arch_coordinate_spaces:

Coordinate Systems & Output Modes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The cursor exists simultaneously in four coordinate spaces. Each domain is responsible for
translating between the spaces it owns. The four spaces map directly onto the domain structure and
onto the output modes exposed by the public API (See :doc:`../requirements/f-req_output_modes`).

.. _arch_coordinate_ownership:

.. list-table::
   :widths: 15 20 20 45
   :header-rows: 1

   * - Output Mode
     - Domain
     - Coordinate
     - Meaning
   * - Raw
     - Logical
     - Absolute Index
     - Offset in characters from the start of the raw text string
   * - Logical
     - Logical
     - ``(line, col)``
     - Zero-based line number and column within that line
   * - Wrapped
     - Visual
     - ``(row, col)``
     - Zero-based row in the full list of visual lines after wrapping
   * - Display
     - Display
     - ``[x, y]``
     - column and row within the visible window

Container Diagram
~~~~~~~~~~~~~~~~~

.. plantuml:: diagrams/domain_containers.puml

Data Flow: Representative Examples
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. plantuml:: diagrams/seq_insert.puml

.. plantuml:: diagrams/seq_delete.puml

.. plantuml:: diagrams/seq_backspace.puml

.. plantuml:: diagrams/seq_move.puml

.. plantuml:: diagrams/seq_get_lines.puml

.. plantuml:: diagrams/seq_get_cursor.puml

.. _arch_components:

Components
----------

.. _arch_component_descriptions:

Component Descriptions
~~~~~~~~~~~~~~~~~~~~~~

#. :doc:`components/arch-text_buffer` holds the raw text string.
#. :doc:`components/arch-logical_domain_service` tracks the raw text in Logical coordinates.
#. :doc:`components/arch-visual_logical_adapter` adapts the LogicalDomain into the VisualDomain.
#. :doc:`components/arch-cursor_state` tracks the cursor position.
#. :doc:`components/arch-movement_resolver` computes visual coordinates, given a direction.
#. :doc:`components/arch-visual_domain_service` tracks the text and cursor in Visual coordinates.
#. :doc:`components/arch-viewport_state` truncates the visual lines to fit the window.
#. :doc:`components/arch-display_domain_service` tracks the text and cursor in Display coordinates.
#. :doc:`components/arch-facade` coordinates cross-domain operations.

:doc:`arch-component_sequences`

.. toctree::
   :maxdepth: 1
   :caption: Components
   :name: components
   :glob:
   :hidden:

   components/*
   arch-component_sequences.rst


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

   decisions/arch-layers
   decisions/arch-display_domain
   decisions/arch-c4_model
   decisions/arch-cursor_domain
   decisions/arch-position_validation
   decisions/*

Open Questions
--------------

.. _arch_error_contract:

Unresolved Questions
~~~~~~~~~~~~~~~~~~~~~

* **Logging:** Should the engine emit structured logs? If so, at which layer? Facade only, or
  also internal components? Using the standard library ``logging`` module is consistent with the
  dependency constraint, but the scope is unresolved.

Known Limitations
~~~~~~~~~~~~~~~~~

* **Single-threaded only.** No concurrency primitives are used. The engine is not safe to call
  from multiple threads simultaneously.
* **In-memory only.** The entire text buffer is held in memory. There is no streaming or paging
  for large documents.
* **Resize Behavior:** The requirements :need:`INV-VIEW-001` and :need:`INV-WRAP-001` define that `display_width` and
  `display_height` are defined once at initialization and cannot be changed. Dynamic resizing is not supported.

.. Future Evolution
   ~~~~~~~~~~~~~~~~

.. TODO: Fill in future evolution
.. Currently no future evolution is planned. So omitting this section.

Appendix A: Glossary
--------------------

.. include:: arch_glossary.rst

Appendix B: Revision History
-----------------------------

.. include:: arch_history.rst

Indices and tables
------------------
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
