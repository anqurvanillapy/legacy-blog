# TOY PROJECT: EMBED BINARY DSF IN BROWSER ENGINE

Since the development of web app and some progressive web operating systems is
trending (e.g. Chrome OS, Firefox OS), many developers and communities keep
improving the performance of UI components written in HTML and CSS, and also the
JavaScript UI frameworks.

In my points of view, as a text-based serialization format, HTML could be more
compact for constructing the native UI components and even no need to be so
human-readable. And the DOM parser and the CSS parser could be optimized for
faster building the parse tree and creating the attachment of both (On WebKit,
DOM tree and style rules will be attached before constructing the render tree).
For further asynchronously DOM rendering, some objects could be also compiled
ahead of time for swapping the initial DOM tree if possible.

![render-engine-main-flow-webkit](http://www.html5rocks.com/en/tutorials/internals/howbrowserswork/webkitflow.png)

<center>
***Fig. WebKit main flow of rendering***
</center>

Thus, I am trying to embed a binary DSF (data serialization format) in the
middle of the work flow of DOM and CSS parsing, and additionally create some
JavaScript APIs for combining future-render DOM with the initial DOM tree, also
the swapping methods if this way of optimization is feasible.

As a matter of fact, I am more concerned about the web-based operating system
going mobile, on which a local database may be associated with a filesystem (or
a filesystem is implemented by a database), and therefore I might pre-store the
query statements in the DSF for the synchronous or asynchronous data
transferring.

Well, hope that I can make it.

## A Compiler Nature for HTML

In spite of the parsing algorithms of HTML and CSS, most of the browsers have
error tolerance to support well-known cases of invalid HTML, and share a
forgiving nature for this language <sup>[[1]](#ref1)</sup>. But inspired by
Python XML/HTML processing module [lxml](http://lxml.de), a compiler nature can
be brought to this structured language, strictly parsing it for those treated
as contents and components. And we can do easy templating within the `lxml`
instances for associating style rules with HTML.

Initially, highly optimization of ahead-of-time compilation could simply be
ignored, for it is not a big deal already. So I choose to use Python to
implement a pre-builder for re-structuring the HTML and CSS files, and a
compiler for translating into binary data.

Doing parsing with `lxml` is easy, but I prefer `bs4` (namely `BeautifulSoup4`)
which can contain `lxml` as the parser and feels good in normal use. The first
thing we can do is opening a file and parsing it, and extracting all the
comments within the document in which there may be some links of scripts for the
legacy browsers, because we are making it more platform-specific.

```python
from bs4 import BeautifulSoup, Comment

with open('index.html', 'r') as filehandle:
    dom = BeautifulSoup(filehandle.read(), 'lxml')
    cmts = dom.findAll(text=lambda t:isinstance(t, Comment))
    [c.extract() for c in cmts]
```

## Choosing A Format

*(WIP)*

## References

1. *The parsing algorithm* section from
[How browsers work](http://www.html5rocks.com/en/tutorials/internals/howbrowserswork/#The_parsing_algorithm).
<a name="ref1"></a>
