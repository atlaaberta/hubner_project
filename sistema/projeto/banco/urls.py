from django.conf.urls import patterns, url
from banco import views
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('banco.views',
	url(r'^$', views.index, name='index'),
	url(r'^sair/$', views.sair, name='sair'),
	url(r'^alterarsenha/$', views.alterasenha, name='altsenha'),
	url(r'^temas/$', login_required(views.tipo_temas), name='temas'),
	url(r'^forum/(?P<termo>\w+)/(?P<pagina_id>\d+)$', login_required(views.inicio_forum), name='forum'),
	url(r'^postagem/(?P<publicacao_id>\d+)$', login_required(views.forum_pergunta), name='repostaforum'),
	url(r'^temas/(?P<tipotema_id>\d+)$', login_required(views.temasespecificos), name='temasespecificos'),
	url(r'^questoes/(?P<tema_id>\d+)/(?P<pagina_id>\d+)$', login_required(views.listaquestoes), name='listaquestoes'),
	url(r'^questao/(?P<questao_id>\d+)$', login_required(views.questao), name='questao'),

)
