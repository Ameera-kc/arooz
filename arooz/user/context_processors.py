from user.models import Category, HeaderFlash, Product, SubCategory


def main_context(request):
    headerflash = HeaderFlash.objects.last()
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    products = Product.objects.all()

    if request.user.is_anonymous:

        return {
            "headerflash": headerflash,
            "categories": categories,
            "subcategories": subcategories,
            "products": products,
            "status": 0,
        }
    else:
        return {
            "headerflash": headerflash,
            "categories": categories,
            "subcategories": subcategories,
            "products": products,
            "status": 1,
        }
