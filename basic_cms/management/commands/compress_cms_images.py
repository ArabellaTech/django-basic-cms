import tempfile
import os
import time
import datetime
from optparse import make_option

from django.core.management.base import BaseCommand  # , CommandError
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from basic_cms import settings
from image_diet import squeeze


class Command(BaseCommand):
    help = "compress all cms images using image_diet. Creates a backup copy of compressed files"

    option_list = BaseCommand.option_list + (
        make_option(
            "--new_only",
            action='store_true',
            default=False,
            dest='new_only',
            help='Compress only new images',
        ),
    )

    def handle(self, new_only, **options):
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

        def compress_files(data, dirtree, new_only=False):
            django_basic_cms_compressed_flag = "dbc_compressed"

            for f in data[1]:  # files from listdir

                if f and f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):  # sometimes if == [u'']
                    dir_path = os.sep.join(dirtree)
                    path = os.path.join(dir_path, f)
                    flagged_file_name = '.%s.%s' % (f, django_basic_cms_compressed_flag)
                    flag_path = os.path.join(dir_path, flagged_file_name)
                    print("Processing %s" % path)
                    if new_only:
                        should_process_file = False

                        if not default_storage.exists(flag_path):
                            should_process_file = True
                        else:
                            file_mt = default_storage.modified_time(path)
                            flag_mt = default_storage.modified_time(flag_path)
                            if flag_mt < file_mt:
                                should_process_file = True

                        if should_process_file:
                            process_file(path)
                    else:
                        process_file(path)

                    # add flag, for all files. This flag is used only when "new_only" option is called.
                    if default_storage.exists(flag_path):
                        default_storage.delete(flag_path)
                    default_storage.save(flag_path, ContentFile(""))

            for d in data[0]:  # directories from list_dir
                dirtree.append(d)
                d = default_storage.listdir(os.sep.join(dirtree))
                compress_files(d, dirtree, new_only)
                dirtree.pop()  # remove last item, not needed anymore

        if settings.BASIC_CMS_COMPRESS_IMAGES:
            if 'image_diet' not in settings.INSTALLED_APPS:
                raise NotImplementedError("You need to install image_diet to use BASIC_CMS_COMPRESS_IMAGES")

            upload_dirs = [settings.PAGE_UPLOAD_ROOT, settings.FILEBROWSER_DIRECTORY]
            for directory in upload_dirs:
                if directory:
                    dirtree = [directory]
                    data = default_storage.listdir(directory)
                    compress_files(data, dirtree, new_only)
