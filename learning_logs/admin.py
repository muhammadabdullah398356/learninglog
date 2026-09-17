from django.contrib import admin

# Register your models here.
# When you define models for an app, Django makes it easy for you to work 
# with your models through the admin site. A site’s administrators use the admin site, not a site’s general users. 

from learning_logs.models import Topic,Entry  # This code imports the model we want to register, Topic
admin.site.register(Topic) #  to tell Django to manage our model throughthe admin site.
admin.site.register(Entry)