from django.contrib import admin
from .models import Answer, Question, QuestionLike, AnswerLike, Profile, Tag

admin.site.register(Tag)
admin.site.register(Profile)
admin.site.register(AnswerLike)
admin.site.register(QuestionLike)
admin.site.register(Question)
admin.site.register(Answer)



