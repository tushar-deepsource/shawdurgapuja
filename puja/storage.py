from django.core.files.storage import FileSystemStorage
from gdstorage.storage import GoogleDriveStorage

class GoogleDriveStorageSystemPuja(GoogleDriveStorage,FileSystemStorage):
    is_secure = False