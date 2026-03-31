from rest_framework import serializers
from .models import Category, Question, Answer

class AnswerSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        fields = ['id', 'text']

    def get_text(self, obj):
        lang = self.context.get("lang", "en")
        return obj.text_en if lang == "en" else obj.text_ar

class QuestionSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ["id", "text", "difficulty", "answers"]

    def get_text(self, obj):
        lang = self.context.get("lang", "en")
        return obj.text_en if lang == "en" else obj.text_ar

class CategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name"]

    def get_name(self, obj):
        lang = self.context.get("lang", "en")
        return obj.name_en if lang == "en" else obj.name_ar