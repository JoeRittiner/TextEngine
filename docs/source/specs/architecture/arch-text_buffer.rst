.. Answer the following questions:
   (1) What is this component's single responsibility?
   (2) What state does it own?
   (3) What are its boundaries — what does it depend on, and what depends on it?
   Do not describe implementation (specific methods, algorithms) here. That belongs in code comments
   or a separate detailed design document.

.. Link to specific Requirements?

Text Buffer
~~~~~~~~~~~

Responsibility
..............

.. One or two sentences. If you cannot state the responsibility in one sentence without using the word
   "and", consider whether this component is doing too much.

Owned State
...........

.. List the data this component is the authoritative owner of. If a component owns no state (i.e. it is
   a pure calculator), say so explicitly — that is a meaningful architectural fact.

Dependencies
............

.. List what this component depends on (other components, standard library modules, etc.).
   Also state what depends on *it*, so the coupling is visible in both directions.

Key Invariants
..............

.. List any state invariants this component is responsible for maintaining. These should be derivable
   from the requirements, but restated here in terms of the component's internal data rather than
   external behaviour.