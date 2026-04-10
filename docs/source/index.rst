========================
TextEditor Documentation
========================

**TextEditor** is a pure-state text and cursor tracking engine designed for headless environments.

Unlike traditional file-backed text editors, this tool focuses exclusively on maintaining a text buffer, tracking
cursor coordinates, and calculating visual line wrapping and viewport boundaries. It is intended to serve as a backend
tool for generating visual frames (e.g., via Pillow) rather than interacting directly with a user interface or
file system.

Philosophy
----------
This project is built using a **Specification-First**, **Documentation-Driven**, and **Test-Driven** methodology.
The documentation here is not an afterthought; it is the blueprint. Features are specified and documented here before
a single line of application code is written.

.. toctree::
   :maxdepth: 2
   :caption: 1. Specifications & Design

.. toctree::
   :maxdepth: 2
   :caption: 2. Usage & Tutorials (Doc-Driven)

.. toctree::
   :maxdepth: 2
   :caption: 3. API Reference

.. toctree::
   :maxdepth: 2
   :caption: 4. Testing & Development (TDD)

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`