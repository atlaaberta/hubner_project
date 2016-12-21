# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as logar, logout, authenticate
from django.contrib import auth
from django.shortcuts import get_object_or_404, render_to_response, render
from banco.models import *
from random import randint
from django.core.mail import send_mail
import datetime
from django.db.models import Q
from django.db.models import Count, Avg


def index(request):
	if request.method == 'POST':
                username = request.POST.get('username', '')
                password = request.POST.get('password', '')
		user = auth.authenticate(username=username, password=password)
		if user is not None:
			auth.login(request, user)
                        return HttpResponseRedirect("/banco/temas/")
                else:
                        return render(request, "login.html")
	return render(request, "login.html")

def sair(request):
	logout(request)
	return HttpResponseRedirect("/banco")

@login_required
def inicio_forum(request, termo, pagina_id):
	res = Resposta.objects.values('publicacao').annotate(Count('publicacao'))
	melhores = Resposta.objects.values('autor').annotate(Count('autor')).order_by('-autor__count')
	pagina = int(pagina_id)
	intervaloi = (pagina-1) * 10
	intervalof = pagina * 10
	usuarios = User.objects.all()
	if request.method == 'POST':
		busca = request.POST.get('busca', '')
		if busca == '1':
			valor = request.POST.get('texto', '')
			publicacoes = Publicacao.objects.filter(Q(duvida__contains=valor) | Q(titulo__contains=valor)).order_by('-data_publicacao')
			totalq = int(Publicacao.objects.filter(Q(duvida__contains=valor) | Q(titulo__contains=valor)).count())
			npage = totalq/10
			rest = totalq%10
			if(rest>0):
				npage = npage + 1
			return render(request,"foruminicio.html",{'publicacoes':publicacoes, 'resp':res, 'npages':npage,'page':pagina})
	if(termo=='solucao'):
		publicacoes = Publicacao.objects.filter(tipo=1).order_by('-data_publicacao')[intervaloi:intervalof]
		totalq = int(Publicacao.objects.filter(tipo=1).count())
		npage = totalq/10
		rest = totalq%10
		if(rest>0):
			npage = npage + 1
		return render(request,"foruminicio.html",{'publicacoes':publicacoes,'termo':'solucao','melhores':melhores, 'users':usuarios,'npages':npage,'page':pagina})
	if(termo=='duvida'):
		publicacoes = Publicacao.objects.filter(tipo=2).order_by('-data_publicacao')[intervaloi:intervalof]
		totalq = int(Publicacao.objects.filter(tipo=2).count())
		npage = totalq/10
		rest = totalq%10
		if(rest>0):
			npage = npage + 1
		return render(request,"foruminicio.html",{'publicacoes':publicacoes,'termo':'duvida','melhores':melhores, 'users':usuarios,'npages':npage,'page':pagina})
	if(termo=='java'):
		publicacoes = Publicacao.objects.filter(linguagem='java').order_by('-data_publicacao')[intervaloi:intervalof]
		totalq = int(Publicacao.objects.filter(linguagem='java').count())
		npage = totalq/10
		rest = totalq%10
		if(rest>0):
			npage = npage + 1
		return render(request,"foruminicio.html",{'publicacoes':publicacoes,'termo':'java','melhores':melhores, 'users':usuarios,'npages':npage,'page':pagina})
	if(termo=='python'):
		publicacoes = Publicacao.objects.filter(linguagem='python').order_by('-data_publicacao')[intervaloi:intervalof]
		totalq = int(Publicacao.objects.filter(linguagem='python').count())
		npage = totalq/10
		rest = totalq%10
		if(rest>0):
			npage = npage + 1
		return render(request,"foruminicio.html",{'publicacoes':publicacoes,'termo':'python','melhores':melhores, 'users':usuarios,'npages':npage,'page':pagina})
	if(termo=='c'):
		publicacoes = Publicacao.objects.filter(linguagem='mode-c_cpp').order_by('-data_publicacao')[intervaloi:intervalof]
		totalq = int(Publicacao.objects.filter(linguagem='mode-c_cpp').count())
		npage = totalq/10
		rest = totalq%10
		if(rest>0):
			npage = npage + 1
		return render(request,"foruminicio.html",{'publicacoes':publicacoes,'termo':'mode-c_cpp','melhores':melhores, 'users':usuarios,'npages':npage,'page':pagina})
	if(termo=='javascript'):
		publicacoes = Publicacao.objects.filter(linguagem='javascript').order_by('-data_publicacao')[intervaloi:intervalof]
		totalq = int(Publicacao.objects.filter(linguagem='javascript').count())
		npage = totalq/10
		rest = totalq%10
		if(rest>0):
			npage = npage + 1
		return render(request,"foruminicio.html",{'publicacoes':publicacoes,'termo':'javascript','melhores':melhores, 'users':usuarios,'npages':npage,'page':pagina})	
	if(termo=='sql'):
		publicacoes = Publicacao.objects.filter(linguagem='sql').order_by('-data_publicacao')[intervaloi:intervalof]
		totalq = int(Publicacao.objects.filter(linguagem='sql').count())
		npage = totalq/10
		rest = totalq%10
		if(rest>0):
			npage = npage + 1
		return render(request,"foruminicio.html",{'publicacoes':publicacoes,'termo':'sql','melhores':melhores, 'users':usuarios,'npages':npage,'page':pagina})	
	publicacoes = Publicacao.objects.all().order_by('-data_publicacao')[intervaloi:intervalof]
	totalq = int(Publicacao.objects.count())
	npage = totalq/10
	rest = totalq%10
	if(rest>0):
		npage = npage + 1
	return render(request,"foruminicio.html",{'publicacoes':publicacoes,'resp':res,'termo':'tudo','melhores':melhores, 'users':usuarios,'npages':npage,'page':pagina})

