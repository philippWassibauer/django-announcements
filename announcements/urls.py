from django.conf.urls.defaults import *
from django.views.generic import list_detail

from announcements.models import Announcement
from announcements.views import *


announcement_detail_info = {
    "queryset": Announcement.objects.all(),
}

announcement_info = {
    "queryset": Announcement.objects.all(),
    "allow_empty": True,
    "paginate_by": getattr(settings, "ANNOUNCEMENTS_PER_PAGE", 10),
}

urlpatterns = patterns("",
    url(r"^(?P<object_id>\d+)/$", list_detail.object_detail,
        announcement_detail_info, name="announcement_detail"),
    url(r"^$", list_detail.object_list,
        announcement_info, name="announcement_home"),
    url(r"^(?P<object_id>\d+)/hide/$", announcement_hide,
        name="announcement_hide"),
    url(r"^current/$", announcement_current_list, name="announcement_current"),
)
