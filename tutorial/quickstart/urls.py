from django.urls import path, include
from tutorial.quickstart import views
from rest_framework import routers


app_name = 'quickstart'
router = routers.DefaultRouter()
router.register(r'Description', views.DescriptionViewSet)
router.register(r'Donate', views.DonateItemViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]