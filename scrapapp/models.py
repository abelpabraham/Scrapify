from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
    ROLE_CHOICES = [
        ('seller', 'Seller'),
        ('dealer', 'Dealer'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    custom_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.role}) - {self.custom_id}"

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save(update_fields=['password'])

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def save(self, *args, **kwargs):
        if not self.pk and self.role == "dealer":
            self.is_active = False
        
        if not self.custom_id:
            prefix = "DLR" if self.role == "dealer" else "SLR"

            last_user = User.objects.filter(role=self.role, custom_id__startswith=prefix).order_by("-id").first()
            if last_user and last_user.custom_id:
                try:
                    last_number = int(last_user.custom_id.split("-")[1])
                except (IndexError, ValueError):
                    last_number = 0
            else:
                last_number = 0

            new_number = last_number + 1
            self.custom_id = f"{prefix}-{new_number:04d}" 

        super().save(*args, **kwargs)


class ScrapCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class DealerRate(models.Model):
    dealer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rates")  
    category = models.ForeignKey(ScrapCategory, on_delete=models.CASCADE, related_name="dealer_rates")
    rate_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    approved = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("dealer", "category") 

    def __str__(self):
        return f"{self.dealer.name} - {self.category.name}: {self.rate_per_kg} ₹/kg"

class PickupRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("scheduled", "Scheduled"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]
    seller = models.ForeignKey("User", on_delete=models.CASCADE, related_name="pickup_requests")
    address = models.TextField()
    city = models.CharField(max_length=100)
    preferred_datetime = models.DateTimeField(null=True, blank=True)   
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    latitude=models.CharField(max_length=100)
    longitude=models.CharField(max_length=100)

    def total_approx_weight(self):
        return sum(item.approx_weight for item in self.items.all())
    
    def total_verified_weight(self):
        """Return total verified/actual weight from dealer side (if available)."""
        if hasattr(self, "dealer_pickup"):  
            return sum(item.actual_weight for item in self.dealer_pickup.items.all())
        return 0

    def __str__(self):
        return f"Pickup #{self.id} - {self.seller.name}"


class PickupItem(models.Model):
    request = models.ForeignKey(PickupRequest, on_delete=models.CASCADE, related_name="items")
    category = models.ForeignKey(ScrapCategory, on_delete=models.CASCADE)
    approx_weight = models.FloatField()

    def __str__(self):
        return f"{self.category.name} ({self.approx_weight}kg)"


class DealerPickup(models.Model):
    request = models.OneToOneField(PickupRequest, on_delete=models.CASCADE, related_name="dealer_pickup")
    dealer = models.ForeignKey("User", on_delete=models.CASCADE, related_name="dealer_pickups")
    scheduled_datetime = models.DateTimeField(null=True, blank=True)  
    schedule_confirmed = models.BooleanField(default=False)           
    recyclable_total = models.FloatField(default=0)
    verified_total = models.FloatField(default=0)
    final_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_final_amount(self):
        total = 0
        for item in self.items.all():
            try:
                rate = DealerRate.objects.get(dealer=self.dealer, category=item.category).rate_per_kg
                total += item.actual_weight * float(rate)
            except DealerRate.DoesNotExist:
                continue
        self.final_amount = total
        self.save()
        return total

    def __str__(self):
        return f"DealerPickup #{self.id} - Dealer: {self.dealer.name}"


class DealerPickupItem(models.Model):
    dealer_pickup = models.ForeignKey(DealerPickup, on_delete=models.CASCADE, related_name="items")
    category = models.ForeignKey(ScrapCategory, on_delete=models.CASCADE)
    actual_weight = models.FloatField()

    def __str__(self):
        return f"{self.category.name} ({self.actual_weight}kg)"
    
class RescheduleRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]
    pickup_request = models.ForeignKey(PickupRequest, on_delete=models.CASCADE, related_name="reschedule_requests")
    requested_by = models.ForeignKey("User", on_delete=models.CASCADE)
    requested_datetime = models.DateTimeField()
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reschedule for {self.pickup_request.id} by {self.requested_by.name}"
    


class PickupFeedback(models.Model):
    pickup = models.OneToOneField("DealerPickup", on_delete=models.CASCADE, related_name="feedback")
    seller = models.ForeignKey("User", on_delete=models.CASCADE)

    fair = models.BooleanField(default=True)  
    action_against_dealer = models.BooleanField(default=False)  
    satisfied = models.CharField(
        max_length=20,
        choices=[("yes", "Yes"), ("no", "No"), ("neutral", "Neutral")],
        default="neutral"
    )
    thoughts = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for Pickup {self.pickup.id} by {self.seller.name}"
