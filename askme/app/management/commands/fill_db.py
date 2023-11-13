import datetime

from django.core.management.base import BaseCommand
from app.models import *
from faker import Faker

fake = Faker()


class Command(BaseCommand):
    help = 'disp hello'

    def add_arguments(self, parser):
        parser.add_argument("num", type=int)

    def handle(self, *args, **kwargs):
        a = datetime.datetime.now()
        self.stdout.write(str(a))
        num = kwargs['num']
        all_profiles = []
        all_names = []
        all_tagwords = []
        all_tags = []
        questions = []
        answers = []
        all_emails = []
        for i in range(100 * num):
            if i < num:
                name = fake.name().replace(' ', '_')
                while name in all_names:
                    name = fake.name().replace(' ', '_')
                all_names.append(name)
                email = fake.email()
                while email in all_emails:
                    email = fake.email()
                all_emails.append(email)
                if i < 50:
                    profile = Profile(
                        user=User.objects.create_user(name, password='passworddd'),
                        creation_date=fake.date_between(start_date='-20y', end_date='-10y'),
                        email=email,
                        nickname=fake.word()
                    )
                else:
                    profile = Profile(
                        user=User.objects.create_user(name, password='passworddd'),
                        creation_date=fake.date_between(start_date='-20y', end_date='now'),
                        email=email,
                        nickname=fake.word()
                    )
                profile.save()

                all_profiles.append(profile)

                tag_word = fake.email()
                tag_word = tag_word[:tag_word.index('@')]
                while tag_word in all_tagwords:
                    tag_word = fake.email()
                    tag_word = tag_word[:tag_word.index('@')]
                all_tagwords.append(tag_word)
                tag = Tag(tag_word=tag_word)
                tag.save()
                all_tags.append(tag)

            if i < 10 * num:
                author = all_profiles[fake.random_int(min=0, max=len(all_profiles) - 1)]
                question = Question.objects.create(title=fake.sentence(nb_words=5)[:-1] + '?',
                                                   content=fake.text(max_nb_chars=1000),
                                                   author=author,
                                                   creation_date=fake.date_between(start_date=author.creation_date,
                                                                                   end_date='now'),
                                                   question_likes=fake.random_int(min=0, max=1000),
                                                   question_dislikes=fake.random_int(min=0, max=1000))

                for _ in range(fake.random_int(min=1, max=5)):
                    question.tag.add(all_tags[fake.random_int(min=0, max=len(all_tags) - 1)])
                question.save()
                questions.append(question)

            if i < 100 * num:
                to_question = questions[fake.random_int(min=0, max=len(questions) - 1)]
                author = all_profiles[fake.random_int(min=0, max=len(all_profiles) - 1)]
                while to_question.creation_date < author.creation_date:
                    author = all_profiles[fake.random_int(min=0, max=len(all_profiles) - 1)]
                answer = Answer(
                    content=fake.text(max_nb_chars=1000),
                    to_question=to_question,
                    author=author,
                    creation_date=fake.date_between(start_date=to_question.creation_date, end_date='now'),
                    is_correct=1 if fake.random_int() % 2 == 0 else 0,
                    answer_likes=fake.random_int(min=0, max=1000),
                    answer_dislikes=fake.random_int(min=0, max=1000)
                )
                answer.save()
                answers.append(answer)

        '''Profile.object.bulk_create(all_profiles)
        Tag.object.bulk_create(all_tags)
        Question.object.bulk_create(questions)
        Profile.object.bulk_create(all_profiles)'''

        '''profiles = [
        
            Profile(
                user=User.objects.create_user(fake.first_name(), password='passworddd'),
                creation_date=fake.date_between(start_date='-15y', end_date='now'),
                email=fake.email(),
                nickname=fake.word()
            )for _ in range(num)
        ]
        Profile.objects.bulk_create(profiles)
        profiles_num = len(profiles)

        tags = [
            Tag(
                tag_word=fake.word()
            ) for _ in range(num)
        ]
        Tag.objects.bulk_create(tags)
        tags_num = len(tags)
        questions = []

        for _ in range(10 * num):
            author = profiles[fake.random_int(min=0, max=profiles_num - 1)]
            q = Question.objects.create(title=fake.sentence(nb_words=5)[:-1] + '?',
                                        content=fake.text(max_nb_chars=1000),
                                        author=author, creation_date=fake.date_between(start_date=author.creation_date,
                                                                                       end_date='now'),
                                        question_likes=fake.random_int(min=0, max=1000))

            for _ in range(fake.random_int(min=1, max=5)):
                q.tag.add(tags[fake.random_int(min=0, max=tags_num - 1)])
            questions.append(q)

        questionsNum = len(questions)

        answers = [
            Answer(
                content=fake.text(max_nb_chars=1000),
                to_question=questions[fake.random_int(min=0, max=questionsNum - 1)],
                author=profiles[fake.random_int(min=0, max=profiles_num - 1)],
                creation_date=fake.date_between(start_date='-15y', end_date='now'),
                is_correct=1 if fake.random_int() % 2 == 0 else 0,
                answer_likes=fake.random_int(min=0, max=1000),
                answer_dislikes=fake.random_int(min=0, max=1000)
            ) for _ in range(100 * num)
        ]
        Answer.objects.bulk_create(answers)'''


        '''questions = [
            Question(
                title=fake.sentence(nb_words=5)[:-1] + '?',
                content=fake.text(max_nb_chars=1000),
                author=profiles[fake.random_int(min=0, max=profiles_num-1)],
                creation_date=fake.date_between(start_date='-15y', end_date='now'),
                tag=Question.tag.add(tags[fake.random_int(min=0, max=tags_num-1)]),
                question_likes=fake.random_int(min=0, max=1000)

            )for _ in range(num)
        ]'''
        self.stdout.write(str(datetime.datetime.now()))
        self.stdout.write(str(datetime.datetime.now() - a))

