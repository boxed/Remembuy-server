from django.urls import path

from remembuy.views import (
    index,
    api_items,
    api_complete,
    api_un_complete,
    api_edit,
    api_add,
    login,
    logout,
    redirect_login,
)

urlpatterns = [
    path('', index),
    path('api/items/', api_items),
    path('api/add/', api_add),
    path('api/items/<int:id>/complete/', api_complete),
    path('api/items/<int:id>/un_complete/', api_un_complete),
    path('api/items/<int:id>/edit/', api_edit),
    path('accounts/login/', redirect_login),
    path('login/', login),
    path('logout/', logout),
]
