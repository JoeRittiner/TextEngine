.. _test_acceptance_testing:

Acceptance Testing
~~~~~~~~~~~~~~~~~~

Acceptance testing evaluates whether the system meets stakeholder needs and is fit for its intended use. It also
provides an opportunity to identify requirements, design decisions, or interfaces that no longer match stakeholder
expectations.

Person Responsibility
.....................

* **Defines acceptance criteria:** Stakeholder, supported by Developer and QA
* **Executes tests:** Stakeholder, supported by Developer and QA
* **Makes the acceptance decision:** Stakeholder
* **Resolves identified defects:** Developer

Test Level Responsibility
.........................

Acceptance testing evaluates the system from the stakeholder's perspective, rather than focusing on its internal
implementation.

Relevant requirements, particularly high-priority requirements as indicated by their RPI, are reviewed against their
intended purpose and acceptance criteria. The interfaces and user workflows are also evaluated for suitability and
usability.

How?
....

* Manual testing.
* Exploratory testing.
* Scenario-based testing using representative user workflows.
* Review of requirements, interfaces, and stakeholder expectations.

Test Basis
..........

* Functional requirements and invariants.
* Acceptance criteria.
* Stakeholder expectations and intended use.
* Relevant interfaces and user workflows.

Entry Criteria
..............

System Tests pass, and the system is sufficiently stable for acceptance testing.

Exit Criteria
.............

* Relevant requirements and acceptance criteria have been reviewed and evaluated.
* Relevant interfaces and user workflows have been evaluated.
* Acceptance criteria are met, or outstanding deviations are explicitly documented and accepted by the responsible stakeholder.
* The Stakeholder / Product Owner records the acceptance decision.

Acceptance is based on stakeholder judgment against agreed criteria; it is not established by code coverage or passing
tests alone.
