from rest_framework.permissions import BasePermission

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

class IsAuthShelter(BasePermission):
    """
    활성화된 보호소 담당자만 접근할 수 있는 권한이 주어집니다.
    """
    def has_permission(self, request, view):
        return bool(not request.user.is_anonymous and request.user.role == "2" and request.user.is_active)


class IsAuthShelterOrReadOnly(BasePermission):
    """
    활성화된 보호소 담당자이면 글을 쓸 수 있는 권한이 주어집니다.
    """

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return bool(request.method in SAFE_METHODS)
        else:
            return bool(request.user.role == "2" and request.user.is_active)

