Cursor State and Movement
~~~~~~~~~~~~~~~~~~~~~~~~~

The Current Model
.................

``CursorState`` represents the cursor as a visual coordinate ``(row, col)``. On every call
to ``get_position()``, it checks the stored coordinate against the current wrapping map
via the ``VisualLogicalAdapter`` and clamps it to the nearest valid position if needed.
This is *lazy validation*: the stored value may be transiently invalid, and the
invalidity is corrected the moment something asks for the position.

``MovementResolver`` is a pure stateless calculator that translates a ``(position,
direction, visual_lines)`` triple into a new valid visual coordinate. It is used not
only for movement commands but also by ``insert``, ``backspace``, and ``delete`` to
update the cursor position after each mutation.


Identified Tensions
...................

**Visual coordinate is a derived value.** A visual coordinate is a function of two
things: the absolute position of the cursor in the text, and the current wrapping map.
When either changes, the stored coordinate may no longer correspond to a valid position
in the updated map. Storing a derived value as ground truth means any change to its
inputs can silently invalidate it.

Lazy validation is the mechanism that recovers from this: defer the validity check until
the value is needed, so the staleness never causes harm. It works. But it means
``CursorState`` carries a permanent dependency on ``VisualLogicalAdapter`` — a component
whose sole purpose is to hold a position now also needs to consult the wrapping
infrastructure on every read.

**The delete-exception case.** A ``delete`` operation does not change the absolut index
position of the cursor. However,:need:`FR-CURSOR-010` defines that when the cursor sits at
the end of a logical line whose final visual line is exactly ``display_width`` characters
long, it must be represented as ``[v_row, display_width]`` rather than normalising to
``[v_row + 1, 0]``. The next visual row does not exist.

Now consider a ``delete`` at this position. The cursor is at ``[v_row, display_width]``,
which is a ``\n`` character. ``delete`` removes it, joining the two logical lines. The
exception no longer holds; the cursor must normalise to ``[v_row + 1, 0]``. The
absolute index of the cursor has not changed. The wrapping map has. The stored visual
coordinate is now wrong, and ``delete`` does not update the cursor.

Lazy validation catches this on the next ``get_position()`` call, and the architecture
is correct. But the fact that the system *anticipates* this possibility — and patches
over it on every read — is the smell. The need for a patch is evidence of a deeper
misalignment in the model.

**``MovementResolver`` is coupled to mutations.** ``insert``, ``backspace``, and
``delete`` currently use ``MovementResolver`` to determine the updated cursor position.
This is architecturally awkward: ``insert`` advances the cursor to the right by
``len(text)`` positions; ``backspace`` decrements it by one; ``delete`` does not move
it at all. None of these require movement resolution logic. They are arithmetic. The
dependency on ``MovementResolver`` for mutations exists because the cursor is stored in
visual space, where arithmetic is not straightforward. This is a symptom, not a design.


The Root
........

The root cause is that visual coordinate is a derived value being stored as though it
were the source of truth. The stable primitive from which a visual coordinate is derived
is the **absolute index**: the cursor's position as a 0-based offset into the raw text
string. Unlike a visual coordinate, an absolute index does not depend on the wrapping
map. Its validity invariant is trivially checkable: ``0 <= k <= len(text)``. It requires
no external reference.

The remaining sections propose two paths, both grounded in this insight.


Path 1 — Absolute Index in the Visual Domain
.............................................

The smallest change that resolves all identified tensions: ``CursorState`` stores ``k:
int`` instead of ``(row, col)``.

**``CursorState``** becomes a minimal container. It stores a single integer, validates
the range ``0 <= k <= len(text)`` on ``set()``, and returns it on ``get()``. It has no
dependency on ``VisualLogicalAdapter`` and performs no clamping.

**``VisualDomainService``** absorbs the translation logic that previously lived
implicitly in the cursor. Before a movement operation, it translates ``k`` to a visual
coordinate via the adapter. After the resolver returns a new visual coordinate, it
translates that back to an absolute index and stores it. For mutations, the cursor
update is direct arithmetic: ``insert`` sets ``k += len(text)``; ``backspace`` sets
``k -= 1``; ``delete`` leaves ``k`` unchanged.

**``MovementResolver``** is unchanged and decoupled from mutations. It remains a pure
stateless function of ``(visual_pos, direction, visual_lines) → visual_pos``. It no
longer needs to be consulted for ``insert``, ``backspace``, or ``delete``.

**``VisualLogicalAdapter``** absorbs ``FR-CURSOR-010``. The normalisation rule — which
previously lived in ``CursorState``'s validation logic — moves into ``to_visual(k)``,
the single point at which visual coordinates are produced from absolute indices. This is
the correct location: the rule describes how to represent a position as a visual
coordinate, which is precisely what ``to_visual()`` does. The ``validate_visual_position()``
method is removed from the public API; its logic is now internal to translation.

