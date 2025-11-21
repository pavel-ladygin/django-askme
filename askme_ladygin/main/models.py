from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q



class QuestionManager(models.Manager):
    def new(self):
        return self.get_queryset().order_by("-created")
    
    def hot(self):
        return self.get_queryset().order_by("-score")
    
    def by_tag(self, tag_slug):
        return self.get_queryset().filter(tags__slug = tag_slug).distinct()
    
    def by_id(self, pk):
        return self.get_queryset().filter(id=pk).first()


class TagManager(models.Manager):
    def slug_to_name(self, slug):
        return self.get_queryset().get(slug=slug).name
    
    def popular(self, n):
        return self.get_queryset().annotate(num_questions=models.Count("questions")).order_by("-num_questions")[:n]

class AnswerManager(models.Manager):
    def for_question(self, question):
        return self.get_queryset().filter(question=question).order_by("-score", "-is_accepted")



class Tag(models.Model):
    name = models.CharField(verbose_name="Название", unique=True, max_length=64)
    slug = models.SlugField(verbose_name="Слаг", unique=True, max_length=64)

    objects = TagManager()

    def __str__(self):
            return self.name
            

class Question(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name="Название вопроса", max_length=225, db_index=True)
    text = models.TextField(verbose_name="Текст вопроса")
    tags = models.ManyToManyField(Tag, related_name="questions", blank=True, verbose_name="Теги")
    views = models.PositiveIntegerField(verbose_name="Просмотры", default=0)
    score = models.IntegerField(verbose_name="Оценка", default=0, db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="questions", verbose_name="Автор")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    objects = QuestionManager()
    def __str__(self):
        return self.title



class Answer(models.Model):
    id = models.BigAutoField(primary_key=True)
    text = models.TextField(verbose_name="Текст ответа")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answers", verbose_name="Автор")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    score = models.IntegerField(verbose_name="Оценка", default=0, db_index=True)
    is_accepted = models.BooleanField(verbose_name="Продтвержение", default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers", verbose_name="Вопрос")

    objects = AnswerManager()
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["question"],
                condition=Q(is_accepted=True),
                name="unique_accepted_answer_per_question",
            )
        ]
    def __str__(self):
        return f"Ответ '{self.question.title}' от {self.author.username}"
    



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", verbose_name="Пользователь")
    avatar = models.URLField(blank=True, verbose_name="Аватар")

    def __str__(self):
        return self.user.username


class Votes(models.IntegerChoices):
    """ Наседованный класс для хранения вариантов голоса для ответов и вопросов """
    UP = 1, "UP"
    DOWN = -1, "DOWN"



class Votes(models.IntegerChoices):
    """ Наседованный класс для хранения вариантов голоса для ответов и вопросов """
    UP = 1, "UP"
    DOWN = -1, "DOWN"


class QuestionLike(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="question_likes", verbose_name="Пользователь")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="likes", verbose_name="Вопрос")
    value = models.SmallIntegerField(choices=Votes.choices, default=Votes.UP, verbose_name="Значение голоса")
        
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "question"], name="unique_user_question_like")
        ]

    def __str__(self):
        return f"Лайк от {self.user.username} для вопроса {self.question.title}"

class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answer_likes", verbose_name="Пользователь")
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="likes", verbose_name="Ответ")
    value = models.SmallIntegerField(choices=Votes.choices, default=Votes.UP, verbose_name="Значение голоса")


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "answer"], name="unique_user_answer_like")
        ]
    def __str__(self):
        return f"Лайк от {self.user.username} для ответа {self.answer.id}"