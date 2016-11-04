from __future__ import unicode_literals

from django.db import models


class Query(models.Model):
	"""
	Model for Facebook query
	"""
	query = models.CharField(max_length=100)
	created_at = models.DateField(auto_now_add=True)
	run_at = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return self.query


class Post(models.Model):
	"""
	Model for Facebook Post
	"""
	status_id = models.CharField(max_length=50, primary_key=True)
	query = models.ForeignKey(Query)
	status_message = models.TextField()
	link_name = models.CharField(max_length=500, blank=True, null=True)
	status_type = models.CharField(max_length=50, blank=True, null=True)
	status_link = models.CharField(max_length=200, blank=True, null=True)
	status_published = models.DateTimeField()
	num_reactions = models.IntegerField()
	num_comments = models.IntegerField()
	num_shares = models.IntegerField()
	num_likes = models.IntegerField()
	num_loves = models.IntegerField()
	num_wows = models.IntegerField()
	num_hahas = models.IntegerField()
	num_sads = models.IntegerField()
	num_angrys = models.IntegerField()

	def __str__(self):
		return self.status_id
		

class Comment(models.Model):
	"""
	Model for Facebook comments
	"""
	comment_id = models.CharField(max_length=50, primary_key=True)
	post = models.ForeignKey(Post)
	parent_id = models.CharField(max_length=50, blank=True, null=True)
	comment_message = models.TextField()
	comment_author = models.CharField(max_length=10)
	comment_published = models.DateTimeField()
	comment_likes = models.IntegerField()

	def __str__(self):
		return self.comment_id
