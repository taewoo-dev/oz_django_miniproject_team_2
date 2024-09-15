from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import LoginSerializer


class LoginAPIView(GenericAPIView):  # type: ignore
    serializer_class = LoginSerializer

    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]  # 시리얼라이저에서 인증된 사용자 가져오기
        refresh = RefreshToken.for_user(user)  # 가져온다음 refresh token 생성

        access_token = refresh.access_token  # type: ignore

        response = Response({"message": "로그인이 성공했습니다."}, status=status.HTTP_200_OK)

        # cookies에 access token 저장
        response.set_cookie(
            key="access_token",
            value=str(refresh.access_token),  # type: ignore
            httponly=True,  # 자바스크립트 접근 불가
            secure=True,  # HTTPS에서만 전송
            samesite="Lax",  # CSRF 방지용
            max_age=3600,  # 1시간동안 쿠키 유지
        )
        # cookies에 refresh token 저장
        response.set_cookie(key="refresh_token", value=str(refresh), httponly=True, secure=True, samesite="Lax")
        return response


# 인증된 사용자만 접근할 수 있도록 하기 위해 필요
class ProtectedAPIView(GenericAPIView):  # type: ignore
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        return Response(status=204)  # 204 = 요청 성공 but 응답데이터는 없음 No Content


class LogoutAPIView(GenericAPIView):  # type: ignore
    def post(self, request: Request) -> Response:
        try:
            refresh_token = request.COOKIES.get("refresh_token")
            token = RefreshToken(refresh_token)  # type: ignore
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
