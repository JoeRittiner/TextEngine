.. _testing_strategy:

Test Strategy
=============

Introduction
------------

Purpose
~~~~~~~

This document describes my Test Strategy. How I approach testing in general.

"outline that describes the testing approach of the software development cycle"
"to provide a rational deduction from organizational, high-level objectives to actual test activities to meet those objectives from a quality assurance perspective."
"ensure that all objectives are fully covered and understood by all stakeholders."

.. Quoted from Wikipedia: https://en.wikipedia.org/wiki/Test_strategy

"What is our overall testing approach, why are we testing this way, what are our rules, and what determines sufficient testing?"

Scope
~~~~~

 ...

Intended Audience
~~~~~~~~~~~~~~~~~~

The primary audience is (again) the author, in a dual role: as the engineer verifying the engine
against its contract, and as a learner using this project to deliberately learn about and practice writing a test
strategy.

Testing Principles
-------------------

1. Test against contracts, not implementations.
2. Prefer automation where practical.
3. Use risk to determine test depth.
4. Lower test levels provide defect localization; higher levels provide requirement verification.
5. Individual tests may isolate dependencies, but each test level's suite must demonstrate its full intended boundary.
6. Tests should be deterministic and reproducible.

7. Automated tests shall be implemented using an appropriate automated testing framework and executed in CI.
8. Testing is performed continuously throughout development, with regression testing performed automatically in CI.

Test levels
-----------

Unit tests isolate an individual component.
Integration tests integrate all components within an architectural domain while isolating that domain's external
dependencies.
System tests integrate the complete system across domain boundaries.

.. TODO: mock vs stub vs fake vs ...

Unit testing
~~~~~~~~~~~~

What/ Why: Code (C4 Level 4)

Responsibility:
    Who defines the tests? Dev
    Who executes the tests? Dev/ CI
    Who is accountable for the result? Dev

Generally, the Requirements treat the System/ the TextEditor/TextEngine as a black box.
As per :ref:`req_conventions` "This document defines requirements using a strict behavioral model."
Thus testing individual methods/ functions/ classes inside that black box may not satisfy the requirements. And therefore
Unit Tests aren't necessarily meant to fully verify or satisfy a specific requirement as defined in :doc:`../specs/requirements/index`.
Their purpose is for the dev to identify and locate defects.

But they probably will partially map to one or more requirements. Otherwise that piece of code likely isn't contributing
to anything that is needed.

How:
- As broad as possible, as deep as necessary. Why: Catch obvious defects early. Higher levels will test deeper and map to actual requirements fully.
- Automated, including CI pipelines
- (May be triggered manually)

Test Basis
..........

Component/unit contract.

Entry Criteria
..............

Per test object:

Unit tests can't start until interface is stubbed.
Note: As per TDD, the unit test should exist before any implementation. Unit tests should be written to "verify" the function its test object is solving. I.e. Unit tests are written to show the presence of defects in the test object, as defined by the "unit's contract". The objects should then be implemented to fulfill that requirement. _Not_ to "pass the test": "Don't modify the test merely because the implementation fails it." If a test fails, check the implementation, not the test. If a test must be re-written it must be done so to meet the requirement, not the code.
This means, if all tests are implemented and all stubs exist, running the tests can lead to all tests failing. That's OK.

Exit Criteria
.............

Per Component (or container):

Code coverage must be 100%. (As per :need:`NFREQ-QA-221`)
100% coverage = every relevant piece of code was executed

.. TODO: what does "coverage" means in NFREQ-QA-221. Line coverage? Statement? Branch? Decision?

No unresolved defects found by tests that map to requirements with an RPI of 4(?) or higher.

.. Why 4? 4 means at least two of severity 2 (See RPI)

Integration Testing
~~~~~~~~~~~~~~~~~~~

What/ Why: Components

Responsibility:
    Who defines the tests? Dev
    Who executes the tests? Dev/ CI
    Who is accountable for the result? Dev

Integration test should verify/ find defects in the components making sure they adhere to their descriptions. :ref:`arch_component_descriptions`

Dependencies of components (As described in each components :ref:`arch_component_descriptions`) in the same Domain  may be mocked.
Dependencies of lower domains must be mocked. E.g. the `Visual-Logical Adapter`s (Visual Domain) dependency on the `LogicalDomainService`. (Logical Domain)

A mock inside the integration boundary is allowed for an individual test, but cannot be the only way that component is exercised at the integration level.

The integration test suite must demonstrate integration of all components within its defined boundary, but individual test cases may isolate components within that boundary when doing so provides useful test control.

How:
- As deep as possible.
- Automated, including CI pipelines
- (May be triggered manually)

Test Basis
..........

Component descriptions (:ref:`arch_component_descriptions`) + domain boundaries + interaction contracts.
.. TODO: add relevant :ref:

Entry Criteria
..............

Per Component

Unit Test Exit Criteria for this Component is met.

Exit Criteria
.............

