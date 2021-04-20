from django.http import HttpResponse, JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from .models import Poll, Question, PollsUser
from .serializers import PollSerializer, QuestionSerializer, AnswerSerializer
from auth.auth import auth


@api_view(["GET", "POST"])
@csrf_exempt
def polls_list(request: Request) -> Response:
    if request.method == "GET":
        polls = Poll.objects.all()
        if not auth(request):
            polls = polls.filter(end__gte=timezone.now())
        serializer = PollSerializer(polls, many=True)
        return Response(data={"polls": serializer.data})

    elif request.method == "POST":
        if not auth(request):
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = PollSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@csrf_exempt
def single_poll(request: Request, pk: int) -> Response:

    if not auth(request):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    try:
        active_poll = Poll.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = PollSerializer(active_poll)
        return Response(serializer.data)

    elif request.method == "DELETE":
        active_poll.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == "PUT":
        serializer = PollSerializer(active_poll, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
@csrf_exempt
def questions(request: Request, pk: int) -> Response:
    if not auth(request):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    try:
        active_poll = Poll.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        poll_questions = active_poll.questions.all()
        serializer = QuestionSerializer(poll_questions, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            question = Question.objects.create(
                serializer.data.get("text"),
                serializer.data.get("question_type"),
                active_poll
            )
            return Response(QuestionSerializer(question).data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@csrf_exempt
def answer_question(request: Request, question_id: int) -> Response:
    try:
        question = Question.objects.get(pk=question_id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "POST":
        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save_answer(question=question)
            except IntegrityError:
                return Response({"error": "question already been answered"},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@csrf_exempt
def user_answers(request: Request, user_id: int) -> Response:
    try:
        user = PollsUser.objects.get(user_id=user_id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        user_polls = Poll.objects.filter(questions__answer__user=user)
        # data = {
        #     poll.title: poll.get_user_answers(user) for poll in user_polls
        # }
        data = {
            "answers": [
                {
                    "poll": {
                        "id": poll.pk,
                        "title": poll.title
                    },
                    "answers": [
                        poll.get_user_answers(user)
                    ]
                }
            ] for poll in user_polls
        }
        return Response(data=data, status=status.HTTP_200_OK)
