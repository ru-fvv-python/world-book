from django.shortcuts import render

from .models import Book, Author, BookInstance


# Create your views here.

def index(request):
    """Генерация количеств некоторых объектов"""
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Доступные книги (статус "на складе")
    num_instances_available = BookInstance.objects.filter(
        status__exact=2).count()

    # Авторы книг
    num_authors = Author.objects.all().count()

    # Отрисовка HTML шаблона index.html с данными
    # внутри переменной context
    return render(request, 'index.html',
                  context={'num_books': num_books,
                           'num_instances': num_instances,
                           'num_instances_available': num_instances_available,
                           'num_authors': num_authors},
                  )
