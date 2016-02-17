from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^enter-tips/$', views.enter_tips, name='enter-tips'),
    # url(r'^edit-tips/$', views.edit_tips, name='edit-tips'),
    url(r'^summary/$', views.tips_summary, name='tips-summary'),
    url(r'^user-test/$', views.user_test, name='user-test'),
    # url(r'^budget/$', views.budget, name='budget'),
    url(r'^expenses/$', views.view_expenses, name='view-expenses'),
    url(r'^enter-expenses/$', views.enter_expenses, name='enter-expenses'),
    # url(r'^edit-expenses/$', views.edit_expenses, name='edit-expenses'),
    url('^', include('django.contrib.auth.urls')),
]
