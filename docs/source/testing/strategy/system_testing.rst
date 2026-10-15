.. _test_system_testing:

System Testing
~~~~~~~~~~~~~~

What/ Why:
    Containers
    Full System End-to-End (C4 Levels 2 and/ or 1)

    E.g. Logical Domain + Visual Domain
        and Visual Domain + Display Domain
        and all three
        and all three + Facade


Person Responsibility
.....................

Who defines the tests? Dev/ QA
Who executes the tests? Dev/ QA/ CI
Who is accountable for the result? Dev/ QA


Test Level Responsibility
.........................

All functional requirements and invariants.

The system test suite must demonstrate the complete system, but individual test cases may isolate domains when doing so provides useful test control.


How?
....

- As broad and deep as possible
- Automated, including CI pipelines

.. GUIDANCE: given the engine is deterministic pure logic, is there a real
.. reason this stays a "?" -- consider just deciding this one.

Test Basis
..........

Requirements + invariants.

Entry Criteria
..............

The Integration Tests of all Containers are passing.

Exit Criteria
.............

Every applicable functional requirement and invariant has
traceable verification evidence, and all required verification
activities have passed.

100% Requirement Coverage (Every FR and INV must be tested)

.. GUIDANCE: "traceable verification evidence" -- decide now what counts as
.. evidence (a passing CI run? a generated report?) since Test Records &
.. Reporting further down still needs to define this term, and this criterion
.. depends on that definition existing.
