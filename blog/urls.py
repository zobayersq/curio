from django.urls import path 
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.blog_index, name="blog_index"),
    path("post/<int:pk>/", views.blog_detail, name="blog_detail"),
    path("category/<category>/", views.blog_category, name="blog_category"),
    path("categories/", views.blog_category_list, name="blog_category_list"),
    path('write_story/', views.CreateBlogView.as_view(), name='create_blog'),
    path("profile/", views.profile, name="profile" ),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('post/<int:pk>/love/', views.love_post, name='love_post'),
     path('api/signup/', views.UserSignupView.as_view(), name='api_signup'),
    path('api/login/', views.UserLoginView.as_view(), name='api_login'),
    path('api/logout/', views.UserLogoutView.as_view(), name='api_logout'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

