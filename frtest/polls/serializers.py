from abc import ABC

from .models import Poll, Question, PollsUser, Answer
from rest_framework import serializers


class QuestionTypeChoiceField(serializers.ChoiceField):

    def to_representation(self, value):
        return self._choices[value]

    def to_internal_value(self, data):
        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail("invalid_choice", input=data)


class QuestionSerializer(serializers.ModelSerializer):
    question_type = QuestionTypeChoiceField(choices=Question.CHOICES)

    class Meta:
        model = Question
        fields = ["id", "text", "question_type"]


class PollSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, required=False)

    class Meta:
        model = Poll
        fields = ["id", "title", "description", "start", "end", "questions"]
        read_only_fields = ["start"]
        depth = 1


class AnswerSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    answer = serializers.CharField(allow_blank=False, max_length=500)

    def save_answer(self, question: Question):
        user = PollsUser.objects.create_or_find(self.data.get("user_id"))
        Answer.objects.create(
            question=question,
            user=user,
            answer=self.data.get("answer")
        )

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
