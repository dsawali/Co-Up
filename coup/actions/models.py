from django.db import models
from ..users.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# creat your models here
class Action(models.Model):
	"""
	This model tracks the actions of an individual user -
	we are using thi model to keep track of users actions in
	the follower system.
	"""
	user = models.ForeignKey(User,
		related_name='actions',
		db_index=True)
	verb = models.CharField(max_length=255)
	target_ct = models.ForeignKey(ContentType,
		blank=True,
		null=True,
		related_name='target_obj')
	target_id = models.PositiveIntegerField(null=True,
		blank=True,
		db_index=True)
	target = GenericForeignKey('target_ct', 'target_id')
	created = models.DateTimeField(auto_now_add=True,
		db_index=True)

	class Meta:
		ordering = ('-created',)
