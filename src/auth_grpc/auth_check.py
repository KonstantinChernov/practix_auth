from concurrent import futures

import grpc
import jwt

import auth_pb2
import auth_pb2_grpc

from core.wsgi_app import app
from models.accounts import User
from models.rbac import Role


class CheckAuth(auth_pb2_grpc.AuthServicer):

    def CheckRole(self, request, context):

        with app.app_context():
            if request.access_token and request.roles:
                return auth_pb2.CheckRoleResponse(result=False, status="Error")
            decoded = jwt.decode(request.access_token, options={"verify_signature": False})
            login = decoded.get('sub', None)
            if not login:
                return auth_pb2.CheckRoleResponse(result=False, status="Error")
            user = User.query.filter_by(login=login).first()
            role = Role.query.filter_by(id=user.role_id).first()

            if user and role and role.name in request.roles.split():
                return auth_pb2.CheckRoleResponse(result=True, status="Success")

            return auth_pb2.CheckRoleResponse(result=False, status="Success")


if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_AuthServicer_to_server(CheckAuth(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()