Layer Reads
~~~~~~~~~~~~~~~~~~~~~

.. TODO Finish

Context
.............

.. What situation or question forced this decision? What were the competing pressures?

The Facade needs to expose read interfaces to the host application in all four output
modes: Display, Wrapped, Logical, and Raw. (See: :ref:`req_software_interfaces`)

Decision
..............

.. What did you decide? State it plainly and unambiguously.

The Facade holds direct references to all three domain services: Logical, Visual, and Display.
It queries them directly for read interfaces.
The Visual Domain must also offer interfaces for the absolute index and logical coordinate. As the
Logical Domain does not hold a cursor and the Visual Domain does the translating.

Rationale
...............

.. Why did you make this choice? What properties does it give you?

If the Facade hadd access only to the Display Domain, which accesses the Visual Domain, which
in turn accesses the Logical Domain, The absolute index would neet to pass through all three layers
before the Facade could return it. The Display domain doesnt need that capability itself and would be
responsible for something it shouldn't be.

Alternatives Considered
..............................

.. What other options did you evaluate and why did you reject them?

Everything is passed through the layers. Facade only has access to the Display Domain. No concern about
desync, where a write command could bypass a layer that should be updated. (E.g. writing directly to the
buffer without updating the CursorState or Viewport)

Consequences
..................

.. What does this decision make easier? What does it constrain or make harder?
   Every architectural decision is a trade-off — if you cannot think of a consequence,
   you have not thought about it hard enough.

Pro: Clearer separation of concerns. Display Domain doesn't need to know about raw text or logical positions.

Con: Layers get bypassed. The Facade may only bypass layers for read operations. "Etiquette:" Don't bypass layers
for write operations.

