from django.contrib.auth import views
from django.contrib import admin
from django.urls import path, include, re_path
import donation.views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'donation'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', donation.views.home_page, name='main'),
    path('request/donate', donation.views.described_item),
    path('request/donate_amount', donation.views.request),
    path('request/donation', donation.views.donation),
    path('list', donation.views.list, name='list'),
    path('set_office', donation.views.session_office, name='set_session_office'),
    path('request/number', donation.views.request),
    re_path('request/correct_request/(?P<req_id>[\d-]+)', donation.views.correct_request),
    path('request/criterion_list', donation.views.criterion),
    path('api/', include('tutorial.quickstart.urls', namespace='api')),
    path('login/', views.LoginView.as_view(), name='login'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
