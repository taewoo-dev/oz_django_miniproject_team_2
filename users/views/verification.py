from typing import Any

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()


# 이메일 인증 확인하는 로직(GenericAPIView or APIView)
class EmailVerificationView(GenericAPIView):  # type: ignore
    # 이메일 인증링크 클릭 -> 해당 URL에 포함된 토큰 -> 유저 확인 -> 활성화/
    #                                                -> 이미 활성화 된 유저 -> 오류메세지, 오류상태코드 반환
    #                                     ->유효하지 않은 토큰이거나 유저조회 실패 -> 오류메세지, 오류상태코드 반환
    def get(self, request: Request) -> Response:
        token = request.query_params.get("token")

        try:
            access_token = AccessToken(token)
            user_id = access_token["user_id"]
            user = User.objects.get(id=user_id)

            if not user.is_active:
                user.is_active = True
                user.save()
                return Response({"message": "이메일 인증이 완료되었습니다."}, status=status.HTTP_200_OK)
            return Response({"message": "이미 인증된 계정입니다."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "유효하지 않은 토큰입니다."}, status=status.HTTP_400_BAD_REQUEST)


# 토큰이 만료 처리
# 토큰 발급시 만료 시간 설정 -> settings에 되어 있는데 여기다 하는 게 더 나은가?
# 이메일 재발송 -> 새로운 인증메일 요청할 수 있게 하기
# 보안을 많이 신경 써야하는 부분인데 보안에 대해 잘 모르겠음
# 저번에 대정님이 Exception as e에 들어갈 예외들을 따로 폴더를 만들어 두셨는데 그것도 생각해보기
