Wrap Engine
~~~~~~~~~~~

Responsibility
..............

The WrapEngine is the authoritative translator between the Logical and Visual coordinate
spaces. It maps logical lines to visual lines by applying the configured display width,
and translates in both directions between absolute indices, logical coordinates, and visual
coordinates ``(visual_line, visual_col)``.

Owned State
...........

The WrapEngine owns two pieces of state:

* **Display width.** A positive integer fixed at initialisation that defines the maximum
  number of characters per visual line. A null value or a value of an incorrect type
  (including a float) must raise an exception and halt initialisation.
  (:need:`FR-INIT-001`, :need:`FR-INIT-003`, :need:`FR-INIT-012`, :need:`FR-INIT-013`,
  :need:`INV-WRAP-001`, :need:`INV-WRAP-002`)
* **Wrapping map.** The structural relationship between logical lines and the visual lines
  they produce. This mapping is included in wrapped output so that callers can determine
  which logical line each visual line belongs to. This is the WrapEngine's derived view of
  the buffer, kept consistent with the TextBuffer's current state. Whether this is held as
  an explicit cache or recomputed on demand is an implementation detail.
  (:need:`FR-MODE-022`)

The WrapEngine does not own cursor state and does not own the text itself.

Behaviour
.........

**Line wrapping.** The WrapEngine exposes the entire buffer as a sequence of visual lines,
calculated from the current ``display_width``. (:need:`FR-MODE-021`) The output includes
structural metadata indicating which visual lines belong to which logical line.
(:need:`FR-MODE-022`) Logical lines are wrapped into visual lines of length
``display_width``. The last visual line of each logical line may be shorter but is never
empty. An empty logical line produces exactly one empty visual line. Wrapping is
non-destructive: joining all visual lines for a logical line reconstructs that logical line
exactly. Characters from different logical lines are never combined into a single visual
line. (:need:`FR-WRAP-001`, :need:`FR-WRAP-002`, :need:`FR-WRAP-003`, :need:`FR-WRAP-004`,
:need:`FR-WRAP-005`)

**Coordinate translation.** The WrapEngine translates in both directions between absolute
indices, logical coordinates ``(logical_line, logical_col)``, and visual coordinates
``(visual_line, visual_col)``. The Visual Domain Service and the Cursor State component
rely on this translation; they do not perform it themselves.

**Mutation pass-through.** All text mutations from the Visual Domain are routed through
the WrapEngine. A caller passes a position in visual coordinates; the WrapEngine
translates it to the absolute index or logical coordinate required by the Logical Domain
Service, issues the mutation, and invalidates or updates the wrapping map accordingly.

Dependencies
............

**Depends on:** The Logical Domain Service, for logical line content used to build and
update the wrapping map, and as the target of delegated mutation operations.

**Depended on by:**

* The Cursor State component, which queries the WrapEngine to validate and clamp visual
  coordinates against the current wrapping map.
* The Visual Domain Service, which owns the WrapEngine instance and routes all external
  read and write calls through it.

Key Invariants
..............

* **Immutable display width.** ``display_width`` is set at initialisation and never
  changes for the lifetime of the instance. A resize requires re-initialisation.
  (:need:`INV-WRAP-001`, :need:`INV-WRAP-002`, :need:`INV-INIT-001`)

* **Wrapping map consistency.** The wrapping map must always reflect the current state of
  the TextBuffer. After any mutation, the map is updated before any coordinate translation
  or wrapped output is served. A stale map would cause coordinate translations to return
  positions that do not correspond to the correct characters. (:need:`INV-WRAP-003`)

* **Non-destructive wrapping.** Wrapping never modifies the text buffer. Querying wrapped
  output is a pure read. (:need:`INV-MODE-001`, :need:`FR-WRAP-001`)

* **Output stability.** For any given buffer state and display width, the visual line
  sequence and all coordinate translations are deterministic. Repeated queries with no
  intervening mutation return identical results. (:need:`INV-MODE-002`)

* **Full content coverage.** Every character in the buffer is assigned to exactly one
  visual line. No character is omitted or duplicated by the wrapping map.
  (:need:`FR-WRAP-002`)
