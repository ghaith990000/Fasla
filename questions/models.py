from django.db import models

# Create your models here.
class Category(models.Model):
    name_en = models.CharField(max_length=255, default="Sample Category")
    name_ar = models.CharField(max_length=255, default="فئة تجريبية")

    def __str__(self):
        return self.name_en

class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    text_en = models.TextField(default="Sample question")
    text_ar = models.TextField(default="سؤال تجريبي")

    difficulty = models.CharField(
        max_length=20, 
        choices=[("easy", "Easy"), ("medium", "Medium"), ("hard", "Hard")],
    )

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    text_en = models.TextField(default="Sample answer")
    text_ar = models.TextField(default="إجابة تجريبية")
    is_correct = models.BooleanField(default=False)