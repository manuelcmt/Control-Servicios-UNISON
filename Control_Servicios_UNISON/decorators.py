from django.shortcuts import redirect

def para_no_autenticados(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('inicio')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def usuarios_admitidos(roles_admitidos=['']):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            grupo = None
            if request.user.groups.exists():
                grupo = request.user.groups.all()[0].name

            if grupo in roles_admitidos:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('inicio')
        return wrapper_func

    return decorator
