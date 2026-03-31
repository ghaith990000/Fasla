from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="categories")

question_list = QuestionViewSet.as_view({
    "get": "list"
})

question_random = QuestionViewSet.as_view({
    "get": "random"
})

question_answer = QuestionViewSet.as_view({
    "post": "answer"
})


urlpatterns = [
    path("", include(router.urls)),

    path("questions/", question_list),
    path("questions/random/", question_random),
    path("questions/answer/", question_answer),
]