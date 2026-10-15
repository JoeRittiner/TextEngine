.. _test_integration_testing:

Integration Testing
~~~~~~~~~~~~~~~~~~~

Integration tests verify that components within the same container / domain interact correctly and collectively fulfill
the domain's intended behavior.

For example, testing `LogicalDomainService` together with `TextBuffer` can reveal defects in how the service uses the
buffer, even when both components pass their unit tests independently.

Person Responsibility
.....................

* **Defines tests:** Developer
* **Executes tests:** Developer and CI pipeline
* **Accountable for results:** Developer

Test Level Responsibility
.........................

Integration tests verify the behavior and interactions of components within a container, as described in
:ref:`arch_containers` and :ref:`arch_component_descriptions`.

Requirements generally specify the system (`TextEngine`) as a black box, using a strict behavioral model
(:ref:`req_conventions`). Integration tests therefore focus on domain-level behavior and interactions rather than
necessarily verifying complete system-level requirements.

Dependencies on lower domains must be replaced with test doubles to keep the integration boundary isolated. For
example, integration tests of the Visual Domain replace its dependency on the `LogicalDomainService` in the Logical
Domain with a test double.

Test doubles may also replace components within the integration boundary in individual tests where this provides useful
control. However, the suite must include tests that exercise all components within the boundary together, without
internal test doubles.

How?
....

* **Scope:** One domain / container per integration test suite.
  Test component interactions and the resulting domain behavior.
  Higher test levels verify behavior across domain boundaries and against system-level requirements.
* **Isolation:** Replace dependencies on lower domains with test doubles.
  Internal components may be doubled in individual tests, but the suite must also exercise their real integration.
* **Automation:** Automate integration tests and include them in CI pipelines.
* **Execution:** Tests may also be triggered manually during development.

Test Basis
..........

The test basis defines the intended behavior and interactions against which the integrated components are tested.

It consists of:

* Container and component descriptions in the architecture documentation (:ref:`arch_containers`,
  :ref:`arch_component_descriptions`), which define responsibilities and boundaries.
* Component contracts and interfaces, which specify the behavior expected from each component.
* Expected interactions, including relevant data passed between components, call sequences where significant, and
  resulting state changes.
* Requirements and invariants relevant to the domain and its components, linked to tests according to
  :ref:`test_traceability`.
* Applicable design documentation, where needed to clarify intended behavior or interactions.

The test basis must make the expected interactions clear enough to determine whether the integrated behavior is correct.
Component contracts describe individual components; the architecture and applicable requirements provide the context for
how those components are expected to work together.

Entry Criteria
..............

Per container, before executing integration tests:

* The interfaces and intended interactions of the components are defined sufficiently to determine expected behavior.
* Unit test exit criteria are met for each component in the container.

**Test-driven development (TDD):** Integration tests may be designed and written before these criteria are met. The
criteria govern execution, not when test design may begin.

Exit Criteria
.............

Per container:

* The integration test suite passes.
* All components within the container are exercised together in tests without internal test doubles.
* Relevant interactions between components are covered by tests.
* Any test doubles used for lower-domain dependencies remain outside the integration boundary.

Passing integration tests provides evidence that the domain's components work together as intended. It does not
establish that behavior across domain boundaries or complete system-level requirements has been verified; those are
addressed at higher test levels.
