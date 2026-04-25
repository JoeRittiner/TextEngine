Glossary
========

.. glossary::

   Character
      The smallest user-perceived unit of text, defined as a single Unicode grapheme cluster.


   Text Buffer
      A continuous, ordered sequence of :term:`characters <character>`.
      It serves as the primary data source for all system operations.

      .. note:: The buffer is a conceptual construct; requirements do not dictate its internal implementation
         (e.g., Gap Buffer, Rope, or String).

   Absolute Index
      A zero-based integer representing a specific position within the :term:`Text Buffer`,
      ranging from 0 to len(text). It is the "source of truth" for all text manipulation.

   Logical Line
      A segment of text within the :term:`Text Buffer` delimited by newline characters (``\n``).

         * Logical lines are independent of :term:`Display Width`.
         * An empty buffer contains exactly one empty logical line.
         * A buffer containing only ``\n`` contains two empty logical lines.

   Logical Coordinate
      A coordinate pair ``[row, col]`` where ``row`` is the zero-based :term:`Logical Line` index and ``col`` is the
      index relative to the start of that line.

   Display Width
      A system-wide constant defining the maximum number of :term:`characters <character>` permitted in a single :term:`Visual Line`.

   Visual Line
      A segment of a :term:`Logical Line` as it appears after :doc:`wrapping <f-req_text_wrapping>`.

         * If a :term:`Logical Line` length exceeds the :term:`Display Width`, it is split into multiple visual lines.

   Visual Coordinate
      A coordinate pair ``[v_row, v_col]`` where ``v_row`` is the zero-based :term:`Visual Line` index
      (calculated across the entire document) and v_col is the index relative to the start of that visual segment.

   Display Height
      A system-wide constant defining the maximum number of :term:`Visual Lines <Visual Line>` that can be rendered in
      the window simultaneously.

   Window Start
      The index of the first :term:`Visual Line` currently rendered at the top of the window.

   Display Line
      A :term:`Visual Line` that is currently visible within the window boundaries
      (i.e., its index is within the range ``[window_start, window_start + display_height]``).

   ScrollOff
      The minimum number of :term:`Visual Lines <Visual Line>` that must remain visible between the :term:`Cursor`
      and the top/bottom edges of the window. This creates a "margin" that triggers scrolling before the cursor hits
      the absolute edge of the display.

   Viewport
      The interior subset of the window where the :term:`Cursor` is allowed to move without triggering a scroll.

         * The top boundary is ``window_start + scrolloff``.
         * The bottom boundary is ``window_start + display_height - scrolloff``.

   Viewport Height
      The vertical capacity of the :term:`Viewport`, calculated as: ``display_height - (2 * scrolloff)``.

   Window Coordinate
      A coordinate pair ``[x, y]`` representing the :term:`Cursor`'s position relative to the visible window.

         * ``x`` is equivalent to the :term:`Visual Coordinate` ``v_col``.
         * ``y`` is the vertical offset from the top of the window (``v_row - window_start``).

   Cursor
      A marker representing the current insertion point. It bijectively maps to an :term:`Absolute Index`,
      a :term:`Logical Coordinate`, a :term:`Visual Coordinate`, and a :term:`Window Coordinate`.

   TextEditor
      The System.
