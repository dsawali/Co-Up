from django.db import models
from django.conf import settings
from ..users.models import User

# Create your models here.
class Contact(models.Model):
	"""
	The relationship between users is a many-to-many relationship. 
	A user can follow multiple users, and can be followed back 
	by multiple users. We'll be creating a many-to-many relationships
	 with an intermediary model i.e. Contact. 
	"""
	user_from = models.ForeignKey(User,related_name='rel_from_set')
	user_to = models.ForeignKey(User, related_name='rel_to_set')
	created = models.DateTimeField(auto_now_add=True, db_index=True)

	class Meta:
		ordering = ('-created',)

	def __str__(self):
		return '{} follows {}'.format(self.user_from, self.user_to)


# Add following field to User dynamically - monkey patching the user model
"""
Note: Symmetircal is set to False - this means if user 1 follows user 2 -
user2 will not follow back user 1 automatically.
"""
User.add_to_class('following',
                  models.ManyToManyField('self',
                                         through=Contact,
                                         related_name='followers',
                                         symmetrical=False))