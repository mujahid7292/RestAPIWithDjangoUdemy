from django.urls import path
from user import views

# Then we can define our app name and the app name is set to
# help identify which app we're creating the URL from.
app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateAuthToken.as_view(), name='token'),
]
