from django.urls import path, include
from accounts import views


urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(next_page='home'), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', include([
        path('detail/', views.ProfileDetailView.as_view(), name='profile-detail'),
        path('edit/', views.ProfileEditView.as_view(), name='profile-edit')
    ]))
]
