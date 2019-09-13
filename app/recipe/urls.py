from django.urls import path, include
from rest_framework.routers import DefaultRouter
from recipe import views

# Now, we will create our default router. The default router is a
# feature of the Django rest framework that will automatically
# generate the URLs for our viewset.
router = DefaultRouter()
router.register('tags', views.TagViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]
