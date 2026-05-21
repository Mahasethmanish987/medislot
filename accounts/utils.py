
from accounts.models import User


def user_redirect_based_on_role(user: User) -> str: 
    if user.role == User.DOCTOR:
        return 'accounts:doctor_dashboard'
    elif user.role == User.PATIENT:
        return 'accounts:user_dashboard'
    else:
        return 'myapp:index'