from polls.models import Question, Poll, PollsUser, Answer


def run():
    Question.objects.all().delete()
    Poll.objects.all().delete()
    PollsUser.objects.all().delete()
    Answer.objects.all().delete()
