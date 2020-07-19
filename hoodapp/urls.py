from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns=[
    url(r'^$',views.index,name = 'index'),    
    url(r'^sendemail/$',views.send_email,name = 'send-email'),
    url(r'^create-profile-admin/$',views.create_profile_admin,name = 'create-profile-admin'),
    # url(r'^myprofile/$',views.my_profile,name = 'my-profile'),
    # url(r'^uploadproject/$',views.upload_project,name = 'upload-project'),
    # url(r'^deleteproject/(\d+)',views.delete_project,name = 'delete-project'),
    # url(r'^updatedescription/(\d+)',views.update_description,name = 'update-description'),
    # url(r'^changeprofilephoto/$',views.change_profile_photo,name = 'change-profile-photo'),
    # url(r'^deleteprofile/$',views.delete_profile,name = 'delete-profile'),
    # url(r'^search/$',views.search_project,name = 'search-project'),
    # url(r'^userprofile/(\d+)',views.user_profile,name = 'user-profile'),
    # url(r'^viewproject/(\d+)',views.view_project,name = 'view-project'),
    # url(r'^ajax/rateproject/$', views.rate_project, name='rate-project'),    
    # url(r'^api/profiles/$', views.ProfileList.as_view()),
    # url(r'^api/projects/$', views.ProjectList.as_view()),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)