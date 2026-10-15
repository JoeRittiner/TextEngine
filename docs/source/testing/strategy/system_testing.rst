.. _test_system_testing:

System Testing
~~~~~~~~~~~~~~

System tests verify the complete system against its functional requirements and invariants, exercising behavior across
domain boundaries and through the Facade.

The test scope covers the system at C4 Levels 1 and/or 2.

The test suite includes the following domain combinations:

* Visual Domain + Logical Domain
* Display Domain + Visual Domain
* **Mandatory:** Display Domain + Visual Domain + Logical Domain
* **Mandatory:** Facade + Display Domain + Visual Domain + Logical Domain

Person Responsibility
.....................

* **Defines tests:** Developer and QA
* **Executes tests:** Developer, QA and CI pipeline
* **Accountable for results:** Developer and QA

Test Level Responsibility
.........................

System testing verifies the system's functional requirements and invariants against the specified behavior.

The suite must exercise the complete system, including interactions across domain boundaries and through the Facade.
Individual tests may isolate domains or use other test controls where useful, provided the required combinations are
covered by the suite.

How?
....

* **Scope:** Verify all applicable functional requirements and invariants, especially behavior that spans multiple
  domains.
* **Automation:** Automate system tests and include them in CI pipelines.

Test Basis
..........

* Functional requirements.
* Invariants.

Entry Criteria
..............

The integration tests for all containers pass.

System tests may be designed before this criterion is met, but execution requires the entry criterion to be satisfied.

Exit Criteria
.............

* Every applicable functional requirement and invariant has traceable verification evidence.
* All required verification activities have passed.
* The test suite covers all mandatory system combinations.

**Verification evidence:** A passing CI run that generates a test report, including the requirement-to-test traceability
matrix. :ref:`test_traceability`

**Requirement coverage:** 100% of functional requirements and invariants must be fully addressed by the system test
suite. Coverage is established through traceability and review of the test cases against each requirement and invariant;
it cannot be established by code coverage alone.

Passing tests provide verification evidence but do not prove the absence of defects.

