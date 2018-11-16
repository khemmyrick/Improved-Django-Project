from menu import views


def index(request):
    return views.menu_list(request)
