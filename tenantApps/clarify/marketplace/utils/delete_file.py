import os
from django.conf import settings

def delete_file(path):
    """ Helper function to delete a file. """
    full_path = os.path.join(settings.MEDIA_ROOT, path)
    try:
        if os.path.isfile(full_path):
            os.remove(full_path)
    except Exception as e:
        # Log the exception for debugging purposes.
        # You could use Python's built-in logging or any logging utility you prefer.
        print(f"Error deleting file {full_path}: {e}")
