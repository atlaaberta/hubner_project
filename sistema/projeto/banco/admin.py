from banco.models import *
from django.contrib import admin
from django.contrib.auth.models import User

class UserInline(admin.TabularInline):
	model = User

class TesteInline(admin.TabularInline):
	model = Disciplina

#class AlunoAdmin(admin.ModelAdmin):
#	inlines = {
#		TesteInline,
#	}	

#class DisciplinaAdmin(admin.ModelAdmin):
#	inlines = {
#		TesteInline,
#	}
#	exclude = ('participantes',)
#	filter_horizontal = ('participantes',)

#class CursoAdmin(admin.ModelAdmin):
#	filter_horizontal = ('professores',)

#class AlunoAdmin(admin.ModelAdmin):
#	inlines = {
#		UserInline,	
#	}


class QuestaoAdmin(admin.ModelAdmin):
	filter_horizontal = ('disciplinas',)


#admin.site.register(Professor)
#admin.site.register(Curso, CursoAdmin)
#admin.site.register(Aluno)
admin.site.register(Disciplina)
admin.site.register(Monitor)
admin.site.register(Tema)
admin.site.register(TipoTema)
admin.site.register(Questao,QuestaoAdmin)
