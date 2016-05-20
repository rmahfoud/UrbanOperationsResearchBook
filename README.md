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

# Quality

The following are issues I found with the book as it's currently present online:

- The URL of [Prof Odoni's home page](http://web.mit.edu/orc/www/faculty/odoni.html) leads nowhere
- [Section 4.8.1](http://web.mit.edu/urban_or_book/www/book/chapter4/4.8.1.html) is missing
- [Table 6-12](http://web.mit.edu/urban_or_book/www/book/chapter6/images6/Table6-12.gif) in [section 6.5.7](http://web.mit.edu/urban_or_book/www/book/chapter6/6.5.7.html) is missing 

# Copyrights

These scripts and resulting EPUB are for personal enjoyment only. Please respect the copyright owners of the original book and do not distribute the ebook that's produced by these scripts.

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
- Parse and collate problems
- Remove inline style and replace with CSS
- Add images to manifest in OPF file
- Figure out why quotes are not showing in epub reader 
- Figure out why "bold" when it starts, it doesn't end till end of file epub reader (1.2)
- Figure out why everything is centered and why formulas as messed-up in epub reader 

# License

This software is released under the [MIT license](https://opensource.org/licenses/MIT).
