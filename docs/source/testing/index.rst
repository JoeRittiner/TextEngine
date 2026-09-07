.. _testing_index:

Testing
=======

Introduction
------------

Purpose
~~~~~~~

This section records how, why, and to what extent the ``TextEditor`` engine is tested. Testing is
part of the project's specification-first methodology: tests are not an afterthought, they are a
first-class deliverable that traces back to individual requirements, in the same way the
:doc:`../specs/architecture/index` traces back to the :doc:`../specs/requirements/index`.

Where the SRS defines *what* the system must do, and the architecture defines *how* it is
structured to do it, this section defines how confidence in *both* is established and
maintained over the life of the project.

Scope
~~~~~

This section covers all testing of the engine itself: unit, property-based, integration,
system, and acceptance testing, together with the strategy, planning, and traceability
that ties them back to the SRS. It does not cover testing of host applications that consume
the engine; that responsibility belongs to the host, per :ref:`arch_out_of_scope`.

Intended Audience
~~~~~~~~~~~~~~~~~~

The primary audience is the author, in a dual role: as the engineer verifying the engine
against its contract, and as a learner using this project to deliberately practice test
design and test planning as a discipline, not just test implementation. A secondary
audience is any future contributor who needs to understand what is tested, at what level,
and why, before adding new tests or code.

Relationship to Other Documents
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Software Requirements Specification (SRS):** :doc:`../specs/requirements/index` -
  every ``FR-*`` and ``INV-*`` need is a candidate test target. This section does not restate
  requirements; it references them via traceability.
* **Architecture:** :doc:`../specs/architecture/index` - the domain and component boundaries
  that determine mock boundaries for isolation testing, and the layering that determines
  integration test scope. See :ref:`arch_containers`.
* **Error Contract:** :doc:`../specs/architecture/arch-error_contract` - defines the
  exception types that dedicated negative tests must verify.

References
~~~~~~~~~~

* ISO/IEC/IEEE 29119, *Software Testing* (test process and documentation vocabulary this
  section borrows from: test policy, test strategy, test plan, entry/exit criteria).
* ISTQB Glossary of Testing Terms: https://glossary.istqb.org/
* "Testing shows the presence, not the absence of defects." - attributed to Dijkstra;
  the working assumption behind the risk-based approach in :doc:`test_strategy`.
* Property-based testing: https://hypothesis.readthedocs.io/

Document Conventions
~~~~~~~~~~~~~~~~~~~~~

This section distinguishes three axes that are easy to conflate and are kept separate
throughout the Testing documentation:

* **Test Level** - *where* in the system a test operates: Unit, Integration, System,
  Acceptance. Defined by scope, not by tooling.
* **Test Type** - *what quality characteristic* is being evaluated: functional,
  structural, non-functional (e.g. performance). A single level may contain multiple types.
* **Test Technique** - *how* a test case is designed: equivalence partitioning, boundary
  value analysis, decision tables, state transition testing, property-based testing. A
  technique is chosen per requirement, independent of level.

A requirement is only as testable as its acceptance criteria are measurable. Where an SRS
or architecture need lacks a measurable criterion (e.g. :need:`NFREQ-PERF-211`'s
"highly performant" is not yet quantified), that gap is recorded rather than silently
worked around; see :doc:`test_strategy`.

Testing Objectives
-------------------

* Verify that every measurable, testable requirement (``FR-*``, ``INV-*``) is actually met.
* Establish and maintain traceability from test cases back to the requirement(s) they verify.
* Surface defects and design flaws as early as possible, ideally before implementation
  (test-first), rather than after.
* Where a requirement is not measurable as written, surface that as a specification gap
  rather than inventing an unstated acceptance criterion.

Testing Principles
-------------------

* **Testability.** Per :need:`NFREQ-QA-221`, the project must be 100% unit-testable, and
  100% unit-test coverage is the goal.

* **Requirement traceability.** Every ``FR-*`` and ``INV-*`` in the
  :doc:`../specs/requirements/index` maps to at least one test. The mapping is maintained
  in :doc:`test_strategy`.

