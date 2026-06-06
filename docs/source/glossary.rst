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
      A system-wide constant defining the maximum number of :term:`characters <character>` permitted in a single
      :term:`Visual Line`.

      The value of :term:`Display Width` may be referred to as ``display_width``.

   Visual Line
      A segment of a :term:`Logical Line` as it appears after :doc:`wrapping <specs/requirements/f-req_text_wrapping>`.

         * If a :term:`Logical Line` length exceeds the :term:`Display Width`, it is split into multiple visual lines.

   Visual Coordinate
      A coordinate pair ``[v_row, v_col]`` where ``v_row`` is the zero-based :term:`Visual Line` index
      (calculated across the entire document) and v_col is the index relative to the start of that visual segment.

   Window
      A rectangular region of the screen that is used to display text limited by :term:`Display Height`.

      The window contains a :term:`Viewport` padded by :term:`ScrollOff` lines.

   Display Height
      A system-wide constant defining the maximum number of :term:`Visual Lines <Visual Line>` that can be rendered in
      the  :term:`window` simultaneously.

      The value of :term:`Display Height` may be referred to as ``display_height``.

   Window Start
      The index of the first :term:`Visual Line` currently rendered at the top of the :term:`window`.

      The value of :term:`Window Start` may be referred to as ``window_start``.

   Display Line
      A :term:`Visual Line` that is currently visible within the  :term:`window` boundaries
      (i.e., its index is within the range ``[window_start, window_start + display_height]``).

   ScrollOff
      The minimum number of :term:`Visual Lines <Visual Line>` that must remain visible between the :term:`Cursor`
      and the top/bottom edges of the  :term:`window`. This creates a "margin" that triggers scrolling before the cursor hits
      the absolute edge of the display.

      The value of :term:`ScrollOff` may be referred to as ``scrolloff``.

   Viewport
      The interior subset of the  :term:`window` where the :term:`Cursor` is allowed to move without triggering a scroll.

         * The top boundary is ``window_start + scrolloff``.
         * The bottom boundary is ``window_start + display_height - scrolloff``.

   Viewport Height
      The vertical capacity of the :term:`Viewport`, calculated as: ``display_height - (2 * scrolloff)``.

      The value of :term:`Viewport Height` may be referred to as ``viewport_height``.

   Window Coordinate
      A coordinate pair ``[x, y]`` representing the :term:`Cursor`'s position relative to the visible  :term:`window`.

         * ``x`` is equivalent to the :term:`Visual Coordinate` ``v_col``.
         * ``y`` is the vertical offset from the top of the  :term:`window` (``v_row - window_start``).

   Cursor
      A marker representing the current insertion point. It bijectively maps to an :term:`Absolute Index`,
      a :term:`Logical Coordinate`, a :term:`Visual Coordinate`, and a :term:`Window Coordinate`.

   System
   TextEditor
      The System. Single threaded.

   Domain
      A layer of the :term:`engine <textEditor>` that implements a distinct responsibility.

   Layer
      A layer of the :term:`engine <textEditor>` that implements a distinct responsibility.

   Container
      C4 Container: A runtime boundary around some code that is being executed or some data that is being stored.

   Component
      C4 Component: A grouping of related functionality encapsulated behind a well-defined interface.
