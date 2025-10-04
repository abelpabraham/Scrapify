from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.forms import modelformset_factory
from django.contrib import messages
from .models import *
from .forms import *
from django.http import JsonResponse
from .decorators import role_required, anonymous_required
from django.db.models import Q, Sum, Count
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.utils.timezone import now, timedelta
from django.db import transaction





def send_notification_email(subject, message, recipient_list, html_message=None):
    """
    Sends an email using Django's configured SMTP settings.

    :param subject: Subject of the email
    :param message: Plain text message
    :param recipient_list: List of recipient emails (['email1@example.com', ...])
    :param html_message: Optional HTML content
    """
    if not isinstance(recipient_list, list):
        recipient_list = [recipient_list]

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        fail_silently=False,
        html_message=html_message
    )



def bas(request):
    return render(request,'admin/bas.html')


def register_admin(request):
    if User.objects.filter(role='admin').exists():
        return HttpResponse("Admin already exists!", status=400)

    name = request.GET.get('name', 'Admin')
    email = request.GET.get('email', 'admin@example.com')
    password = request.GET.get('password', 'admin123')

    admin = User.objects.create(name=name, email=email, role='admin')
    admin.set_password(password)

    return HttpResponse(f"Admin {name} created successfully! You can now login.", status=201)


def index(request):
    total_recycled = DealerPickup.objects.filter(
        request__status="completed"
    ).aggregate(total=Sum("recyclable_total"))["total"] or 0

    total_completed_pickups = DealerPickup.objects.filter(
        request__status="completed"
    ).count()

    context = {
        "total_recycled": total_recycled,
        "total_completed_pickups": total_completed_pickups,
    }

    return render(request, 'land/index.html', context)

def about(request):
    return render(request,'land/about.html')

def contact(request):
    return render(request,'land/contact.html')

@anonymous_required
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password']) 
            user.save()
            messages.success(request, "Account created successfully! Please login.")
            return redirect("login")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()

    return render(request, "auth/register.html", {"form": form})

@anonymous_required
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "Invalid email or password.")
                return redirect("login")

            if user.check_password(password):
                if user.role == "dealer" and not user.is_active:
                    messages.error(request, "Your account is not yet activated. Please wait for admin approval.")
                    return redirect("login")

                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                request.session['user_role'] = user.role
                messages.success(request, f"Welcome, {user.name} ({user.role})!")

                if user.role == "admin":
                    return redirect("admin_dashboard")
                elif user.role == "dealer":
                    return redirect("dealer_dashboard")
                else:
                    return redirect("seller_dashboard")
            else:
                messages.error(request, "Invalid email or password.")
                return redirect("login")
    else:
        form = LoginForm()

    return render(request, "auth/login.html", {"form": form})


def logout_view(request):
    request.session.flush()
    return redirect("login")


@role_required(['admin'])
def admin_dashboard(request):
    # 1. Dealers
    total_dealers = User.objects.filter(role="dealer").count()
    approved_dealers = User.objects.filter(role="dealer", is_active=True).count()

    # 2. Sellers
    total_sellers = User.objects.filter(role="seller").count()

    # 3. Pending Dealer Approvals
    pending_dealer_approvals = User.objects.filter(role="dealer").exclude(
        id__in=DealerRate.objects.filter(approved=True).values("dealer")
    ).count()

    # 4. Open Pickup Requests
    open_requests = PickupRequest.objects.filter(status="pending").count()

    # 5. Completed Pickups (this month)
    today = now().date()
    completed_this_month = DealerPickup.objects.filter(
        request__status="completed",
        created_at__year=today.year,
        created_at__month=today.month,
    ).count()

    # 6. Total Recycled
    total_recycled = DealerPickup.objects.filter(request__status="completed").aggregate(
        total=Sum("verified_total")
    )["total"] or 0

    # 7. Graph Data with filter
    period = request.GET.get("period", "month")  
    if period == "week":
        start_date = today - timedelta(days=7)
    else:  
        start_date = today.replace(day=1)

    pickups = DealerPickup.objects.filter(
        request__status="completed",
        created_at__date__gte=start_date
    )

    total_picked = pickups.aggregate(total=Sum("verified_total"))["total"] or 0
    total_recycled_period = pickups.aggregate(total=Sum("recyclable_total"))["total"] or 0
    
    context = {
        "total_dealers": total_dealers,
        "approved_dealers": approved_dealers,
        "total_sellers": total_sellers,
        "pending_dealer_approvals": pending_dealer_approvals,
        "open_requests": open_requests,
        "completed_this_month": completed_this_month,
        "total_recycled": total_recycled,
        "period": period,
        "total_picked": total_picked,
        "total_recycled_period": total_recycled_period,
    }
    return render(request, "admin/dashboard.html", context)


