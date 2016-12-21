from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#class Professor(models.Model):
#	nome = models.CharField(max_length=100)
#	siape = models.IntegerField()
#	email = models.EmailField(max_length=100)
#	def __unicode__(self):
#		return self.nome

#class Curso(models.Model):
#	nome = models.CharField(max_length=100)
#	codigo = models.CharField(max_length=25)
#	professores = models.ManyToManyField(Professor)
#	def __unicode__(self):
#		return self.nome

#class Aluno(models.Model):
#	user = models.OneToOneField(User)
#	nome = models.CharField(max_length=100)
#	codigo = models.CharField(max_length=25)
#	email = models.EmailField(max_length=100)
#	def __unicode__(self):
#		return self.nome

#def create_user_aluno(sender, instance, created, **kwargs):
 #   if created:
 #       Aluno.objects.create(user=instance)

#post_save.connect(create_user_aluno, sender=User)

class Disciplina(models.Model):
	nome = models.CharField(max_length=100)
	codigo = models.CharField(max_length=25)
	def __unicode__(self):
		return self.nome

class Monitor(models.Model):
	usuario = models.ForeignKey(User)
	materia = models.ForeignKey(Disciplina)
	def __unicode__(self):
		return self.usuario.username

class TipoTema(models.Model):
	descricao = models.CharField(max_length=200)
	def __unicode__(self):
		return self.descricao

class Tema(models.Model):
	tema = models.ForeignKey(TipoTema)
	descricao = models.CharField(max_length=200)
	codigo = models.CharField(max_length=25)
	def __unicode__(self):
		return self.codigo

class Questao(models.Model):
	tema = models.ForeignKey(Tema)
	descricao = models.TextField(max_length=1000)
	titulo = models.CharField(max_length=200)
	dificuldade = models.IntegerField()
	data_cadastro = models.DateTimeField('Data de cadastro:')
	disciplinas = models.ManyToManyField(Disciplina)
	def __unicode__(self):
		return self.titulo


class Publicacao(models.Model):
	titulo = models.CharField(max_length=254)
	questao = models.ForeignKey(Questao)
	tipo = models.IntegerField()
	autor = models.ForeignKey(User)
	linguagem = models.CharField(max_length=50)
	status = models.BooleanField(default=False)
	codigo = models.CharField(max_length=10000)
	duvida = models.CharField(max_length=1000)
	dificuldade = models.IntegerField()
	data_publicacao = models.DateTimeField('Data de publicacao:')

class Resposta(models.Model):
	publicacao = models.ForeignKey(Publicacao)
	data_resposta = models.DateTimeField('Data de resposta:')
	resposta = models.CharField(max_length=1000)
	autor = models.ForeignKey(User)
	codigo = models.CharField(max_length=10000)
class Curtida(models.Model):
	resposta = models.ForeignKey(Resposta)
	autor = models.ForeignKey(User)
