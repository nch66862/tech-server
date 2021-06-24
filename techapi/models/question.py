from django.db import models


class Question(models.Model):

    type = models.ForeignKey("Type", on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    required = models.BooleanField(default=False)

    # @property
    # def  question_display_text(self):
    #     return self.__question_display_text

    # @question_display_text.setter
    # def question_display_text(self):

    #     self.__question_display_text = self.question_text