Per Container

Tests that don't rely on mocks within the same Domain. (I.e. The visual Domain is tested in full without mocking any components in the visual domain. The Logical Domain must be mocked.)
At the end of integration testing, we have tested the complete domain with its internal components integrated, while external/lower-level dependencies remain isolated/ mocked.

The complete integration test suite includes tests exercising all components within the integration boundary without internal mocks.

System testing
~~~~~~~~~~~~~~

What/ Why: Containers/ Full System End-to-End

Responsibility:
    Who defines the tests? Dev/ QA
    Who executes the tests? Dev/ QA/ CI
    Who is accountable for the result? Dev/ QA

All functional requirements and invariants.

The system test suite must demonstrate the complete system, but individual test cases may isolate domains when doing so provides useful test control.

How:
- As broad and deep as possible
- Automated, including CI pipelines?

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

Acceptance Testing
~~~~~~~~~~~~~~~~~~

What/ Why: Interface, UX

Responsibility:
    Who defines the tests? Stakeholder / Product Owner
    Who executes the tests? Stakeholder / Product Owner
    Who is accountable for the result? Dev/ QA

This is more about "testing" the requirements and interfaces themselves. Now that it's tested and live, does this
requirement/ decision/ interface still make sense as written?

How:
- Manual

Test Basis
..........

Requirements + interfaces + stakeholder expectations.

Entry Criteria
..............

Integration or System Tests.

Exit Criteria
.............

User satisfaction? (How to measure)

Each requirement (especially high priority ones, as defined by their RPI) is considered and accepted. The interface(s)
are also looked at and accepted.

Risk Priority Index
-------------------

- **Business Relevanz:** Auswirkung im Fehlerfall, wie schlimm ist ein Fehler? (3 = am schlimmsten)
- **Auffindbarkeit:** Wie offensichtlich und schnell kann ein Fehler entdeckt werden (3 = schwer und aufwendig erkennbar)
- **Komplexität:** Wie komplex ist die Anforderung und die dazu notwendige Umsetzung und Realisierung? (3 = sehr komplex)

"Das Produkt dieser drei Kriterien führt zum «Risiko Prioritäts Index (RPI)».
Der so ermittelte RPI ist ein Führungsinstrument und bildet die Grundlage
für die konsequente Bestimmung der Testtiefe, des Testumfangs sowie der
Testreihenfolge."

  RPI >= 27  ->  Very High
  RPI >= 12  ->  High
  RPI >= 6   ->  Medium
  RPI >= 2   ->  Low
  RPI >= 1   ->  Very Low

Test Techniques
---------------

Static Testing
~~~~~~~~~~~~~~

E.g.
- Reviews
- Inspections
- Static analysis
- ...

(Solo Project, so...)

Dynamic Testing
~~~~~~~~~~~~~~~

- Equivalence Partitioning
- Boundary Value Analysis
- Decision Table Testing
- State Transition Testing
- Property-Based Testing
- ...

Test Environment & Test Data
----------------------------

.. What properties must the test environment have?

Test data should be deterministic, reproducible, version-controlled where appropriate, and representative of relevant equivalence classes/boundary conditions.

.. The system is pure-logic/deterministic. Therefore it is basically independent of the Test Environment. (Python Version and library versions?) A simplification because of the architecture.
.. Fixtures: input strings/configs

Test Automation & CI
--------------------


.. Tool: Sphinx-Test-Reports

.. @pytest.mark.requirement("FR-INIT-001")
.. def test_text_editor_initialization():



Regression test approach
------------------------

.. When something changes, what tests do we rerun?

Every change -> Unit tests
Relevant domain changed -> Domain integration tests
System-impacting change -> System regression suite
Release/acceptance/Requirement -> Acceptance regression


Defect Management
-----------------

.. How a failing test becomes a tracked issue, severity/priority, (distinct from RPI) and how it's linked back to the requirement it violates.
.. "Test status collections and reporting"

.. Tracked: A GitHub Issue is created containing a description of the defect, relevant test information, severity/priority, and sufficient information for reproduction. (Also the requirement ID)
.. A defect should be tracked when it represents outstanding work that cannot or should not be resolved as part of the current development activity.
.. separate "tracking" from "documenting."

Requirements Traceability
-------------------------

.. explain how that traceability works.

Test Records & Reporting
------------------------

.. what constitutes test evidence
.. what results are recorded
.. how test results are retained
.. how test results relate to requirements
.. what constitutes a test summary
.. who reviews/approves results


Metrics
-------

.. Flag :need:`NFREQ-PERF-211` (performance) as an ambiguous/untestable requirement.

.. "requirement testability review" before writing a test plan?

Test Organization
-----------------

Testing tools
-------------

.. Strategy can define tool policy; specific tools may belong in Plan

Test Groups
-----------

.. Strategy can define grouping principles; exact groups probably Plan

Given (roughly) by the architecture: Container -> Component -> Class

.. RPI for Groups?
