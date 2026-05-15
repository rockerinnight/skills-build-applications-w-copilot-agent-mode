from djongo import models

class User(models.Model):
	_id = models.ObjectIdField(primary_key=True, editable=False)
	name = models.CharField(max_length=100)
	email = models.EmailField(unique=True)
	team = models.CharField(max_length=50)
	def __str__(self):
		return self.name

class Team(models.Model):
	_id = models.ObjectIdField(primary_key=True, editable=False)
	name = models.CharField(max_length=100)
	members = models.ArrayField(model_container=User, blank=True)
	def __str__(self):
		return self.name

class Activity(models.Model):
	_id = models.ObjectIdField(primary_key=True, editable=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	activity = models.CharField(max_length=100)
	duration = models.IntegerField()
	def __str__(self):
		return f"{self.user.name} - {self.activity}"

class Leaderboard(models.Model):
	_id = models.ObjectIdField(primary_key=True, editable=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	points = models.IntegerField()
	def __str__(self):
		return f"{self.user.name} - {self.points}"

class Workout(models.Model):
	_id = models.ObjectIdField(primary_key=True, editable=False)
	name = models.CharField(max_length=100)
	suggested_for = models.CharField(max_length=50)
	def __str__(self):
		return self.name
