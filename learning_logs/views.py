from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm, EntryForm


def check_topic_owner(topic, request):
    if topic.owner != request.user:
        raise Http404


# Create your views here.
def index(request):
    """The home page for Learning Log."""
    return render(request, "learning_logs/index.html")


@login_required
def topics(request):
    """Show all topics"""
    topics = Topic.objects.filter(owner=request.user).order_by("date_added")
    context = {"topics": topics}
    return render(request, "learning_logs/topics.html", context)


@login_required
def topic(request, topic_id):
    """Show a single topic and all its entries."""
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(topic, request)

    entries = topic.entry_set.order_by("-date_added")
    context = {"topic": topic, "entries": entries}
    return render(request, "learning_logs/topic.html", context)


@login_required
def new_topic(request):
    """Add a new topic"""
    if request.method != "POST":
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()

            return redirect("learning_logs:topics")

    # Display a blank or invalid form.
    context = {"form": form}
    return render(request, "learning_logs/new_topic.html", context)


@login_required
def new_entry(request, topic_id):
    """Add a new entry for a particular topic."""
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(topic, request)

    if request.method != "POST":
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()

            return redirect("learning_logs:topic", topic_id=topic_id)

    # Display a blank or invalid form.
    context = {"topic": topic, "form": form}
    return render(request, "learning_logs/new_entry.html", context)


@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(topic, request)

    if request.method != "POST":
        # Initial request; pre-fill form with the current entry
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()

            return redirect("learning_logs:topic", topic_id=topic.id)

    context = {"entry": entry, "topic": topic, "form": form}
    return render(request, "learning_logs/edit_entry.html", context)


@login_required
def delete_entry(request, entry_id):
    """Delete an existing entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(topic, request)

    results = entry.delete()
    if results[0] == 1:
        return redirect("learning_logs:topic", topic_id=topic.id)
    else:
        raise Exception("Error deleting the entry")


@login_required
def delete_topic(request, topic_id):
    """Delete an existing topic"""
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(topic, request)

    entries = topic.entry_set.all()
    print(entries)

    # check if there are associated entries
    num_entries_to_be_deleted = len(entries)
    if len(entries) > 0:
        num_deleted = entries.delete()
        if num_entries_to_be_deleted != num_deleted[0]:
            raise Exception("Error deleting associated entries")

    delete_results = topic.delete()
    if delete_results[0] == 1:
        return redirect("learning_logs:topics")
    else:
        print(delete_results)
        raise Exception("Error deleting the topic")
