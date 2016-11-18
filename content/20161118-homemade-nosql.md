title:        Homemade NoSQL. Part 1
date:         Nov 18, 2016
properties:   homemade
              codereading
              db

*NoSQL* moniker underwent a great surge of popularity in recent years due to the
spread of some key-value store (KVDB) and document store databases, although
NoSQL could be extended as *not only SQL* and meet some demand in other areas
like big data.

> Buzzwords, buzzwords everywhere.

Some weeks ago, I was browsing the `Lib` directory in `py35` source to do some
code reading, where I got a module that provides a
[geohashing algorithm](https://xkcd.com/426/) and a wrapper based on several
successors of the Unix's simple database engine,
[dbm](https://en.wikipedia.org/wiki/Dbm). After playing the geohash for a while,
I decided to implement the fallback `dbm` module initially written in Python for
handling the unavailability of `ndbm` and `gdbm`, by using `Node.js v6.0.0`. The
fallback module is simply called `dbm.dumb`.

By the way, `dbm` is so-called a pre-relational database that uses a both
in-memory and on-disk key-value store, based on extensible hashing. What a NoSQL
database in the late 1970s...

The implementation of `dbm.dumb` is really clear. It inherits the
`MutableMapping` abstract base class and additionally implements some abstract
methods like `__setitem__` and `__delitem__` for mutable use. It stores three
kinds of files, whose extensions are `.dat`, `.dir` and `.bak`, where the `.dat`
is `latin1`-encoded that stores the values, which are aligned by a block size
constant to set the boundaries for compactness (maybe overriding-prone), `.dir`,
AKA directory file, contains the keys and a pair of their positions
(file offset) and value sizes, and `.bak` is the backup of the directory file.
In memory, the class inheriting the `py35`'s mutable mappings, which acts
seemingly like a `dict`, easily copes with the Python-style indexing (but it
needs to be `bytes` object, e.g. `foo[b'bar'] = b'baz'`).

(WIP)
