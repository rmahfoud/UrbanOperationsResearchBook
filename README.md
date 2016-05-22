<div style="text-align:center">

![UOR Map](https://raw.githubusercontent.com/rmahfoud/UrbanOperationsResearchBook/master/map3.jpg)

</div>

# Summary

This project is an effort to convert the online version of the first edition of [Urban Operations Research](http://web.mit.edu/urban_or_book/www/book/) book (Prentice-Hall © 1981) into a more readable ebook format (EPUB). This book is one of my favorites since I read parts of it during my graduate school. Unfortunately, it's out of print and used copies are sold at exorbitant prices. I thought it should be a nice exercise to scrape the online book and convert it to an EPUB that I can enjoy again.

# Running

To produce the EPUB book, run the following: 

```bash
git clone https://github.com/rmahfoud/UrbanOperationsResearchBook.git
cd UrbanOperationsResearchBook
bin/run.py
```

The EPUB book will appear in <tt>/tmp/uor/uor.epub</tt> for you to enjoy on your favorite e-reader.

The settings (including file paths) are defined in <tt>UrbanOperationsResearchBook/settings.py</tt>.

# Validation

The generated EPUB was validated using the online [EPUB Validator (beta)](http://validator.idpf.org/application/validate) tool.

The resulting EPUB was visually inspected with:

- [calibre](https://calibre-ebook.com/) on the desktop (Ubuntu and Windows).
- [Moon+ Reader Pro](http://www.moondownload.com/) on an Android phone.

Please report any issues in the EPUB on [github](https://github.com/rmahfoud/UrbanOperationsResearchBook/issues).

# Quality

The following are issues I found with the book as it's currently present online:

- The URL of [Prof Odoni's home page](http://web.mit.edu/orc/www/faculty/odoni.html) leads nowhere. I linked to his [new profile page](https://cee.mit.edu/odoni)
- The URL of [Prof Larson's home page](http://www-caes.mit.edu/people/larson.html) leads nowhere. I linked to his [new profile page](https://esd.mit.edu/Faculty_Pages/larson/larson.htm)
- [Section 4.8.1: Why Are M/G/m, G/G/1, and G/G/m Difficult?](http://web.mit.edu/urban_or_book/www/book/chapter4/4.8.1.html) is missing
- [Table 6-12](http://web.mit.edu/urban_or_book/www/book/chapter6/images6/Table6-12.gif) in [section 6.5.7](http://web.mit.edu/urban_or_book/www/book/chapter6/6.5.7.html) is missing 
- Its HTML in general is not of modern quality and does not translate directly to XHTML

While doing the conversion I ignored many of the warnings/errors due to non-canonical XHTML because it turns out most good readers do not require canonical XHTML and will work and render pages just fine. I ended up doing the bare-minimum required translations. Some things you might encounter (and might want to submit fixes for) if you use a reader that doesn't entirely like the current XHTML:

- The use of the ```<center>``` tag which is disallowed
- The use of the ```<font>``` tag which is disallowed
- The use of inline styles (e.g. ```<table cellpadding="5">```, or ```<p align="center">```) instead of CSS

# Dependencies:

On Ubuntu/Debian, run the following:

```bash
sudo apt-get install libffi-dev libssl-dev build-essential \
     g++-4.4 libboost-all-dev libsparsehash-dev \
     git-core perl ipython
```

or equivalent on non-Debian systems. 

Then install the following python dependencies:

```bash
sudo pip install cryptography
sudo pip install scrapy
```

# TODO:

1. Successfully convert to MOBI format in calibre to use on Kindle.
1. Add images to manifest in OPF file
1. 1.2: messed up blockquote
1. Remove use of ```<font>``` tag
1. Remove use of ```<center>``` tag
1. Remove inline style and replace with CSS

# Copyrights

These scripts and resulting EPUB are for personal enjoyment only. Please respect the copyright owners of the original book and do not distribute the ebook that's produced by these scripts.
 
# License

This software is released under the [MIT license](https://opensource.org/licenses/MIT).
