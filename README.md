Horrible RAM: My Personal Blog
==============================

This blog site generator is based on
[postocol](https://github.com/anqurvanillapy/postocol), which is an abstract
class for fast constructing a homemade SSG.

**Attention!** This generator is only for **User** or **Organization** Pages
sites.

Requirements
------------

- [postocol](https://github.com/anqurvanillapy/postocol) `== 0.2.0`
- [ghp-import](https://github.com/davisp/ghp-import), for publishing things to
`master` branch (note that `gh-pages` is `ghp-import`'s default target)

Usage
-----

First of all, delete all the files in `content` to start your own publishing,
and type `git remote` to check out and add your remote repository.

```bash
$ git remote
# use `$ git remote add ...` to add your remote repo
```

Secondly, put your Markdown files in the `content` folder, and run

```bash
$ python3 publish.py
```

And all the output files will be stored in `site` folder. Now you can use the
tool `ghp-import` to auto-commit to your remote repo on `master` branch.

```
$ ghp-import site/ -b master -m "your messages"
```

- Valid Markdown formats are:
    + `.markdown`
    + `.mdown`
    + `.mkdn`
    + `.md`
    + `.mkd`
    + `.mdwn`
    + `.mdtxt`
    + `.mdtext`
    + `.text`
    + `.txt`

License
-------

MIT
