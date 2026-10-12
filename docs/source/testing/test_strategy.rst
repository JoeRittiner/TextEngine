.. _testing_strategy:

Test Strategy
=============

Introduction
------------

Purpose
~~~~~~~

This document describes my Test Strategy. How I approach testing in general.

This document provides me with **structure**. How I should approach Testing as a discipline rather than a "TODO".

Rather than writing a couple of Unit tests and calling it a day, writing this document itself forces me to think how I
want to test this project. The thinking and consistency that the document forces me to establish.
When do I write Unit tests, how do I write them, what tools/ technologies/ methodologies can I and should I rely on.
(Testing Principles, Test Levels, Test Techniques, etc.) As well as when to move on to the next testing levels
(exit/ entry criteria) and when not to. It also makes me think about Test Techniques, what could be valuable for
this project, and why?

Then, the structure tells me how to trace and log tests rather than inventing stuff on-the fly when executing tests.
How to structure the tests themselves, how to group dirs, files, scripts, data, etc.
Makes me think about what metrics are actually important. (E.g. RPI, what "code coverage" actually means, and what
it's value actually is.)

Scope
~~~~~

This document is not meant as a Test Plan. I.e. no concrete decisions on when to test, what specific tools to use etc.
Instead, this descries a guideline.
This Strategy likely will evolve over time. It is currently being written before any implementation details. I might
later realize that different tools, ways of thinking or whatever might change this strategy.

In the case of a change in strategy, the change and reasoning should be documented as well.

Intended Audience
~~~~~~~~~~~~~~~~~~

.. GUIDANCE: Every Responsibility block further down lists Dev / CI / QA /
.. Stakeholder as if they might be distinct people. If they're always the same
.. person, consider stating that once here ("all roles below are held by the
.. author; the labels indicate which hat is worn for which activity") instead
.. of re-justifying it each time it comes up (it currently resurfaces under
.. Acceptance Testing and implicitly under Risk Priority Index).

The primary audience is (again) the author, in multiple roles:

* The Dev: The person implementing the engine, and designing the logic, interfaces, etc. CI maintainer
* The QA: The person responsible for making sure requirements are met, and designed to satisfy Stakeholder needs.
* The Stakeholder: The person who wants to use the finished project. And defines the requirements
* The Learner: Using this project to deliberately learn about and practice writing a test strategy and test plan.
  And learn about/ to live the different roles.

"all roles below are held by the author; the labels indicate which hat is worn for which activity"


Testing Principles
------------------

1. Test against contracts, not implementations.
2. Prefer automation where practical.
3. Use risk (RPI) to determine test depth.
4. Lower test levels provide defect localization; higher levels provide requirement verification.
5. Individual tests may isolate dependencies, but each test level's suite must demonstrate its full intended boundary.
6. Tests should be deterministic and reproducible.
7. Traceability: The relationship between artifacts (requirements, test cases, implementations) should be trackable.

Each of these principles should have concrete explanations in the Test plan. (e.g. How exactly will artifacts be traced
and linked? What tool(s) are used and why? traceability matrix or through links between requirements and tests? etc.)


Test levels
-----------

Unit tests isolate an individual component.
Integration tests integrate all components within an architectural domain while isolating that domain's external
dependencies.
System tests integrate the complete system across domain boundaries.


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

100% Requirement Coverage (Every FR and INV must be tested) and 100% Branch Coverage.

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

Dependencies of components (As described in each components :ref:`arch_component_descriptions`) in the same Domain  may be replaced with a test double or otherwise substituted.
Dependencies of lower domains must be replaced by test doubles. E.g. the `Visual-Logical Adapter`s (Visual Domain) dependency on the `LogicalDomainService`. (Logical Domain)

Test doubles inside the integration boundary are allowed for an individual test, but cannot be the only way that component is exercised at the integration level.

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

Tests that don't rely on test double within the same Domain. (I.e. The visual Domain is tested in full without test doubles of any components in the visual domain. The Logical Domain must be replaced with a test double.)
At the end of integration testing, we have tested the complete domain with its internal components integrated, while external/lower-level dependencies remain isolated/ doubled.

The complete integration test suite includes tests exercising all components within the integration boundary without internal test doubles.

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

.. include:: ./strategy/traceability.rst

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
