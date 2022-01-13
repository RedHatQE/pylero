import sys
from distutils.command.install import INSTALL_SCHEMES

from setuptools import setup

PACKAGE_NAME = "pylero"
CLI_NAME = "pylero-cmd"

# change the data dir to be the etc dir under the package dir
for scheme in list(INSTALL_SCHEMES.values()):
    scheme['data'] = '%s/%s/etc' % (scheme['purelib'], PACKAGE_NAME)

install_requires_ = [
    'click',
    'pre-commit',
]

if sys.version_info >= (3, 0):
    install_requires_.insert(0, 'suds-py3')
else:
    install_requires_.insert(0, 'suds')

# reading description from README.md
with open("README.md", "r") as handle:
    LONG_DESCRIPTION = handle.read()

if __name__ == "__main__":
    setup(
        name=PACKAGE_NAME,
        version='0.0.1',
        description="Python SDK for Polarion",
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/markdown',
        url="https://github.com/RedHatQE/pylero",
        author="%s Developers" % PACKAGE_NAME,
        author_email="szacks@redhat.com",
        license='MIT',
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
        install_requires=install_requires_,
        classifiers=[
            'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
            'Intended Audience :: Developers',      # Define that your audience are developers
            'Topic :: Software Development :: Build Tools',
            'License :: OSI Approved :: MIT License',   # Again, pick a license
            'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.8',
          ]
    )
