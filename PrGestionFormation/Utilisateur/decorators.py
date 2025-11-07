from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

def access_required(roles=None, permission=None):
    """
    Décorateur flexible pour FBV et CBV :
    
    - Sans paramètre : vérifie seulement la connexion
      @access_required()
      
    - Avec roles : vérifie que l'utilisateur a un des rôles
      @access_required(roles=['ADMIN', 'AGENT'])
      
    - Avec permission : vérifie une permission Django
      @access_required(permission='Utilisateur.add_utilisateur')

    - Avec les deux
      @access_required(roles=['ADMIN'], permission='Utilisateur.change_utilisateur')
    """
    def decorator(view):
        # Cas CBV
        if isinstance(view, type):
            # Appliquer le décorateur sur la méthode dispatch de la classe
            view.dispatch = method_decorator(decorator)(view.dispatch)
            return view
        
        # Cas FBV
        @wraps(view)
        @login_required(login_url='login')
        def _wrapped_view(request, *args, **kwargs):
            # Vérification des rôles
            if roles is not None and getattr(request.user, 'role', None) not in roles:
                return redirect('custom_403')
            
            # Vérification de permission
            if permission is not None and not request.user.has_perm(permission):
                return redirect('custom_403')

            return view(request, *args, **kwargs)
        
        return _wrapped_view

    return decorator
