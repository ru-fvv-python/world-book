from django.db import models

# Create your models here.
from django.urls import reverse


class Genre(models.Model):
    """Представляет собой список с жанрами книг"""
    name = models.CharField(max_length=200,
                            help_text='Введите жанр книги',
                            verbose_name='Жанр книги')

    def __str__(self):
        """Возвращает имя жанра"""
        return self.name


class Language(models.Model):
    """Справочник языков"""
    name = models.CharField(max_length=20,
                            help_text='Введите жанр книги',
                            verbose_name='Жанр книги')

    def __str__(self):
        """Возвращает язык книги"""
        return self.name


class Author(models.Model):
    """Представляет собой сравочник, в котором хранится информация об авторах
     книг"""
    first_name = models.CharField(max_length=100,
                                  help_text='Введите имя автора',
                                  verbose_name='Имя автора')
    last_name = models.CharField(max_length=100,
                                 help_text='Введите фамилию автора',
                                 verbose_name='Фамилия автора')
    date_of_birth = models.DateField(help_text='Введите дату рождения',
                                     verbose_name='Дата рождения',
                                     null=True)
    date_of_death = models.DateField(help_text='Введите дату смерти',
                                     verbose_name='Дата смерти',
                                     null=True)

    def __str__(self):
        """Возвращает фамилию автора"""
        return self.last_name


class Book(models.Model):
    """Информация о книгах"""
    title = models.CharField(max_length=200,
                             help_text='Введите название книги',
                             verbose_name='Название книги')
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE,
                              help_text='Выберите жанр книги',
                              verbose_name='Жанр книги', null=True)
    language = models.ForeignKey('Language', on_delete=models.CASCADE,
                                 help_text='Выберите язык книги',
                                 verbose_name='Язык книги', null=True)
    author = models.ManyToManyField('Author',
                                    help_text='Выберите автора книги',
                                    verbose_name='Автор книги')
    summary = models.TextField(max_length=1000,
                               help_text='Введите краткое описание книги',
                               verbose_name='Аннотация книги')
    isbn = models.CharField(max_length=13,
                            help_text='Должно содержать 13 символов',
                            verbose_name='ISBN книги')

    def __str__(self):
        """Возвращает название книги"""
        return self.title

    def get_absolute_url(self):
        """Возвращает URL-адрес для доступа к определенному экземпляру книги"""
        return reverse('book-detail', args=[str(self.id)])


class Status(models.Model):
    """Статус книги"""
    name = models.CharField(max_length=20,
                            help_text='Введите статус экземпляра книги',
                            verbose_name='Статус экземпляра книги')

    def __str__(self):
        """Возвращает значение статуса экземпляра книги"""
        return self.name


class BookInstance(models.Model):
    """модель для хранения отдельных экземпляров книг и их статусов """
    book = models.ForeignKey('Book', on_delete=models.CASCADE,
                             null=True)
    inv_nom = models.CharField(max_length=20, null=True,
                               help_text='Введите инвентарный номер экземпляра',
                               verbose_name='Инвентарный номер')
    imprint = models.CharField(max_length=200,
                               help_text='Введите издательство и год выпуска',
                               verbose_name='Издательство')
    status = models.ForeignKey('Status', on_delete=models.CASCADE,
                               null=True,
                               help_text='Изменить состояние экземпляра',
                               verbose_name='Статус экземпляра книги')
    due_back = models.DateField(null=True, blank=True,
                                help_text='Введите конец срока статуса',
                                verbose_name='Дата окончания статуса')

    def __str__(self):
        """Представляет объект Istance"""
        return '%s %s %s' % (self.inv_nom, self.book, self.status)
