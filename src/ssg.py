#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
import markdown
from jinja2 import *


class Publish(object):
    """Publish all the md fies in content folder"""
    def __init__(self):
        self.mddir = 'content/'
        self.htmldir = 'site/'
        self.clean(self.htmldir)
        self.posts = self.load_posts(self.mddir)
        self.publish(self.posts)

    def clean(self, htmldir):
        for item in os.listdir(htmldir):
            if os.path.isfile(htmldir + item):
                if os.path.splitext(item)[1] in ['html', 'htm']:
                    try:    
                        os.remove(htmldir + item)
                    except:
                        print('error: unable to delete {0}'.format(item))

    def load_posts(self, mddir):
        valid_md = []
        md_exts = [
            '.markdown',
            '.mdown',
            '.mkdn',
            '.md',
            '.mkd',
            '.mdwn',
            '.mdtxt',
            '.mdtext',
            '.text'
        ]

        for item in os.listdir(mddir):
            if os.path.isfile(mddir + item):
                if os.path.splitext(item)[1] in md_exts:
                    valid_md.append(mddir + item)

        if not valid_md:
            print('warning: nothing to publish')
            return

        try:
            posts = []
            for md in valid_md:
                with codecs.open(md, 'r', encoding='utf-8') as filehandle:
                    html = markdown.markdown(filehandle.read())
                    fn = os.path.splitext(os.path.basename(md))[0]
                    post = {
                        'filename': '%s%s.html' % (self.htmldir, fn),
                        'html': html
                    }
                    posts.append(post)
        except Exception, e:
            raise e

        return posts

    def publish(self, posts):
        env = Environment(loader=PackageLoader('publish', '../templates'))
        index_tmpl = env.get_template('index.tmpl')
        layout_tmpl = env.get_template('layout.tmpl')

        try:
            with open('site/index.html', 'w') as filehandle:
                filehandle.write(index_tmpl.render(posts=len(posts)))
        except Exception, e:
            raise e

        try:
            for ch in posts:
                with codecs.open(
                    ch['filename'], 'w',
                    encoding='utf-8',
                    errors='xmlcharrefreplace'
                ) as filehandle:
                    filehandle.write(layout_tmpl.render(
                        title='Chapter ' + os.path.splitext(ch['filename'])[0][-1],
                        content=ch['html'])
                    )
        except Exception, e:
            raise e
