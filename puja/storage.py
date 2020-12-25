from django.core.files.storage import FileSystemStorage
from gdstorage.storage import GoogleDriveStorage

class GoogleDriveStorageSystemPuja(GoogleDriveStorage):
    is_secure = False