@role_required(['seller'])
def seller_dashboard(request):
    user = get_object_or_404(User, id=request.session.get('user_id'))

    pickup_requests = PickupRequest.objects.filter(seller=user).order_by('-created_at')

    total_requests = pickup_requests.count()
    pending_requests = pickup_requests.filter(status="pending").count()

    total_earned = DealerPickup.objects.filter(
        request__seller=user,
        request__status="completed"
    ).aggregate(total=Sum('final_amount'))['total'] or 0

    total_recyclable = DealerPickup.objects.filter(
        request__seller=user,
        request__status="completed"
    ).aggregate(total=Sum('recyclable_total'))['total'] or 0

    pickup_data = []
    for pr in pickup_requests:
        dealer_pickup = getattr(pr, "dealer_pickup", None)

        actual_weight = 0
        final_amount = 0
        scheduled_datetime = None
        recyclable_total = 0

        if dealer_pickup:
            actual_weight = dealer_pickup.items.aggregate(
                total_weight=Sum('actual_weight')
            )['total_weight'] or 0
            final_amount = dealer_pickup.final_amount
            scheduled_datetime = dealer_pickup.scheduled_datetime
            recyclable_total = dealer_pickup.recyclable_total

        pickup_data.append({
            'request': pr,
            'approx_weight': pr.total_approx_weight(),
            'actual_weight': actual_weight,
            'final_amount': final_amount,
            'recyclable_total': recyclable_total,
            'scheduled_datetime': scheduled_datetime,
        })

    context = {
        'user': user,
        'pickup_data': pickup_data,
        'total_requests': total_requests,
        'pending_requests': pending_requests,
        'total_earned': total_earned,
        'total_recyclable': total_recyclable,
    }

    return render(request, 'seller/dashboard.html', context)


@role_required(['dealer'])
def dealer_dashboard(request):
    dealer = get_object_or_404(User, id=request.session.get('user_id'), role="dealer")

    total_requests_in_city = PickupRequest.objects.filter(city=dealer.city).count()

    accepted_pickups = DealerPickup.objects.filter(dealer=dealer, request__status="accepted").count()

    completed_requests = DealerPickup.objects.filter(dealer=dealer, request__status="completed").count()

    yet_to_complete = DealerPickup.objects.filter(
        dealer=dealer, request__status__in=["accepted", "scheduled"]
    ).count()

    last_verified_pickups = DealerPickup.objects.filter(
        dealer=dealer, request__status="completed"
    ).order_by("-created_at")[:3]

    verified_pickups_data = []
    for pickup in last_verified_pickups:
        total_weight = pickup.items.aggregate(total=Sum("actual_weight"))["total"] or 0
        verified_pickups_data.append({
            "id": pickup.request.id,
            "seller": pickup.request.seller.name,
            "date": pickup.created_at,
            "total_weight": total_weight,
            "final_amount": pickup.final_amount,
        })

    # 6. Total recycled kg
    total_recycled_kg = DealerPickupItem.objects.filter(
        dealer_pickup__dealer=dealer
    ).aggregate(total=Sum("actual_weight"))["total"] or 0

    has_rates = dealer.rates.exists()
    
    context = {
        "dealer": dealer,
        "total_requests_in_city": total_requests_in_city,
        "accepted_pickups": accepted_pickups,
        "completed_requests": completed_requests,
        "yet_to_complete": yet_to_complete,
        "verified_pickups_data": verified_pickups_data,
        "total_recycled_kg": total_recycled_kg,
        "has_rates": has_rates,
    }

    return render(request, "dealer/dashboard.html", context)


