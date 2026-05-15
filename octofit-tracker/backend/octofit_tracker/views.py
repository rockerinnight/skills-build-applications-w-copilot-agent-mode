from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pymongo import MongoClient
from bson import ObjectId
import os

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['octofit_db']

# Helper function to convert MongoDB documents and ObjectIds
def serialize_doc(doc):
	if doc is None:
		return None
	if isinstance(doc, dict):
		result = {}
		for key, value in doc.items():
			if isinstance(value, ObjectId):
				result[key] = str(value)
			elif isinstance(value, dict):
				result[key] = serialize_doc(value)
			elif isinstance(value, list):
				result[key] = [serialize_doc(item) if isinstance(item, dict) else (str(item) if isinstance(item, ObjectId) else item) for item in value]
			else:
				result[key] = value
		return result
	return doc

class UserViewSet(viewsets.ViewSet):
	def list(self, request):
		users = list(db.users.find({}))
		return Response([serialize_doc(u) for u in users])
    
	def retrieve(self, request, pk=None):
		user = db.users.find_one({'_id': ObjectId(pk)})
		return Response(serialize_doc(user) if user else {})

class TeamViewSet(viewsets.ViewSet):
	def list(self, request):
		teams = list(db.teams.find({}))
		return Response([serialize_doc(t) for t in teams])
    
	def retrieve(self, request, pk=None):
		team = db.teams.find_one({'_id': ObjectId(pk)})
		return Response(serialize_doc(team) if team else {})

class ActivityViewSet(viewsets.ViewSet):
	def list(self, request):
		activities = list(db.activities.find({}))
		return Response([serialize_doc(a) for a in activities])
    
	def retrieve(self, request, pk=None):
		activity = db.activities.find_one({'_id': ObjectId(pk)})
		return Response(serialize_doc(activity) if activity else {})

class LeaderboardViewSet(viewsets.ViewSet):
	def list(self, request):
		leaderboard = list(db.leaderboard.find({}))
		return Response([serialize_doc(l) for l in leaderboard])
    
	def retrieve(self, request, pk=None):
		entry = db.leaderboard.find_one({'_id': ObjectId(pk)})
		return Response(serialize_doc(entry) if entry else {})

class WorkoutViewSet(viewsets.ViewSet):
	def list(self, request):
		workouts = list(db.workouts.find({}))
		return Response([serialize_doc(w) for w in workouts])
    
	def retrieve(self, request, pk=None):
		workout = db.workouts.find_one({'_id': ObjectId(pk)})
		return Response(serialize_doc(workout) if workout else {})

@api_view(['GET'])
def api_root(request, format=None):
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
