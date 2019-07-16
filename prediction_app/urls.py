from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
from global_login_required import login_not_required


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<match_id>[0-9]+)/$', views.match_detail),
    url(r'^question/(?P<question_id>[0-9]+)/$', views.question_detail),
    url(r'^answer/(?P<question_id>[0-9]+)/$', views.answer),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^login/$', login_not_required(auth_views.LoginView.as_view(template_name='registration/login.html')), name='login'),
    url(r'^password_reset/$', auth_views.PasswordChangeView.as_view(), name='password_reset'),
    url(r'^user_info/$', views.user_info, name='user'),
     url(r'^get_model_data/$', views.get_model_data, name='model_data'),

    
]

