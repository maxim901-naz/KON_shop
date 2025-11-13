from .models import Category

def categories(request):
    """
    Делает список категорий доступным во ВСЕХ шаблонах
    """
    return {
        'categories': Category.objects.filter(is_active=True)
    }