from django.urls import include, path
from rest_framework import routers
from tastevineapi.views import register_user, login_user, RecipeView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"recipes", RecipeView, "recipe")


urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user)
]
