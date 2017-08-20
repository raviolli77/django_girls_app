from django.db import models
from django.utils import timezone
# Create your models here.

class Post(models.Model):
	"""
	Model instantiates a Post model, includes attributes described 
	below and two functions utilizing the self concept 
	Read this article for more explanation: 
	https://pythontips.com/2013/08/07/the-self-variable-in-python-explained/
	
	Attributes:
	* author: We're using the auth.User model where we're utilizing 
	the concept of foreign keys to join the two tables on the key 
	that is the authorized user in our web app. 
	* title: Utilizing the string functionality where we have to 
	set a max_length, in this case we're setting our length to a maximum 
	of 200. 
	* text: Recommended functionality for larger bodies of text, hence
	we are utilizing it for our text. 
	* created_date: Date field created to show when the post instance
	was created, self-explained.
	* published_date: Date field created to show when the post was published
	i.e. viewable on the web app. 
	"""
	author = models.ForeignKey('auth.User')
	title = models.CharField(max_length=200)
	text = models.TextField()
	created_date = models.DateTimeField(
		default=timezone.now)
	published_date = models.DateTimeField(
		blank=True, 
		null=True)

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def __str__(self):
		return self.title		

