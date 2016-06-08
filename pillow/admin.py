from django.contrib import admin
from models import Produto
from forms import ProdutoForm
from image_cropping import ImageCroppingMixin


class ProdutoAdmin(ImageCroppingMixin, admin.ModelAdmin):
    model = Produto
    form = ProdutoForm
    list_display = ('id', 'nome', 'picture_max_size', 'picture_regular_size', 'picture_sm')


admin.site.register(Produto, ProdutoAdmin)
