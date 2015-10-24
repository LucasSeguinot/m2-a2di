#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import sys

import pweave
import markdown
import locale

locale.setlocale(locale.LC_ALL, '')

rootdir = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(rootdir, "reports", "template.html"), "r") as f:
    template = f.read()

md = markdown.Markdown(
    output_format = "html5",
    extensions = [
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.smarty',
        'markdown.extensions.meta',
        'lib.markdown.mdx_math',
        'lib.markdown.figureAltCaption',
        'lib.markdown.meta_yaml',
        'lib.markdown.mdx_outline'
    ],
    extension_configs = {
        'markdown.extensions.smarty': {
            'substitutions': {
                'left-double-quote': '&laquo;&nbsp;',
                'right-double-quote': '&nbsp;&raquo;'
            }
        },
        'lib.markdown.mdx_math' : {
            'enable_dollar_delimiter' : True
        }
    })

def make_report(filename):
    mdw_filename = os.path.realpath(filename)
    md_filename = os.path.splitext(mdw_filename)[0] + ".md"
    html_filename = os.path.splitext(mdw_filename)[0] + ".html"

    pweave.weave(mdw_filename, doctype="pandoc", figformat=".svg")

    with open(md_filename, "r") as md_fileobj:
        content = md.convert(md_fileobj.read())

    metadata = {
        'title' : md.Meta["title"][0],
        'content' : content
    }

    with open(html_filename, "w") as f:
        f.write(template % metadata)

    #os.remove(md_filename)

def main():
    make_report(sys.argv[1])
    os.rmdir("figures")

if __name__ == "__main__":
    main()