@login_required
def forum_pergunta(request, publicacao_id):
	melhores = Resposta.objects.values('autor').annotate(Count('autor')).order_by('-autor__count')
	usuarios = User.objects.all()
	publicacao = Publicacao.objects.get(pk = publicacao_id)
	vars = {}
	if request.method == 'POST':
		tipo = request.POST.get('tip', '')
		if tipo == 'curtir':
			user = request.user
			aux = int(request.POST.get('resp', ''))
			resposta = Resposta.objects.get(pk = aux)
			try:
				user_liked = Curtida.objects.get(resposta=resposta, autor=user)
			except:
				user_liked = None

			if user_liked:
				user_liked.delete()
			else:
				cur = Curtida(resposta=resposta, autor=user)
				cur.save()
		elif tipo == 'apagar':
			user = request.user
			aux = int(request.POST.get('resp', ''))
			resposta = Resposta.objects.get(pk = aux)
			Curtida.objects.filter(resposta=resposta).delete()
			resposta.delete()
		elif tipo == 'concl':
			user = request.user
			aux = int(request.POST.get('pub', ''))
			pub = Publicacao.objects.get(pk = aux)
			pub.status = True
			pub.save()
		else:
			cod = request.POST.get('codigo', '')
			res = request.POST.get('resposta', '')
			usuario = request.user
			aux = int(request.POST.get('publicacao', ''))
			pub = Publicacao.objects.get(pk = aux)
			dat = datetime.datetime.now()
			res = Resposta(codigo = cod, resposta = res, autor = usuario, data_resposta = dat, publicacao = pub)
			res.save()
	lista_curtidas = Curtida.objects.values('resposta').annotate(Count('resposta')).order_by('-resposta__count')
	curtidas = Curtida.objects.all()
	lista_respostas = Resposta.objects.filter(publicacao=publicacao_id).order_by('data_resposta')
	lista_aux = []
	if lista_curtidas:
		for cur in lista_curtidas:
			aux = int(cur['resposta'])
			for res in lista_respostas:		
				if res.id == aux:
					lista_aux.append(res)
	for res2 in lista_respostas:
		if res2 not in lista_aux:
			lista_aux.append(res2)
		
	return render(request,"forumpergunta.html",{'publicacao': publicacao,'lista_respostas': lista_aux,'melhores':melhores, 'users':usuarios,'cur':lista_curtidas,'curtidas':curtidas})

@login_required
def tipo_temas(request):
	lista_questoes = Questao.objects.all().order_by('-data_cadastro')[:5]
	lista_forum = Publicacao.objects.all().order_by('-data_publicacao')[:5]
	lista_tipo_tema=TipoTema.objects.all().order_by('descricao')
	return render_to_response('temas.html',{'lista_tipo_tema': lista_tipo_tema,'lista_questao': lista_questoes, 'publicacoes':lista_forum})

