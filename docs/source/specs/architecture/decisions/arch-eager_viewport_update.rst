Viewport Update
~~~~~~~~~~~~~~~

.. TODO Finish

.. Eager viewport update. arch-display_domain_service.rst has a thorough, well-reasoned section on this.
   The argument — that window_start is a function of movement history, not current position, so lazy derivation
   would lose intermediate scroll positions — is exactly the kind of non-obvious rationale that belongs in an ADR.
   This is the most complete "missing" decision in the set.

**Eager viewport update.** ``window_start`` must be updated after every operation that
changes the cursor's visual row. It cannot be derived lazily on read, because
``window_start`` is not a function of the cursor's current position alone. It is a
function of the cursor's movement *history* relative to the viewport. A lazy
implementation would lose the history of intermediate scroll positions and produce
incorrect output for any caller that moves the cursor without immediately reading the
display state. The service enforces this by treating the viewport update as part of every
cursor-changing operation, not as part of the read path.

Context
.......

.. What situation or question forced this decision? What were the competing pressures?

Decision
........

.. What did you decide? State it plainly and unambiguously.

Rationale
.........

.. Why did you make this choice? What properties does it give you?

Alternatives Considered
.......................

.. What other options did you evaluate and why did you reject them?

Consequences
............

.. What does this decision make easier? What does it constrain or make harder?
   Every architectural decision is a trade-off — if you cannot think of a consequence,
   you have not thought about it hard enough.
