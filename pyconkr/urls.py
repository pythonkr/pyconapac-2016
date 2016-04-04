from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.flatpages import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required

from .views import index, schedule, robots
from .views import RoomDetail
from .views import AnnouncementList, AnnouncementDetail
from .views import SpeakerList, SpeakerDetail, SpeakerUpdate
from .views import SponsorList, SponsorDetail
from .views import ProgramList, ProgramDetail, ProgramUpdate
from .views import ProposalCreate, ProposalUpdate, ProposalDetail
from .views import ProfileDetail, ProfileUpdate
from .views import login, login_req, login_mailsent, logout

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^$', index, name='index'),

    url(r'^room/(?P<pk>\d+)$',
        RoomDetail.as_view(), name='room'),
    url(r'^about/announcements/$',
        AnnouncementList.as_view(), name='announcements'),
    url(r'^about/announcement/(?P<pk>\d+)$',
        AnnouncementDetail.as_view(), name='announcement'),
    url(r'^about/sponsors/$',
        SponsorList.as_view(), name='sponsors'),
    url(r'^about/sponsor/(?P<slug>\w+)$',
        SponsorDetail.as_view(), name='sponsor'),
    url(r'^programs/list/$',
        ProgramList.as_view(), name='programs'),
    url(r'^program/(?P<pk>\d+)$',
        ProgramDetail.as_view(), name='program'),
    url(r'^program/(?P<pk>\d+)/edit$',
        ProgramUpdate.as_view(), name='program_edit'),
    url(r'^programs/speakers/$',
        SpeakerList.as_view(), name='speakers'),
    url(r'^programs/speaker/(?P<slug>\w+)$',
        SpeakerDetail.as_view(), name='speaker'),
    url(r'^programs/speaker/(?P<slug>\w+)/edit$',
        SpeakerUpdate.as_view(), name='speaker_edit'),
    url(r'^programs/schedule/$',
        schedule, name='schedule'),
    url(r'^cfp/propose/$',
        login_required(ProposalCreate.as_view()), name='propose'),
    url(r'^profile/proposal/$',
        login_required(ProposalDetail.as_view()), name='proposal'),
    url(r'^profile/proposal/edit$',
        login_required(ProposalUpdate.as_view()), name='proposal-update'),
    url(r'^profile$',
        login_required(ProfileDetail.as_view()), name='profile'),
    url(r'^profile/edit$',
        login_required(ProfileUpdate.as_view()), name='profile_edit'),

    url(r'^login/$', login, name='login'),
    url(r'^login/req/(?P<token>[a-z0-9\-]+)$', login_req, name='login_req'),
    url(r'^login/mailsent/$', login_mailsent, name='login_mailsent'),
    url(r'^logout/$', logout, name='logout'),

    url(r'^registration/', include('registration.urls')),
    url(r'^robots.txt$', robots, name='robots'),
    url(r'^summernote/', include('django_summernote.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/', include('allauth.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]

# for development
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# for rosetta
if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        url(r'^rosetta/', include('rosetta.urls')),
    ]

# for flatpages
urlpatterns += [
    url(r'^(?P<url>.*/)$', views.flatpage),
]
