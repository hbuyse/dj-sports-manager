"""."""

# Standard library
import logging
import os

# Django
from django.conf import settings
from django.core.files.storage import FileSystemStorage

logger = logging.getLogger(__name__)


class OverwriteStorage(FileSystemStorage):
    """Standard filesystem storage that override a file."""

    def get_available_name(self, name, max_length):
        """Return a filename that's free on the target storage system, and available for new content to be written to.

        Found at http://djangosnippets.org/snippets/976/.
        """
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            logger.info("Removing file {}".format(os.path.join(settings.MEDIA_ROOT, name)))
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name
