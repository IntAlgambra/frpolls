from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from auth.auth import create_session, AccessError
from auth.serializers import LoginSerializer


@api_view(["POST"])
@csrf_exempt
def login(request: Request) -> Response:
    if request.method == "POST":
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer)
            print(serializer.data)
            try:
                token = create_session(
                    username=serializer.data.get("username"),
                    password=serializer.data.get("password")
                )
                return Response(
                    data={"token": token}
                )
            except AccessError:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

