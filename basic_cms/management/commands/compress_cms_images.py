import tempfile
import os

from django.core.management.base import BaseCommand  # , CommandError
from django.core.files.storage import default_storage
from basic_cms import settings
from image_diet import squeeze


class Command(BaseCommand):
    help = "compress all cms images using image_diet"

    def handle(self, *args, **options):

        def compress_files(data, dirtree):
            for f in data[1]:  # files from listdir
                path = os.sep.join(dirtree)
                path = os.path.join(path, f)
                try:
                    path = default_storage.path(path)
                    squeeze(path)
                except NotImplementedError:
                    if path[-1:] != os.sep:
                        pf = default_storage.open(path, 'rwb')
                        print("Processing %s" % pf.name)
                        image = pf.read()
                        tmpfilehandle, tmpfilepath = tempfile.mkstemp()
                        tmpfilehandle = os.fdopen(tmpfilehandle, 'wb')
                        tmpfilehandle.write(image)
                        tmpfilehandle.close()
                        squeeze(tmpfilepath)
                        tmpfilehandle = open(tmpfilepath)
                        pf.close()
                        default_storage.save(path, tmpfilehandle)
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
