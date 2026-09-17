from django.urls import path
from . import views

app_name = 'learning_logs'

urlpatterns = [
    path('', views.index, name='index'),  # to index template then it inherits base.html by this base shows and then index shows
    path('topics/', views.topics, name='topics'),   # goes to views then to topic from there we get data from our models then go to toipcs .html
    path('topics/<int:topic_id>/', views.topic, name='topic'),  
    path('new_topic/', views.new_topic, name ='new_topic'),
    path('new_entry/<int:topic_id>/', views.new_entry, name = 'new_entry'),
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
]


"""That's why name='new_topic' in urls.py is so important: it is the name Django uses to find this URL when you write {% url 'learning_logs:new_topic' %}."""