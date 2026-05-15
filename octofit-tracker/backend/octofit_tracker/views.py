import os

from bson import ObjectId
from bson.errors import InvalidId
from rest_framework import permissions, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Activity, Leaderboard, Team, User, Workout
from .serializers import (
    ActivitySerializer,
    LeaderboardSerializer,
    TeamSerializer,
    UserSerializer,
    WorkoutSerializer,
)


class StandardPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100


class SafeRetrieveModelViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardPagination

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_value = self.kwargs.get(self.lookup_field)

        try:
            lookup_object_id = ObjectId(lookup_value)
        except (InvalidId, TypeError):
            raise NotFound()

        instance = queryset.filter(pk=lookup_object_id).first()
        if instance is None:
            raise NotFound()

        self.check_object_permissions(self.request, instance)
        return instance


class UserViewSet(SafeRetrieveModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TeamViewSet(SafeRetrieveModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class ActivityViewSet(SafeRetrieveModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer


class LeaderboardViewSet(SafeRetrieveModelViewSet):
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer


class WorkoutViewSet(SafeRetrieveModelViewSet):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer


class ApiRootView(APIView):
    """Read-only API root – explicitly restricted to safe HTTP methods only."""
    http_method_names = ['get', 'head', 'options']
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        codespace_name = os.environ.get('CODESPACE_NAME')
        if codespace_name:
            base_url = f"https://{codespace_name}-8000.app.github.dev"
        else:
            base_url = "http://localhost:8000"

        return Response({
            'users': f"{base_url}/api/users/",
            'teams': f"{base_url}/api/teams/",
            'activities': f"{base_url}/api/activities/",
            'leaderboard': f"{base_url}/api/leaderboard/",
            'workouts': f"{base_url}/api/workouts/",
        })
