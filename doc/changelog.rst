============
 Changelog
============

This file describe new features and incompatibilites between released version of the CMS.

Release 0.2.3.1
===============

    * Firefox CSS fix


Release 0.2.3
==============

    * Fix removing parent


Release 0.2.2
==============

    * Set default PAGE_UNIQUE_SLUG_REQUIRED to True
    * Did redirect for old slug names


Release 0.2.1
==============

    * Added get_pages_with_tag templatetag


Release 0.2.0
==============

    * Compatibility with Django 1.6


Release 0.1.x
==============

    * Added preview near textarea
    * Added tags in export/import
    * Remove the dependency on django-staticfiles
    * Upgraded html5lib to 1.0b3
    * Python 3.3 compatibility
    * Fix actions on grapelli
    * import/export fixes
    * File and Image placeholer now users the same filename scheme that preserve the original filename
    * Remove the dependency on BeautifulSoup
    * Tiny MCE javascript is not included with this CMS anymore. Please use https://github.com/aljosa/django-tinymce
    * Fix revision drop-down
    * Fix js
    * Fix setup
    * Fix migrations for custom user model
    * Set django-taggit as required
    * Reset migrations
    * Renamed to Django Basic CMS (basic_cms)
    * Fixed tests (added travis + coveralls)
    * Released on PyPI
    * Released on readthedocs.org
