My Blog
=======

This blog is generated by my own Static Site Generator which can
faster my post publishing by simply adding Markdown format articles
to the archive folder.

Usage
-----

First of all, delete all the files in `content` and all the HTML files
in `site` to start your own publishing, and type `git remote` to check
out and add your remote repository.

```bash
$ git remote
# use `$ git remote add ...` to add your remote repo
```

Second, put your Markdown files in the `content` folder, and run

```bash
$ python publish.py
```

And all the output files will be stored in `site` folder. If you place
some arguments as messages like

```
$ python publish.py -m "updated blog posts"
```

It will generate the pages and automatically commit to your remote
repository with messages.

**Attention!** This generator is only for **User** or **Organization**
Pages sites.

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

Requirements
------------

- `Jinja2 == 2.8`
- `Markdown == 2.6.5`
- `beautifulsoup4 == 4.4.1`

TODO
----

* [ ] Update auto-commit method using `ghp-import` and `argparse`
* [ ] Use [Disqus](https://disqus.com/) as commenting plugin
* [x] Code block hightlighting
* [ ] Use a dev server to utilize hot reloading

License
-------

MIT
