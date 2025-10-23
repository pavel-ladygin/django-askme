from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q


class Tag(models.Model):
    name = models.CharField("Название", unique=True, max_length=64)
    slug = models.SlugField("Слаг", unique=True, max_length=64)

'''         "id" : i,
            "title" : f"Название вопроса номер {i}",
            "text" : f"Описание вопроса {i}, что то должно быть написано",
            "tags" : [tags[rnd.randint(0, len(tags)/2)], tags[rnd.randint(len(tags)/2, len(tags)-1)]],
            "ansver_count" : rnd.randint(0, 10),
            "views" : rnd.randint(1, 1000),
            "score" : rnd.randint(-5, 100),
            "author" : authors[rnd.randint(0, len(authors)-1)],
            "created" : f"{time[rnd.randint(0, len(time)- 1)]} назад",
'''


class Question(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField("Название вопроса", max_length=225)
    text = models.TextField("Текст вопроса")
    tags = models.ManyToManyField(Tag, related_name="questions")
    ansver_count = models.IntegerField("Ответы")
    views = models.PositiveIntegerField("Просмотры", default=0)
    score = models.IntegerField("Оценка", default=0, db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="questions")
    created = models.DateTimeField(auto_now_add=True)




'''         "id" : i,
            "text" : f"Какой то текст {i}-го ответа на вопрос номер {pk}",
            "author" : authors[rnd.randint(0, len(authors)-1)],
            "created" : f"{time[rnd.randint(0, len(time)- 1)]} назад",
            "score" : rnd.randint(-5, 100),
            "is_accepted": rnd.choice([True, False])
'''


class Answer(models.Model):
    id = models.BigAutoField(primary_key=True)
    text = models.TextField("Текст ответа")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answers")
    created = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField("Оценка")
    is_accepted = models.BooleanField("Продтвержение")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="questions")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["question"],
                condition=Q(is_accepted=True),
                name="unique_accepted_answer_per_question",
            )
        ]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.URLField(blank=True)

class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="question_likes", )
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="question_likes")
        
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "answer"], name="unique_user_question_like")
        ]

class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answer_likes")
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="answer_likes")
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "answer"], name="unique_user_answer_like")
        ]
