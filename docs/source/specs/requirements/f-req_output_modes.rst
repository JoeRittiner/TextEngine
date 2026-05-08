4.6 Output Modes
================

4.6.1 Description and Priority
------------------------------
**Priority: High**

The system must provide four distinct output modes to support different levels of abstraction for external interfaces:
**Display**, **Wrapped**, **Logical**, and **Raw**. See :ref:`req_software_interfaces`.

These modes allow consumers to view the :term:`text buffer` as a raw string, a collection of
:term:`logical lines <logical line>`, a fully wrapped :term:`text buffer` (:term:`visual lines <visual line>`),
or a windowed :term:`viewport` (:term:`display lines <display line>`).

4.6.2 State Invariants
----------------------

.. inv:: Read-Only Operations
   :id: INV-MODE-001
   :tags: mode, state

   Requesting output in any mode must be a non-destructive operation. It must not modify the :term:`text buffer`, change
   the :term:`cursor` position, or alter the :term:`viewport` range.

.. inv:: Buffer-Based Idempotency
   :id: INV-MODE-002
   :tags: mode, state

   For **Raw**, **Logical**, and **Wrapped** modes, the output must remain identical across multiple requests as long as
   the :term:`text buffer` state remains unchanged.

.. inv:: Viewport-Dependent Idempotency
   :id: INV-MODE-003
   :tags: mode, state

   For **Display Mode**, the output is a function of both the :term:`text buffer` state and the current :term:`viewport`
   range. The output only remains identical if both the :term:`buffer <Text Buffer>` content and the :term:`window`
   boundaries (:term:`window start`) are unchanged.


4.6.3 Preconditions
-------------------

All operations in this section assume a valid :term:`text buffer` as per :doc:`f-req_text_manipulation`.

All operations in this section assume a valid :term:`display width` as per :doc:`f-req_text_wrapping`.

All operations in this section assume a valid :term:`display height` and :term:`viewport` as per :doc:`f-req_window`.

4.6.4 Stimulus/Response Sequences
---------------------------------

* **Stimulus:** An external consumer requests the :term:`buffer <Text Buffer>` content in a specific output mode.

  **Response:** The system evaluates the current state against the requested mode's logic and returns the formatted data.

4.6.5 Functional Requirements
-----------------------------

Raw Mode
~~~~~~~~

.. freq:: Raw Text Output
   :status: Open
   :id: FR-MODE-001
   :tags: raw mode, mode

   The system must provide an interface to return the entire content of the :term:`text buffer` as a single, continuous
   string of :term:`characters <character>`.

   This output must include all newline characters (``\n``) exactly as they exist in the :term:`buffer <Text Buffer>`
   without modification.

Logical Mode
~~~~~~~~~~~~

.. freq:: Logical Line Output
   :status: Open
   :id: FR-MODE-011
   :tags: logical mode, mode

   The system must provide an interface to return the contents of the :term:`text buffer` as a sequence of
   :term:`logical lines <logical line>`.

   The sequence must be split at newline characters (``\n``), and the newline characters themselves must be excluded
   from the returned strings.

Wrapped Mode
~~~~~~~~~~~~

.. freq:: Wrapped Visual Output
   :status: Open
   :id: FR-MODE-021
   :tags: wrapped mode, mode
   :links: FR-WRAP-003

   The system must provide an interface to return the entire :term:`text buffer` as a sequence of
   :term:`visual lines <visual line>`, calculated based on the current ``display_width``.

   The wrapping logic must strictly follow :need:`FR-WRAP-003`.

.. freq:: Visual-to-Logical Mapping
   :status: Open
   :id: FR-MODE-022
   :tags: wrapped mode, mode

   The output for Wrapped Mode must include metadata or a structural representation indicating which
   :term:`visual lines <visual line>` belong to which :term:`logical line`.

Display Mode
~~~~~~~~~~~~

.. freq:: Viewport-Truncated Output
   :status: Open
   :id: FR-MODE-031
   :tags: display mode, mode
   :links: INV-VIEW-001, INV-VIEW-003

   The system must provide an interface to return only the subset of :term:`visual lines <visual line>` currently
   visible within the :term:`window`.

   The number of lines returned must not exceed the :term:`display height`, and the content must correspond to the
   range defined by :term:`window start`.

.. freq:: Display-to-Logical Mapping
   :status: Open
   :id: FR-MODE-032
   :tags: display mode, mode

   The output for Display Mode must include metadata indicating which :term:`display lines <display line>` belong to
   which :term:`logical line`.

4.6.6 Out of Scope
------------------

.. nreq:: Rendering & I/O
   :id: NR-MODE-101
   :tags: out-of-scope

   The system does not handle any rendering or GUI operations.
