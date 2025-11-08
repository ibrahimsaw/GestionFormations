from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied



def access_required(roles=None, permission=None):
    """
    Décorateur flexible pour protéger les vues (FBV & CBV)

    UTILISATIONS :

    1️⃣ Vérifier seulement que l'utilisateur est connecté :
        @access_required()
        def my_view(request):

    2️⃣ Autoriser uniquement certains rôles :
        @access_required(roles=['ADMIN', 'AGENT'])
        def my_view(request):

    3️⃣ Vérifier une permission Django :
        @access_required(permission='Utilisateur.add_utilisateur')
        def my_view(request):

    4️⃣ Vérifier *rôle + permission* :
        @access_required(roles=['ADMIN'], permission='Utilisateur.change_utilisateur')
        def my_view(request):

    5️⃣ Sur une vue basée classe (CBV) :
        @access_required(roles=['ETUDIANT'])
        class TableauEtudiantView(TemplateView):
            template_name = "Utilisateur/Etudiant/tableau.html"
    """
    
    def decorator(view_func):

        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):

            # Vérifie connexion
            if not request.user.is_authenticated:
                return redirect('login')

            # Vérifie rôle
            if roles is not None and getattr(request.user, 'role', None) not in roles:
                raise PermissionDenied

            # Vérifie permission Django
            if permission is not None and not request.user.has_perm(permission):
                raise PermissionDenied

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    def wrapper(target):
        # Si c'est une Classe (CBV)
        if isinstance(target, type):
            target.dispatch = method_decorator(login_required(login_url='login'))(target.dispatch)
            target.dispatch = method_decorator(decorator)(target.dispatch)
            return target

        # Sinon : Vue fonctionnelle (FBV)
        return login_required(login_url='login')(decorator(target))

    return wrapper
