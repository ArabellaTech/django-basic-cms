===========
 Image_diet
===========

For installation instructions plese visit `image diet documentation <https://github.com/ArabellaTech/image-diet>`_.

Enabling in CMS
===============
Add ``BASIC_CMS_COMPRESS_IMAGES`` to setting::

    BASIC_CMS_COMPRESS_IMAGES = True

This will add manage command ``compress_cms_images``.
Refer to 

    ./manage.py compress_cms_images --help

for further information.
We recommend using ``./manage.py compress_cms_images --new_only`` as a cron job.
