from rest_framework import serializers

from api.models import Category, Comment, Genre, Review, Title, User


class EmailConfirmationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username", "role", "email", "first_name", "last_name",
            "bio"
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        exclude = ("title",)

    def validate(self, attrs):
        is_review_exist = Review.objects.filter(
            author=self.context["request"].user,
            title=self.context["view"].kwargs.get("title_id")).exists()
        if is_review_exist and self.context["request"].method == "POST":
            raise serializers.ValidationError(
                "Вы уже оставляли отзыв на это произведение")
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )

    class Meta:
        fields = ("id", "text", "author", "pub_date")
        model = Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug",)
        model = Category
        lookup_field = "slug"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug",)
        model = Genre
        lookup_field = "slug"


class TitleListSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            "id", "name", "year", "rating", "description", "genre", "category"
        )
        model = Title


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field="slug",
        queryset=Genre.objects.all()
    )

    class Meta:
        fields = ("__all__")
        model = Title
