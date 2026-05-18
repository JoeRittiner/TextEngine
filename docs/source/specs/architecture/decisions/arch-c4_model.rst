..The engine is within the *System*; its three domains are *Containers*; the modules within each domain are
  *Components*, which are made up of *Classes*, *Functions* and *Code*.

.. Though the domains are not separately deployable processes; they are bounded objects within a single Python module.
   See :doc:`decisions/arch-c4_model`.

C4 Model
~~~~~~~~

.. Aim for one record per non-obvious choice.
   Examples of decisions worth recording for this project:
   - Why a Facade pattern rather than a flat module of functions.
   - Whether Cursor is a class with its own state or a value computed from TextBuffer's state.
   - Whether WrapEngine is stateful (caches results) or stateless (recalculates on every call).
   - Whether components may call each other directly or only through the Facade.

Context
.......

.. What situation or question forced this decision? What were the competing pressures?

A way to describe (and define) the architecture of the Text Editor.

Decision
........

.. What did you decide? State it plainly and unambiguously.

Base the Architecture of the Text Editor on the C4 model.

Rationale
.........

.. Why did you make this choice? What properties does it give you?

It seemed to fit naturally with the layered concept. Seeing the three domains as containers.

Alternatives Considered
.......................

.. What other options did you evaluate and why did you reject them?

Consequences
............

.. What does this decision make easier? What does it constrain or make harder?
   Every architectural decision is a trade-off — if you cannot think of a consequence,
   you have not thought about it hard enough.