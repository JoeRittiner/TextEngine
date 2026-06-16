========================
TextEditor Documentation
========================

**TextEditor** is a pure-state text and cursor tracking engine designed for headless environments.

Unlike traditional file-backed text editors, this tool focuses exclusively on maintaining a text buffer, tracking
cursor coordinates, and calculating visual line wrapping and viewport boundaries. It is intended to serve as a backend
tool for generating visual frames (e.g., via Pillow) rather than interacting directly with a user interface or
file system.

Project Goal
------------

The goal of this personal project is to learn and practice clean documentation, test-first development, and a
professional project workflow and structure. The focus is on the engineering process surrounding the code rather than
on feature completeness.

Philosophy
----------

This project is built using a **Specification-First**, **Documentation-Driven**, and **Test-Driven** methodology.
The documentation here is not an afterthought; it is the blueprint. Features are specified and documented here before
a single line of application code is written.

How to Read This Documentation
-------------------------------

The four sections below form a deliberate reading order:

* **Specifications & Design** defines *what* the system does and *how it is structured*. Start here.
* **Guides** provides step-by-step walkthroughs for the two primary audiences: host application
  integrators and engine contributors.
* **Testing** records *how* correctness is verified: strategy, property-based test design, coverage,
  and the intentional gaps.
* **API Reference** is auto-generated from source docstrings and serves as the definitive method-level
  lookup.

.. toctree::
   :maxdepth: 2
   :caption: 1. Specifications & Design
   :numbered: 3

   specs/requirements/index
   specs/architecture/index

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
* :doc:`glossary`