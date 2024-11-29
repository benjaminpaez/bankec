from django.urls import path
from .views import FavoritosViewCreate, FavoritosViewList, FavoritoViewDelete

app_name = 'favoritos'

urlpatterns = [
    path('', FavoritosViewList.as_view(), name='lista_favoritos'),
    path('agregar/<int:pk>/', FavoritosViewCreate.as_view(), name='crear_favorito'),
    path('eliminar/<int:pk>/', FavoritoViewDelete.as_view(), name='eliminar_favorito'),

]