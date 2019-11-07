from django.core.paginator import Paginator
from django.conf import settings


def getPages(request, objectlist):
    """get the paginator"""
    currentPage = request.GET.get('page', 1)

    paginator = Paginator(objectlist, settings.EACHPAGE_NUMBER)
    objectlist = paginator.page(currentPage)

    return paginator, objectlist