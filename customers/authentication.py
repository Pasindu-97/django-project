import base64
import hashlib
import hmac

import boto3
import firebase_admin
from botocore.exceptions import ClientError
from django.conf import settings
from django.contrib.auth.models import User
from firebase_admin import auth, credentials
from rest_framework.authentication import BaseAuthentication

from customers import exceptions

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


client_id = "3jqqvqvven1qi3f7bd4f2m23r"


class CognitoAuthentication(BaseAuthentication):
    def calculate_secret_hash(self, client_id, client_secret, username):
        message = username + client_id
        secret_hash = hmac.new(
            str(client_secret).encode("utf-8"), msg=str(message).encode("utf-8"), digestmod=hashlib.sha256
        ).digest()
        secret_hash_base64 = base64.b64encode(secret_hash).decode()
        return secret_hash_base64

    def initiate_auth(self, username, password):
        cidp = boto3.client(
            "cognito-idp",
            region_name="us-west-1",
            aws_access_key_id="AKIA3JEGTLJ2K7DOFSMP",
            aws_secret_access_key="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",
        )
        try:
            response = cidp.initiate_auth(
                AuthFlow="USER_PASSWORD_AUTH",
                AuthParameters={
                    "USERNAME": username,
                    "PASSWORD": password,
                },
                ClientId=client_id,
            )
            return response
        except ClientError as err:
            print(err)
            return "User does not exist"

    def sign_up(self, username, password):
        cidp = boto3.client(
            "cognito-idp",
            region_name="us-west-1",
            aws_access_key_id="AKIA3JEGTLJ2K7DOFSMP",
            aws_secret_access_key="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",
        )

        secret_hash = self.calculate_secret_hash(client_id, "", username)
        response = cidp.sign_up(
            ClientId=client_id,
            SecretHash=secret_hash,
            Username=username,
            Password=password,
        )

        return response

    def delete_user(self, token):
        cidp = boto3.client(
            "cognito-idp",
            region_name="us-west-1",
            aws_access_key_id="AKIA3JEGTLJ2K7DOFSMP",
            aws_secret_access_key="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",
        )
        response = cidp.delete_user(AccessToken=token)
        return response
