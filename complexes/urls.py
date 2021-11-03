from django.urls import path
from .views import GetComplexesList, GetComplex, UpdateComplex, CreateComplex, DeleteComplex

urlpatterns = [
    path('get_complexes_list/', GetComplexesList.as_view()),
    path('get_complex/', GetComplex.as_view()),
    path('update_complex/', UpdateComplex.as_view()),
    path('create_complex/', CreateComplex.as_view()),
    path('delete_complex/', DeleteComplex.as_view())
]
