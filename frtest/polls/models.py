from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from .managers import QuestionManager, PollsUserManager, AnswerManager


# Create your models here.

class Poll(models.Model):
    """
    Модель опроса
    """
    title = models.CharField(max_length=150, unique=True)
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(null=True)
    description = models.TextField(default="")

    def get_user_answers(self, user):
        """
        Возвращает ответы пользователя на вопросы
        """
        answers = [
            {
                "question_id": question.pk,
                "question": question.text,
                "answer": question.get_user_answer(user).answer
            } for question in self.questions.filter(answer__user=user)
        ]
        return answers


class Question(models.Model):
    TYPES = {
        "text": 1,
        "single_select": 2,
        "several_select": 3
    }
    CHOICES = [(value, key) for key, value in TYPES.items()]
    text = models.TextField()

    question_type = models.IntegerField(choices=CHOICES,
                                        default=1)
    poll = models.ForeignKey(to=Poll,
                             related_name="questions",
                             on_delete=models.CASCADE)

    objects = QuestionManager()

    def get_user_answer(self, user):
        try:
            answer = self.answer.get(user=user)
            return answer
        except ObjectDoesNotExist:
            return None


class PollsUser(models.Model):
    user_id = models.IntegerField(primary_key=True)
    objects = PollsUserManager()


class Answer(models.Model):
    class Meta:
        unique_together = ("user", "question")
    answer = models.TextField()
    user = models.ForeignKey(to=PollsUser,
                             on_delete=models.CASCADE,
                             related_name="answer")
    question = models.ForeignKey(to=Question,
                                 on_delete=models.CASCADE,
                                 related_name="answer")
    objects = AnswerManager()
