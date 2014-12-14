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
    url(r'^questions/(\d+)$', 'finalproject.views.view_question'),
    url(r'^questions/add_question$', 'finalproject.views.add_question_login_form'),
    url(r'^questions/edit_question/(\d+)$', 'finalproject.views.edit_question_login_form'),
    url(r'^questions/add_answer/(\d+)$', 'finalproject.views.add_answer_login_form'),
    url(r'^questions/edit_answer/(\d+)$', 'finalproject.views.edit_answer_login_form'),
    url(r'^questions/question_vote_up/(\d+)$', 'finalproject.views.question_vote_up_login_form'),
    url(r'^questions/question_vote_down/(\d+)$', 'finalproject.views.question_vote_down_login_form'),
    url(r'^questions/answer_vote_up/(\d+)$', 'finalproject.views.answer_vote_up_login_form'),
    url(r'^questions/answer_vote_down/(\d+)$', 'finalproject.views.answer_vote_down_login_form'),
    url(r'^questions/tag_questions/(\w+)$', 'finalproject.views.tag_questions'),
    url(r'^questions/rss_feed/(\d+)$', 'finalproject.views.rss_feed'),
    url(r'^questions/upload_image/(\w+)$', 'finalproject.views.upload_image'),
    url(r'^questions/retrieve_image$', 'finalproject.views.retrieve_image'),
)
