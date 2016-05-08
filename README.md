<div style="text-align:center">

![UOR Map](map3.jpg)

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

The EPUB book will appear in the current director as <tt>UrbanOperationsResearch.epub</tt> for you to enjoy on your favorite e-reader.

# Copyrights

These scripts are for personal enjoyment only. Please respect the copyright owners of the original book and do not distribute the ebook that's produced by these scripts.

# Dependencies:

```bash
sudo apt-get install libffi-dev libssl-dev build-essential \
     g++-4.4 libboost-all-dev libsparsehash-dev \
     git-core perl ipython
sudo pip install cryptography scrapy
```

# License

This software is released under the [MIT license](https://opensource.org/licenses/MIT).
