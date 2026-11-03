# Laboratory 4B — Inheritance, Polymorphism and Composition

**Course:** Design of Software Systems  
**Python:** 3.10+  
**Scope:** Main tasks 1–10

## Project structure

- `task01.py` — Payment methods and polymorphic checkout
- `task02.py` — Abstract notifier and shared notification logic
- `task03.py` — Subscription pricing and VAT
- `task04.py` — Append-only audit log using composition
- `task05.py` — Employee roles and role history
- `task06.py` — Duck typing and `typing.Protocol`
- `task07.py` — Immutable Money value object
- `task08.py` — Search API and optional filters
- `task09.py` — Cooperative multiple inheritance and MRO
- `task10.py` — Payment method registry

## Install

```bash
python -m pip install pytest mypy pyflakes
```

## Run tests

Run all tests from this folder:

```bash
python -m pytest -v
```

Run one task:

```bash
python -m pytest task01.py -v
```

## Static checks

```bash
python -m mypy task06.py
python -m pyflakes task08.py
```

Task 6 includes the invalid `object()` example as a comment. Uncommenting it
demonstrates the static type error from mypy. Task 8's answer describes the
`F811` warning produced by the duplicate method in the original lab snippet.

## Notes

The main tasks are included. Optional extra tasks E1–E5 are not included,
because the handout says to attempt them only if time remains.
