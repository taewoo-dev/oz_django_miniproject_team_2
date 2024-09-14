from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import SignupSerializer
from users.utils.email_utils import send_verification_email


class SignUpAPIView(GenericAPIView):  # type: ignore
    serializer_class = SignupSerializer

    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            # 이메일 인증 토큰
            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)  # type: ignore
            verification_url = request.build_absolute_uri(reverse("email-verify") + f"?token={token}")

            # 이메일 발송
            send_verification_email(user, verification_url)  # type: ignore

            return Response(
                {"message": "회원가입이 완료되었습니다.이메일을 확인해 인증해주세요."}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
