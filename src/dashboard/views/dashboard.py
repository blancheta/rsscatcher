from django.shortcuts import redirect, reverse
from django.contrib.auth.decorators import login_required
from ..models import Subscription


@login_required()
def dashboard(request):

    """
    Redirect on a specific view depending on the user authentication
    """

    user_subscriptions_count = Subscription.objects.filter(user=request.user).count()
    if not user_subscriptions_count:
        return redirect(reverse('dashboard-discover'))
    return redirect("dashboard-filter", filter_state="today")
