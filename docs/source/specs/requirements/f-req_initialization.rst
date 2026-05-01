4.1 System Initialization
=========================

4.1.1 Description and Priority
------------------------------
**Priority: High**

.. Provide a short description of the feature and indicate whether it is of High, Medium, or Low priority. You could
   also include specific priority component ratings, such as benefit, penalty, cost, and risk (each rated on a relative
   scale from a low of 1 to a high of 9).

4.1.2 State Invariants
----------------------

4.1.3 Preconditions
-------------------

4.1.4 Stimulus/Response Sequences
---------------------------------

.. List the sequences of user actions and system responses that stimulate the behavior defined for this feature.
   These will correspond to the dialog elements associated with use cases.

4.1.5 Functional Requirements
-----------------------------

.. Itemize the detailed functional requirements associated with this feature. These are the software capabilities that
   must be present in order for the user to carry out the services provided by the feature, or to execute the use case.
   Include how the product should respond to anticipated error conditions or invalid inputs. Requirements should be
   concise, complete, unambiguous, verifiable, and necessary. Use “TBD” as a placeholder to indicate when necessary
   information is not yet available.

Happy Path
~~~~~~~~~~

.. freq:: System Initialization
   :status: Open
   :id: FR-INIT-001
   :tags: initialization
   :links:

   At initialization, the :term:`system` must define:
      * Initial text
      * :term:`Display Width` (``display_width``)
      * :term:`Display Height` (``display_height``)
      * :term:`ScrollOff`
      * :term:`Cursor` position
      * :term:`Window Start`

.. freq:: Text Initialization
   :status: Open
   :id: FR-INIT-002
   :tags: initialization

   A text/ sequence of :term:`characters <character>` may be provided by the **user** at initialization.

   This must result in the same state as initializing the :term:`system` with no text, followed by inserting each
   :term:`characters <character>` individually.

   If no text is provided, the :term:`system` must define an empty text.

.. freq:: Display Width Initialization
   :status: Open
   :id: FR-INIT-003
   :tags: initialization

   A positive integer value for :term:`Display Width` must be **user defined** at initialization.

   If a negative value or zero is provided, the :term:`system` must throw an exception and prevent the user from initializing
   the :term:`system`.

.. freq:: Display Height Initialization
   :status: Open
   :id: FR-INIT-004
   :tags: initialization

   A positive integer value for :term:`Display Height` must be **user defined** at initialization.

   If a negative value or zero is provided, the :term:`system` must throw an exception and prevent the user from initializing
   the :term:`system`.

.. freq:: ScrollOff Initialization
   :status: Open
   :id: FR-INIT-005
   :tags: initialization

   A positive integer value for :term:`ScrollOff` must be **user defined** at initialization.

   If a negative value or zero is provided, the :term:`system` must throw an exception and prevent the user from initializing
   the :term:`system`.

.. freq:: Cursor Initialization
   :status: Open
   :id: FR-INIT-006
   :tags: initialization

   An :term:`Absolute Index` may be defined by the **user** at initialization.

   If no value is provided, the :term:`system` must define an absolute index of ``len(text_buffer)``. (i.e. to the right of
   the last :term:`character` in the :term:`Text Buffer`)

   If a value outside the range of the :term:`Text Buffer` is provided (negative value or value greater than
   ``len(text_buffer)``), the :term:`system` must throw an exception and prevent
   the user from initializing the :term:`system`.

.. freq:: Viewport Initialization
   :status: Open
   :id: FR-INIT-007
   :tags: initialization
   :links: FR-VIEW-001, FR-INIT-006

   A positive integer value for :term:`Window Start` must be **:term:`system` defined** at initialization.

   The :term:`Window Start` must be the smallest possible, while keeping the :term:`Cursor` (:need:`FR-INIT-006`)
   inside the :term:`Viewport` or :term:`Window` as per :need:`[[id]] FR-VIEW-001`.

Conflicts
~~~~~~~~~

.. freq:: Height
   :status: Open
   :id: FR-INIT-011
   :tags: initialization, conflict

   In the case that twice the :term:`ScrollOff` is greater than or equal to :term:`Display Height`, the :term:`system` must
   throw an exception and prevent the user from initializing the :term:`system`.

.. freq:: Null Values
   :status: Open
   :id: FR-INIT-012
   :tags: initialization, conflict

   In the case that a Null value is passed to user defined values, the :term:`system` must throw an exception and prevent the
   user from initializing the :term:`system`.

.. freq:: Type Conflicts
   :status: Open
   :id: FR-INIT-013
   :tags: initialization, conflict

   In the case that an invalid type is passed to any user defined values, the :term:`system` must throw an exception and
   prevent the user from initializing the :term:`system`.

   (E.g. a float in place of an integer)
