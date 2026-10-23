from django.db import models
from django.contrib.auth.models import User


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    booking_id = models.CharField(max_length=20, unique=True)
    booking_type = models.CharField(max_length=50, default='Flight')  # 'Flight' or 'Hotel'
    service_title = models.CharField(max_length=150)
    destination_state = models.CharField(max_length=100, blank=True, default='')
    departure_city = models.CharField(max_length=100, blank=True, default='')
    date = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    status = models.CharField(max_length=20, default='Confirmed')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.booking_type}] {self.booking_id} - {self.customer_name}"