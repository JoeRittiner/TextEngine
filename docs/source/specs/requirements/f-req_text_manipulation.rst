Text Manipulation
~~~~~~~~~~~~~~~~~

#. The component must maintain a mutable text buffer.

   * The text buffer must be protected from external modification.
        No external operation can mutate the buffer.

#. Text must be manipulated at the components logical cursor position.

   * No operation can bypass the cursor.
   * The logical cursor position lies between characters, not on a character.
   * The logical cursor position may be before the first character.
   * The logical cursor position may be after the last character.
   * The logical cursor position must always be between ``[0, len(text)]`` (inclusive).
     * ``0`` is the position before the first character.
     * ``len(text)`` is the position after the last character.
     * The logical cursor position may not be negative.

#. The Component must support character insertion.

   * Characters are inserted at the logical cursor position/ index.
   * Multiple characters may be inserted in a single operation.
   * Zero characters may be inserted in an operation.
        This is a valid operation that does nothing.
   * Inserting a character must insert it without replacing or removing existing characters.
        Cursor position must remain unchanged, if nothing is inserted.
   * After insertion, the logical cursor position must advance to immediately after the inserted character(s).
   * Newline (``\n``) characters may be inserted.

#. The component must support delete operation.

   * Deletion must remove one character immediately after the logical cursor position. (If present)
   * No more than one character may be deleted in a single operation.
   * Newline (``\n``) characters may be deleted.
   * After deletion, the cursor must remain at the same logical position.
   * Deleting at the end of the text buffer must not remove any characters.
   * Deleting an empty text buffer must not remove any characters.

#. The component must support backspace operation.

   * Backspace must remove one character immediately before the logical cursor position. (If present)
   * No more than one character may be removed in a single operation.
   * Newline (``\n``) characters may be removed.
   * Backspace at the start of the text buffer must not remove any characters.
   * After deletion, the cursor must move to the logical position of the removed character. (Move left by one character.)
   * Deleting an empty text buffer must not remove any characters.

#. The component must not support selection.
#. The component must not support Copy, Cut, and Paste operations.
#. The component must not support Undo/Redo operations.