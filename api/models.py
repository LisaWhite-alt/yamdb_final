from datetime import date

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from rest_framework.exceptions import ValidationError


class Roles(models.TextChoices):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"


class User(AbstractUser):
    email = models.EmailField(
        max_length=200, unique=True, verbose_name="Электронная потча",
    )
    role = models.CharField(
        max_length=15, choices=Roles.choices, default=Roles.USER,
        verbose_name="Роль",
    )
    bio = models.TextField(
        db_column="description",
        max_length=2000,
        blank=True,
        verbose_name="Биография"
    )
    confirmation_code = models.CharField(
        max_length=70, unique=True, blank=True, null=True, editable=False,
        verbose_name="Код подтверждения",
    )

    @property
    def is_admin(self):
        return self.role == Roles.ADMIN or self.is_staff

    @property
    def is_moderator(self):
        return self.role == Roles.MODERATOR

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(
        "Категория",
        max_length=50,
        unique=True,
    )
    slug = models.SlugField(
        max_length=50, unique=True,
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ("-name",)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        "Жанр",
        max_length=50,
        unique=True,
    )
    slug = models.SlugField(
        max_length=50, unique=True
    )

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ("-id",)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        "Название произведения",
        max_length=200,
        db_index=True
    )
    year = models.PositiveSmallIntegerField(
        "Год публикации",
        blank=False,
        validators=[year_validate],
    )
    category = models.ForeignKey(
        Category,
        db_column="category",
        related_name="titles",
        verbose_name="Категория",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    raiting = models.IntegerField(
        "Рейтинг",
        null=True,
        blank=True,
    )
    description = models.CharField(
        "Описание",
        max_length=200,
        null=True,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name="titles",
        verbose_name="Жанр",
        blank=True,
        db_index=True
    )

    class Meta:
        verbose_name = "Название произведения"
        verbose_name_plural = "Названия произведений"
        ordering = ("-year",)

    def __str__(self):
        return (
            f"Название {self.name}, год публикации {self.year}, жанр "
            f"{self.genre}, краткое описание: {self.description}, "
            f"из категории = {self.category}"
        )

    def year_validate(self):
        year_now = date.today().year
        if not (1 <= self.year <= year_now):
            raise ValidationError(
                f"Год указан некорректно! "
                f"Допускается укзание года от 1 до {year_now} (включительно)"
            )


class Review(models.Model):
    text = models.TextField(
        "Текст отзыва",
    )
    pub_date = models.DateTimeField(
        "Дата публикации отзыва",
        auto_now_add=True,
        db_index=True
    )
    score = models.PositiveSmallIntegerField(
        "Рейтинг",
        validators=[
            MinValueValidator(1, message="Минимальный рейтинг: 1"),
            MaxValueValidator(10, message="Максимальный рейтинг: 10")
        ],
        help_text="Оценка произведения от 1 до 10"
    )
    author = models.ForeignKey(
        User,
        db_column="author",
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор отзыва"
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Оцениваемое произведение"
    )

    class Meta:
        verbose_name = "Обзор"
        verbose_name_plural = "Обзоры"
        ordering = ("-pub_date",)

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    text = models.TextField("Текст комментария", )
    pub_date = models.DateTimeField(
        "Дата публикации комментария",
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        db_column="author",
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор комментария"
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Комментируемый отзыв"
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ("-pub_date",)

    def __str__(self):
        return self.text[:15]
