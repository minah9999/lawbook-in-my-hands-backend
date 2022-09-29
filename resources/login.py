from flask import request
from flask_restful import Resource
from http import HTTPStatus
from db.db import get_mysql_connection
from flask_jwt_extended import create_access_token


# 로그인 api
class LoginResource(Resource):
    def post(self):
        data = request.get_json()

        # 필수값이 있는지 체크
        if 'loginId' not in data or 'password' not in data:
            return {'status': HTTPStatus.BAD_REQUEST, 'message': '필수값이 없습니다.'}, HTTPStatus.BAD_REQUEST

        # 데이터베이스에서 로그인아이디로 사용자 조회
        connection = get_mysql_connection()
        cursor = connection.cursor()
        query = """select * from user where loginId = %s;"""
        param = (data['loginId'], )

        cursor.execute(query, param)
        result = cursor.fetchone()
        print(result)

        cursor.close()
        connection.close()

        # 해당 사용자가 존재하는지 확인
        if result is None:
            return {'status': HTTPStatus.BAD_REQUEST, 'message': '사용자가 존재하지 않습니다.'}, HTTPStatus.BAD_REQUEST

        # 존재하면 request 비밀번호와 db 비밀번호를 비교
        user_id = result[0]
        user_password = result[4]

        if data['password'] != user_password:
            return {'status': HTTPStatus.BAD_REQUEST, 'message': '비밀번호가 옳바르지 않습니다.'}, HTTPStatus.BAD_REQUEST

        # jwt로 인증 토큰 생성
        access_token = create_access_token(identity=user_id)

        # 클라이언트에 토큰 보내기
        return {'user_id' : user_id, 'access_token' : access_token}, HTTPStatus.OK