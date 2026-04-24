Glossary
========

.. glossary::

   Character
      A character is defined as a Unicode grapheme cluster (i.e. the smallest user-perceived unit of text).


   Text Buffer
      A Text Buffer is a continuous sequence of :term:`characters <character>`.

      .. note:: A Text Buffer is a conceptual construct and does not necessarily represent any internal data structure
                or system components.


   Cursor
      The cursor is a marker that represents the current position of the user's input within the :term:`Text Buffer`.

      .. note:: The cursor is a conceptual construct and does not necessarily represent any internal data structure
                or system components.


   Logical Line
      Logical lines are derived by splitting the :term:`Text Buffer` at newline characters (``\n``).
      A newline character defines a logical line boundary.

      Logical lines are independent of screen width.

      Examples:
         * ``""`` represents one empty logical line.
         * ``"\n"`` represents two empty logical lines.
         * ``"This is a very long line that may wrap."`` represents one logical line.
         * ``"\nThis is a line.\nThis is another line.\n"`` represents _four_ logical lines.


   Visual Line
      A subset of a :term:`logical line` that fits within the display width.

      Example with ``display_width = 15``::


         ""
         "This is a line."
         "This is another"
         " line."
         ""


   Display Height
      The number of :term:`visual lines <visual line>` that can be shown at once.


   Display Line
      A :term:`visual line` that is currently visible in the window.


   Scrolloff
      The minimum number of :term:`visual lines <visual line>` that must remain visible above and below the cursor,
      unless near the start or end of the file.


   Viewport
      The range of :term:`visual lines <visual line>` where the cursor is allowed to move without scrolling.

      If the cursor moves inside the :term:`viewport`, no scrolling occurs.
      If the cursor leaves the :term:`viewport`, the window scrolls to bring it back.


   Viewport Height
      Calculated as: ``display_height - 2 * scrolloff``.

      Example with ``display_height = 20`` and ``scrolloff = 3``::

         [3 lines top margin]
         [14 line viewport]
         [3 lines bottom margin]