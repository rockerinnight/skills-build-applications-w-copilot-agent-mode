from rest_framework import serializers
from .models import User, Team, Activity, Leaderboard, Workout
from bson import ObjectId

class ObjectIdField(serializers.Field):
	def to_representation(self, value):
		return str(value)
	def to_internal_value(self, data):
		return ObjectId(data)

class UserSerializer(serializers.ModelSerializer):
	_id = ObjectIdField(read_only=True)
	class Meta:
		model = User
		fields = ['_id', 'name', 'email', 'team']

class TeamSerializer(serializers.ModelSerializer):
	_id = ObjectIdField(read_only=True)
	class Meta:
		model = Team
		fields = ['_id', 'name', 'members']

class ActivitySerializer(serializers.ModelSerializer):
	_id = ObjectIdField(read_only=True)
	user = serializers.CharField(source='user.name', read_only=True)
	class Meta:
		model = Activity
		fields = ['_id', 'user', 'activity', 'duration']

class LeaderboardSerializer(serializers.ModelSerializer):
	_id = ObjectIdField(read_only=True)
	user = serializers.CharField(source='user.name', read_only=True)
	class Meta:
		model = Leaderboard
		fields = ['_id', 'user', 'points']

class WorkoutSerializer(serializers.ModelSerializer):
	_id = ObjectIdField(read_only=True)
	class Meta:
		model = Workout
		fields = ['_id', 'name', 'suggested_for']
