Visual-Logical Adapter
~~~~~~~~~~~~~~~~~~~~~~

Responsibility
..............

The ``VisualLogicalAdapter`` is the sole point of contact between the Visual Domain and
the Logical Domain. It translates in both directions: outbound, it maps visual coordinates
to the absolute indices required by the Logical Domain; inbound, it maps the Logical
Domain's text content into visual lines. All reads from and all mutations to the Logical
Domain pass through this component.

Owned State
...........

The ``VisualLogicalAdapter`` owns two pieces of state:

* **Display width.** A positive integer fixed at initialisation that defines the maximum
  number of characters per visual line. A null value or a value of an incorrect type
  (including a float) raises an exception and halts initialisation.
  (:need:`FR-INIT-001`, :need:`FR-INIT-003`, :need:`FR-INIT-012`, :need:`FR-INIT-013`,
  :need:`INV-WRAP-001`, :need:`INV-WRAP-002`)
* **Wrapping map.** The structural relationship between logical lines and the visual lines
  they produce: how many visual lines each logical line yields and where the breaks fall.
  The map is the adapter's internal model of the Logical Domain's current state, expressed
  in visual terms. It is kept consistent with the buffer after every mutation.
  (:need:`FR-MODE-022`)

The ``VisualLogicalAdapter`` does not own cursor state and does not own the text itself.

Behaviour
.........

**Inbound: Logical to Visual (reads).** The adapter exposes the buffer's content as a
sequence of visual lines by applying ``display_width`` to the logical lines retrieved from
the ``LogicalDomainService``. (:need:`FR-MODE-021`) The output includes structural
metadata indicating which visual lines belong to which logical line, so callers can
correlate visual and logical positions. (:need:`FR-MODE-022`) The wrapping rules are
defined in :need:`FR-WRAP-001` through :need:`FR-WRAP-005`. Reads are non-destructive:
querying visual output never modifies the buffer, the wrapping map, or any other state.
(:need:`INV-MODE-001`)

The adapter also exposes the current cursor position in visual coordinates, by retrieving
it from the ``LogicalDomainService`` and translating it to visual coordinates using the
wrapping map and translation rules. (:need:`FR-CURSOR-004`, :need:`FR-CURSOR-010`)

**Outbound: Visual to Logical (mutations).** The adapter accepts mutation operations
(``insert``, ``delete``, ``backspace``) expressed in visual coordinates. It translates the
given visual coordinate to the absolute index required by the ``LogicalDomainService``,
issues the mutation, and immediately updates the wrapping map to reflect the new buffer
state. The map is guaranteed consistent before any subsequent read or coordinate translation
is served. (:need:`INV-WRAP-003`) Invalid visual coordinates are rejected with an exception;
the adapter does not clamp or correct positions it receives.

The adapter also accepts direct cursor setting, and horizontal movement commands. These
are passed to the ``LogicalDomainService``. An invalid position is rejected with an
exception; the adapter does not clamp or correct positions it receives. Movement commands
are non-destructive: they do not modify the buffer, or any other state and don't warrant updating
the map. (:need:`FR-CURSOR-021`)

**Coordinate translation.** The adapter translates on demand between visual coordinates
``(v_row, v_col)`` and absolute indices in both directions. This is the only component in
the Visual Domain that crosses coordinate spaces; ``MovementResolver`` operates exclusively in
visual coordinates and relies on the adapter for any translation it requires.
(:need:`FR-CURSOR-004`)

Dependencies
............

**Depends on:** The ``LogicalDomainService``, as the target of all read and mutation
operations on the underlying text. This is the only cross-domain dependency in the Visual
Domain.

**Depended on by:**

* The ``VisualDomainService``, which owns the adapter instance and routes all mutation
  operations and visual-line reads through it.

Key Invariants
..............

* **Sole domain boundary.** The ``VisualLogicalAdapter`` is the only component in the
  Visual Domain permitted to call the ``LogicalDomainService``. Any direct call from
  ``VisualDomainService`` or ``MovementResolver`` to the Logical Domain
  bypasses the adapter and breaks the boundary.

* **Wrapping map consistency.** The wrapping map always reflects the current buffer state.
  After any mutation, the map is updated before any read, translation, or validity check
  is served. A stale map would cause coordinate translations to silently return wrong
  positions. (:need:`INV-WRAP-003`)

* **Immutable display width.** ``display_width`` is fixed at initialisation and never
  changes for the lifetime of the instance. A change to display width requires
  re-initialisation of the adapter. (:need:`INV-WRAP-001`, :need:`INV-WRAP-002`,
  :need:`INV-INIT-001`)

* **Full content coverage.** Every character in the buffer is assigned to exactly one
  visual line. No character is omitted or duplicated by the wrapping map.
  (:need:`FR-WRAP-002`)

* **Output stability.** For any given buffer state and display width, the visual line
  sequence and all coordinate translations are deterministic. Repeated reads with no
  intervening mutation return identical results. (:need:`INV-MODE-002`)
