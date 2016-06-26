from django import forms
from models import Picture
from PIL import Image
import base64
import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile


def image_to_b64(source, size_img_blur):
    data_img = StringIO.StringIO()
    tiny_img = Image.open(source)
    tiny_img.thumbnail(size_img_blur)
    tiny_img.save(data_img, format="BMP")
    tiny_img.close()
    encoded_b64_picture = base64.b64encode(data_img.getvalue())
    return encoded_b64_picture


def generate_resized_image(source, size):
    img_l = Image.open(source)
    img_l.thumbnail(size, Image.ANTIALIAS)
    data_img = StringIO.StringIO()
    img_l.save(data_img, 'JPEG')
    img_l.close()
    img_temp_file = InMemoryUploadedFile(data_img, None,
                                         str(size[0]) + '.jpg', 'image/jpeg',
                                         data_img.len, None)
    return img_temp_file


class PictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ['title', 'description', 'img_l']

    def save(self, commit=True):
        instance = super(PictureForm, self).save(commit=False)
        source = instance.img_l
        size_img_l = 1920, 1080
        size_img_m = 1366, 768
        size_img_s = 768, 432
        size_img_blur = 9, 9
        instance.save()
        instance.img_blur = image_to_b64(source, size_img_blur)
        img1 = generate_resized_image(source, size_img_l)
        instance.img_l = img1
        instance.img_m = generate_resized_image(source, size_img_m)
        instance.img_s = generate_resized_image(source, size_img_s)
        instance.save()
        return instance
