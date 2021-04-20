import random
from datetime import timedelta

from django.utils import timezone

from polls.models import Poll, Question


def populate():
    """
    Наполняет БД рандомными опросами с рандомными ответами
    """
    for i in range(5):
        title = "Really important poll number {}".format(i)
        start = timezone.now() - timedelta(days=random.randint(1, 5))
        end = timezone.now() + timedelta(days=random.randint(1, 5))
        description = "Lorem Ipsum Datum Si vi pasem really cool"
        poll = Poll.objects.create(
            title=title,
            start=start,
            end=end,
            description=description
        )
        for j in range(random.randint(2, 7)):
            text = "so meaningful question number {}".format(j)
            question_type = random.choice(["text", "single_select", "several_select"])
            Question.objects.create(
                text=text,
                question_type=question_type,
                poll=poll
            )


def run():
    populate()
