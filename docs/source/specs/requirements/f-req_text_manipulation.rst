4.1 Text Buffer & Manipulation
==============================

4.1.1 Description and Priority
------------------------------
**Priority: High**

The Text Buffer is the conceptual source of truth for document content. It is modeled as a sequence of [...] characters.

**State Model: The Buffer**
The buffer represents text as a continuous sequence where positions exist between characters.

**State Invariants**

.. inv:: Empty Buffer Definition
   :id: INV-TEXT-001

   The buffer must always contain at least one logical line; an empty editor contains exactly one empty line.

4.1.2 Stimulus/Response Sequences
---------------------------------

* **Stimulus:** External system provides a string to :ref:`insert <insertion_specs>`.
    **Response:** System updates the buffer at the current cursor position and shifts the cursor.
* **Stimulus:** External system triggers :ref:`delete <delete_specs>`.
    **Response:** System removes the character right of the cursor. The cursor position does not change.
* **Stimulus:** External system triggers :ref:`backspace <backspace_specs>`.
    **Response:** System removes the character preceding the cursor and updates the cursor position.

4.1.3 Functional Requirements
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

   The text buffer must be mutable via system operations.

.. _insertion_specs:

Insertion
~~~~~~~~~

.. freq:: Insert Operation Support
   :status: Open
   :id: FR-INSERT-001
   :tags: insert

   The system must support string insertion.

.. freq:: Insert at Cursor Position
   :id: FR-INSERT-002
   :status: Open
   :links: FR-CURSOR-001
   :tags: insert

   Characters must be inserted at the cursor position.

.. freq:: Inserting Nothing
   :status: Open
   :id: FR-INSERT-003
   :tags: insert

   Inserting zero characters must be a valid no-op.

.. freq:: No Overwrite
   :status: Open
   :id: FR-INSERT-004
   :tags: insert

   Insertion must not overwrite existing characters.

.. freq:: Cursor Update After Insert
   :status: Open
   :id: FR-INSERT-005
   :tags: insert

   After insertion, the cursor must move after inserted characters.

.. freq:: Inserting Newline
   :status: Open
   :id: FR-INSERT-006
   :tags: insert

   Newline characters may be inserted.

.. _delete_specs:

Delete
~~~~~~

.. freq:: Delete Operation Support
   :status: Open
   :id: FR-DELETE-001
   :links: FR-CURSOR-001
   :tags: delete

   The system must support a discrete delete operation that targets the character right of the cursor.

.. freq:: Single Character Deletion
   :status: Open
   :id: FR-DELETE-002
   :links: FR-CURSOR-001

   The delete operation must remove exactly one character immediately right of the cursor position,
   if such a character is present.

.. freq:: Cursor Position on Delete
   :status: Open
   :id: FR-DELETE-003
   
   The delete operation must not change the cursor position.

.. freq:: Delete Boundary Behavior
   :status: Open
   :id: FR-DELETE-004

   If the cursor is positioned at the absolute end of the text buffer, the delete operation must result in a no-op.

.. freq:: Empty Buffer Delete
   :status: Open
   :id: FR-DELETE-005

   If the buffer is empty, (i.e. only one empty line) the delete operation must result in a no-op.

.. freq:: Newline Character Deletion
   :status: Open
   :id: FR-DELETE-006

   Newline characters can be removed by delete.

.. _backspace_specs:

Backspace
~~~~~~~~~

.. freq:: Backspace Operation Support
   :status: Open
   :id: FR-BACKSPACE-001
   :links: FR-CURSOR-001

   The system must support a discrete backspace operation that targets the character left of the cursor.

.. freq:: Single Character Deletion
   :status: Open
   :id: FR-BACKSPACE-002
   :links: FR-CURSOR-001

   The backspace operation must remove exactly one character immediately left of the cursor position,
   if such a character is present.

.. freq:: Cursor Position on backspace
   :status: Open
   :id: FR-BACKSPACE-003
   
   The backspace operation must move the cursor position one character back, if a character is removed by the backspace
   operation.

.. freq:: backspace Boundary Behavior
   :status: Open
   :id: FR-BACKSPACE-004

   If the cursor is positioned at the absolute start of the text buffer, the backspace operation must result in a no-op.

.. freq:: Empty Buffer Backspace
   :status: Open
   :id: FR-BACKSPACE-005

   If the buffer is empty (i.e. only one empty line), the backspace operation must result in a no-op.

.. freq:: Newline Character Backspace
   :status: Open
   :id: FR-BACKSPACE-006

   Newline characters can be removed by backspace.


Out of Scope
~~~~~~~~~~~~

.. nfreq:: Text Selection
   :id: FR-SCOPE-001

   The system must not support text selection.

.. nfreq:: Clipboard Functions
   :id: FR-SCOPE-002

   The system must not support copy, cut, or paste.

.. nfreq:: Undo/ Redo
   :id: FR-SCOPE-003

    The system must not support undo or redo.
