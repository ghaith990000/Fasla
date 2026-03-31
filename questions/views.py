from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import random
from .models import Category, Question, Answer
from .serializers import CategorySerializer, QuestionSerializer

# Create your views here.
def get_lang(request):
    return request.query_params.get("lang", "en")

class QuestionViewSet(ViewSet):
    # GET /questions/?category=1
    def list(self, request):
        lang = get_lang(request)
        
        category_id = request.query_params.get("category")
        queryset = Question.objects.all()

        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        serializer = QuestionSerializer(queryset, many=True, context={"lang": lang})
        return Response(serializer.data)

    # GET /questions/random/?category=1&limit=5
    def random(self, request):
        lang = get_lang(request)

        category_id = request.query_params.get("category")
        limit = int(request.query_params.get("limit", 5))

        queryset = Question.objects.all()

        queryset = Question.objects.filter(category_id=category_id)

        questions = list(queryset)
        random.shuffle(questions)

        selected = questions[:limit]

        serializer = QuestionSerializer(selected, many=True, context={"lang": lang})
        return Response(serializer.data)

    # POST /questions/answer/
    def answer(self, request):
        question_id = request.data.get("question_id")
        answer_id = request.data.get("answer_id")

        answer = get_object_or_404(Answer, id=answer_id, question_id=question_id)

        return Response({
            "correct": answer.is_correct
        })

class CategoryViewSet(ViewSet):
    def list(self, request):
        lang = get_lang(request)
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True, context={"lang": lang})
        return Response(serializer.data)