from django.contrib import admin

from q_and_a.models import Question, Answer

class QuestionAdmin(admin.ModelAdmin):
    exclude = ['reputation_owner', 'reputation']
    readonly_fields = ['current_vote']

class AnswerAdmin(admin.ModelAdmin):
    exclude = ['reputation_owner', 'reputation']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)