import json
import random
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Booking

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

gemini_client = None
try:
    from google import genai
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if api_key:
        gemini_client = genai.Client(api_key=api_key)
except Exception as e:
    print("Gemini initialization info:", e)


def index_view(request):
    return render(request, 'index.html')


@csrf_exempt
def api_signup(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))
            username = body.get('username', '').strip()
            email = body.get('email', '').strip()
            password = body.get('password', '').strip()

            if not all([username, email, password]):
                return JsonResponse({'error': 'All fields are required.'}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username is already taken.'}, status=400)

            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return JsonResponse({'message': 'Account created successfully!', 'username': user.username}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def api_login(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))
            username = body.get('username', '').strip()
            password = body.get('password', '').strip()

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'message': 'Logged in successfully!', 'username': user.username})
            else:
                return JsonResponse({'error': 'Invalid username or password.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def api_logout(request):
    logout(request)
    return JsonResponse({'message': 'Logged out successfully!'})


def api_auth_status(request):
    if request.user.is_authenticated:
        return JsonResponse({'isAuthenticated': True, 'username': request.user.username, 'email': request.user.email})
    return JsonResponse({'isAuthenticated': False})


def api_data(request):
    states = [
        {"id": "lagos", "name": "Lagos State", "code": "LOS"},
        {"id": "abuja", "name": "Abuja (FCT)", "code": "ABV"},
        {"id": "rivers", "name": "Rivers State (Port Harcourt)", "code": "PHC"},
        {"id": "kano", "name": "Kano State", "code": "KAN"},
        {"id": "cross_river", "name": "Cross River State (Calabar)", "code": "CBQ"},
    ]

    hotels = [
        # --- LAGOS STATE ---
        {
            "id": "h1",
            "state_id": "lagos",
            "name": "Eko Pearl Luxury Suites",
            "rating": "5 Stars",
            "price": "$220 / night",
            "address": "Victoria Island, Lagos",
            "description": "Oceanfront luxury tower with panoramic Atlantic views, swimming pools, private spa, and fine dining.",
            "images": [
                "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&auto=format&fit=crop",
                "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=800&auto=format&fit=crop",
                "https://images.unsplash.com/photo-1618773928121-c32242e63f39?w=800&auto=format&fit=crop"
            ]
        },
        {
            "id": "h2",
            "state_id": "lagos",
            "name": "Radisson Blu Anchorage",
            "rating": "4.5 Stars",
            "price": "$160 / night",
            "address": "Ozumba Mbadiwe, Victoria Island, Lagos",
            "description": "Lagos Lagoon-view boutique hotel offering serene infinity pool, fitness center, and express airport shuttle.",
            "images": [
                "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&auto=format&fit=crop",
                "https://images.unsplash.com/photo-1590490360182-c33d57733427?w=800&auto=format&fit=crop"
            ]
        },
        {
            "id": "h3",
            "state_id": "lagos",
            "name": "The Wheatbaker Ikoyi",
            "rating": "5 Stars",
            "price": "$240 / night",
            "address": "Lawrence Road, Ikoyi, Lagos",
            "description": "Exclusive boutique luxury hotel featuring fine art collections, peaceful spa retreats, and world-class culinary experiences.",
            "images": [
                "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&auto=format&fit=crop",
                "https://images.unsplash.com/photo-1591088398332-8a7791972843?w=800&auto=format&fit=crop"
            ]
        },

        # --- ABUJA (FCT) ---
        {
            "id": "h4",
            "state_id": "abuja",
            "name": "Transcorp Hilton Resort",
            "rating": "5 Stars",
            "price": "$210 / night",
            "address": "Maitama, Abuja",
            "description": "Capital city landmark featuring lush garden grounds, tennis courts, executive lounge, and 24-hour security.",
            "images": [
                "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&auto=format&fit=crop",
                "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&auto=format&fit=crop"
            ]
        },
        {
            "id": "h5",
            "state_id": "abuja",
            "name": "Fraser Suites Abuja",
            "rating": "4.8 Stars",
            "price": "$185 / night",
            "address": "Central Business District, Abuja",
            "description": "Modern luxury serviced apartments with full kitchenettes, outdoor lap pool, and high-speed executive lounge.",
            "images": [
                "https://images.unsplash.com/photo-1591088398332-8a7791972843?w=800&auto=format&fit=crop",
                "https://images.unsplash.com/photo-1611892440504-42a792e24d32?w=800&auto=format&fit=crop"
            ]
        },

        # --- RIVERS STATE ---
        {
            "id": "h6",
            "state_id": "rivers",
            "name": "Hotel Presidential",
            "rating": "4 Stars",
            "price": "$125 / night",
            "address": "Aba Road, Port Harcourt, Rivers",
            "description": "Classic Port Harcourt hospitality center equipped with Olympic-size pool, night lounge, and conference center.",
            "images": [
                "https://images.unsplash.com/photo-1455587734955-081b22074882?w=800&auto=format&fit=crop",
                "https://images.unsplash.com/photo-1566665797739-1674de7a421a?w=800&auto=format&fit=crop"
            ]
        },

        # --- KANO STATE ---
        {
            "id": "h7",
            "state_id": "kano",
            "name": "Grand Central Hotel Kano",
            "rating": "4 Stars",
            "price": "$115 / night",
            "address": "Bompai Road, Kano",
            "description": "Historic and secure Kano hotel offering spacious executive suites, traditional northern hospitality, and banquet facilities.",
            "images": [
                "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&auto=format&fit=crop",
                "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800&auto=format&fit=crop"
            ]
        },

        # --- CROSS RIVER STATE ---
        {
            "id": "h8",
            "state_id": "cross_river",
            "name": "Tinapa Lakeshore Resort",
            "rating": "4.2 Stars",
            "price": "$110 / night",
            "address": "Tinapa Free Zone, Calabar, Cross River",
            "description": "Eco-friendly waterfront resort near waterparks, monorail tours, and nature reserves.",
            "images": [
                "https://images.unsplash.com/photo-1540555700478-4be289fbecef?w=800&auto=format&fit=crop",
                "https://images.unsplash.com/photo-1584132967334-10e028bd69f7?w=800&auto=format&fit=crop"
            ]
        }
    ]

    flights = [
        {"id": "f1", "from": "Lagos (LOS)", "to": "Abuja (ABV)", "airline": "EasyTravels Air", "price": "$110", "duration": "1h 15m"},
        {"id": "f2", "from": "Abuja (ABV)", "to": "Port Harcourt (PHC)", "airline": "EasyTravels Express", "price": "$130", "duration": "1h 10m"},
        {"id": "f3", "from": "Lagos (LOS)", "to": "Calabar (CBQ)", "airline": "EasyTravels Shuttle", "price": "$145", "duration": "1h 25m"}
    ]

    return JsonResponse({"states": states, "hotels": hotels, "flights": flights})


@csrf_exempt
def api_bookings(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required. Please sign in.'}, status=401)

    if request.method == 'GET':
        data = list(Booking.objects.filter(user=request.user).values().order_by('-created_at'))
        return JsonResponse(data, safe=False)

    elif request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))

            booking_type = body.get('bookingType', 'Flight')
            service_title = body.get('serviceTitle')
            destination_state = body.get('destinationState', '')
            departure_city = body.get('departureCity', '')
            date = body.get('date')
            time = body.get('time')
            customer_name = body.get('customerName')
            customer_email = body.get('customerEmail')

            if not all([service_title, date, time, customer_name, customer_email]):
                return JsonResponse({'error': 'All fields are required.'}, status=400)

            prefix = 'HOT' if booking_type == 'Hotel' else 'FLT'
            new_b = Booking.objects.create(
                user=request.user,
                booking_id=prefix + '-' + str(random.randint(1000, 9999)),
                booking_type=booking_type,
                service_title=service_title,
                destination_state=destination_state,
                departure_city=departure_city,
                date=date,
                time=time,
                customer_name=customer_name,
                customer_email=customer_email,
                status='Confirmed'
            )

            return JsonResponse({
                'message': 'Booking confirmed successfully!',
                'booking_id': new_b.booking_id
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def api_chat(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))
            user_message = body.get('message', '').strip()

            if not user_message:
                return JsonResponse({'error': 'Message cannot be empty.'}, status=400)

            if gemini_client:
                system_prompt = (
                    "You are the official AI Concierge for 'EasyTravels'. "
                    "Answer questions politely, help clients choose hotels in Lagos, Abuja, Rivers, Kano, and Cross River, "
                    "explain flight routes, and guide bookings."
                )
                response = gemini_client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=system_prompt + "\n\nUser Question: " + user_message
                )
                return JsonResponse({'reply': response.text})

            msg_lower = user_message.lower()

            if 'hotel' in msg_lower or 'stay' in msg_lower or 'room' in msg_lower:
                reply = "We offer verified luxury hotels in Lagos, Abuja, Port Harcourt, Kano, and Calabar! Pick a state under 'Destination Hotels' to view pictures."
            elif 'flight' in msg_lower or 'fly' in msg_lower:
                reply = "We operate flights between Lagos, Abuja, Port Harcourt, Kano, and Calabar! Click 'Flights' in the top menu to view schedules."
            elif 'price' in msg_lower or 'cost' in msg_lower:
                reply = "Our flight tickets start from $110, and hotel rooms range between $110/night and $240/night."
            else:
                reply = f"Thank you for reaching out! You can easily book flights or hotels in Lagos, Abuja, Rivers, Kano, and Cross River through our navigation menu."

            return JsonResponse({'reply': reply})

        except Exception as e:
            return JsonResponse({'reply': "How can I assist with your flight or hotel reservation today?"}, status=200)

    return JsonResponse({'error': 'Method not allowed'}, status=405)