import django_filters
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from rest_framework import status, filters
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from customers.authentication import FirebaseAuthentication
from customers.filters import ItemFilter
from customers.forms import GroupForm
from customers.models import Customer, CustomerOrder, AdvertisementItem, Item, Category, Order, CustomImage
from customers.serializers import CustomerSerializer, CustomerOrderSerializer, ItemSerializer, ItemViewSerializer, \
    CategorySerializer, OrderSerializer, CustomImageSerializer

from wagtail.users.views.groups import GroupViewSet as WagtailGroupViewSet


class CustomerViewSet(ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()


class CustomerOrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerOrderSerializer
    queryset = CustomerOrder.objects.all()


def home(request):
    search_query = request.GET.get('search', '')
    customers = Customer.objects.filter(
        Q(first_name__icontains=search_query) |
        Q(last_name__icontains=search_query)
    )
    return render(request, 'customers/home_page.html', {'customers': customers})


def view_orders(request, customer_id):
    customer = Customer.objects.get(id=customer_id)

    orders = CustomerOrder.objects.filter(customer=customer)

    context = {
        'customer': customer,
        'orders': orders,
        'title': f"Orders of {customer.first_name}",
        'subtitle': 'Subtitle Here',
        'description': 'Description Here',
    }

    return render(request, 'customers/customer_orders.html', context)


def advertisement_detail(request, advertisement_id):
    advertisement = get_object_or_404(AdvertisementItem, pk=advertisement_id)
    context = {
        'advertisement': advertisement,
    }
    return render(request, 'customers/advertisement_detail.html', context)


def advertisement_list(request):
    advertisements = AdvertisementItem.objects.all()
    context = {
        'advertisements': advertisements,
    }
    return render(request, 'customers/advertisements.html', context)


class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = ItemFilter
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return ItemViewSerializer
        return ItemSerializer

    @action(methods=["GET"], detail=True, url_path="toggle_visibility")
    def toggle_visibility(self, request, pk, **kwargs):
        try:
            item = Item.objects.get(id=pk)
        except Item.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        item.visible = not item.visible
        item.save()
        return Response({"message": "Item visibility toggled successfully"})

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class CustomImageViewSet(ModelViewSet):
    queryset = CustomImage.objects.all()
    serializer_class = CustomImageSerializer


class GroupViewSet(WagtailGroupViewSet):
    def get_form_class(self, for_update=False):
        return GroupForm
