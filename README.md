# Django Image Preview with Dominant or Blurred images.

### The problem.
Image load is a major topic when the subject is fast load and presentation of a website or web application. I've recently learned and coded a solution that I think you guys could use in your own projects.

First of all, I expect anyone in here to know the concept of thumbnails, if you don't, make a quick search then get back :)

### The context
I've created this solution on a Django App that works as an API to provide information to another app. In this application, the admin had to be able to upload Images to fill a ImageField of one of my models.

As the admins who provide those images to the app aren't trained to treat the images for web, i need my app to do it for them.

### The solution
First thing to do: Create thumbnails
There are a lot of good packages to create thumbnails that you can find in [djangopackages.com](https://www.djangopackages.com/search/?q=thumbnails).

I chose to create my own solution using the "[PIllow](http://pillow.readthedocs.io/en/3.2.x/)"- a fork of Python Imaging Library that provides lots of resources. Pillow has a module called "Image" with a thumbnail function, this function will re-size your image with the size that you provide as an argument and will remove [ExIf](https://en.wikipedia.org/wiki/Exchangeable_image_file_format) as well, creating a lighter version of your original file.

### Show me the code
Here is where everything happens. While my model.py defines a class with 3 ImageFields, only one field is shown on my django admin, this way, the admin will provide only one picture, and the form will override the standard save method, using him to create other versions of the original picture.
forms.py:
``` python
from django import forms
from models import Picture
from PIL import Image
import base64
import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile

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
        img1 = generate_resized_image(source, size_img_l)
        instance.img_l = img1
        instance.img_m = generate_resized_image(source, size_img_m)
        instance.img_s = generate_resized_image(source, size_img_s)
        instance.save()
        return instance
```
admin.py:
``` python
from django.contrib import admin
from models import Picture
from forms import PictureForm


class PictureAdmin(admin.ModelAdmin):
    model = Picture
    form = PictureForm
    verbose_name = "Picture"
    verbose_name_plural = "Pictures"
    list_display = ('id', 'title', 'description', 'img_s',
                    'img_m', 'img_l', 'img_blur')


admin.site.register(Picture, PictureAdmin)
```
models.py
``` python
from __future__ import unicode_literals
from django.db import models


def rename_picture(instance, filename):
    return '{0}_{1}'.format(instance.id, filename)


class Picture(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=3000, null=True, blank=True)
    img_l = models.ImageField(upload_to=rename_picture, null=False)
    img_m = models.ImageField(upload_to=rename_picture)
    img_s = models.ImageField(upload_to=rename_picture)
    img_blur = models.CharField(max_length=3000)

    def __unicode__(self):
        return str(self.nome)
```
----pictures----

Now, in this example I’m using the '[storages](http://django-storages.readthedocs.io/en/latest/)' package to upload these files to my Amazon S3 bucket, but it works on local storage too.

### GO FURTHER!
OK, now that we have thumbnails, it's time to go a little further to speed up the application load time. Users are impatient, they demand to see something ASAP when they try to load your app, so lets show them something.

Lets create a preview that will be displayed only in the interval between data load from our API and the complete load of our original or thumbnails images from my Amazon S3 bucket.
There are 2 ways to do it.
* Find the dominant color of a image and display it on the original image size. (Used by Google and Pinterest). I won't be showing how to implement this method, but you can look for functions that already find the right color for each image and store it with your data like the blurred image.
* Create a really tiny thumbnail to be stored as a string on our database and display it. It will be blurred and fill the original image size. This way the content will be larger than choosing the dominant approach, but the result is far better.

In both cases, as the data will be really small, we can convert the data to a base64 encoded string and save it on the database and return the preview image data along with the rest of the data from the requested object. So the users browser won’t need to wait for the response from Amazon (or your local storage) to see the app. Of course, the preview image should be replaced immediately after the load of the original/thumbnail image. But you already get some seconds displaying something to hold your users attention.

### Shitty resolution image preview  (A.k.a. blurred image)
In this approach I set a [9, 9] pixels size to create a extra thumbnail and encoded the data to be storage on the DB. Check the code and some results bellow:
``` python
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

```
Results:

--tons of images--
Nice website to test your images:
[http://codebeautify.org/base64-to-image-converter](http://codebeautify.org/base64-to-image-converter)

also, I chose to save the [9, 9] image as .bmp because it’s smaller than JPG format… Didn’t research why is that, but I think it’s because the JPG has info to decompress his data, and this extra info must be the reason to the extra bytes.

Thanks to [Wagner Barreto](https://br.linkedin.com/in/wagnerbarretto/pt) for many tips about the topic.

Usefull links:

https://code.facebook.com/posts/991252547593574/the-technology-behind-preview-photos/

https://dev.opera.com/articles/native-responsive-images/

http://davidbcalhoun.com/2011/when-to-base64-encode-images-and-when-not-to/

https://jmperezperez.com/medium-image-progressive-loading-placeholder/

https://manu.ninja/dominant-colors-for-lazy-loading-images
