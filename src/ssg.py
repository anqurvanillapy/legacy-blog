#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
import markdown
from bs4 import BeautifulSoup
from datetime import datetime
from jinja2 import *


class SSG(object):
    """Publish all the Markdown files in content folder"""
    def __init__(self):
        self.mddir = 'content/'
        self.htmldir = 'site/'
        self.clean(self.htmldir)
        self.posts = self.load_posts(self.mddir)
        self.publish(self.posts)

    def clean(self, htmldir):
        for item in os.listdir(htmldir):
            if os.path.isfile(htmldir + item):
                if os.path.splitext(item)[1] in ['.html', '.htm']:
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
        valid_md = sorted(valid_md, key=lambda md: md.split('-')[0], reverse=True)

        try:
            posts = []
            for post in valid_md:
                with codecs.open(post, 'r', encoding='utf-8') as filehandle:
                    html = BeautifulSoup(markdown.markdown(filehandle.read()), 'lxml')
                    html.html.hidden = True
                    html.body.hidden = True # remove html and body tags
                    fn = os.path.splitext(os.path.basename(post))[0]
                    title = html.h1.string
                    date = datetime.strptime(fn.split('-')[0], "%Y%m%d").strftime("%B %d %Y")
                    html.find('h1').extract() # remove title after getting it
                    post = {
                        'filepath': '%s%s.html' % (self.htmldir, fn),
                        'fnext': '%s.html' % fn,
                        'title': title,
                        'date': date.upper(),
                        'content': html
                    }
                    posts.append(post)
        except Exception, e:
            raise e

        return posts

    def publish(self, posts):
        env = Environment(loader=PackageLoader('src', '../templates'))
        index_tmpl = env.get_template('index.tmpl')
        post_tmpl = env.get_template('post.tmpl')

        try:
            with open('site/index.html', 'w') as filehandle:
                filehandle.write(index_tmpl.render(posts=posts))
        except Exception, e:
            raise e

        try:
            for post in posts:
                with codecs.open(
                    post['filepath'], 'w',
                    encoding='utf-8',
                    errors='xmlcharrefreplace'
                ) as filehandle:
                    filehandle.write(post_tmpl.render(post=post))
        except Exception, e:
            raise e
