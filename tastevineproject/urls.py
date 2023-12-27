from django.urls import include, path
from tastevineapi.views import UserViewSet, RecipeView, IngredientView, CategoryView, FavoriteView, NoteView
from rest_framework import routers
from django.conf.urls.static import static
from . import settings

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"recipes", RecipeView, "recipe")
router.register(r"ingredients", IngredientView, "ingredient")
router.register(r"categories", CategoryView, "category")
router.register(r"users", UserViewSet, "user")
router.register(r"favorites", FavoriteView, "favorite")
router.register(r"notes", NoteView, "note")


urlpatterns = [
    path('', include(router.urls)),
    path('register', UserViewSet.as_view({"post": "register_account"})),
    path('login', UserViewSet.as_view({"post": "user_login"}))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
