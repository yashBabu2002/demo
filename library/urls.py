from django.urls import path

from . import views
from .views import ListRetrieveView, CreateUpdateView, DeleteView

from .views import BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView


urlpatterns = [
    path('books/', views.get_books, name='get_books'),
    path('books/<int:pk>/', views.get_books, name='get_book'),
    path('books/add/', views.create_books, name='create_book'),
    path('books/update/<int:pk>/', views.update_books, name='update_book'),
    path('books/delete/<int:pk>/', views.delete_book, name='delete_book'),

    path('view/books/', ListRetrieveView.as_view(), name='list_books'),
    path('view/books/<int:pk>/', ListRetrieveView.as_view(), name='list_books'),
    path('view/books/create/', CreateUpdateView.as_view(), name='create-book'),
    path('view/books/update/<int:pk>/', CreateUpdateView.as_view(), name='create-book'),
    path('view/books/delete/<int:pk>/', DeleteView.as_view(), name='delete-books'),

    path('generic/books/', BookListView.as_view(), name='list_books'),
    path('generic/books/<int:pk>/', BookDetailView.as_view(), name='list_books'),
    path('generic/books/create/', BookCreateView.as_view(), name='create-book'),
    path('generic/books/update/<int:pk>/', BookUpdateView.as_view(), name='update-book'),
    path('generic/books/delete/<int:pk>/', BookDeleteView.as_view(), name='delete-book'),


    
]