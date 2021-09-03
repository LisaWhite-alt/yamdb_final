from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    auth_token,
    CategoryViewSet,
    CommentViewSet,
    email_confirmation,
    GenreViewSet,
    ReviewViewSet,
    TitlesViewSet,
    UserViewSet,
)

router_v1 = DefaultRouter()
router_v1.register("genres", GenreViewSet, basename="genre")
router_v1.register("categories", CategoryViewSet, basename="category")
router_v1.register("titles", TitlesViewSet, basename="title")
router_v1.register("users", UserViewSet, basename="user")
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews",
    ReviewViewSet,
    basename="review"
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comment"
)

auth_paths = [
    path("email/", email_confirmation, name="confirmation_code"),
    path("token/", auth_token, name="auth_token")
]

urlpatterns = [
    path("v1/", include(router_v1.urls)),
    path("v1/auth/", include(auth_paths)),
]
