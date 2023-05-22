from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView, UpdateView, DeleteView

from .forms import AuthorsForm
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


def authors_add(request):
    """получение данных из бд и загрузка шаблона authors_add.html"""
    author = Author.objects.all()
    authorsform = AuthorsForm()
    return render(request, 'catalog/authors_add.html',
                  {'form': authorsform, 'author': author})


def create(request):
    """Сохранение данных об авторах в БД"""

    if request.method == 'POST':
        author = Author()
        author.first_name = request.POST.get('first_name')
        author.last_name = request.POST.get('last_name')
        author.date_of_birth = request.POST.get('date_of_birth')
        author.date_of_death = request.POST.get('date_of_death')
        author.save()
        return HttpResponseRedirect('/authors_add/')


def delete(request, id):
    """Удаление авторов из БД"""
    try:
        author = Author.objects.get(id=id)
        author.delete()
        return HttpResponseRedirect('/authors_add/')
    except Author.DoesNotExist:
        return HttpResponseNotFound('<h2>Автор не найден</h2>')


def edit_1(request, id):
    """Изменение данных в БД"""
    author = Author.objects.get(id=id)

    if request.method == 'POST':
        author.first_name = request.POST.get('first_name')
        author.last_name = request.POST.get('last_name')
        author.date_of_birth = request.POST.get('date_of_birth')
        author.date_of_death = request.POST.get('date_of_death')
        author.save()
        return HttpResponseRedirect('/authors_add/')
    else:
        return render(request, 'catalog/edit_1.html',
                      {'author': author})


class BookCreate(CreateView):
    """Класс для создания книг"""
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')


class BookUpdate(UpdateView):
    """Класс для редактирования книг"""
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')


class BookDelete(DeleteView):
    """Класс для удаления книг"""
    model = Book
    success_url = reverse_lazy('books')
