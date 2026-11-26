from rest_framework.permissions import BasePermission

from account.models import Profile


class HasRole(BasePermission):

    allowed_roles = []

    def has_permission(self, request, view):

        user = request.user

        if not user or not user.is_authenticated:
            return False

        try:
            profile = user.profile
        except Profile.DoesNotExist:
            return False

        return profile.role in self.allowed_roles
    
    
    
class IsSuperAdmin(HasRole):
    allowed_roles = ["SUPERADMIN"]


class IsAdmin(HasRole):
    allowed_roles = ["SUPERADMIN", "ADMIN"]


class IsOperator(HasRole):
    allowed_roles = ["SUPERADMIN", "ADMIN", "OPERATEUR"]


class IsVictim(HasRole):
    allowed_roles = ["VICTIM"]
    
    
class IsVictimOrOperator(HasRole):
    allowed_roles = [
        "SUPERADMIN",
        "ADMIN",
        "OPERATEUR",
        "VICTIM",
    ]
