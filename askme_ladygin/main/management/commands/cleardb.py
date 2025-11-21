# main/management/commands/cleardb.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import Profile, Tag, Question, Answer, QuestionLike, AnswerLike

class Command(BaseCommand):
    help = "Полностью очищает БД от данных, кроме администраторов"

    def handle(self, *args, **options):
        self.stdout.write("ОЧИСТКА БД...")

        # Лайки
        deleted, _ = QuestionLike.objects.all().delete()
        self.stdout.write(f"Удалено лайков к вопросам: {deleted}")
        deleted, _ = AnswerLike.objects.all().delete()
        self.stdout.write(f"Удалено лайков к ответам: {deleted}")

        # Ответы и вопросы
        deleted, _ = Answer.objects.all().delete()
        self.stdout.write(f"Удалено ответов: {deleted}")
        deleted, _ = Question.objects.all().delete()
        self.stdout.write(f"Удалено вопросов: {deleted}")

        # Теги (если нет других зависимостей)
        deleted, _ = Tag.objects.all().delete()
        self.stdout.write(f"Удалено тегов: {deleted}")


        # Юзеры, исключая суперпользователей
        deleted, _ = User.objects.filter(is_superuser=False).delete()
        self.stdout.write(f"Удалено обычных пользователей: {deleted}")

        self.stdout.write(self.style.SUCCESS("Очистка БД завершена."))
