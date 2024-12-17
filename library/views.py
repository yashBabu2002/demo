from django.shortcuts import render

# Create your views here.

from .models import Book
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
import json
from .validations import check_validate
from urllib.parse import parse_qs

'''
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    published_year = models.PositiveIntegerField()

'''

def get_books(request, pk=None):
    if request.method == "GET":
        if pk:
            try:
                book = Book.objects.get(id=pk)
                book_data = {"id":book.id,
                             "title":book.title,
                             "author":book.author,
                             "price":book.price,
                             "published_year":book.published_year
                             }
                return JsonResponse(book_data, safe=False)
                
            except Book.DoesNotExist:
                return JsonResponse({'error': 'Book not found'}, status=404)
        else:
            books = Book.objects.all()
            book_data = [{"id":book.id,
                        "title":book.title,
                        "author":book.author,
                        "price":book.price,
                        "published_year":book.published_year}
                        for book in books]
            return JsonResponse(book_data, safe=False)
        
    return JsonResponse({'error':'Invalid request method'}, status=405)


@csrf_exempt 
def create_books(request):
    print(request.POST.get('title'))
    if request.method == "POST":
        title = request.POST.get('title')
        author = request.POST.get('author')
        price = request.POST.get('price')
        published_year = request.POST.get('published_year')

        validate_data = check_validate(title=title, author=author, price=price, published_year=published_year)
        if validate_data:
            return validate_data
        
        if not title or not author or price or published_year:
            return JsonResponse({'error':'All fields are required'}, status=403)

        book = Book.objects.create(
            title=title,
            author=author,
            price=price,
            published_year=published_year
        )

        return JsonResponse({'message':'Books added successfully'})
    return JsonResponse({"error":"Invalid Request mehotd"}, status=405)

@csrf_exempt
def update_books(request, pk):
    if request.method == 'PUT' or request.method == 'PATCH':

        data = json.loads(request.body)

        book = get_object_or_404(Book, id=pk)
        # book = Book.objects.get(id=pk)

        title = data.get('title', book.title)
        author = data.get('author', book.author)
        price = data.get('price', book.price)
        published_year = data.get('published_year', book.published_year)

        validate_data = check_validate(title=title, author=author, price=price, published_year=published_year)
        if validate_data:
            return validate_data

        
        book.title = title
        book.author = author
        book.price = price
        book.published_year = published_year
        book.save()

        return JsonResponse({'message':'Books updated successfully',
                             'book':{
                                 'id':book.id,
                                 'title':book.title,
                                 'author':book.author,
                                 'price':book.price,
                                 'published_year':book.published_year
                             }})
    return JsonResponse({'error':'Invalid request method'}, status=405)


@csrf_exempt
def delete_book(request, pk):

    if request.method == 'DELETE':
        book = get_object_or_404(Book, id=pk)
        book.delete()
        return JsonResponse({'message': f'{book.title} has been deleted'})
    return JsonResponse({'error':'Invalid request method'}, status=405)
    


class ListRetrieveView(View):

    def get(self, request, pk=None):
        if pk:
            book = get_object_or_404(Book, id=pk)
            book_data = {
                'id':book.id,
                'title':book.title,
                'author':book.author,
                'price':book.price,
                'published_year':book.published_year
            }
            return JsonResponse(book_data)


        else:
            books = Book.objects.all()
            book_data = [{
                'id':book.id,
                'title':book.title,
                'author':book.author,
                'price':book.price,
                'published_year':book.published_year
            } for book in books]
            return JsonResponse(book_data, safe=False)
 

class CreateUpdateView(View):
    def post(self, request):
    
        title = request.POST.get('title')
        author = request.POST.get('author')
        price = request.POST.get('price')
        published_year = request.POST.get('published_year')

        validate_data = check_validate(title=title, author=author, price=price, published_year=published_year)
        if validate_data:
            return validate_data

        book = Book.objects.create(
            title=title,
            author=author,
            price=price,
            published_year=published_year
        )

        return JsonResponse({"message":f"'{book.title}' book added successfully"})
        
    def put(self, request, pk):

        book = get_object_or_404(Book, id=pk)

        data = parse_qs(request.body.decode('utf-8'))

        title = data.get('title', [book.title])[0]
        author = data.get('author', [book.author])[0]
        price = data.get('price', [book.price])[0]
        published_year = data.get('published_year', [book.published_year])[0]


        validate_data = check_validate(title=title, author=author, price=price, published_year=published_year)
        if validate_data:
            return validate_data
        
        book.title=title
        book.author=author
        book.price=price
        book.published_year=published_year
        book.save()

        return JsonResponse({'message':f'{book.title} updated successfully'})


class DeleteView(View):
    def delete(self, request, pk):
        book = get_object_or_404(Book, id=pk)
        book.delete()
        return JsonResponse({"message":f"{book.title} deleted"})
    


from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator

class BookCreateView(CreateView):
    def post(self, request, *args, **kwargs):
        model = Book
        data = json.loads(request.body)

        title = data.get('title')
        author = data.get('author')
        price = data.get('price')
        published_year = data.get('published_year')

        validate_data = check_validate(title=title, author=author, price=price, published_year=published_year)
        if validate_data:
            return validate_data
        
        book = Book.objects.create(
            title=title,
            author=author,
            price=price,
            published_year=published_year
        )

        return JsonResponse({'message':f'{book.title} book is added'})
    
class BookUpdateView(UpdateView):
    def post(self, request, pk, *args, **kwargs):
        book = get_object_or_404(Book, pk=pk)

        data = json.loads(request.body)

        title = data.get('title', book.title)
        author = data.get('author', book.author)
        price = data.get('price', book.price)
        published_year = data.get('published_year', book.published_year)

        validate_data = check_validate(title=title, author=author, price=price, published_year=published_year)
        if validate_data:
            return validate_data
        
        book.title = title
        book.author = author
        book.price = price
        book.published_year = published_year
        book.save()
        return JsonResponse({'message':f'{book.title} book has been updated'})
    

class BookListView(ListView):
    def get(self, request, *args, **kwargs):
        model = Book

        books = Book.objects.all()
        paginator = Paginator(books, 3)
        
        book_data = [{
            'id':book.id,
            'title':book.title,
            'author':book.author,
            'price':book.price,
            'published_year':book.published_year
        }for book in books]

        return JsonResponse(book_data, safe=False)
    
class BookDetailView(DetailView):
    def get(self, request, pk, *args, **kwargs):
        model = Book

        book = get_object_or_404(Book, pk=pk)
        book_data = {
            'id':book.id,
            'title':book.title,
            'author':book.author,
            'price':book.price,
            'published_year':book.published_year
        }

        return JsonResponse(book_data)
    
class BookDeleteView(DeleteView):
    def post(self, request, pk, *args, **kwargs):
        book = get_object_or_404(Book, pk=pk)

        book.delete()

        return JsonResponse({'message':'book has been deleted'})