The delete-exception case becomes a non-event. After ``delete`` removes the ``\n``, the
wrapping map updates, and ``k`` is unchanged. The next call to ``adapter.to_visual(k)``
consults the new map and returns the correct normalised coordinate. No special handling,
no deferred clamping. The problem disappears because ``k`` does not depend on the
wrapping map.

The one real cost is movement: two adapter translations per operation (``k`` to visual
before resolving, visual to ``k`` after). Both are lookups into the wrapping map and
localized to the ``VisualDomainService``. For a project at this scale, this is not really
a concern.

Path 1 is a conservative, self-contained refactor. It solves all identified problems and
does not preclude Path 2.


Path 2 — The Cursor-Centric Logical Domain
..........................................

Path 1 places the absolute index in the Visual Domain because that is where the cursor
currently lives. But the absolute index is a position in the raw text string — a Logical
Domain concept. Taking the insight to its conclusion: the cursor belongs in the Logical
Domain.

This is not a refactoring of where ``CursorState`` sits. It is a reconceptualisation of
what the Logical Domain *is*.

Currently the Logical Domain is a text manipulation layer. Its API takes explicit
positions: ``insert(text, abs_index)``, ``delete(abs_index)``, ``backspace(abs_index)``.
The position is a parameter; the domain is agnostic about which position the caller
intends. This is the API of a library, not an editor.

A text editor is cursor-centric. The cursor is not a parameter to an operation; it is a
persistent, shared context that defines where every operation acts. ``insert(text)``
means *insert at the cursor*. ``backspace()`` means *remove the character before the
cursor*. ``delete()`` means *remove the character at the cursor*. These are the
semantically correct signatures for the core layer of a text editor, and they become
possible the moment the cursor lives in the Logical Domain.

**``CursorState``** moves to the Logical Domain, owned by ``LogicalDomainService``. It
stores ``k: int``, validates range, and exposes ``get_cursor() → int`` and
``set_cursor(k: int)``.

**``LogicalDomainService``** becomes cursor-centric. ``insert(text)`` inserts at the
cursor and advances it: ``k += len(text)``. ``backspace()`` removes the character before
the cursor and decrements it: ``k -= 1``. ``delete()`` removes the character at the
cursor; ``k`` is unchanged. The ``abs_index`` parameter disappears from all three. The
domain now models the natural semantics of editing.

**``VisualLogicalAdapter``** mediates cursor state across the domain boundary, as it
already mediates text mutations. It exposes ``get_cursor_abs() → int``, which reads from
``LogicalDomainService``, and ``set_cursor(k: int)``, which writes to it. Mutation calls
lose their index parameter: ``adapter.insert(text)`` delegates to
``logical.insert(text)``; the cursor update is internal to the Logical Domain.

**``VisualDomainService``** handles movement as in Path 1 — read cursor via adapter,
translate to visual, resolve, translate back, write cursor via adapter — but performs
no cursor arithmetic for mutations. It delegates to the adapter and steps aside.

**There is no cursor state in the Visual Domain.** The Visual Domain borrows the cursor
from the Logical Domain when it needs it. ``VisualDomainService`` and
``DisplayDomainService`` derive their coordinate representations on demand.

The ``set_cursor(k)`` call from the Visual Domain to the Logical Domain — issued after a
movement operation — is a Visual → Logical write, consistent with the existing
unidirectional dependency. The Adapter already mediates all cross-domain calls from
Visual to Logical; this is one more, distinguished only by the fact that it updates
cursor state rather than text. It should be documented as a deliberate design choice
rather than left implicit.

The Facade also becomes cleaner. ``editor.insert(text)`` is the natural call; the cursor
position is implicit. The ``arch-layer_reads`` principle applies unchanged: cursor reads
flow directly to the owning layer (``LogicalDomainService``), while write operations
propagate through the full domain hierarchy.

One question is worth stating plainly: does adding cursor ownership to the Logical
Domain violate the principle that it is a "general text manipulation layer"? It does not,
because a text editor's core layer is not a general text manipulation library. The cursor
is a first-class concept at every level of the system; the argument for keeping the
Logical Domain cursor-agnostic was never architectural — it was habitual. Correcting
the scope of the Logical Domain is not feature creep; it is naming the domain honestly.


Assessment
..........

Both paths eliminate lazy validation, remove the ``VisualLogicalAdapter`` dependency
from cursor state, decouple ``MovementResolver`` from mutations, and resolve the
delete-exception case cleanly.

Path 1 is the conservative option. The change surface is small, the risk is low, and the
existing domain boundaries are preserved. It is a sound refactor that stands on its own.

Path 2 is the more coherent final state. The cursor belongs in the Logical Domain because
the absolute index is a Logical Domain concept, and ``insert(text)`` is the correct API
for a cursor-centric editor. The architecture at every level becomes simpler to reason
about: the cursor has one home, mutations are semantically correct, and the Visual Domain
borrows what it needs without owning it. Path 2 is more ambitious because it changes the
Logical Domain's contract, but the result is an architecture whose structure matches its
intent.

The recommended direction is Path 2.
