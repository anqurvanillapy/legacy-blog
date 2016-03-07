#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import ssg


def init_path():
    path = os.getcwd()
    if path not in sys.path:
        sys.path.append(path)


def main():
    init_path()
    run = ssg.SSG()
