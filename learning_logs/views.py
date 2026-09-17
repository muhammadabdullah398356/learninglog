from django.shortcuts import render
from .models import Topic,Entry
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import TopicForm,EntryForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404

def index(request):
    """The home page for Learning Log"""
    return render(request, 'index.html')

@login_required
def topics(request):
    """Show all topics."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'topics.html', context)

@login_required
def topic(request, topic_id):
    """Show a single topic and all its entries."""
    topic = Topic.objects.get(id=topic_id)  # we use get() to retrieve the topic, just as we did in the Django shell. 
     # Make sure the topic belongs to the current user.
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added') # we get the entries associated with this topic, and we order them according to date_added: the minus sign in front of date_added sorts the results in reverse order, which will display the most recent entries first. 
    context = {'topic': topic, 'entries': entries} # We store the topic and entries in the context dictionary
    return render(request, 'topic.html', context) #  send context to the template topic.html    ,  "Render topic.html, and give it the data stored inside context."


#topics.html
#    │
#    │ User clicks "Django"
#    ↓
#URL: /topics/2/
#    │
#    ↓
#views.py
#    │
#    │ topic_id = 2
#    ↓
#Get Topic 2
#    │
#    ↓
#Get Topic 2's entries
#    │
#    ↓
#topic.html
#    │
#    ↓
#Display Django + its entries
@login_required
def new_topic(request): #  The request contains information about the user's request,
    
    """Add a new topic."""
    """When the user fills out the form and presses Submit, the form sends the data using POST."""
    """GETUsually means:"I want to view this page."For example, the user clicks:New Topic The browser requests the page using GET."""
    
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TopicForm()  # "Give me an empty form."
    else:
        # POST data submitted; process data.
        form = TopicForm(request.POST)  # "Give me a form containing the data the user submitted."
        
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))   # For example, if your URL is:path('topics/', views.topics, name='topics')then:reverse('learning_logs:topics')  can produce:/topics/So reverse() gets the URL.  and redirect to that url
    context = {'form': form}
    return render(request, 'new_topic.html', context)  # Render new_topic.html and give it the form variable.  This is actually useful because the user can see what was wrong and correct the form.

@login_required
def new_entry(request, topic_id):
    """Add a new entry for a particular topic."""

    # Get the topic whose ID was received from the URL.
    # For example, if topic_id is 3, Django retrieves Topic with id=3.
    topic = Topic.objects.get(id=topic_id)

    # Check whether the user has NOT submitted the form yet.
    if request.method != 'POST':

        # No data has been submitted, so create an empty EntryForm.
        form = EntryForm()

    else:
        # The form was submitted using POST.
        # Put the submitted data into the EntryForm.
        form = EntryForm(data=request.POST)

        # Check whether the submitted form contains valid data.
        if form.is_valid():

            # Create an Entry object from the form,
            # but don't save it to the database yet.
            new_entry = form.save(commit=False)  # But the form does not know which topic this entry belongs to. So we first create the Entry without saving it. But the form does not know which topic this entry belongs to. So we first create the Entry without saving it.

            # Connect this new entry to the topic we retrieved above.
            new_entry.topic = topic

            # Now save the entry to the database.
            new_entry.save()

            # After saving, redirect the user back to the topic page.
            # topic_id is passed so Django knows which topic to display.
            return HttpResponseRedirect(
                reverse('learning_logs:topic', args=[topic_id])
            )

    # Put the topic and form into a context dictionary.
    # This allows the template to use {{ topic }} and {{ form }}.
    context = {'topic': topic, 'form': form}

    # Display the new_entry.html template and send the context to it.
    return render(request, 'new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry."""

    # Get the Entry object whose ID was passed in the URL.
    # For example, if entry_id = 5, this gets Entry with id=5.
    entry = Entry.objects.get(id=entry_id)

    # Get the Topic that this entry belongs to.
    # entry.topic gives us the Topic object related to this Entry.
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    # Check if the request is NOT a POST request.
    # This means the user is opening the edit page for the first time.
    if request.method != 'POST':

        # Create the form and pre-fill it with the current entry's data.
        # instance=entry tells Django which existing Entry we want to edit.
        form = EntryForm(instance=entry)

    else:
        # The user has submitted the edited form using POST.
        # instance=entry tells Django to UPDATE this existing entry
        # instead of creating a completely new Entry.
        # request.POST contains the new data submitted by the user.
        form = EntryForm(instance=entry, data=request.POST)

        # Check whether the submitted data is valid.
        if form.is_valid():

            # Save the changes to the existing Entry in the database.
            form.save()

            # After saving, redirect the user back to the topic page.
            # topic.id gives us the ID of the topic this entry belongs to.
            return HttpResponseRedirect(
                reverse('learning_logs:topic', args=[topic.id])
            )

    # Put the entry, topic, and form into a context dictionary.
    # These can now be accessed inside edit_entry.html.
    context = {
        'entry': entry,
        'topic': topic,
        'form': form
    }

    # Render the edit_entry.html template and send the context to it.
    return render(request, 'edit_entry.html', context)