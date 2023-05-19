from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from .models import Book, Author, BookInstance


class BookListView(generic.ListView):
    """обобщенный класс для отображения списка книг"""
    model = Book
    paginate_by = 3


class BookDetailView(generic.DetailView):
    """Класс для обображения информации о конкретной книге"""
    model = Book


class AuthorListView(generic.ListView):
    """обощенный класс для вывода списка авторов"""
    model = Author
    paginate_by = 4


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

    # количество посещений этого view, посчитанное в переменной session
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Отрисовка HTML шаблона index.html с данными
    # внутри переменной context
    return render(request, 'index.html',
                  context={'num_books': num_books,
                           'num_instances': num_instances,
                           'num_instances_available': num_instances_available,
                           'num_authors': num_authors,
                           'num_visits': num_visits},
                  )


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Универсальный класс представления списка книг,
     находящихся в заказе у текущего пользователя"""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(
            status__exact='2').order_by('due_back')
