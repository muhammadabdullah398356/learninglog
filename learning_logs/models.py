from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#A module called models is being imported for us, and we’re being invited to create models of our own. A model tells Django how to work with the data 
#that will be stored in the app. Code-wise, a model is just a class; it has attributes and methods,

#The command makemigrations tells Django to figure out how to modify the database so it can store the data associated with any new models we’ve 
#defined. The output here shows that Django has created a migration file called 0001_initial.py. This migration will create a table for the model Topic in the database. 
# talking about ( python manage.py makemigrations learning_log )

class Topic(models.Model):
    # Topic is a model that inherits from Django's built-in Model class.
    # A model represents data that will be stored in the database.

    """A topic the user is learning about."""

    # Stores the name/text of the topic.
    # CharField is used for a relatively short piece of text.
    # max_length=200 means the topic can contain up to 200 characters.
    text = models.CharField(max_length=200)

    # Stores the date and time when this Topic object was created.
    # auto_now_add=True automatically sets the current date/time
    # when the object is created.
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        # Returns a string representation of the Topic object.
        # For example, if text = "Python", printing the object gives "Python".
        return self.text


class Entry(models.Model):
    # Entry also inherits from Django's built-in Model class.
    # An Entry represents something specific learned about a Topic.

    """Something specific learned about a topic."""

    # Creates a relationship between Entry and Topic.
    # Each Entry belongs to one Topic.
    # on_delete=models.CASCADE means:
    # if a Topic is deleted, its related Entries are deleted too.
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE) # Entry → belongs to → Topic

    # TextField is used for larger amounts of text.
    # This is where the actual information learned about the topic is stored.
    text = models.TextField()

    # Automatically stores the date and time when the Entry is created.
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:  # Django lets you provide extra settings/options about how the model behaves or is displayed.
        # Django normally uses "Entrys" as the plural.
        # We tell Django to use "entries" instead.
        verbose_name_plural = 'entries'  # Entry  → one  it is about calss
                                         # Entries → many

        def __str__(self):
        # Returns the first 50 characters of the Entry's text.
        # "..." is added so it is clear that the text has been shortened.
            if len(self.text)<50:
                return self.text()
            else:
                return self.text[:50] + "..."

