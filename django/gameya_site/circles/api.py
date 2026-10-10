"""The REST API: viewsets for gameyas and members. Module 06."""

from rest_framework import filters, viewsets  # noqa: F401  (you will use it)
from rest_framework.authentication import TokenAuthentication  # noqa: F401
from rest_framework.decorators import action  # noqa: F401
from rest_framework.exceptions import ValidationError  # noqa: F401
from rest_framework.pagination import PageNumberPagination  # noqa: F401
from rest_framework.permissions import SAFE_METHODS, BasePermission  # noqa: F401
from rest_framework.response import Response  # noqa: F401

# Add the app's imports as you need them, for example:
#   from .models import Gameya, Member
#   from .serializers import GameyaSerializer, MemberSerializer
# Do not import a name before it exists: a failed import here breaks every view in this file.

# TODO 18: a permission class, a subclass of BasePermission. Anyone may read (the SAFE_METHODS).
#          Only a logged-in user with is_staff=True may write. Override has_permission(), which
#          sees the request and the view. Give the class any name you like.
# TODO 19: a pagination class, a subclass of PageNumberPagination, with page_size = 2.
# TODO 20: class GameyaViewSet(viewsets.ModelViewSet), with:
#          queryset = all gameyas, serializer_class = GameyaSerializer,
#          authentication_classes = [TokenAuthentication], your permission class,
#          your pagination class, filter_backends with SearchFilter and OrderingFilter,
#          search_fields = name, and ordering_fields = name and weeks.
#          Add a detail action named members (@action(detail=True, methods=["get"])). It
#          returns the members of this gameya with MemberSerializer, not paginated.
# TODO 21: class MemberViewSet(viewsets.ModelViewSet), with serializer_class = MemberSerializer,
#          the same authentication and permission classes as TODO 20, and get_queryset().
#          get_queryset() returns the members with their gameya loaded (select_related). If the
#          query string has ?gameya=<id>, it keeps only that gameya's members. A value that is
#          not a whole number, or is outside 1 to 2**31 - 1, is a 400 (raise ValidationError).
#          Read it with self.request.query_params.get("gameya"). Convert it with int() inside
#          try/except ValueError. Do not use isdigit(): it accepts characters, such as "²",
#          that int() rejects.

# Module 11: ownership. An organiser changes their own gameya and its members.
# TODO 40: a permission class IsStaffOrOrganiser(BasePermission), used in place of the module 06
#          permission on both viewsets. Anyone may read. Creating a gameya or a member needs a
#          logged-in staff user. Changing or deleting needs staff, or the organiser of that gameya.
#          has_permission() is the first check: it sees the request and the view, so use
#          view.action to tell a create from an update. has_object_permission() is the second
#          check, and it sees the object: a Gameya, or a Member through its gameya field.
#          Read the lesson, section 4.
#          Also add JWTAuthentication (from rest_framework_simplejwt.authentication) to the
#          authentication_classes of both viewsets, after TokenAuthentication. Section 3 explains.
# TODO 41: MemberViewSet.perform_update(self, serializer). A member may move to another gameya
#          only when the user is staff, or organises the new gameya. The new gameya is in
#          serializer.validated_data under "gameya", and only when the request sent one. Raise
#          PermissionDenied (from rest_framework.exceptions) when the move is not allowed.
#          Otherwise call serializer.save(). Checking the member alone is not enough: section 4.
