from cleo import Application, Command
import os
import sys
from pydoc import ErrorDuringImport
from .helpers.helpers import add_venv_site_packages

from .commands.NewCommand import NewCommand
from .commands.InstallCommand import InstallCommand
from .commands.PackageCommand import PackageCommand

application = Application('Craft Version:', '2.0.1')
application.add(NewCommand())
application.add(InstallCommand())
application.add(PackageCommand())


ERROR = None

# try to add commands from the service container
sys.path.append(os.getcwd())
try:
    add_venv_site_packages()
    from wsgi import container
except Exception:
    pass

try:
    from config import packages
    # Add additional site packages to vendor if they exist
    for directory in packages.SITE_PACKAGES:
        path = os.path.join(os.getcwd(), directory)
        sys.path.append(path)
    from wsgi import container

    commands = []
    for key, value in container.providers.items():
        if key.endswith('Command'):
            commands.append(key)

    for command in commands:
        application.add(
            container.make('{0}'.format(command))
        )
except ErrorDuringImport as e:
    print(e)

except ImportError as e:
    pass

if __name__ == '__main__':
    application.run()
