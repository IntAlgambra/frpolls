from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import Poll, Question, PollsUser

from django.core.exceptions import ObjectDoesNotExist

from django.db import models


class QuestionTypeError(Exception):
    pass


class QuestionManager(models.Manager):

    def create(self, text: str, question_type: str, poll: Poll) -> Question:
        question_type_identifier = self.model.TYPES.get(question_type)
        if not question_type_identifier:
            raise QuestionTypeError()
        question = self.model(
            text=text,
            question_type=question_type_identifier,
            poll=poll
        )
        question.save()
        return question


class PollsUserManager(models.Manager):

    def create_or_find(self, user_id):
        """
        Возвращает пользователя опроса по переданному id. Если
        пользователя с таким id нет, то сохдает его и возвращает
        """
        try:
            user = self.get(user_id=user_id)
            return user
        except ObjectDoesNotExist:
            user = self.model(user_id=user_id)
            user.save()
            return user


class AnswerManager(models.Manager):

    def create(self, question, user, answer):
        answer_object = self.model(
            answer=answer,
            question=question,
            user=user
        )
        answer_object.save()
        return answer_object