@role_required(['admin','dealer','seller'])
def profile_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "You must be logged in to view profile.")
        return redirect("login")

    user = get_object_or_404(User, id=user_id)
    if user.role=='dealer':
        return render(request, "dealer/profile.html", {"user": user})
    elif user.role=='seller':
        return render(request, "seller/profile.html", {"user": user})


@role_required(['admin','dealer','seller'])
def edit_profile_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "You must be logged in to edit profile.")
        return redirect("login")

    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileForm(instance=user)
    if user.role=='dealer':
        return render(request, "dealer/edit_profile.html", {"form": form})
    elif user.role=='seller':
        return render(request, "seller/edit_profile.html", {"form": form})



@role_required(['admin'])
def add_category(request):
    if request.method == "POST":
        form = ScrapCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Scrap category added successfully!")
            return redirect("list_categories")
    else:
        form = ScrapCategoryForm()
    return render(request, "admin/add_category.html", {"form": form})


@role_required(['admin'])
def list_categories(request):
    categories = ScrapCategory.objects.all()
    return render(request, "admin/list_categories.html", {"categories": categories})


@role_required(['admin'])
def edit_category(request, category_id):
    category = get_object_or_404(ScrapCategory, id=category_id)
    if request.method == "POST":
        form = ScrapCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully!")
            return redirect("list_categories")
    else:
        form = ScrapCategoryForm(instance=category)
    return render(request, "admin/edit_category.html", {"form": form, "category": category})


@role_required(['admin'])
def delete_category(request, category_id):
    category = get_object_or_404(ScrapCategory, id=category_id)
    category.delete()
    messages.success(request, "Category deleted successfully!")
    return redirect("list_categories")



@role_required(['dealer'])
def manage_rates(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "Login required.")
        return redirect("login")

    dealer = get_object_or_404(User, id=user_id)
    if dealer.role != "dealer":
        messages.error(request, "Only dealers can manage rates.")
        return redirect("profile")

    if request.method == "POST":
        form = DealerRateForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            rate_per_kg = form.cleaned_data['rate_per_kg']

            rate_obj, created = DealerRate.objects.update_or_create(
                dealer=dealer,
                category=category,
                defaults={'rate_per_kg': rate_per_kg}
            )

            if created:
                messages.success(request, f"Rate added for {category.name}")
            else:
                messages.success(request, f"Rate updated for {category.name}")

            return redirect("manage_rates")
    else:
        form = DealerRateForm()

    rates = DealerRate.objects.filter(dealer=dealer)

    return render(request, "dealer/manage_rates.html", {"form": form, "rates": rates})


@role_required(['admin'])
def dealers_list(request):
    dealers = User.objects.filter(role="dealer")
    return render(request, "admin/dealers_list.html", {"dealers": dealers})

