import tempfile
import os
import time
import datetime
from optparse import make_option

from django.core.management.base import BaseCommand  # , CommandError
from django.core.files.storage import default_storage
from basic_cms import settings
from image_diet import squeeze


class Command(BaseCommand):
    help = "compress all cms images using image_diet. Creates a backup copy of compressed files"

    option_list = BaseCommand.option_list + (
        make_option(
            "--recently_changed",
            action='store_true',
            default=False,
            dest='recently_changed',
            help='Compress only images changed during last 24 hours',
        ),
    )

    def handle(self, *args, **options):
        timestamp = time.time()
        timestamp = datetime.datetime.fromtimestamp(timestamp).strftime('-%Y-%m-%d-%H:%M:%S')

        def process_file(path):
            """Process single file"""
            # failsafe copy of file
            copy = default_storage.open(path, 'rb')
            default_storage.save(path + timestamp, copy)
            copy.close()
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

        def compress_files(data, dirtree):
            for f in data[1]:  # files from listdir
                if f and f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):  # sometimes it is [u'']
                    path = os.sep.join(dirtree)
                    path = os.path.join(path, f)
                    process_file(path)

            for d in data[0]:  # directories from list_dir
                dirtree.append(d)
                d = default_storage.listdir(os.sep.join(dirtree))
                compress_files(d, dirtree)
                dirtree.pop()  # remove last item, not needed anymore

        if 'image_diet' in settings.INSTALLED_APPS and settings.BASIC_CMS_COMPRESS_IMAGES:
            upload_dirs = [settings.PAGE_UPLOAD_ROOT, settings.FILEBROWSER_DIRECTORY]
            for directory in upload_dirs:
                if directory:
                    dirtree = [directory]
                    data = default_storage.listdir(directory)
                    compress_files(data, dirtree)
