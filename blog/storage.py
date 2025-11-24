from cloudinary_storage.storage import MediaCloudinaryStorage

class CKEditorCloudinaryStorage(MediaCloudinaryStorage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.folder = 'ckeditor_uploads/'