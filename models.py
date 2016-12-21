from django.db import models

# Create your models here.
class Professor(models.Model)
	nome = models.CharField(max_length=100)
	siape = models.IntergerField()
	email = models.CharField(max_length=100)
	def __unicode__(self)
		return self.nome

class Curso(models.Model):
	nome = models.CharField(max_length=100)
	codigo = models.CharField(max_length=25)
	professores = models.ManyToManyField(Professor, through='Professor_Curso')
	def __unicode__(self)
		return self.nome

class Aluno(models.Model)
	nome = models.CharField(max_length=100)
	codigo = models.CharField(max_length=25)
	email = models.CharField(max_length=100)
	def __unicode__(self)
		return self.nome

class Disciplina(models.Model)
	nome = models.CharField(max_length=100)
	codigo = models.CharField(max_length=25)
	periodo = models.IntegerField()
	participantes = models.ManyToManyField(Aluno, through='Turma')
	models.ForeignKey(Curso)
	models.ForeignKey(Professor)
	def __unicode__(self)
		return self.nome

class Turma(models.Model)
	disciplina = models.ForeignKey(Disciplina)
	aluno = models.ForeignKey(Aluno)
	codigo = models.CharField(max_length=25)
	def __unicode__(self)
		return self.codigo

class Monitor(models.Model)
	models.ForeignKey(Aluno)

class Professor_Curso(models.Model)
	professor = models.ForeignKey(Professor)
	curso = models.ForeignKey(Curso)

class Tema(models.Model)
	descricao = models.CharField(max_length=200)
	codigo = models.CharField(max_length=25)
	def __unicode__(self)
		return self.codigo

class Questionario(models.Model)
	tema = models.ForeignKey(Tema)
	disciplina = models.ForeignKey(Disciplina)
	num_questoes = models.IntergerField()
	titulo = models.CharField(max_length=50)
	def __unicode__(self)
		return self.titulo

class Questao(models.Model)
	questionario = models.ForeignKey(Questionario)
	descricao = models.CharField(max_length=1000)
	titulo = models.CharField(max_length=200)
	def __unicode__(self)
		return self.titulo

class Forum(models.Model)
	questao = models.ForeignKey(Questao)
	monitor = models.ForeignKey(Monitor)
	resposta = models.CharField(max_length=1000)
	data_resposta = models.DateTimeField('Data de resposta:')
