import mimetypes
import uuid
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.utils.deconstruct import deconstructible


@deconstructible
class UploadTo:
    """
    This utility provides a generalised way for
    storing files based on a UUID naming scheme
    """

    def __init__(self, folder_name):
        """
        Initialise a callable instance of the class with the given parameters
        :param folder_name: the name of the folder where to write the file
        """

        self.folder_name = folder_name

    def __call__(self, instance, filename):
        """
        Compute the location of where to store the file, removing any
        existing file with the same name
        :param instance: the instance to which file is being uploaded
        :param filename: the original name of the file, used for the extension
        :return: the path to the uploaded file
        """

        now = datetime.now()
        folder_name = now.strftime(self.folder_name)

        # Name of the file
        uuid_key = uuid.uuid4()

        # Extension of the file
        extension = filename.split('.')[-1]
        extension = extension.lower()
        extension = f'.{extension}'
        if extension not in mimetypes.types_map.keys():
            extension = ''

        # Full path to the file
        destination = Path(folder_name, f'{uuid_key}{extension}',)

        # Change the uuid_key if destination file already exists (highly unlikely)
        while Path(settings.MEDIA_ROOT, destination).exists():
            uuid_key = uuid.uuid4()
            destination = Path(folder_name, f'{uuid_key}{extension}', )

        return destination
