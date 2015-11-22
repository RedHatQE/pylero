import os
import ConfigParser
from distutils.core import setup

old_file = '/etc/pylarion/pylarion.cfg'
new_file = 'etc/pylarion/pylarion.cfg'


def get_settings_dir():
    return os.path.join('/etc', 'pylarion')


def update_config_file(path_to_old_file, path_to_new_file):
    """if a .cfg file already exists, we add the new fields
    from the prject .cfg file (if there are such fields).
    if there isnt a .cfg file we create it at the given path.
    """
    section = 'webservice'
    new_configs = []
    old_configs = []
    existing_keys = []

    config = ConfigParser.ConfigParser()
    config.read(path_to_new_file)

    if(os.path.isfile(path_to_old_file)):
        new_configs = config.items(section)
        config.remove_section(section)
        config.read(path_to_old_file)
        old_configs = config.items(section)
        existing_keys = map(lambda x: x[0], old_configs)
        for element in new_configs:
            if(element[0] not in existing_keys):
                config.set(section, element[0], element[1])

    with open(path_to_old_file, 'w') as configfile:
        print("Writing pylarion.cfg to " + path_to_old_file)
        config.write(configfile)

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
            (get_settings_dir(), ['etc/pylarion/newca.crt'])
        ],
    )
    update_config_file(
        old_file,
        new_file)
