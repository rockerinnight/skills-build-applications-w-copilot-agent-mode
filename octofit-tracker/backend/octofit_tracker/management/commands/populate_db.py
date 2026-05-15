from django.core.management.base import BaseCommand

from octofit_tracker.models import Activity, Leaderboard, Team, User, Workout


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete existing OctoFit records before inserting sample data.',
        )

    def handle(self, *args, **options):
        if options['reset']:
            Activity.objects.all().delete()
            Leaderboard.objects.all().delete()
            Workout.objects.all().delete()
            Team.objects.all().delete()
            User.objects.all().delete()

        users_data = [
            {"name": "Superman", "email": "superman@dc.com", "team": "DC"},
            {"name": "Batman", "email": "batman@dc.com", "team": "DC"},
            {"name": "Wonder Woman", "email": "wonderwoman@dc.com", "team": "DC"},
            {"name": "Iron Man", "email": "ironman@marvel.com", "team": "Marvel"},
            {"name": "Captain America", "email": "cap@marvel.com", "team": "Marvel"},
            {"name": "Black Widow", "email": "widow@marvel.com", "team": "Marvel"},
        ]

        users_by_name = {}
        for user_data in users_data:
            user, _ = User.objects.update_or_create(
                email=user_data['email'],
                defaults={'name': user_data['name'], 'team': user_data['team']},
            )
            users_by_name[user.name] = user

        for team_name in ['Marvel', 'DC']:
            members = User.objects.filter(team=team_name).values_list('_id', flat=True)
            Team.objects.update_or_create(
                name=team_name,
                defaults={'members': [str(member_id) for member_id in members]},
            )

        activities_data = [
            {"user": "Superman", "activity": "Running", "duration": 30},
            {"user": "Batman", "activity": "Cycling", "duration": 45},
            {"user": "Iron Man", "activity": "Swimming", "duration": 60},
        ]
        for activity_data in activities_data:
            Activity.objects.update_or_create(
                user=users_by_name[activity_data['user']],
                activity=activity_data['activity'],
                defaults={'duration': activity_data['duration']},
            )

        leaderboard_data = [
            {"user": "Superman", "points": 100},
            {"user": "Iron Man", "points": 120},
        ]
        for entry_data in leaderboard_data:
            Leaderboard.objects.update_or_create(
                user=users_by_name[entry_data['user']],
                defaults={'points': entry_data['points']},
            )

        workouts_data = [
            {"name": "Morning Cardio", "suggested_for": "Marvel"},
            {"name": "Strength Training", "suggested_for": "DC"},
        ]
        for workout_data in workouts_data:
            Workout.objects.update_or_create(
                name=workout_data['name'],
                defaults={'suggested_for': workout_data['suggested_for']},
            )

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
