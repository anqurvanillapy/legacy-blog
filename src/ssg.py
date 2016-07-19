#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from markdown import markdown
from bs4 import BeautifulSoup
from datetime import datetime
from jinja2 import *
from pygments.formatters import HtmlFormatter


class SSG(object):
    """Publish all the Markdown files in content folder"""
    def __init__(self):
        self.inityear = 2016
        self.thisyear = int(datetime.now().strftime('%Y'))
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
        post_md = []
        md_exts = ['.markdown', '.mdown', '.mkdn', '.md', '.mkd', 
            '.mdwn', '.mdtxt', '.mdtext', '.text']

        for item in os.listdir(mddir):
            if os.path.isfile(mddir + item):
                if os.path.splitext(item)[1] in md_exts:
                    post_md.append(mddir + item)

        if not post_md:
            print('warning: nothing to publish')
            return
        post_md = sorted(post_md,
                         key=lambda md: md.split('-')[0],
                         reverse=True)

        try:
            posts = []
            for post in post_md:
                with codecs.open(post, 'r', encoding='utf-8') as filehandle:
                    html = BeautifulSoup(
                        markdown(
                            filehandle.read(),
                            extensions=[
                                'markdown.extensions.fenced_code',
                                'markdown.extensions.tables',
                                'markdown.extensions.codehilite']
                        ), 'lxml')
                    html.html.hidden = True
                    html.body.hidden = True # remove html and body tags
                    fn = os.path.splitext(os.path.basename(post))[0]
                    title = html.h1.string
                    try:
                        date = datetime.strptime(fn.split('-')[0],
                            "%Y%m%d").strftime("%B %d %Y").upper()
                    except:
                        date = False    # misc posts, hidden on index
                    html.find('h1').extract() # remove title after getting it
                    hlcss = HtmlFormatter().get_style_defs('.codehilite')
                    post = {
                        'filepath': '%s%s.html' % (self.htmldir, fn),
                        'fnext': '%s.html' % fn,
                        'title': title,
                        'date': date,
                        'content': html.decode('utf-8'),
                        'hlcss': hlcss  # FIXME: waste of memory
                    }
                    posts.append(post)
        except Exception, e:
            raise e # a post must have title and date

        return posts

    def publish(self, posts):
        env = Environment(loader=PackageLoader('src', '../templates'))
        index_tmpl = env.get_template('index.tmpl')
        post_tmpl = env.get_template('post.tmpl')

        try:
            with open('site/index.html', 'w') as filehandle:
                filehandle.write(index_tmpl.render(
                    posts=posts,
                    inityear=self.inityear,
                    thisyear=self.thisyear).encode('utf-8'))    # FIXME: use layouts
        except Exception, e:
            raise e

        try:
            for post in posts:
                with codecs.open(
                    post['filepath'], 'w',
                    encoding='utf-8',
                    errors='xmlcharrefreplace'
                ) as filehandle:
                    filehandle.write(post_tmpl.render(
                        post=post,
                        inityear=self.inityear,
                        thisyear=self.thisyear))
        except Exception, e:
            raise e
