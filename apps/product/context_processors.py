from .models import Category
import json


def categories(request):
    categories = Category.objects.filter(cat_parent__isnull=True).prefetch_related("category_set")
    return {"categories": categories}


def red_dot_cart(request):
    if (cart:=request.COOKIES.get("cart")):
        cart = json.loads(cart)
        if cart:
            result = True
        else:
            result = False
    return {"red_dot_cart": result}
