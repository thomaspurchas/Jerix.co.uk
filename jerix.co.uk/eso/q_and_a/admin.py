from django.contrib import admin

from q_and_a.models import Question, Answer

class AnswerInline(admin.TabularInline):
    """docstring for SubPostInline"""
    model = Answer
    fk_name = 'question'
    extra = 2
    classes = ['collapse', 'collapsed']
    exclude = ['reputation_owner', 'reputation']

class QuestionAdmin(admin.ModelAdmin):
    exclude = ['reputation_owner', 'reputation']
    readonly_fields = ['current_vote']
    inlines = [AnswerInline]

class AnswerAdmin(admin.ModelAdmin):
    exclude = ['reputation_owner', 'reputation']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)