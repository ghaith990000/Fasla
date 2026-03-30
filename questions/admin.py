from django.contrib import admin
from .models import Category, Question, Answer

# Register your models here.
class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "category", "difficulty")
    list_filter = ("category", "difficulty")
    search_fields = ("text",)

    inlines = [AnswerInline]

admin.site.register(Category)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)