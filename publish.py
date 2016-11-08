#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from postocol import Postocol
from collections import defaultdict
from os.path import join, basename, splitext


class Blog(Postocol):
    """SSG Example"""
    def __init__(self):
        self.pymd_exts = ['fenced_code', 'codehilite']

    def run(self):
        self.clean()
        self.tmpls = self.load_templates()
        self.posts = self.load_posts()
        self.pages = self.render(self.posts)
        self.publish(self.pages, self.tmpls)
        self.send_codehilite_style(theme='tango')
        self.send_static(join(self.ofpath, self.staticpath))

    def render(self, posts):
        pages = []
        contents_table = []
        props = defaultdict(list)
        chfn = lambda x: '{}.html'.format(splitext(basename(x))[0])

        for c, m, f in posts:
            pages.append({'content': c, 'meta': m, 'fname': chfn(f)})

            if 'misc' not in m.get('type'):
                contents_table.append({'title': m['title'][0],
                                       'fname': chfn(f),
                                       'date': m['date'][0]})

            for mname in m.get('properties', []):
                props[mname].append({'title': m['title'][0], 'fname': chfn(f)}) 

        contents_table = sorted(contents_table, reverse=True,
            key=lambda p: p['fname'].split('-')[0])
        pages += [self.create_page_dict(c, n) for c, n in \
                  list(zip([contents_table, props], ['index', 'properties']))]
        return pages


if __name__ == '__main__':
    blog = Blog()
    blog.run()