* **Tests without a requirement are permitted, narrowly.** Only for implementation details
  internal to a domain. A ``MovementResolver``, for example, is not itself a requirement,
  but implements core behaviour required to fulfil one and is worth testing independently.

* **Invariants are properties, not examples.** State invariants are verified with
  property-based tests (:doc:`property_based`), not only example-based unit tests. See also
  :need:`NFREQ-QA-222`.

* **Domain isolation.** Each domain is unit-tested in isolation by mocking the domain
  service immediately below it (:ref:`arch_containers`). A test of the Display Domain
  supplies a mock ``VisualDomainService`` and never instantiates the Visual or Logical
  Domains.

* **Domain expansion.** Each domain is also integration-tested with the domain immediately
  below it, using the real service instead of a mock, to verify the contract between them
  holds in practice, not just on paper.

* **No host dependency.** No test requires a GUI framework, terminal library, or external
  process. Every test runs in a standard ``pytest`` session with no special setup
  (:need:`NFREQ-QA-221`).

* **Risk-based, not exhaustive.** Exhaustive testing is impossible. Test effort is
  allocated using a per-requirement risk priority, not spread evenly; see
  :doc:`test_strategy`.

Motivation
~~~~~~~~~~

Beyond verifying the engine, this section exists as a deliberate exercise in test
*design* and test *planning*, not only test *implementation*. Writing a real test
strategy and test plan, choosing techniques and levels intentionally rather than
defaulting to "unit tests and done," and practicing a test-first mindset are treated
as project goals in their own right, alongside the correctness of the engine itself.

Out of Scope
------------

* **Exhaustiveness.** The engine's state space is not exhaustively tested; coverage is
  guided by risk and by requirement, not by attempting every possible input.
* **Host application testing.** Rendering, input handling, and any host-side behaviour
  are outside this engine's boundary (:ref:`arch_out_of_scope`) and outside this section.
* **Performance benchmarking against a numeric target**, until :need:`NFREQ-PERF-211` is
  given a measurable acceptance criterion. Until then, performance is a qualitative
  observation, not a pass/fail test.

Contents
--------

.. toctree::
   :maxdepth: 2
   :glob:

   test_strategy
   test_plan
   test_*

Related Documents
------------------

* :doc:`../specs/requirements/index`: the behavioural contracts under test.
* :doc:`../specs/architecture/index`: the domain structure that determines mock boundaries.
* :doc:`../specs/architecture/arch-error_contract`: error conditions that require dedicated
  tests.

.. * :doc:`../guides/contributor`

Appendix: Glossary
-------------------

:doc:`../../glossary`

Indices and tables
-------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. This "Testing" section should include everything related to testing.
.. - Why: personal philosophy and motivation for testing this project specifically. Learn to
..   effectively *design*, not just implement, unit tests, property-based tests, integration
..   tests, system tests, acceptance tests, and their relation to requirements and quality.
..   Learn to plan tests: Test Strategy vs Test Plan, what belongs in each, test levels,
..   execution, analysis, documentation. Train a test-first mindset.
.. - Why (professional): make sure all measurable and testable requirements are met.
.. - What: what is tested at what level, and why. "Exhaustive testing is impossible."
.. - Test Levels / Test Strategy:
..     - Automated: unit tests during dev (inform debugging) -> property-based + unit once
..       "done" (verify requirements) -> integration (one container, with mocking) -> system
..       (all containers/domains together).
..     - CI/CD: pushes/merges on main-ish branches run the suites above.
..     - Manual: acceptance tests - is the interface intuitive, does it work as intended.
..     - Performance testing: unresolved, see NFREQ-PERF-211 measurability gap above.
.. - Documentation: what/why/how/why-that-way is tested; auto coverage + doc updates via
..   Sphinx-Needs / CI.
.. - Risk Assessment: assign each requirement an RPI, to learn to think about risk estimation.
.. - Test Objectives: verify requirements met; find defects; traceability of tests to reqs.