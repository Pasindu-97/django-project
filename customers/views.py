from django.db.models import Q
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from customers.authentication import FirebaseAuthentication
from customers.models import Customer, CustomerOrder
from customers.serializers import CustomerSerializer, CustomerOrderSerializer


class CustomerViewSet(ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()


class CustomerOrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [FirebaseAuthentication]
    serializer_class = CustomerOrderSerializer
    queryset = CustomerOrder.objects.all()


def home(request):
    search_query = request.GET.get('search', '')
    customers = Customer.objects.filter(
        Q(first_name__icontains=search_query) |
        Q(last_name__icontains=search_query)
    )
    return render(request, 'customers/home_page.html', {'customers': customers})


def advertisement(request):
    return render(request, 'customers/advertisements.html')
