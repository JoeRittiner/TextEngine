4.2 Cursor & Movement
=====================

4.2.1 Description and Priority
------------------------------

.. Provide a short description of the feature and indicate whether it is of High, Medium, or Low priority. You could
   also include specific priority component ratings, such as benefit, penalty, cost, and risk (each rated on a relative
   scale from a low of 1 to a high of 9).

4.2.2 State Invariants
----------------------


4.2.3 Preconditions
-------------------

4.2.4 Stimulus/Response Sequences
---------------------------------

.. List the sequences of user actions and system responses that stimulate the behavior defined for this feature.
   These will correspond to the dialog elements associated with use cases.

4.2.5 Functional Requirements
-----------------------------

.. Itemize the detailed functional requirements associated with this feature. These are the software capabilities that
   must be present in order for the user to carry out the services provided by the feature, or to execute the use case.
   Include how the product should respond to anticipated error conditions or invalid inputs. Requirements should be
   concise, complete, unambiguous, verifiable, and necessary. Use “TBD” as a placeholder to indicate when necessary
   information is not yet available.

Invariants
~~~~~~~~~~

.. inv:: The cursor must be within [0, len(text)]
   :id: INV-CURSOR-001

Cursor Model
~~~~~~~~~~
.. moved from f-req_text_manipulation.rst

.. freq:: Text manipulation must occur at the logical cursor position
   :id: FR-CURSOR-001

.. freq:: No operation may bypass the logical cursor
   :id: FR-CURSOR-002

.. freq:: The logical cursor position lies between characters
   :id: FR-CURSOR-003

.. freq:: The cursor may be positioned before the first character
   :id: FR-CURSOR-004

.. freq:: The cursor may be positioned after the last character
   :id: FR-CURSOR-005

.. freq:: The cursor position must be within [0, len(text)]
   :id: FR-CURSOR-006
