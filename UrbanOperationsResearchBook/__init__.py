import re
import urlparse

# Try the tests: python -m doctest -v UrbanOperationsResearchBook/__init__.py

def join_url(base_url, url):
    """
        Joins a relative URL to a base URL if provided.
        
        >>> join_url(None, 'images/1.gif')
        'images/1.gif'
        >>> join_url('www.example.com/chapter1/', 'images/1.gif')
        'www.example.com/chapter1/images/1.gif'
        >>> join_url('www.example.com/chapter1', 'images/1.gif')
        'www.example.com/images/1.gif'
        >>> join_url('http://www.example.com/chapter1/', 'images/1.gif')
        'http://www.example.com/chapter1/images/1.gif'
        >>> join_url('http://www.example.com/chapter1', 'images/1.gif')
        'http://www.example.com/images/1.gif'
    """
    if base_url:
        return urlparse.urljoin(base_url, url)
    return url

def relative_url(base_url, url):
    """
        Gets the relative URL w.r.t. a base URL if provided.
        
        >>> relative_url(None, 'http://www.example.com/images/1.gif')
        'http://www.example.com/images/1.gif'
        >>> relative_url('http://www.example.com', 'http://www.example.com/images/1.gif')
        'images/1.gif'
        >>> relative_url('http://www.example.com/', 'http://www.example.com/images/1.gif')
        'images/1.gif'
    """
    if base_url:
        if not base_url.endswith('/'): base_url = base_url + '/'
        return re.sub(r'^' + base_url, '',  url)
    return url

