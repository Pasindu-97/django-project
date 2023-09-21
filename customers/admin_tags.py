from django.http import JsonResponse

from customers.models import Item


def toggle_visibility(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
        item.visibility = not item.visibility
        item.save()

        response_data = {
            "success": True,
            "visibility": item.visibility,
        }

    except Item.DoesNotExist:
        response_data = {
            "success": False,
            "error_message": "Item not found",
        }

    return JsonResponse(response_data)
