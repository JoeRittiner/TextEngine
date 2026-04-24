Text Manipulation
=================

Buffer
------

.. req:: The system must maintain an internal text buffer
   :id: FR-TEXT-001

.. req:: The text buffer must be mutable via system operations
   :id: FR-TEXT-002

.. req:: The text buffer must not be externally mutable
   :id: FR-TEXT-003

Insertion
---------

.. req:: The system must support string insertion
   :id: FR-INSERT-001

.. req:: Multiple characters may be inserted in a single operation
   :id: FR-INSERT-002

.. req:: Characters must be inserted at the cursor position
   :id: FR-INSERT-003
   :links: FR-CURSOR-001

.. req:: Inserting zero characters must be a valid no-op
   :id: FR-INSERT-004

.. req:: Insertion must not overwrite existing characters
   :id: FR-INSERT-005

.. req:: After insertion, the cursor must move after inserted characters
   :id: FR-INSERT-006

.. req:: Newline characters may be inserted
   :id: FR-INSERT-007


Delete
------

.. req:: The system must support a delete operation
   :id: FR-DELETE-001

.. req:: Delete must remove one character after the cursor if present
   :id: FR-DELETE-002
   :links: FR-CURSOR-001

.. req:: Delete must not remove more than one character per operation
   :id: FR-DELETE-003

.. req:: Delete must not change cursor position
   :id: FR-DELETE-004

.. req:: Deleting at end of buffer must be a no-op
   :id: FR-DELETE-005

.. req:: Deleting an empty buffer must be a no-op
   :id: FR-DELETE-006

.. req:: Newline characters may be deleted
   :id: FR-DELETE-007


Backspace
---------

.. req:: The system must support a backspace operation
   :id: FR-BACKSPACE-001

.. req:: Backspace must remove one character before the cursor if present
   :id: FR-BACKSPACE-002
   :links: FR-CURSOR-001

.. req:: Backspace must not remove more than one character per operation
   :id: FR-BACKSPACE-003

.. req:: Backspace at start of buffer must be a no-op
   :id: FR-BACKSPACE-004

.. req:: After backspace, the cursor must move left by one position
   :id: FR-BACKSPACE-005

.. req:: Backspace on an empty buffer must be a no-op
   :id: FR-BACKSPACE-006

.. req:: Newline characters may be removed by backspace
   :id: FR-BACKSPACE-007


Out of Scope
------------

.. req:: The system must not support selection
   :id: FR-SCOPE-001

.. req:: The system must not support copy, cut, or paste
   :id: FR-SCOPE-002

.. req:: The system must not support undo or redo
   :id: FR-SCOPE-003