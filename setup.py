import os
from distutils.core import setup


def get_settings_dir():
    return os.path.join('/etc', 'pylarion')


if __name__ == "__main__":
    setup(
        name="pylarion",
        version='0.0.1',
        description="Python SDK for Polarion",
        url="NONE",  # FIXME: once it is public
        author="Pylarion Developers",
        author_email="szacks@redhat.com",
        package_dir={
            'pylarion': 'src/pylarion',
        },
        packages=[
            'pylarion',
        ],
        scripts=[
            'scripts/pylarion',
        ],
        data_files=[
            (get_settings_dir(), ['etc/pylarion/pylarion.cfg']),
        ],
    )
