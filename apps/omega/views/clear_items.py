from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.omega.services.vznab_stock_service import fetch_stock_tree_with_row_numbers
from apps.declaration.models import DeclaredItem, Declaration
from apps.sez.models import ClearedItem
from apps.omega.serializers.clear_items import ClearItemsRequestSerializer


class ClearItemsView(APIView):
    def post(self, request):
        serializer = ClearItemsRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_number = serializer.validated_data["order_number"]
        model = serializer.validated_data["model"]
        quantity = serializer.validated_data["quantity"]
        is_tv = serializer.validated_data.get("is_tv", False)

        fetched_items = fetch_stock_tree_with_row_numbers(order_number, model, quantity, is_tv)

        result = []
        for item in fetched_items:
            row_number = item["row_number"]
            nom_reg = item["nom_reg"]
            abs_qty = item["absolute_quantity"]
            item_name = item["name"]

            try:
                declared_item = DeclaredItem.objects.select_related("declaration").get(
                    ordinal_number=row_number,
                    declaration__declaration_number=nom_reg
                )
            except DeclaredItem.DoesNotExist:
                result.append({
                    "item": item_name,
                    "expected": abs_qty,
                    "actual": 0,
                    "missing": abs_qty,
                    "message": "Declared item not found"
                })
                continue

            available = declared_item.available_quantity or 0.0
            to_clear = min(abs_qty, available)

            declared_item.available_quantity = available - to_clear
            declared_item.save(update_fields=['available_quantity'])

            # Сохраняем списание, как ранее
            if to_clear > 0:
                ClearedItem.objects.create(
                    product_id=int(model),
                    declared_item_id=declared_item,
                    quantity=to_clear
                )

            result.append({
                "item": item_name,
                "expected": abs_qty,
                "actual": to_clear,
                "missing": max(0.0, abs_qty - to_clear)
            })

        return Response(result, status=status.HTTP_200_OK)

