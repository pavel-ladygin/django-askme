from django.contrib import admin
from .models import Answer, Question, QuestionLike, AnswerLike, Profile, Tag


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    fields = ["text", "author", "is_accepted", "score", "created"]
    readonly_fields = ["created"]
    autocomplete_fields = ["author"]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'created', 'views', 'score']
    list_filter = ['created', 'tags']
    search_fields = ['title', 'text', 'author__username', 'tags__name']
    ordering = ['-created']
    inlines = [AnswerInline]
    autocomplete_fields = ['author', 'tags']
    def answers_count(self, obj):
        return obj.answers.count()
    answers_count.short_description = "Ответов"

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ["id", "question", "author", "created", "is_accepted", "score"]
    list_filter = ["is_accepted", "created", "score"]
    search_fields = ["text", "question__title", "author__username"]
    autocomplete_fields = ["question", "author"]
    ordering = ["-created"]



@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    search_fields = ['name', 'slug']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'avatar']

@admin.register(AnswerLike)
class AnswerLikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'answer', 'user', 'value']

@admin.register(QuestionLike)
class QuestionLikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'user', 'value']
