from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import Profile, Tag, Question, Answer, QuestionLike, AnswerLike, Votes
from django.db.models import Sum
from django.utils.text import slugify
import time
from django.db import transaction

from faker import Faker
import random

class Command(BaseCommand):
    help = "Создаёт тестовых пользователей"

    def add_arguments(self, parser):
        parser.add_argument("ratio", type=int, help="Количество создаваемых пользователей")

    def handle(self, *args, **kwargs):
        start_time = time.time()
        ratio = kwargs["ratio"]
        fake_ru = Faker("ru_RU")
        fake_en = Faker("en_US")

        user_cnt = ratio
        question_cnt = ratio*10
        answer_cnt = ratio*100
        tag_cnt = ratio
        like_cnt = ratio*200

        # Создание пользователей
        users = []
        self.stdout.write("Создание пользователей..")
        for i in range(user_cnt):

            user, is_created = User.objects.get_or_create(
                username=f"user{i}",
                email=f"user{i}@example.com",
                password=f"passwd{i}"
            )
            
            if is_created:
                users.append(user)
            

        # Создание профилей
        for i in users:

            profile = Profile.objects.create(
                user=i,
                avatar=fake_en.image_url()
            )
 

        self.stdout.write(f"Создано пользователей: {len(users)}")


        # Создание тегов
        tags = []
        self.stdout.write("Создание тегов..")
        for i in range(tag_cnt):

            tag, is_created = Tag.objects.get_or_create(
                name=f"{fake_en.word()}{i}",
                slug=slugify(f"{fake_en.word()}{i}")
            )
            if is_created:
                tags.append(tag)
        self.stdout.write(f"Создано тегов: {len(tags)}")

        # Создание вопросов
        questions = []
        self.stdout.write("Создание вопросов..")
        for i in range(question_cnt):

            questions.append(
                Question(
                    title=fake_ru.sentence(nb_words=6),
                    text=fake_ru.paragraph(nb_sentences=5),
                    author=random.choice(users),
                    views=random.randint(0, 1000)
                )
            )
        Question.objects.bulk_create(questions, batch_size=question_cnt//10)


        # Добавление тегов к вопросам
        for q in questions:
            q.tags.set(random.sample(tags, k=random.randint(1, 3)))


        self.stdout.write(f"Создано вопросов: {len(questions)})")

        # Создание ответов
        answers = []
        self.stdout.write("Создание ответов..")

        for question in questions:
            num_answers = random.randint(1, 20)  # Случайное количество ответов
            
            question_answers = []
            for i in range(num_answers):
                question_answers.append(
                    Answer(
                        text=fake_ru.paragraph(nb_sentences=3),
                        author=random.choice(users),
                        question=question,
                        is_accepted=False
                    )
                )
            
            # Случайно выбираем один как принятый
            if random.random() < 0.4:
                question_answers[random.randint(0, num_answers - 1)].is_accepted = True

            answers.extend(question_answers)


        Answer.objects.bulk_create(answers, batch_size=10000)

        self.stdout.write(f"Создано ответов: {len(answers)}")


        # Создание лайков и дизлайков для вопросов
        self.stdout.write("Создание лайков и дизлайков..")
        question_votes = []
        for q in questions:
            voters = random.sample(users, k=random.randint(0, min(len(users) // 10, 10)))
            for user in voters:
                question_votes.append(
                    QuestionLike(
                        user=user,
                        question=q,
                        value=random.choice([Votes.UP, Votes.DOWN])
                    )
                )
        QuestionLike.objects.bulk_create(question_votes, batch_size=like_cnt//13)

        # Создание лайков и дизлайков для ответов
        answer_votes = []
        for a in answers:
            voters = random.sample(users, k=random.randint(0, min(len(users) // 10, 3)))
            for user in voters:
                answer_votes.append(
                    AnswerLike(
                        user=user,
                        answer=a,
                        value=random.choice([Votes.UP, Votes.DOWN])
                    )
                )

        AnswerLike.objects.bulk_create(answer_votes, batch_size=like_cnt//10)
        self.stdout.write(f"Создано лайков и дизлайков: {len(question_votes) + len(answer_votes)})")


        # Пересчёт рейтинга вопросов и ответов
        @transaction.atomic
        def recalc_score():
            self.stdout.write("Пересчёт рейтинга вопросов и ответов...")
            Question.objects.update(score=0)  # один UPDATE на всю таблицу

            qs = (
                QuestionLike.objects
                .values("question_id")
                .annotate(total=Sum("value"))
            )

            # Словарь id -> score
            q_scores = {row["question_id"]: row["total"] for row in qs}

            # Список объектов для bulk_update
            questions_to_update = [
                Question(id=qid, score=score)
                for qid, score in q_scores.items()
            ]
            Question.objects.bulk_update(questions_to_update, ["score"], batch_size=1000)

            # Ответы
            Answer.objects.update(score=0)

            as_ = (
                AnswerLike.objects
                .values("answer_id")
                .annotate(total=Sum("value"))
            )
            a_scores = {row["answer_id"]: row["total"] for row in as_}
            answers_to_update = [
                Answer(id=aid, score=score)
                for aid, score in a_scores.items()
            ]
            Answer.objects.bulk_update(answers_to_update, ["score"], batch_size=1000)
            
        recalc_score()

        end_time = time.time()

        self.stdout.write(self.style.SUCCESS(f"Генерация данных завершена за {end_time - start_time:.2f} секунд"))