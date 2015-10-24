#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
from lib import tp0

def main():
    parser = argparse.ArgumentParser()
    tp0.setup_parser(parser)

    args = parser.parse_args()

    tp0.main(**vars(args))

if __name__ == "__main__":
    main()
