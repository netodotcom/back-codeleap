from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth.views import LogoutView
from app.quickstart import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'posts', views.PostViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('logout/', views.UserLogout.as_view(), name='logout'),
    path('register/', views.UserCreate.as_view(), name='register'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('isTokenValid/', views.IsTokenValid.as_view(), name='isTokenValid')
]
