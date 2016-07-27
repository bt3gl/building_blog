#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'bt3'
SITENAME = u'Higher Bytes by bt3'
SITEURL = 'http://bt3gl.github.io'

PATH = 'content'

TIMEZONE = 'America/New_York'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None


# Social widget
SOCIAL = (('GitHub', 'https://github.com/bt3gl'),
          ('Twitter', 'https://twitter.com/_b_t_'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True


GITHUB_URL = 'http://github.com/bt3gl/'
REVERSE_CATEGORY_ORDER = True
LOCALE = "C"
FEED_ALL_RSS = 'feeds/all.rss.xml'
CATEGORY_FEED_RSS = 'feeds/%s.rss.xml'


# custom page generated with a jinja2 template
THEME = "./themes/bootstrap2-dark"


FEED_MAX_ITEMS = 5

DISQUS_SITENAME = "bt3gl"
DISQUS_SHORTNAME = "bt3gl"
TIMEZONE = 'America/New_York'
CATEGORY_FEED = 'feeds/%s.atom.xml'
FEED = 'feeds/all.atom.xml'
TAG_FEED = 'feeds/%s.atom.xml'
