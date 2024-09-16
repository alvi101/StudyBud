from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Username or Password does not match")

    page = "login"
    context = {"page": page}
    return render(request, "./base/login_register.html", context)


def logout_view(request):
    logout(request)
    return redirect("home")


def register_view(request):

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # get the user just created without saving to User db
            # done to check and sanitize form fields
            # lowercase username
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            # login and redirect to home page
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "An errror occured durng registration")
    else:
        form = UserCreationForm()
    context = {"form": form}
    return render(request, "./base/login_register.html", context)


@login_required(login_url="login")
def update_user(request):
    user = request.user
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile", user.id)
    else:
        form = UserForm(instance=user)
        context = {"form": form}
    return render(request, "base/update-user.html", context)


def home(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    # Room model has field name topic. With topic__name we are checking
    # the related Topic model as in Topic.name
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) |
        Q(host__username__icontains=q)
    )
    # faster than len(rooms)
    room_count = rooms.count()
    topics = Topic.objects.all()[0:5]
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {"rooms": rooms, "topics": topics,
               "room_count": room_count, "room_messages": room_messages}
    return render(request, './base/home.html', context)


def profile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {"user": user, "rooms": rooms,
               "room_messages": room_messages, "topics": topics}
    return render(request, "base/profile.html", context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by("-created")
    participants = room.participants.all()

    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            # ("body") is from name="body" in the form
            body=request.POST.get("body")
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {"room": room, "room_messages": room_messages,
               "participants": participants}
    return render(request, "./base/room.html", context)


@login_required(login_url="login")
def create_room(request):
    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get("name"),
            description=request.POST.get("description"),
        )

        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        return redirect("home")
    else:
        form = RoomForm()
        topics = Topic.objects.all()
    context = {"form": form, "topics": topics}
    return render(request, "./base/room_form.html", context)


@login_required(login_url="login")
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    # allow only creator or super user to update
    if request.user != room.host:
        return HttpResponse("Can only edit your own rooms")

    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get("name")
        room.topic = topic
        room.description = request.POST.get("description")
        room.save()
        return redirect("home")
    else:
        room = Room.objects.get(id=pk)
        form = RoomForm(instance=room)
    context = {"form": form, "room": room}
    return render(request, "./base/room_form.html", context)


@login_required(login_url="login")
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect("home")
    return render(request, "./base/delete.html", {"obj": room})


@login_required(login_url="login")
def delete_message(request, pk):
    message = Message.objects.get(id=pk)

    if message.user != request.user:
        return redirect("room", pk=pk)

    if request.method == "POST":
        message.delete()
        print(message.room.id)
        return redirect("room", pk=message.room.id)
    context = {"obj": message}
    return render(request, "./base/delete.html", context)


def topics(request):
    q = request.GET.get('q')
    if q is not None:
        q = q
    else:
        q = ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {"topics": topics})
