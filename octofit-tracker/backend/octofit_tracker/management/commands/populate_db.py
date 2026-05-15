from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection
from bson import ObjectId

# Sample data for population
def get_sample_data():
    users = [
        {"_id": ObjectId(), "name": "Superman", "email": "superman@dc.com", "team": "DC"},
        {"_id": ObjectId(), "name": "Batman", "email": "batman@dc.com", "team": "DC"},
        {"_id": ObjectId(), "name": "Wonder Woman", "email": "wonderwoman@dc.com", "team": "DC"},
        {"_id": ObjectId(), "name": "Iron Man", "email": "ironman@marvel.com", "team": "Marvel"},
        {"_id": ObjectId(), "name": "Captain America", "email": "cap@marvel.com", "team": "Marvel"},
        {"_id": ObjectId(), "name": "Black Widow", "email": "widow@marvel.com", "team": "Marvel"},
    ]
    teams = [
        {"_id": ObjectId(), "name": "Marvel", "members": [u["_id"] for u in users if u["team"] == "Marvel"]},
        {"_id": ObjectId(), "name": "DC", "members": [u["_id"] for u in users if u["team"] == "DC"]},
    ]
    activities = [
        {"_id": ObjectId(), "user_id": users[0]["_id"], "activity": "Running", "duration": 30},
        {"_id": ObjectId(), "user_id": users[1]["_id"], "activity": "Cycling", "duration": 45},
        {"_id": ObjectId(), "user_id": users[3]["_id"], "activity": "Swimming", "duration": 60},
    ]
    leaderboard = [
        {"_id": ObjectId(), "user_id": users[0]["_id"], "points": 100},
        {"_id": ObjectId(), "user_id": users[3]["_id"], "points": 120},
    ]
    workouts = [
        {"_id": ObjectId(), "name": "Morning Cardio", "suggested_for": "Marvel"},
        {"_id": ObjectId(), "name": "Strength Training", "suggested_for": "DC"},
    ]
    return users, teams, activities, leaderboard, workouts

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        db = connection.cursor().db_conn
        users, teams, activities, leaderboard, workouts = get_sample_data()

        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Insert data
        db.users.insert_many(users)
        db.teams.insert_many(teams)
        db.activities.insert_many(activities)
        db.leaderboard.insert_many(leaderboard)
        db.workouts.insert_many(workouts)

        # Create unique index on email
        db.users.create_index([("email", 1)], unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
