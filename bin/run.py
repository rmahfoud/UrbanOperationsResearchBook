#! /usr/bin/python
import sys, os

if __name__ == '__main__':
    bindir = os.path.dirname(os.path.abspath(sys.argv[0]))
    os.system(os.path.join(bindir, "scrape.py"))
    os.system(os.path.join(bindir, "generate.py"))
    os.system(os.path.join(bindir, "package-epub.py"))
