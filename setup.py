import os
from distutils.command.install import INSTALL_SCHEMES

from setuptools import setup

with open("README.md", "r") as handle:
    LONG_DESCRIPTION = handle.read()

PACKAGE_NAME = "pylero"
CLI_NAME = "pylero-cmd"
RELEASE_FILE = "/etc/system-release-cpe"
SUDS_NAME_CHANGE = False

# change the data dir to be the etc dir under the package dir
for scheme in list(INSTALL_SCHEMES.values()):
    scheme['data'] = '%s/%s/etc' % (scheme['purelib'], PACKAGE_NAME)

install_requires_ = [
    'click',
]

# Update install_requires_ for feodra 36 and greater
if os.path.exists(RELEASE_FILE):
    with open(RELEASE_FILE) as version_file:
        version_file_content = version_file.read().split(":")
        if (version_file_content[3] == "fedora") and (
                int(version_file_content[4]) > 35):
            SUDS_NAME_CHANGE = True

if SUDS_NAME_CHANGE:
    install_requires_.append('suds')
else:
    install_requires_.append('suds-community')


if __name__ == "__main__":
    setup(
        name=PACKAGE_NAME,
        version='0.0.3',
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
            PACKAGE_NAME+'.cli',
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
            'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
            'Intended Audience :: Developers',      # Define that your audience are developers
            'Topic :: Software Development :: Build Tools',
            'License :: OSI Approved :: MIT License',   # Again, pick a license
            'Programming Language :: Python :: 3',      # Specify which pyhton versions that you want to support
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
          ]
    )
