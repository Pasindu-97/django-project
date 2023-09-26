import boto3
import firebase_admin
from botocore.exceptions import ClientError
from django.conf import settings
from django.contrib.auth.models import User
from firebase_admin import auth, credentials
from rest_framework import authentication
from rest_framework.authentication import BaseAuthentication, get_authorization_header

from customers import exceptions
from exampleProject.settings import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    CLIENT_ID,
    REGION_NAME,
    USER_POOL_ID,
)

if settings.FIREBASE_PRIVATE_KEY is not None and isinstance(settings.FIREBASE_PRIVATE_KEY, str):
    private_key = settings.FIREBASE_PRIVATE_KEY.replace("\\n", "\n")
else:
    private_key = None

"""SETUP FIREBASE CREDENTIALS"""
cred = credentials.Certificate(
    {
        "type": settings.FIREBASE_ACCOUNT_TYPE,
        "project_id": settings.FIREBASE_PROJECT_ID,
        "private_key_id": settings.FIREBASE_PRIVATE_KEY_ID,
        "private_key": private_key,
        "client_email": settings.FIREBASE_CLIENT_EMAIL,
        "client_id": settings.FIREBASE_CLIENT_ID,
        "auth_uri": settings.FIREBASE_AUTH_URI,
        "token_uri": settings.FIREBASE_TOKEN_URI,
        "auth_provider_x509_cert_url": settings.FIREBASE_AUTH_PROVIDER_X509_CERT_URL,
        "client_x509_cert_url": settings.FIREBASE_CLIENT_X509_CERT_URL,
    }
)
default_app = firebase_admin.initialize_app(cred)
"""FIREBASE AUTHENTICATION"""


class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            raise exceptions.NoAuthToken("No auth token provided")
        id_token = auth_header.split(" ").pop()
        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception:
            raise exceptions.InvalidAuthToken("Invalid auth token")
        if not id_token or not decoded_token:
            return None
        try:
            uid = decoded_token.get("uid")
        except Exception:
            raise exceptions.FirebaseError()
        user, created = User.objects.get_or_create(username=uid)
        return user, None


# ----------------------COGNITO--------------------------------------------

client_id = CLIENT_ID
region_name = REGION_NAME
aws_access_key_id = AWS_ACCESS_KEY_ID
aws_secret_access_key = AWS_SECRET_ACCESS_KEY
user_pool_id = USER_POOL_ID

cidp = boto3.client(
    "cognito-idp",
    region_name=region_name,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)


def initiate_auth(username, password):
    try:
        response = cidp.initiate_auth(
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": username,
                "PASSWORD": password,
            },
            ClientId=client_id,
        )
        print("User Access Tokens: ", response)
        return response
    except ClientError as err:
        return str(err)


def create_user(username):
    try:
        cidp.admin_create_user(
            UserPoolId=user_pool_id,
            Username=username,
            TemporaryPassword="Userpassword1@",
        )
    except ClientError as err:
        return str(err)


def delete_user(username):
    try:
        cidp.admin_delete_user(
            UserPoolId=user_pool_id,
            Username=username,
        )
    except ClientError as err:
        return str(err)


def set_password(username, password):
    try:
        cidp.admin_set_user_password(UserPoolId=user_pool_id, Username=username, Password=password, Permanent=True)
        return "Set the new password"
    except ClientError as err:
        return str(err)


class CognitoAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = get_authorization_header(request).split()
        if not token:
            return None

        try:
            user = cidp.get_user(AccessToken=token)
        except User.DoesNotExist:
            raise exceptions.InvalidAuthToken("No such user")

        return user, None
