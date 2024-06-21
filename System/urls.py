# urls.py
from django.urls import path
from .views import add_post, update_post, delete_post, get_user_posts, add_comment, update_comment, delete_comment

urlpatterns = [
    path('add_post/', add_post, name='add_post'),
    path('update_post/<int:post_id>/', update_post, name='update_post'),
    path('delete_post/<int:post_id>/', delete_post, name='delete_post'),
    path('get_user_posts/', get_user_posts, name='get_user_posts'),
    path('add_comment/<int:post_id>/', add_comment, name='add_comment'),
    path('update_comment/<int:comment_id>/', update_comment, name='update_comment'),
    path('delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),
]