@login_required
def temasespecificos(request, tipotema_id):
	lista_questoes = Questao.objects.filter().order_by('data_cadastro')[:5]
	lista_temas=Tema.objects.filter(tema=tipotema_id).order_by('descricao')
	tema = TipoTema.objects.get(pk = tipotema_id)
	page = 1
	lista_forum = Publicacao.objects.all().order_by('-data_publicacao')[:5]
	return render_to_response('temasespecificos.html',{'lista_temas': lista_temas, 'lista_questao': lista_questoes, 'tema':tema, 'publicacoes':lista_forum, 'page':page})

@login_required
def listaquestoes(request, tema_id, pagina_id):
	tema = Tema.objects.get(pk = tema_id)
	pagina = int(pagina_id)
	rating = Publicacao.objects.values('questao').annotate(Avg('dificuldade'))
	intervaloi = (pagina-1) * 10
	intervalof = pagina * 10
	if request.method == 'POST':
		valor = request.POST.get('texto', '')
		questoes = Questao.objects.filter(Q(descricao__contains=valor) | Q(titulo__contains=valor)).order_by('-data_cadastro')
		totalq = int(Questao.objects.filter(Q(descricao__contains=valor) | Q(titulo__contains=valor)).count())
		npage = totalq/10
		rest = totalq%10
		if(rest>0):
			npage = npage + 1
		return render(request,'listaquestao.html',{'questoes': questoes, 'tema':tema, 'rating':rating,'npages':npage,'page':pagina})
	totalq = int(Questao.objects.count())
	npage = totalq/10
	rest = totalq%10
	if(rest>0):
		npage = npage + 1
	lista_questoes=Questao.objects.filter(tema=tema_id).order_by('titulo').order_by('-data_cadastro')[intervaloi:intervalof]
	return render(request,'listaquestao.html',{'questoes': lista_questoes, 'tema':tema, 'rating':rating,'npages':npage,'page':pagina})

@login_required
def questao(request, questao_id):
	c = {}
	c.update(csrf(request))
	if request.method == 'POST':
		logica = request.POST.get('duvida', '')
		if(logica == '0'):
                	tit = request.POST.get('titulo', '')
			aux = int(request.POST.get('questao', ''))
                	que = Questao.objects.get(pk = aux)
			tip = int(request.POST.get('tipo', ''))
			ling = request.POST.get('linguagem', '')
			sta = False
			usuario = request.user
			cod = request.POST.get('codigo', '')
			duv = request.POST.get('problema', '')
			dif = int(request.POST.get('dificuldade', ''))
		else: 
			tit = request.POST.get('titulod', '')
			aux = int(request.POST.get('questaod', ''))
                	que = Questao.objects.get(pk = aux)
			tip = int(request.POST.get('tipod', ''))
			ling = request.POST.get('linguagemd', '')
			sta = False
			usuario = request.user
			cod = request.POST.get('codigod', '')
			duv = request.POST.get('duvidad', '')
			dif = int(request.POST.get('dificuldaded', ''))
		dat = datetime.datetime.now()
		pub = Publicacao(titulo = tit, questao = que, tipo = tip, autor = usuario, linguagem = ling, status = sta, codigo = cod, duvida = duv, dificuldade = dif, data_publicacao = dat)
		disciplinas = que.disciplinas.all()
		if disciplinas:
			for d in disciplinas:
				monitor = Monitor.objects.get(materia = d)
				print(monitor.usuario.email)
				send_mail('Forum Recursos digitais','Ha uma nova duvida ou solucao no forum em relacao a sua monitoria.','edukempf@outlook.com',[monitor.usuario.email],fail_silently=False)
		pub.save()
		return HttpResponseRedirect("/banco/forum/tudo/1")
	questao = Questao.objects.get(pk = questao_id)
	return render(request,'questao.html',{'questao': questao})

@login_required
def alterasenha(request):
	if request.method == 'POST':
		npass = request.POST.get('npass', '')
		u = User.objects.get(username=request.user)
		u.set_password(npass)
		u.save()
		return HttpResponseRedirect("/banco/temas/")
	return render(request,'alterarsenha.html')
