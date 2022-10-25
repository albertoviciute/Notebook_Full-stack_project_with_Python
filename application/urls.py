from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import home, sign_up, CreateCategoryView, show_user_categories, show_category, show_note, show_user_notes, search
from . import views

urlpatterns = [
    path('', home, name='home'),
    path('registration/sign_up/', sign_up, name='sign_up'),
    path('create_category', views.CreateCategoryView.as_view(), name='create_category'),
    path('categories', show_user_categories, name='show_user_categories'),
    path('edit_category/<int:id>', views.EditCategory.as_view(), name='edit_category'),
    path('delete_category/<int:id>', views.DeleteCategory.as_view(), name='delete_category'),
    path('show_category/<int:id>', show_category, name='show_category'),
    path('create_note', views.CreateNote.as_view(), name='create_note'),
    path('edit_note/<int:id>', views.EditNote.as_view(), name='edit_note'),
    path('delete_note/<int:id>', views.DeleteNote.as_view(), name='delete_note'),
    path('show_note/<int:id>', show_note, name='show_note'),
    path('notes', show_user_notes, name='show_user_notes'),
    path('search/', search, name='search'),
]
