from setuptools import setup
from distutils.command.install import INSTALL_SCHEMES

PACKAGE_NAME = "pylarion"
CLI_NAME = "pylarion-cmd"

# change the data dir to be the etc dir under the package dir
for scheme in list(INSTALL_SCHEMES.values()):
    scheme['data'] = '%s/%s/etc' % (scheme['purelib'], PACKAGE_NAME)

if __name__ == "__main__":
    setup(
        name=PACKAGE_NAME,
        version='0.0.1',
        description="Python SDK for Polarion",
        url="NONE",  # FIXME: once it is public
        author="%s Developers" % PACKAGE_NAME,
        author_email="szacks@redhat.com",
        package_dir={
            PACKAGE_NAME: 'src/%s' % PACKAGE_NAME,
        },
        packages=[
            PACKAGE_NAME,
            PACKAGE_NAME+".cli",
        ],
        scripts=[
            'scripts/%s' % PACKAGE_NAME,
            'scripts/%s' % CLI_NAME,
        ],
        data_files=[
            ('', ['etc/%s/%s.cfg' % (PACKAGE_NAME, PACKAGE_NAME)])
        ],
        install_requires=[
            'suds-py3;python_version>="3"',
            'suds;python_version<"3"',
            'click',
            'requests>=2.6.0'

        ],
    )
