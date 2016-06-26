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
