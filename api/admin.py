from django.contrib import admin

from api.models import Category, Comment, Genre, Review, Title, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "bio", "email")
    search_fields = ("username",)
    empty_value_display = "-пусто-"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "text",
        "pub_date",
        "score",
        "author",
        "title"
    )
    search_fields = ("text",)
    list_filter = ("title", "author", "score")
    empty_value_display = "-пусто-"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "pub_date", "author", "review")
    search_fields = ("text",)
    list_filter = ("review", "author")
    empty_value_display = "-пусто-"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("pk", "name",)
    ordering = ("-pk",)
    search_fields = ("name",)
    empty_value_display = "-пусто-"


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("pk", "name",)
    ordering = ("-pk",)
    search_fields = ("name",)
    empty_value_display = "-пусто-"


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "year",
        "raiting",
        "category",
    )
    ordering = ("-pk",)
    search_fields = ("name",)
    list_filter = ("category", "year", "raiting", "genre")
    empty_value_display = "-пусто-"
