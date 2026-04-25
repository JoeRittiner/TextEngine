4.1 Text Buffer & Manipulation
==============================

4.1.1 Description and Priority
------------------------------
**Priority: High**

The :term:`Text Buffer` is the conceptual source of truth for document content. It is modeled as a continuous sequence
of :term:`characters <character>`.

The :term:`buffer <Text Buffer>` defines the observable state of the document. All text manipulation operations modify
this state.

4.1.2 State Invariants
----------------------

.. inv:: Empty Buffer Definition
   :id: INV-TEXT-001

   The :term:`buffer <Text Buffer>` must always represent at least one :term:`logical line`.
   An empty :term:`buffer <Text Buffer>` is defined as a :term:`buffer <Text Buffer>` containing zero
   :term:`characters <character>`.

.. inv:: Left-to-right Script
   :id: INV-TEXT-002

   The :term:`buffer <Text Buffer>` must be processed in a left-to-right manner. Therefore a :term:`character`
   "in front of" the cursor is visually to the right of the cursor. A :term:`character` "behind" the cursor is visually
   to the left of the cursor.

4.1.3 Preconditions
-------------------

All operations in this section assume a valid :term:`cursor` position as defined in
:doc:`Cursor Specification <f-req_cursor_movement>`.

4.1.4 Stimulus/Response Sequences
---------------------------------

* **Stimulus:** External system provides a sequence of :term:`characters <character>` to
  :ref:`insert <insertion_specs>`.

  **Response:** The system inserts the :term:`characters <character>` at the current :term:`cursor` position and updates
  the :term:`cursor` position accordingly.

* **Stimulus:** External system triggers :ref:`delete <delete_specs>`.

  **Response:** The system removes the :term:`character` immediately right of the :term:`cursor`, if present.

* **Stimulus:** External system triggers :ref:`backspace <backspace_specs>`.

  **Response:** The system removes the :term:`character` immediately left of the :term:`cursor`, if present, and updates
  the :term:`cursor` position.

4.1.5 Functional Requirements
-----------------------------

.. freq:: Text Buffer
   :status: Open
   :id: FR-TEXT-001
   :tags: text

   The system must maintain an internal representation of text that is not externally mutable.

.. freq:: Text Buffer Mutation
   :status: Open
   :id: FR-TEXT-002
   :tags: text

   The :term:`text buffer <Text Buffer>` must only be modified through defined system operations.

.. _insertion_specs:

Insertion
~~~~~~~~~

.. freq:: Insert Operation Support
   :status: Open
   :id: FR-TEXT-011
   :tags: insert

   The system must support insertion of a sequence of
:term:`characters <character>`.

.. freq:: Insert at Cursor Position
   :status: Open
   :id: FR-TEXT-012
   :links: FR-CURSOR-001
   :tags: insert

   :term:`Characters <character>` must be inserted at the current :term:`cursor` position.

.. freq:: Inserting Nothing
   :status: Open
   :id: FR-TEXT-013
   :tags: insert

   Inserting zero :term:`characters <character>` must result in a no-op.

.. freq:: No Overwrite
   :status: Open
   :id: FR-TEXT-014
   :tags: insert

   Insertion must not overwrite existing :term:`characters <character>`.

.. freq:: Cursor Update After Insert
   :status: Open
   :id: FR-TEXT-015
   :tags: insert

   After insertion, the :term:`cursor` must be positioned immediately after the inserted :term:`characters <character>`.

.. freq:: Inserting Newline
   :status: Open
   :id: FR-TEXT-016
   :tags: insert

   Newline :term:`characters <character>` (``\n``) may be inserted and must introduce a :term:`logical line` boundary.

.. freq:: Insert Atomicity
   :status: Open
   :id: FR-TEXT-017
   :tags: insert

   Inserting a sequence of multiple :term:`characters <character>` must produce the same resulting
   :term:`buffer <Text Buffer>` state and :term:`cursor` position as inserting each :term:`character` of
   the sequence sequentially.

.. _delete_specs:

Delete
~~~~~~

.. freq:: Delete Operation Support
   :status: Open
   :id: FR-TEXT-021
   :links: FR-CURSOR-001
   :tags: delete

   The system must support a delete operation that targets the :term:`character` immediately right of the
   :term:`cursor`.

.. freq:: Single Character Deletion
   :status: Open
   :id: FR-TEXT-022
   :links: FR-CURSOR-001

   The delete operation must remove exactly one :term:`character` immediately right of the :term:`cursor`, if such a
   :term:`character` exists.

.. freq:: Cursor Position on Delete
   :status: Open
   :id: FR-TEXT-023

   The delete operation must not change the :term:`cursor` position.

.. freq:: Delete Boundary Behavior
   :status: Open
   :id: FR-TEXT-024

   If no :term:`character` exists to the right of the :term:`cursor`, the delete operation must result in a no-op.

.. freq:: Newline Character Deletion
   :status: Open
   :id: FR-TEXT-025

   Deleting a newline :term:`character` must remove the :term:`logical line` boundary and merge the adjacent
   :term:`logical lines`.

.. _backspace_specs:

Backspace
~~~~~~~~~

.. freq:: Backspace Operation Support
   :status: Open
   :id: FR-TEXT-031
   :links: FR-CURSOR-001

   The system must support a backspace operation that targets the :term:`character` immediately left of the
   :term:`cursor`.

.. freq:: Single Character Deletion
   :status: Open
   :id: FR-TEXT-032
   :links: FR-CURSOR-001

   The backspace operation must remove exactly one :term:`character` immediately left of the :term:`cursor`, if such a
   :term:`character` exists.

.. freq:: Cursor Position on Backspace
   :status: Open
   :id: FR-TEXT-033

   If a :term:`character` is removed, the :term:`cursor` must move one position to the left.

.. freq:: Backspace Boundary Behavior
   :status: Open
   :id: FR-TEXT-034

   If no :term:`character` exists to the left of the :term:`cursor`, the backspace operation must result in a no-op.

.. freq:: Newline Character Backspace
   :status: Open
   :id: FR-TEXT-035

   Removing a newline :term:`character` via backspace must remove the :term:`logical line` boundary and merge the
   adjacent :term:`logical lines <logical line>`.

Out of Scope
~~~~~~~~~~~~

.. nreq:: Text Selection
   :id: NR-Text-101
   :tags: out-of-scope

   The system must not support text selection.

.. nreq:: Clipboard Functions
   :id: NR-TEXT-102
   :tags: out-of-scope

   The system must not support copy, cut, or paste operations.

.. nreq:: Undo / Redo
   :id: NR-TEXT-103
   :tags: out-of-scope

   The system must not support undo or redo functionality.
