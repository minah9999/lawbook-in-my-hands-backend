from flask import Flask
from flask_jwt_extended import *
from flask_restful import Api
from config.config import Config
from resources.consult_mecab import ConsultResource, ConsultGetResource
from resources.logout import jwt_blocklist
from resources.scrap import ScrapResource, ScrapListResource
from resources.test import TestResource
from resources.signup import SignupResource, LoginidResource
from resources.login import LoginResource
from resources.user import UserResource, PasswordResource

# Flask 객체 인스턴스 생성
application = Flask(__name__)

# jwt 환경 설정
jwt = JWTManager(application)
# 로그인/로그아웃 관리를 위한s jwt 설정
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return jti in jwt_blocklist


# 접속 url 설정
@application.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


# 1. 환경변수 설정
application.config.from_object(Config)
# 2. api 설정
api = Api(application)  # API 설정을 한다. 괄호 안에는 위에서 받은 플라스크 변수
# 3. 경로(Path)와 리소스(Resource)를 연결 한다.
api.add_resource(TestResource, '/test')

api.add_resource(SignupResource, '/signup')
api.add_resource(LoginidResource, '/loginid/<string:loginid>')
api.add_resource(LoginResource, '/login')

api.add_resource(ConsultResource, '/consult')
api.add_resource(ConsultGetResource, '/consult/<int:consult_id>')

api.add_resource(ScrapResource, '/scrap/<int:case_serial_id>')
api.add_resource(ScrapListResource, '/scrap')

api.add_resource(UserResource, '/user/profile')
api.add_resource(PasswordResource, '/user/password')

if __name__ == '__main__':
    application.run(debug=False, host='0.0.0.0')
