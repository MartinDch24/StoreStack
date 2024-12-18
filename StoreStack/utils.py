from django.utils.text import slugify


def product_image_folder(instance):
    """
    Dynamic folder path function for storing product images in Cloudinary.
    Creates a folder based on the product name.
    """
    return f'products/{slugify(instance.name)}/'