@role_required(['admin'])
def toggle_user_active(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active  
    user.save(update_fields=["is_active"])

    status = "activated" if user.is_active else "deactivated"
    messages.success(request, f"{user.name} ({user.role}) has been {status}.")
    return redirect("dealers_list")


@role_required(['admin'])
def dealer_rates(request, dealer_id):
    dealer = get_object_or_404(User, id=dealer_id, role="dealer")
    rates = DealerRate.objects.filter(dealer=dealer).select_related("category")

    rates_data = [
        {
            "id": r.id,
            "category": r.category.name,
            "rate": str(r.rate_per_kg),
            "approved": r.approved,
            "updated_at": r.updated_at.strftime("%Y-%m-%d %H:%M"),
        }
        for r in rates
    ]
    return JsonResponse({"dealer": dealer.name, "rates": rates_data})


@role_required(['admin'])
def approve_rate(request, rate_id):
    rate = get_object_or_404(DealerRate, id=rate_id)
    rate.approved = True
    rate.save()
    messages.success(request, f"Approved {rate.dealer.name}'s rate for {rate.category.name}")
    return redirect("dealers_list")


@role_required(['admin'])
def reject_rate(request, rate_id):
    rate = get_object_or_404(DealerRate, id=rate_id)
    rate.approved = False
    rate.save()
    messages.warning(request, f"Rejected {rate.dealer.name}'s rate for {rate.category.name}")
    return redirect("dealers_list")


@role_required(['admin'])
def sellers_list(request):
    sellers = User.objects.filter(role="seller")
    return render(request, "admin/sellers_list.html", {"sellers": sellers})


@role_required(["seller"])
def create_pickup_request(request):
    ItemFormSet = modelformset_factory(PickupItem, form=PickupItemForm, extra=1, can_delete=True)

    if request.method == "POST":
        request_form = PickupRequestForm(request.POST)
        formset = ItemFormSet(request.POST, queryset=PickupItem.objects.none())

        if request_form.is_valid() and formset.is_valid():
            # Calculate total approximate weight
            total_weight = sum(
                form.cleaned_data["approx_weight"]
                for form in formset
                if form.cleaned_data and not form.cleaned_data.get("DELETE")
            )

            if total_weight < 10:
                messages.error(request, "Total approximate weight must be at least 10 kg.")
            else:
                pickup_request = request_form.save(commit=False)
                pickup_request.seller = get_object_or_404(User, id=request.session.get("user_id"))
                pickup_request.latitude = request.POST.get("latitude")
                pickup_request.longitude = request.POST.get("longitude")
                pickup_request.save()

                for form in formset:
                    if form.cleaned_data and not form.cleaned_data.get("DELETE"):
                        item = form.save(commit=False)
                        item.request = pickup_request
                        item.save()

                messages.success(request, "Pickup request created successfully!")
                return redirect("my_pickup_requests")
    else:
        request_form = PickupRequestForm()
        formset = ItemFormSet(queryset=PickupItem.objects.none())

    return render(request, "seller/create_request.html", {
        "request_form": request_form,
        "formset": formset,
    })


@role_required(["seller"])
def my_pickup_requests(request):
    seller = User.objects.get(id=request.session.get('user_id'))
    requests = PickupRequest.objects.filter(seller=seller).order_by("-created_at")
    

    return render(request, "seller/my_pickup_requests.html", {"requests": requests})

@role_required(["seller"])
def edit_pickup_request(request, request_id):
    user = get_object_or_404(User, id=request.session.get('user_id'))
    pr = get_object_or_404(PickupRequest, id=request_id, seller=user)

    if pr.status != "pending":
        messages.error(request, "You can only edit request while it's pending.")
        return redirect("my_pickup_requests")

    if request.method == "POST":
        form = PickupRequestForm(request.POST, instance=pr)
        if form.is_valid():
            form.save()
            messages.success(request, "Pickup request updated.")
            return redirect("my_pickup_requests")
    else:
        form = PickupRequestForm(instance=pr)

    return render(request, "seller/edit_request.html", {"form": form, "request_obj": pr})

@role_required(["seller"])
def cancel_pickup_request(request, request_id):
    pickup_request = get_object_or_404(
        PickupRequest,
        id=request_id,
        seller_id=request.session.get("user_id")
    )

    if pickup_request.status in ["completed", "cancelled"]:
        messages.error(request, "This pickup request cannot be cancelled.")
        return redirect("seller_dashboard")

    pickup_request.status = "cancelled"
    pickup_request.save()

    messages.success(request, f"Pickup request #{pickup_request.id} has been cancelled successfully.")
    return redirect("seller_dashboard")


@role_required(["dealer"])
def dealer_pickup_requests(request):
    dealer = User.objects.get(id=request.session.get('user_id'))
    req = PickupRequest.objects.filter(
            Q(city__iexact=dealer.city),
            Q(status__iexact="pending")
        ).order_by("-created_at")
    return render(request, "dealer/pickup_requests_list.html", {
        "requests": req
    })
    
def pickup_map(request):
    return render(request, 'dealer/pickup_map.html')


@role_required(["dealer"])
def accept_pickup_request(request, request_id):
    dealer = get_object_or_404(User, id=request.session.get("user_id"), role="dealer")
    
    if not dealer.is_active:
        messages.error(request, "Your account is not activated. You cannot accept pickup requests.")
        return redirect("dealer_pickup_requests")
    
    pickup_request = get_object_or_404(PickupRequest, id=request_id, status="pending")

    if hasattr(pickup_request, "dealerpickup"):
        messages.warning(request, "This pickup request has already been accepted.")
        return redirect("dealer_pickup_requests")

    dealer_pickup, created = DealerPickup.objects.get_or_create(
    request=pickup_request,
    defaults={'dealer': dealer}
    )

    if not created:
        messages.warning(request, "This pickup request has already been accepted.")
        print("This pickup request has already been accepted.")
        return redirect("dealer_pickup_requests")

    pickup_request.status = "accepted"
    pickup_request.save()
    subject = "Your Pickup Request Has Been Accepted!"
    message = f"Hello {pickup_request.seller.name},\n\nDealer {dealer.name} has accepted your pickup request."
    send_notification_email(subject, message, pickup_request.seller.email)

    messages.success(request, f"Pickup request from {pickup_request.seller.name} accepted successfully!")
    return redirect("dealer_pickup_requests")  


@role_required(["dealer"])
def dealer_accepted_pickup_requests(request):
    dealer = get_object_or_404(User, id=request.session.get("user_id"), role="dealer")
    pickups = DealerPickup.objects.filter(dealer=dealer).select_related("request").order_by("-id")
    return render(request, "dealer/accepted_requests.html", {"pickups": pickups})


@role_required(["dealer"])
def schedule_pickup(request, request_id):
    dealer_id = request.session.get("user_id")
    dealer_role = request.session.get("user_role")

    if not dealer_id or dealer_role != "dealer":
        messages.error(request, "Unauthorized access.")
        return redirect("login")

    dealer = get_object_or_404(User, id=dealer_id, role="dealer")

    try:
        with transaction.atomic():
            pr = PickupRequest.objects.select_for_update().get(id=request_id)

            if pr.status != "accepted":
                messages.error(request, "Pickup request is not available for scheduling.")
                return redirect("dealer_accepted_pickup_requests")

            dealer_pickup = DealerPickup.objects.filter(request=pr, dealer=dealer).first()
            if not dealer_pickup:
                messages.error(request, "No pickup is assigned to you for this request.")
                return redirect("dealer_accepted_pickup_requests")

            if request.method == "POST":
                form = DealerScheduleForm(request.POST, instance=dealer_pickup)
                if form.is_valid():
                    dealer_pickup = form.save(commit=False)
                    dealer_pickup.schedule_confirmed = True
                    dealer_pickup.save()

                    pr.status = "scheduled"
                    pr.save()

                    subject = "Your Pickup Has Been Scheduled!"
                    scheduled_time = dealer_pickup.scheduled_datetime.strftime("%d %b %Y, %I:%M %p")
                    message = (
                        f"Hello {pr.seller.name},\n\n"
                        f"Your pickup request (ID: {pr.id}) has been scheduled by dealer {dealer.name}.\n"
                        f"Scheduled Date & Time: {scheduled_time}\n\n"
                        "Please make sure your scrap items are ready for collection.\n\n"
                        "Thank you,\nScrap Management System"
                    )
                    send_notification_email(subject, message, pr.seller.email)

                    messages.success(request, "Pickup scheduled successfully and seller notified via email.")
                    return redirect("dealer_accepted_pickup_requests")
            else:
                form = DealerScheduleForm(instance=dealer_pickup)

    except PickupRequest.DoesNotExist:
        messages.error(request, "Pickup request not found.")
        return redirect("dealer_accepted_pickup_requests")

    return render(request, "dealer/schedule_pickup.html", {
        "form": form,
        "pickup_request": pr,
    })


@role_required(["seller"])
def request_reschedule(request, request_id):
    seller = get_object_or_404(User, id=request.session.get('user_id'), role="seller")
    pr = get_object_or_404(PickupRequest, id=request_id, seller=seller)
    if pr.status not in ("accepted", "scheduled"):
        messages.error(request, "You can only request reschedule after dealer accepts.")
        return redirect("my_pickup_requests")

    if request.method == "POST":
        form = SellerRescheduleForm(request.POST)
        if form.is_valid():
            rr = form.save(commit=False)
            rr.pickup_request = pr
            rr.requested_by = seller
            rr.save()
            messages.success(request, "Reschedule request sent to dealer.")
            return redirect("my_pickup_requests")
    else:
        form = SellerRescheduleForm()

    return render(request, "seller/request_reschedule.html", {"form": form, "pickup_request": pr})


@role_required(["dealer"])
def dealer_reschedule_list(request):
    dealer = get_object_or_404(User, id=request.session.get('user_id'), role="dealer")
    reschedules = RescheduleRequest.objects.filter(pickup_request__dealer_pickup__dealer=dealer, status="pending").order_by("-created_at")
    return render(request, "dealer/reschedule_list.html", {"reschedules": reschedules})

@role_required(["dealer"])
def respond_reschedule(request, rr_id, action):
    dealer = get_object_or_404(User, id=request.session.get('user_id'), role="dealer")
    rr = get_object_or_404(RescheduleRequest, id=rr_id, pickup_request__dealer_pickup__dealer=dealer)

    if action == "accept":
        rr.status = "accepted"
        rr.save()
        dp = rr.pickup_request.dealer_pickup
        dp.scheduled_datetime = rr.requested_datetime
        dp.schedule_confirmed = True
        dp.save()
        rr.pickup_request.status = "scheduled"
        rr.pickup_request.save()
        messages.success(request, "Reschedule accepted and scheduled.")
    else:
        rr.status = "rejected"
        rr.save()
        messages.warning(request, "Reschedule request rejected.")
    return redirect("dealer_reschedule_list")

@role_required(["dealer"])
def verify_pickup_request(request, request_id):
    pickup_request = get_object_or_404(PickupRequest, id=request_id, status="accepted")
    dealer_pickup = get_object_or_404(DealerPickup, request=pickup_request)

    ItemFormSet = modelformset_factory(DealerPickupItem, form=DealerPickupItemForm, extra=0)

    if request.method == "POST":
        pickup_form = DealerPickupForm(request.POST, instance=dealer_pickup)
        formset = ItemFormSet(request.POST, queryset=dealer_pickup.items.all())

        if pickup_form.is_valid() and formset.is_valid():
            pickup_form.save()
            formset.save()

            dealer_pickup.calculate_final_amount()

            pickup_request.status = "completed"
            pickup_request.save()

            messages.success(request, "Pickup verified and finalized successfully!")
            return redirect("dealer_dashboard")
    else:
        pickup_form = DealerPickupForm(instance=dealer_pickup)

        if not dealer_pickup.items.exists():
            for item in pickup_request.items.all():
                DealerPickupItem.objects.create(
                    dealer_pickup=dealer_pickup,
                    category=item.category,
                    actual_weight=item.approx_weight
                )

        formset = ItemFormSet(queryset=dealer_pickup.items.all())

    return render(request, "dealer/verify_pickup.html", {
        "pickup_form": pickup_form,
        "formset": formset,
        "pickup_request": pickup_request,
    })


@role_required(["seller"])
def give_feedback(request, pickup_id):
    pickup = get_object_or_404(DealerPickup, id=pickup_id, request__seller=request.user)

    if pickup.request.status != "completed":
        messages.error(request, "You can only give feedback after the pickup is completed.")
        return redirect("seller_dashboard")

    if hasattr(pickup, "feedback"):  
        messages.warning(request, "You already submitted feedback for this pickup.")
        return redirect("seller_dashboard")

    if request.method == "POST":
        form = PickupFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.pickup = pickup
            feedback.seller = request.user
            feedback.save()
            messages.success(request, "Thank you for your feedback!")
            return redirect("seller_dashboard")
    else:
        form = PickupFeedbackForm()

    return render(request, "seller/give_feedback.html", {"form": form, "pickup": pickup})