from django.contrib import admin

from .models import Author, Genre, Language, Status, Book, BookInstance


# Register your models here.
# Определение к классу администратор
class AuthorAdmin(admin.ModelAdmin):
    """автор"""
    list_display = ('last_name', 'first_name', 'date_of_birth',
                    'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth',
                                          'date_of_death')]


class BookInstanceInline(admin.TabularInline):
    """сведения о конкретных экземплярах книги"""
    model = BookInstance


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """книга"""
    list_display = ('title', 'genre', 'language', 'display_author')
    list_filter = ('genre', 'author')
    inlines = [BookInstanceInline]


@admin.register(BookInstance)
class BookIstanceAdmin(admin.ModelAdmin):
    """экземпляр книги"""
    list_filter = ('book', 'status')
    fieldsets = (
        ('Экземпляр книги', {
            'fields': ('book', 'imprint', 'inv_nom')
        }),
        ('Статус и окончание его действия', {
            'fields': ('status', 'due_back')
        }),
    )


# регистрируем классы администратора
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Status)
