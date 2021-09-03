from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets, filters
from rest_framework.decorators import api_view, action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from api.filters import TitleFilter
from api.models import Category, Genre, Review, Title, User
from api.permissions import (
    IsAdmin,
    IsAdminOrReadOnly,
    IsAuthorOrAdminOrModeratorOrReadOnly
)
from api.serializers import (
    AuthTokenSerializer,
    CategorySerializer,
    CommentSerializer,
    EmailConfirmationCodeSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleListSerializer,
    TitleCreateSerializer,
    UserSerializer
)


class CreateDestroyListViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    pass


@api_view(["POST"])
def email_confirmation(request):
    serializer = EmailConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get("email")
    user = get_object_or_404(User, email=email)
    confirmation_code = default_token_generator.make_token(user)
    user.confirmation_code = confirmation_code
    user.save()

    mail_subject = "yaMDB: Код подтверждения email"
    message = f"Код подтверждения: {confirmation_code}"
    user.email_user(mail_subject, message)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def auth_token(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get("email")
    confirmation_code = serializer.data.get("confirmation_code")
    user = get_object_or_404(User, email=email)

    if user.confirmation_code == confirmation_code:
        token = AccessToken.for_user(user)
        return Response({"token": f"{token}"}, status=status.HTTP_200_OK)
    return Response(
        "Неправильный код подтвержения",
        status=status.HTTP_400_BAD_REQUEST
    )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("id")
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    lookup_field = "username"

    @action(
        methods=["GET", "PATCH"],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        if request.method == "GET":
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)

        serializer = UserSerializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthorOrAdminOrModeratorOrReadOnly
    ]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        queryset = title.reviews.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title, id=self.kwargs.get("title_id"))
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthorOrAdminOrModeratorOrReadOnly
    ]

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get("review_id"),
            title_id=self.kwargs.get("title_id")
        )
        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(
                Review,
                id=self.kwargs.get("review_id"),
                title_id=self.kwargs.get("title_id")
            )
        )


class TitlesViewSet(ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg("reviews__score")).order_by("-year")
    filter_backends = (DjangoFilterBackend,)
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,
    ]
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH"]:
            return TitleCreateSerializer
        return TitleListSerializer


class CategoryViewSet(CreateDestroyListViewSet):
    queryset = Category.objects.all().order_by("id")
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    pagination_class = PageNumberPagination
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,
    ]
    search_fields = ["name"]
    lookup_field = "slug"


class GenreViewSet(CreateDestroyListViewSet):
    queryset = Genre.objects.all().order_by("id")
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    pagination_class = PageNumberPagination
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,
    ]
    search_fields = ["name", ]
    lookup_field = "slug"
