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
    api_autocomplete,
)

urlpatterns = [
    path('', index),
    path('api/items/', api_items),
    path('api/autocomplete/', api_autocomplete),
    path('api/add/', api_add),
    path('api/complete/', api_complete),
    path('api/un_complete/', api_un_complete),
    path('api/edit/', api_edit),
    path('accounts/login/', redirect_login),
    path('login/', login),
    path('logout/', logout),
]
