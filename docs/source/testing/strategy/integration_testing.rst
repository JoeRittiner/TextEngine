.. _test_integration_testing:

Integration Testing
~~~~~~~~~~~~~~~~~~~

What/ Why:
    Components (C4 Level 3)
    Full Classes, Multiple Components

    E.g. `Cursor`, and `LogicalDomainService` + `TextBuffer`,
        and all "Logical Domain Layer" Components together


Person Responsibility
.....................

Who defines the tests? Dev
Who executes the tests? Dev/ CI
Who is accountable for the result? Dev


Test Level Responsibility
.........................

Integration test should verify/ find defects in the components making sure they adhere to their descriptions. :ref:`arch_component_descriptions`

Dependencies of components (As described in each components :ref:`arch_component_descriptions`) in the same Domain  may be replaced with a test double or otherwise substituted.
Dependencies of lower domains must be replaced by test doubles. E.g. the `Visual-Logical Adapter`s (Visual Domain) dependency on the `LogicalDomainService`. (Logical Domain)

Test doubles inside the integration boundary are allowed for an individual test, but cannot be the only way that component is exercised at the integration level.

The integration test suite must demonstrate integration of all components within its defined boundary, but individual test cases may isolate components within that boundary when doing so provides useful test control.


How?
....
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

.. GUIDANCE: the two paragraphs above this say much the same thing twice --
.. worth merging into one. Also decide whether Integration needs its own
.. RPI-driven exit condition (like Unit's "no unresolved defects at RPI>=4"),
.. or whether "no internal mocks remain" is the only gate at this level.