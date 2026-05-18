Text Buffer
~~~~~~~~~~~

Responsibility
..............

The TextBuffer is the single authoritative store for the content of the document. It
accepts mutation operations (:need:`FR-TEXT-011`, :need:`FR-TEXT-021`) at a given absolute index and exposes the
resulting text as a raw string. It is the only component permitted to hold or modify the underlying text.
(:need:`FR-TEXT-001`, :need:`FR-TEXT-002`)

Owned State
...........

The TextBuffer owns one piece of state: the raw text string. This is the ground truth of
the document. All other representations of the text (logical lines, wrapped visual lines,
window-clipped output) are derived from this string by other components.

| The TextBuffer does **not** own a cursor position.
| The TextBuffer operates exclusively on absolute indices passed to it by its callers.

Behaviour
.........

Insertion is always a pure splice: characters are inserted at the
given absolute index without overwriting existing content. (:need:`FR-TEXT-014`)
Inserting a multi-character string produces the same buffer state as inserting each character
sequentially. (:need:`FR-TEXT-017`)

"Delete" targets the character immediately to the right of the given index. Deleting past
the end of the buffer is a no-op. (:need:`FR-TEXT-024`)

Dependencies
............

The TextBuffer depends on nothing. It has no imports from other engine components and uses
only the Python standard library.

Key Invariants
..............

* **Buffer always exists.** The buffer always represents at least one logical line. An
  empty buffer contains zero characters and yields one empty line when split.
  (:need:`INV-TEXT-001`)

* **Left-to-right processing.** The buffer is processed left-to-right. A character "in
  front of" the cursor is to its right; a character "behind" it is to its left.
  Characters are indexed accordingly. (:need:`INV-TEXT-002`)

* **Post-initialisation validity.** After initialisation, the buffer contains exactly the
  provided initial text (or is empty), and this state is indistinguishable from one
  reached through normal operation. (:need:`INV-INIT-002`)

* **Output stability.** For any given buffer state, repeated queries for raw text return identical results.
  Output is a pure function of the buffer contents.
  (:need:`INV-MODE-002`)
