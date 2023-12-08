from django.urls import include, path
from django.conf.urls.static import static
from rest_framework import routers
from tastevineapi.views import register_user, login_user, RecipeView, IngredientView, CategoryView
from . import settings

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"recipes", RecipeView, "recipe")
router.register(r"ingredients", IngredientView, "ingredient")
router.register(r"categories", CategoryView, "category")


urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
