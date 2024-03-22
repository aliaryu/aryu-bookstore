from .models import Category


def categories(request):
    categories = Category.objects.filter(cat_parent__isnull=True).prefetch_related("category_set")
    return {"categories": categories}
