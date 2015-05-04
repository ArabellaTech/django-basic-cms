import os
import sys
coverage = None
try:
    from coverage import coverage
except ImportError:
    coverage = None

os.environ['DJANGO_SETTINGS_MODULE'] = 'basic_cms.testproj.test_settings'
current_dirname = os.path.dirname(__file__)
sys.path.insert(0, current_dirname)
sys.path.insert(0, os.path.join(current_dirname, '..'))

from django import setup
setup()

from django.test.runner import DiscoverRunner
from django.db.models import get_app, get_apps
import fnmatch

# necessary for "python setup.py test"
patterns = (
    "basic_cms.migrations.*",
    "basic_cms.tests.*",
    "basic_cms.testproj.*",
    "basic_cms.urls",
    "basic_cms.__init__",
    "basic_cms.search_indexes",
    "basic_cms.test_runner",
    "basic_cms.management.commands.*",
)


def match_pattern(filename):
    for pattern in patterns:
        if fnmatch.fnmatch(filename, pattern):
            return True
    return False


def get_all_coverage_modules(app_module, exclude_patterns=[]):
    """Returns all possible modules to report coverage on, even if they
    aren't loaded.
    """
    # We start off with the imported models.py, so we need to import
    # the parent app package to find the path.
    app_path = app_module.__name__.split('.')[:-1]
    app_package = __import__('.'.join(app_path), {}, {}, app_path[-1])
    app_dirpath = app_package.__path__[-1]

    mod_list = []
    for root, dirs, files in os.walk(app_dirpath):
        root_path = app_path + root[len(app_dirpath):].split(os.path.sep)[1:]
        for filename in files:
            if filename.lower().endswith('.py'):
                mod_name = filename[:-3].lower()
                path = '.'.join(root_path + [mod_name])
                if not match_pattern(path):
                    try:
                        mod = __import__(path, {}, {}, mod_name)
                    except ImportError:
                        pass
                    else:
                        mod_list.append(mod)

    return mod_list


class PageTestSuiteRunner(DiscoverRunner):

    def run_tests(self, test_labels=('basic_cms',), extra_tests=None):

        if coverage:
            cov = coverage()
            cov.erase()
            cov.use_cache(0)
            cov.start()

        results = DiscoverRunner.run_tests(self, test_labels, extra_tests)

        if coverage:
            cov.stop()
            app = get_app('basic_cms')
            modules = get_all_coverage_modules(app)
            cov.html_report(modules, directory='coverage')

        sys.exit(results)


def build_suite():
    runner = PageTestSuiteRunner()
    runner.setup_test_environment()
    runner.setup_databases()
    return runner.build_suite(test_labels=('basic_cms',), extra_tests=None)


if __name__ == '__main__':
    runner = PageTestSuiteRunner()
    if len(sys.argv) > 1:
        runner.run_tests(test_labels=(sys.argv[1], ))
    else:
        runner.run_tests()
