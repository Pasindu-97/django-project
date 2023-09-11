from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from customers.authentication import FirebaseAuthentication
# from customers.authentication import FirebaseAuthentication
from customers.models import Customer, CustomerOrder
from customers.serializers import CustomerSerializer, CustomerOrderSerializer


class CustomerViewSet(ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()


class CustomerOrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    """Here just add FirebaseAuthentication class in authentication_classes"""
    authentication_classes = [FirebaseAuthentication]
    serializer_class = CustomerOrderSerializer
    queryset = CustomerOrder.objects.all()