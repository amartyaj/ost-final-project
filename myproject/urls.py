from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('myproject',
    # Examples:
    # url(r'^$', 'myproject.views.home', name='home'),
    # url(r'^myproject/', include('myproject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'finalproject.views.home'),
    url(r'^questions$', 'finalproject.views.home'),
    url(r'^questions/$', 'finalproject.views.home'),
    url(r'^questions/add_question$', 'finalproject.views.add_question_login_form'),
    url(r'^questions/edit_question/(\d*)$', 'finalproject.views.edit_question_login_form'),
    url(r'^questions/answers/(\d*)$', 'finalproject.views.view_question'),
)
