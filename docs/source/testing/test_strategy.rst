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

Then, the structure tells me how to trace and log tests rather than inventing stuff on-the-fly when executing tests.
How to structure the tests themselves, how to group dirs, files, scripts, data, etc.
Makes me think about what metrics are actually important. (E.g. RPI, what "code coverage" actually means, and what
its value actually is.)

Scope
~~~~~

This document is not meant as a Test Plan. I.e. no concrete decisions on when to test, what specific tools to use etc.
Instead, this describes a guideline.
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

* The Dev: The person implementing the engine, and designing the logic, interfaces, etc.
* The CI maintainer: ...
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

.. include:: ./strategy/unit_testing.rst

.. include:: ./strategy/integration_testing.rst

.. include:: ./strategy/system_testing.rst

.. include:: ./strategy/acceptance_testing.rst

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

* Reviews
* Inspections
* Static analysis
* ...

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

Test data should be deterministic, reproducible, version-controlled where appropriate, and representative of relevant
equivalence classes/boundary conditions.

The system is pure-logic/deterministic. Therefore it is basically independent of the Test Environment.
(Minimum Python version and library versions must be defined) A simplification because of the architecture.
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
