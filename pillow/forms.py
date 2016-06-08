from django import forms
from models import Produto
from PIL import Image
import base64
import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from image_cropping import ImageCropWidget


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        exclude = ['picture_sm', 'picture_regular_size']
        widgets = {
            'picture_max_size': ImageCropWidget,
        }

    def save(self, commit=True):
        instance = super(ProdutoForm, self).save(commit=False)
        print instance
        img = instance.picture_max_size
        img_sm = Image.open(img)
        print img
        if img_sm:
            size = 9, 7
            img_sm.thumbnail(size)
            buffr = StringIO.StringIO()
            img_sm.save(buffr, format="JPEG")
            img_sm.close()
            encoded_b64_picture = base64.b64encode(buffr.getvalue())
            print encoded_b64_picture
            instance.picture_sm = encoded_b64_picture
        img_md = Image.open(img)
        if img_md:
            size_md = 500, 300
            img_md.thumbnail(size_md, Image.ANTIALIAS)
            temp_handle = StringIO.StringIO()
            img_md.save(temp_handle, 'JPEG')
            img_md.close()
            file_temp = InMemoryUploadedFile(temp_handle, None,
                                             instance.nome + '_medium.jpg', 'image/jpeg',
                                             temp_handle.len, None)
            instance.picture_regular_size = file_temp
        img_lg = Image.open(img)
        if img_lg:
            size_lg = 1366, 768
            img_lg.thumbnail(size_lg, Image.ANTIALIAS)
            temp_handle = StringIO.StringIO()
            img_lg.save(temp_handle, 'JPEG')
            img_lg.close()
            file_tempe = InMemoryUploadedFile(temp_handle, None,
                                             instance.nome + '_medium.jpg', 'image/jpeg',
                                             temp_handle.len, None)
            instance.picture_max_size = file_tempe
        instance.save()
        return instance

