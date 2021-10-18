from rest_framework import viewsets
from .serializers import BookSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Book, Author, Category
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
import requests
from django.core.exceptions import ObjectDoesNotExist


class BookView(viewsets.ModelViewSet):
    """Można zastosować ListAPIView do wyświetlenia listy, a następnie
    APIView do wyświetlenia szczegółów danej książki"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['published_date', 'authors', 'categories', 'published_date']
    search_fields = ['published_date', 'title']
    http_method_names = ['get', 'head']


def prep_data(data: list):
    """Przygotowanie danych pobranych z google books"""
    book = {
        'title': data['title'],
        'authors': [],
        'categories': []
    }
    try:
        for author in data['authors']:
            author_obj, created = Author.objects.get_or_create(name=author)
            book['authors'].append(author_obj.id)
    except KeyError:
        pass
    try:
        for category in data['categories']:
            category_obj, created = Category.objects.get_or_create(name=category)
            book['categories'].append(category_obj.id)
    except KeyError:
        pass
    book['published_date'] = data.get('publishedDate', None)
    book['average_rating'] = data.get('averageRating', None)
    book['ratings_count'] = data.get('ratingsCount', None)
    try:
        book['thumbnail'] = data['imageLinks']['thumbnail']
    except KeyError:
        book['thumbnail'] = None
    return book


def get_books(data: str) -> list:
    """Funkcja pobierająca dane z google books"""
    r = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={data}").json()
    books_list = [i["volumeInfo"] for i in r["items"]]
    return books_list


@api_view(['POST'])
def new_book(request):
    if request.method == 'POST':
        books_list = get_books(request.data['q'])
        for book in books_list:
            book = prep_data(book)
            try:
                book_query = Book.objects.get(title=book["title"])
                for book_authors in book['authors']:
                    book_query.authors.add(book_authors)
                for book_categories in book['categories']:
                    book_query.categories.add(book_categories)
                book_query.published_date = book['published_date']
                book_query.average_rating = book['average_rating']
                book_query.ratings_count = book['ratings_count']
                book_query.thumbnail = book['thumbnail']
                book_query.save()
            except ObjectDoesNotExist:
                serializer = BookSerializer(data=book)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("Database updated", status=status.HTTP_200_OK)
