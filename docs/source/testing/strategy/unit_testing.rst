.. _test_unit_testing:

Unit Testing
~~~~~~~~~~~~

Unit tests verify the behavior of individual components. Such as functions, methods and classes.

Example: `CursorState.move_up()`

Their primary purpose is to detect and localize defects early in development.


Person Responsibility
.....................

* **Defines tests:** Developer
* **Executes tests:** Developer and CI pipeline
* **Accountable for results:** Developer


Test Level Responsibility
.........................

Requirements generally specify the system (`TextEngine`) as a black box, using a strict behavioral model
(:ref:`req_conventions`).

Consequently, a unit test may verify only part of a requirement's behavior and does not necessarily establish that the
requirement is fully satisfied. Unit tests primarily support early defect detection and localization.

Unit tests should nevertheless be traceable to relevant requirements where applicable. Requirements that span multiple
components or describe system-level behavior may require integration or system tests for complete verification.


How?
....

* **Scope:** Test as broadly as practical and as deeply as necessary to detect defects early. Higher test levels
  verify behavior across component boundaries and against system-level requirements.
* **Automation:** Automate unit tests and include them in CI pipelines.
* **Execution:** Tests may also be triggered manually during development.

Test Basis
..........

The test basis defines the expected behavior against which a unit is tested. Unit tests must be derived from documented
behavior and requirements, not (solely) from the current implementation.

The test basis consists of:

* Component descriptions in the architecture documentation (:ref:`arch_component_descriptions`), which describe each
  component's responsibilities, behavior, and place within the system.
* Requirements and invariants relevant to the component. These are the authoritative source for required behavior and
  are linked to tests according to :ref:`test_traceability`.
* Component contracts, including interface definitions, preconditions, postconditions, invariants, and behavioral
  constraints, where these are needed to make the expected behavior unambiguous.
* Applicable design documentation, where additional detail is necessary to understand the intended behavior.

Component contracts are documented at the most appropriate level:

* Architecture documentation describes the component's responsibilities, externally relevant behavior, and interactions
  with other components.
* Docstrings describe the behavior of public classes and methods, including relevant preconditions, postconditions,
  exceptions, and side effects.
* Type annotations define the expected types of inputs and outputs. They complement the behavioral contract but do not,
  by themselves, specify what a method must do.
* Explicit contract statements document non-obvious constraints, invariants, or behavioral requirements that cannot be
  expressed clearly through the above alone.

These sources should complement one another rather than duplicate the same information unnecessarily. Requirements
remain authoritative for required system behavior. If the sources conflict or leave expected behavior ambiguous, the
discrepancy must be resolved before the affected tests are considered complete.

Unit tests are written against the intended contract, not the implementation's internal details. Where practical, the
interface is defined before implementation and tests are written against that interface before the behavior is
implemented, following a test-first approach. Tests are reviewed against the test basis to ensure that their expected
results are justified independently of the implementation.

.. Explicit component contracts are in the architecture.

Test Oracle
...........

.. The means of determining whether the actual result is correct (e.g., expected values, invariants, a reference implementation).

.. The test oracle determines whether the observed behavior of a unit is correct.

Expected results and assertions must be justified by the applicable test basis, such as a component contract,
requirement, invariant, or defined input-output relationship. Depending on the behavior under test, the oracle may
specify an exact expected result, a property that must always hold, an exception that must be raised, or a state
transition that must occur.

The implementation under test must not be the sole authority for determining expected results. Deriving expectations
exclusively from the implementation risks reproducing the same defects in the tests.

Where the expected behavior cannot be determined unambiguously from the test basis, the contract or requirement must be
clarified before the test is treated as valid verification evidence.


Entry Criteria
..............

For each unit under test:

* Its interface is defined sufficiently to write tests against it.
* The intended behavior is specified well enough to determine expected results.
* Tests can be written independently of the implementation, following the test-first approach where practical.

**Test-driven development (TDD):** Write tests before implementing the corresponding behavior. Initially, tests may
fail because the behavior is not yet implemented. A failure should prompt investigation: check the implementation
against the contract, and check the test against the requirement and intended behavior. Change a test only when its
assumptions or expectations are incorrect—not merely to make the implementation pass.

Exit Criteria
.............

For each component:

* **Branch coverage:** 100% of relevant branches are exercised by unit tests. Any exclusions must be justified and
  documented.
* **Requirement coverage:** Every requirement assigned to the component is linked to one or more unit tests, and all
  those tests pass.

Passing tests provide verification evidence; they do not prove the absence of defects. Requirements that involve
behavior beyond the component's scope must also be verified at the appropriate higher test level.

Test coverage measurement and tooling are defined in :ref:`test_automation_ci`.