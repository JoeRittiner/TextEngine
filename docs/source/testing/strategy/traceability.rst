Requirements Traceability
-------------------------

Traceability links every requirement to the tests that verify it, and every test to the requirements it verifies.
This shows four things:

* **Coverage:** A requirement without a test is unimplemented, untested, or cannot be verified.
* **Justification:** A test without a requirement checks something nobody specified, or contributes nothing and is
  likely dead weight.
* **Impact:** When a requirement changes, its linked tests show what to review. When a test fails, its linked
  requirements show what is affected.
* **Evidence:** For each requirement, whether it was verified and by which tests.

A requirement that cannot be linked to a test because it cannot be measured is likely poorly defined, or is not a
requirement at all. This is a specification defect to be fixed, not an exemption to be granted. Until it is fixed,
it is reported as *Not Covered*, so the gap stays visible.

.. KNOWN GAP (current): NFREQ-PERF-211 is not measurable as written, so it will report "Not Covered"
   until it is quantified (see Metrics).

Scope
~~~~~

In this section, "requirement" means any traceable need: a functional requirement (``FR-*``), a state invariant
(``INV-*``) or a non-functional requirement (``NFREQ-*``). Out-of-scope statements (``NR-*``) are not traced.

Tests of every level are traced, both automated and manual. Manual tests (acceptance) are traced the same way:
each manual test record names the requirement IDs it covers, and its result. How those records are captured will
be defined in the Test Plan.

Link Rules
~~~~~~~~~~

* Every test declares the ID(s) of the requirement(s) it verifies. A link states that the test verifies *at least
  a part* of the requirement, not that it verifies all of it.
* **Unit tests** link to the specific requirements the tested behaviour verifies. These are typically found on the
  component's page in the architecture documentation (:ref:`arch_components`). A requirement that a test verifies
  but the page does not cite is a gap in one or the other and should be resolved.
* **Integration tests** link to the requirements of the components being integrated, or to a requirement that only
  emerges from their interaction within the domain.
* **System tests** link directly to the requirement they verify, typically one that spans several domains.
* A test of an internal detail that no requirement describes is permitted, but it must be marked explicitly as
  having no requirement. "No link" is then always a deliberate, visible choice, never an accident.

Each link is stored in exactly one place: with the test. Everything else is derived and never stored or edited by
hand: the other direction (requirement to tests), the matrix, and any grouping by requirement type (``FR``,
``INV``, ``NFREQ``) or category (e.g. ``TEXT``, ``QA``), which is read from the ID. This keeps the two directions
from drifting apart. Links must be machine-readable and live with the test, so that the views below can be
generated. How tests declare them is decided in the Test Plan.

Requirement IDs are therefore the stable key of the whole scheme. An ID is never reused for a different requirement
and never renumbered. The ID of a removed requirement is retired. When a requirement is changed or removed, its
linked tests are reviewed as part of the same change.

Derived Views
~~~~~~~~~~~~~

Two views are derived from the links:

* **Requirement to tests (forward):** For each requirement, its linked tests and their results. A requirement
  without tests is a coverage gap.
* **Test to requirements (backward):** For each test, the requirements it verifies. A test with no requirement and
  no explicit exemption is flagged for review. A test linked to many requirements is also flagged: it may be doing
  too much. This is a signal to review, not a violation.

Both views are presented in a Requirements Traceability Matrix (RTM), generated automatically from test results.
The RTM includes requirements with no linked tests and tests with no linked requirements, so gaps are shown rather
than hidden.

Goal: Each requirement in the specification also displays its verification status. This is a goal, not a
commitment. The Test Plan must confirm that it is feasible.

Verification Status
~~~~~~~~~~~~~~~~~~~

Each requirement has exactly one verification status, derived from the results of its linked tests. If more than
one status applies, the one with the lowest precedence number wins.

.. NOTE: rows 1 and 2 can never overlap with anything else. Precedence really only decides between
   Defect (3), Unverified (4) and Verified (5): a failure beats a skip, and a skip beats a pass.

.. list-table::
   :header-rows: 1
   :widths: 10 14 33 43

   * - Precedence
     - Status
     - Condition
     - Meaning
   * - 1
     - Not Covered
     - No test is linked to the requirement.
     - Nothing verifies it. It is unimplemented, untested, or untestable as written.
   * - 2
     - Not Run
     - Every linked test was skipped.
     - Tests exist, but none produced a result.
   * - 3
     - Defect
     - At least one linked test failed or errored.
     - The requirement is considered not met until the failure is resolved.
   * - 4
     - Unverified
     - At least one linked test was skipped, and none failed.
     - Some verification is missing. The tests that did run found no defects.
   * - 5
     - Verified
     - Every linked test ran and passed.
     - No defects were found. This is not proof that the requirement is met (see below).

A test that errors (cannot run to completion) is treated as failed. Only *Verified* counts as traceable verification
evidence for the System Testing exit criteria. Every other status blocks them until it is resolved or the
requirement is amended.

*Verified* means no defects were found. It does not prove that the requirement is fully met, nor that its tests are
adequate. Traceability shows that verification exists and what its results were. Whether that verification is
sufficient is addressed by the test techniques, coverage criteria and RPI-driven depth defined elsewhere in this
document.
