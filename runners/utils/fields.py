from django.utils.deconstruct import deconstructible


@deconstructible
class UploadTo:
    """
    Generates path function usable for ImageField upload_to argument.

    Given format string is formatted with using .format(instance=instance, filename=filename) so
    you can use format like:

    - /{instance.application.user.id}/signature/{filename}

    """

    def __init__(self, *_, path_fmt):
        self.path_fmt = str(path_fmt)

    def __call__(self, instance, filename):
        return self.path_fmt.format(instance=instance, filename=filename)
