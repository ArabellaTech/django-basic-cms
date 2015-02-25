import tempfile
import os
import urllib2

from django.core.management.base import BaseCommand, CommandError
from django.core.files.storage import default_storage
from basic_cms import settings
from image_diet import squeeze


class Command(BaseCommand):
    help = "compress all cms images using image_diet"

    def handle(self, *args, **options):
        results = []

        def compress_files(data, dirtree):
            # print data
            print dirtree
            for f in data[1]:  # files from listdir
                path = os.sep.join(dirtree)
                path = os.path.join(path, f)
                try:
                    path = default_storage.path(path)
                    squeeze(path)
                except NotImplementedError:
                    # print default_storage.url(f)
                    if path[-1:] != os.sep:
                        pf = default_storage.open(path)
                        url = default_storage.url(path)
                        response = urllib2.urlopen(url)
                        image = response.read()
                        tmpfilehandle, tmpfilepath = tempfile.mkstemp()
                        # print tmpfilehandle
                        tmpfilehandle = os.fdopen(tmpfilehandle, 'w')
                        # print tmpfilehandle
                        tmpfilehandle.write(image)
                        tmpfilehandle.close()
                        squeeze(tmpfilepath)
                        tmpfilehandle = open(tmpfilepath)
                        compressed_image = tmpfilehandle.read()
                        pf.write(compressed_image)
                        pf.close()
                        os.remove(tmpfilepath)

            for d in data[0]:  # directories from list_dir
                dirtree.append(d)
                d = default_storage.listdir(d)
                compress_files(d, dirtree)
                dirtree.pop()  # remove last item, not needed anymore

        if 'image_diet' in settings.INSTALLED_APPS and settings.BASIC_CMS_COMPRESS_IMAGES:
            upload_dirs = [settings.PAGE_UPLOAD_ROOT, settings.FILEBROWSER_DIRECTORY]
            for directory in upload_dirs:
                if directory:
                    dirtree = [directory]
                    data = default_storage.listdir(directory)
                    compress_files(data, dirtree)

        return results
