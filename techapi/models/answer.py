from django.db import models


class Answer(models.Model):

    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    answer_value = models.CharField(max_length=200)
