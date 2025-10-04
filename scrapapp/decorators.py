from django.shortcuts import redirect
from django.contrib import messages

# def role_required(allowed_roles=[]):
#     """
#     Usage: @role_required(['admin', 'dealer'])
#     Only allows users with specified roles to access the view.
#     """
#     def decorator(view_func):
#         def wrapper(request, *args, **kwargs):
#             user_role = request.session.get('user_role')
#             if not user_role:
#                 messages.error(request, "Login required to access this page.")
#                 return redirect("login")
#             if user_role not in allowed_roles:
#                 messages.error(request, "You do not have permission to access this page.")
#                 return redirect("profile")
#             return view_func(request, *args, **kwargs)
#         return wrapper
#     return decorator

def role_required(allowed_roles=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            user_role = request.session.get('user_role')
            if not user_role:
                messages.error(request, "Login required to access this page.")
                return redirect("login")
            if user_role not in allowed_roles:
                messages.error(request, "You do not have permission to access this page.")
                # Redirect based on role
                if user_role == "admin":
                    return redirect("admin_dashboard")
                elif user_role == "dealer":
                    return redirect("dealer_dashboard")
                elif user_role == "seller":
                    return redirect("seller_dashboard")
                else:
                    return redirect("login")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator



def anonymous_required(view_func):
    """
    If user is already logged in, redirect to their dashboard.
    """
    def wrapper(request, *args, **kwargs):
        user_role = request.session.get('user_role')
        if user_role:
            # Redirect based on role
            if user_role == "admin":
                return redirect("admin_dashboard")
            elif user_role == "dealer":
                return redirect("dealer_dashboard")
            else:
                return redirect("seller_dashboard")
        return view_func(request, *args, **kwargs)
    return wrapper
