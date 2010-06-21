from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import list_detail
from django.shortcuts import get_object_or_404

from announcements.models import Announcement, current_announcements_for_request

try:
    set
except NameError:
    from sets import Set as set   # Python 2.3 fallback


def announcement_list(request):
    """
    A basic view that wraps ``django.views.list_detail.object_list`` and
    uses ``current_announcements_for_request`` to get the current
    announcements.
    """
    queryset = current_announcements_for_request(request)
    return list_detail.object_list(request, **{
        "queryset": queryset,
        "allow_empty": True,
        "paginate_by": getattr(settings, "ANNOUNCEMENTS_PER_PAGE", 10),
    })


def announcement_hide(request, object_id):
    """
    Mark this announcement hidden in the session for the user.
    """
    announcement = get_object_or_404(Announcement, pk=object_id)
    
    # TODO: perform some basic security checks here to ensure next is not bad
    redirect_to = request.GET.get("next")
    if not announcement.is_dismissable:
        messages.add_message(request, messages.ERROR, 'The announcement "%s" cannot be dismissed.' % announcement)
    else:
        if request.user.is_authenticated():
            announcement.dismissals.add(request.user)
            announcement.save()
        else:
            excluded_announcements = request.session.get("excluded_announcements", set())
            excluded_announcements.add(announcement.pk)
            request.session["excluded_announcements"] = excluded_announcements
        
    return HttpResponseRedirect(redirect_to)
