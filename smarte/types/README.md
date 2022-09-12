# Types

This directory contains custom types for simulation data.
These types are extensions to dictionaries for which:
* There are specified keys that are strings
* Values are elemental types: int, str, float, bool, or a list of the foregoing

The root class in ``ElementalDict``. It contains common methods (e.g., translation to and from a string representation).

* A ``SVDict`` is an ElementalDict for which each key has a single value.
* A ``MVDict`` is an ElementalDict for which each key has a list of values. A ``MVDict`` recognizes the keyword ``all``, and substitutes a default list as specified
by ``expansion_dct``. Also, these objects have an iterator that is restartable after
the last entry returned.
* An MVDictTable is a tabular representation of
an ``MVDict`` where each list has the same length.
* An MVDictHypercube is a 
``MVDict`` that has a
multi-dimensional representation of table in which the 
elements of the table are the cross product of attribute values.
