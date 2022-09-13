from tokenize import Name
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from messenger.models import Contact, ContactMessage, Group, GroupMessage
from .connection import Connection
import json
from .forms import ContactForm, GroupForm
from .threads import SimpleSender, PubSubSender, SimpleConsumer, PubSubConsumer


def auth(request):
    return render(request, 'auth.html')


def checkauth(request):
    name = request.POST['name']
    connection = Connection()
    connection = connection.start_connection()
    channel = connection.channel()
    channel.queue_declare(queue=name)
    connection.close()
    consumer = SimpleConsumer(name)
    consumer.start()
    groups = Group.objects.all()
    for group in groups:
        consumer = PubSubConsumer(group.group)
        consumer.start()
    url = "home/" + str(name)
    return redirect(url)


def home(request, name):
    return render(request, 'home.html', {'name': name})


def getContacts(request):
    contacts = Contact.objects.all()
    return JsonResponse({"contacts": list(contacts.values())})


def getGroups(request):
    groups = Group.objects.all()
    return JsonResponse({"groups": list(groups.values())})


def getContactMessages(request, pk):
    contact = Contact.objects.get(pk=pk)
    messages = ContactMessage.objects.filter(contact=contact)
    return JsonResponse({"messages": list(messages.values())})


def getGroupMessages(request, pk):
    group = Group.objects.get(pk=pk)
    messages = GroupMessage.objects.filter(group=group)
    return JsonResponse({"messages": list(messages.values())})


def addContact(request, name):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home', name)
    return render(request, 'registration.html', {'form': form, 'name': name})


def contactConversation(request, name, pk, template_name='contactConversation.html'):
    contact = get_object_or_404(Contact, pk=pk)

    return render(request, template_name, {
        'name': name,
        'contact': contact
    })


def addGroup(request, name):
    form = GroupForm()
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            t = PubSubConsumer(group.group)
            t.start()
            return redirect('home', name)
    return render(request, 'registration.html', {'form': form, 'name': name})


def groupConversation(request, name, pk, template_name='groupConversation.html'):
    group = get_object_or_404(Group, pk=pk)

    return render(request, template_name, {
        'name': name,
        'group': group
    })


def encoder(dictionary):
    object = json.dumps(dictionary)
    json_encoded = str(object).encode('utf-8')
    return json_encoded


def sendContactMessage(request):
    name = request.POST['name']
    message = request.POST['message']
    receiver = request.POST['receiver']
    dictionary = {"SENDER": name,
                  "MESSAGE": message,
                  "RECEIVER": receiver}
    json_encoded = encoder(dictionary)
    sender = SimpleSender(receiver, json_encoded)
    sender.start()
    sender.join()
    con = Contact.objects.get(name=receiver)
    message = ContactMessage.objects.create(message=message, contact=con, origin="You")
    message.save()
    return HttpResponse('Message sent successfully')


def sendGroupMessage(request):
    origin = request.POST['origin']
    message = request.POST['message']
    group = request.POST['group']
    dictionary = {"SENDER": origin,
                  "MESSAGE": message,
                  "GROUP": group}
    json_encoded = encoder(dictionary)
    sender = PubSubSender(group, json_encoded)
    sender.start()
    sender.join()
    return HttpResponse('Message sent successfully')
