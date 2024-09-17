import hashlib
from .models import Event
from django.template import loader
from profiles.models import Profile
from django.http import HttpResponse
from django.core.mail import send_mail
from .forms import EventCreationForm, EventEditForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .utils import generateUUID
from django.conf import settings
from django.template.loader import render_to_string

from django.views import View
from django.conf import settings
import stripe
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.urls import reverse

stripe.api_key = settings.STRIPE_SECRET_KEY

from events.models import Event


# Create your views here.

@login_required
def homeView(request):
    profile = Profile.objects.get(user=request.user) # Get the user's profile
    form    = EventCreationForm(request.POST or None, request.FILES or None) # Create an instance of EventCreationForm with POST data if available, or None
    events  = Event.objects.all()  # Retrieve all events from the Event model
    if request.method == 'POST': 
        if form.is_valid():
            event = form.save(commit=False) # save form data to create a new event
            event.organizer = profile   # Assigns the organizer of the event to the user's profile
            event.ksh = float(event.price) * 130.00   
            event.save()
            event.attendees.add(profile) # Add the user's profile as an attendee of the event

            # Set a flag in the session to indicate a successful event creation
            request.session['eventCreated'] = True

    template = loader.get_template('events/home.html') # load template
    context  = {
        "profile": profile,
        'form'   : form,
        'events' : events,
    }
    return HttpResponse(template.render(context, request))



@login_required
def eventDetailView(request, id):
    profile = Profile.objects.get(user=request.user) # get the profile from the request object
    event = Event.objects.get(pk=id) #
    eventName = event.title # get the name of the event
    product = Event.objects.get(title=eventName)

    profileEmail = profile.email # get the email address of the profile
    # profileName = profile # get the name of the profile
    # senderEmail = settings.DEFAULT_FROM_EMAIL # get the email address of the sender
    # profileSubject = f'Your tickets for : {eventName} {eventLocation}'
    # eventLocation = event.venue 
    uuid = generateUUID(profileEmail)
    

    if request.method == 'POST': 
        if profile not in event.attendees.all():   # Check if the profile is not already in the list of event attendees
            # sendUUID(profileSubject, profileName, senderEmail, profileEmail, uuid, event) # Send an email with a unique UUID to the profile
            event.attendees.add(profile) # Add the profile to the list of event attendees
            request.session['eventBooked'] = True  # Set a session variable indicating that the event has been booked

    template = loader.get_template('events/eventDetail.html')
    context = {
        'event': event,
        'profile': profile,
        'event': product,
        'uuid': uuid,  
    }
    return HttpResponse(template.render(context, request))

# def sendUUID(subject, name, from_email, to_email, uuid, event):
#     message = render_to_string('email_template.html', {
#         'name': name,
#         'uuid': uuid,
#         'event': event,
#     })
#     send_mail(subject, message, from_email, [to_email]) # Send the email using Django's send_mail function

def generateUUID(email):
    hashObject = hashlib.sha1(email.encode())  # Create a hash object and encode the email
    hexDigit = hashObject.hexdigest() # Convert the hash to a hexadecimal string
    uuid = '-'.join([hexDigit[:3], hexDigit[3:6], hexDigit[6:9]])
    return uuid

# def sendUUID(subject, recipient_name, sender_email, recipient_email, uuid, event):
#     message = f"""
#     Dear {recipient_name},

#     We hope you're as excited as we are because you’re about to experience an unforgettable event! 🎟️✨

#     Here are your exclusive ticket details:

#     **Event Name:** {event.title}
#     **Secret Code:** {uuid}
#     **Date:** {event.date}

#     Make sure to keep this secret code safe. It's your golden ticket to an amazing time!

#     We're thrilled to have you join us and can't wait to see you there!

#     Best regards,
#     planz) Events Team
#     """
#     send_mail(subject, message, 'planz) Events <astroevents0@gmail.com>', [recipient_email], fail_silently=False)


@login_required
def eventEditView(request, id):
    profile = Profile.objects.get(user=request.user)
    event   = Event.objects.get(pk=id)

    if request.method == 'POST':
        form = EventEditForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('home:eventDetail', id=id)
    else:
        form = EventEditForm(instance=event)

    template = loader.get_template('events/eventEdit.html')
    context = {
        'event'  : event,
        'profile': profile,
        'form'   : form,
    }
    return HttpResponse(template.render(context, request))


@login_required
def eventDeleteView(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == 'POST': # If the request method is POST, delete the event
        event.delete()
        return redirect('profiles:profile')  
    
    template = loader.get_template('events/eventEdit.html')
    context = {
        'event'  : event,
              }
    return HttpResponse(template.render(context, request))


# class ProductLandingPageView(TemplateView):
#     template_name = 'eventDetail.html'
#     def get_context_data(self, **kwargs):
#         product = Event.objects.get(name="the gaming")
#         context = super(ProductLandingPageView, self).get_context_data(**kwargs)
#         context.update({
#             "event": product,
#         })
#         return context


# class CreateCheckoutSessionsView(View):
#     def post(self, request, *args, **kwargs):
#         YOUR_DOMAIN = "http://127.0.0.1:8000"
#         checkout_session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=[
#                 {
#                     'price-data': {
#                         'currency': 'usd',
#                         'unit_amount': 2000,
#                         'product_data': {
#                             'name': 'stubborn attachment'
#                         },
#                     },
#                     # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
#                     # 'price': '{{PRICE_ID}}',
#                     'quantity': 1,
#                 },
#             ],
#             mode='payment',
#             success_url=YOUR_DOMAIN + '/success/',
#             cancel_url=YOUR_DOMAIN + '/cancel/',
#         )
#         print("**************** this is working in the event view ****************")
#         return JsonResponse({
#             'id': checkout_session.id
#         })

def CreateCheckoutSession(request):
    if request.method == "POST":
        try:
            # Create a new Stripe Checkout Session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Event Ticket',
                        },
                        'unit_amount': 2000,  # Amount in cents
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='http://127.0.0.1:8000/events/success',
                cancel_url='http://127.0.0.1:8000/events/cancel',
            )
            return JsonResponse({'id': session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)




# def charge(request):
# 	amount = int(request.POST['amount'])
# 	if request.method == 'POST':
# 		print('Data:', request.POST)

# 		customer = stripe.Customer.create(
# 			email = request.POST['email'],
# 			name = request.POST['nickname'],
# 			source = request.POST['stripeToken'],
# 		)

# 		charge = stripe.Charge.create(
# 			customer = customer,
# 			amount = amount*100,
# 			currency = 'kes',
# 			description = "Donation",
# 		)

# 	return redirect(reverse('success', args=[amount]))


# def successMsg(request, args):
# 	amount = args
# 	return render(request, 'base/success.html', {'amount':amount})
