import datetime

from django.utils import timezone
from django.test import TestCase
from polls.models import Question
from polls.views import QuestionModelForm
from django.core.urlresolvers import reverse, resolve
from django.contrib.auth.models import User

from django.db import DataError

from django.core.exceptions import ValidationError
import validators

class QuestionMethodTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertEqual(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is older than 1 day
        """
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertEqual(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() should return True for questions whose
        pub_date is within the last day
        """
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date=time)
        self.assertEqual(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    """
    Creates a question with the given `question_text` published the given
    number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,pub_date=time)

class QuestionViewTests(TestCase):

    def test_index_view_with_no_questions(self):
        """
        If no questions exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_a_past_question(self):
        """
        Questions with a pub_date in the past should be displayed on the
        index page
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past question.>'])

    def test_index_view_with_a_future_question(self):
        """
        Questions with a pub_date in the future should not be displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.", status_code=200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        should be displayed.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_index_view_with_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past question 2.>', '<Question: Past question 1.>'])

class QuestionURLTests(TestCase):
    #See: https://docs.djangoproject.com/en/1.7/ref/urlresolvers/#resolve
    # for additional information on resolve()
    def test_url_index(self):
        """
        /polls/ should resolve to polls:index
        """
        resolver = resolve('/polls/')
        self.assertEqual(resolver.namespace,'polls')
        self.assertEqual(resolver.view_name,'polls:index')

    def test_url_detail(self):
        """
        /polls/1/ should resolve to polls:detail
        """
        resolver = resolve('/polls/1/')
        self.assertEqual(resolver.namespace,'polls')
        self.assertEqual(resolver.view_name,'polls:detail')

    def test_url_results(self):
        """
        /polls/1/results/ should resolve to polls:results
        """
        resolver = resolve('/polls/1/results/')
        self.assertEqual(resolver.namespace,'polls')
        self.assertEqual(resolver.view_name,'polls:results')
        
    def test_url_vote(self):
        """
        /polls/1/vote/ should resolve to polls:vote
        """
        resolver = resolve('/polls/1/vote/')
        self.assertEqual(resolver.namespace,'polls')
        self.assertEqual(resolver.view_name,'polls:vote')        
        
class QuestionIndexDetailTests(TestCase):
    def test_detail_view_with_a_future_question(self):
        """
        The detail view of a question with a pub_date in the future should
        return a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        response = self.client.get(reverse('polls:detail',args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_question(self):
        """
        The detail view of a question with a pub_date in the past should
        display the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        response = self.client.get(reverse('polls:detail', args=(past_question.id,)))
        self.assertContains(response, past_question.question_text, status_code=200)
		
class QuestionResultsTests(TestCase):
    def test_results_view_without_login(self):
        """
        The results view of a question should redirect (302) to the login page if the user is not
		logged in.
        """
        question = create_question(question_text='Not logged in', days=-1)
        response = self.client.get(reverse('polls:results',args=(question.id,)))
        self.assertEqual(response.status_code, 302)

    def test_detail_view_with_login(self):
        """
        The results view of a question should return the results if the user is
		logged in.
        """
        User.objects.create_superuser('fred', 'fred@fred.fred', 'secret')
        self.client.login(username='fred',password='secret')
        question = create_question(question_text='Loged in', days=-1)
        response = self.client.get(reverse('polls:results',args=(question.id,)))
        self.assertContains(response, 'Loged in',status_code=200)
        
class QuestionModelTests(TestCase):
    #When using PostgreSQL (via the psycopg2 DBI) max_length is enforced by
    # django.db so we can use a simple unit test for that.
    # This unit test will fail when using sqlite3 because it does not enforce
    # max_length.
    def test_question_text_max_length(self):
        """
        Should not allow question text longer than 200 characters
        """
        with self.assertRaises(DataError):
            question = create_question(question_text=u'a'*201, days=-1)

    #validators are not enforced by django.db so we need to use an
    #integration test with a ModelForm.
    def test_pub_date_not_future(self):
        """
        Should not allow questions published in the future
        """
        #create an invalid model object
        question = create_question(question_text=u'a'*200, days=1000)
        #load the invalid object into it's corresponding ModelForm
        form = QuestionModelForm(instance=question)
        #assert that the form is not valid
        self.assertFalse(form.is_valid())
        
class ValidatorTests(TestCase):
    def test_not_future_fails(self):
        """Raise a ValidationError if the value is in the future.
        """
        value = timezone.now() + datetime.timedelta(days=30)
        with self.assertRaises(ValidationError):
            validators.not_future(value)
        
    def not_unauthorized_word(self):
        """Raise a ValidationError if the value is in the unauthorized word list.
        """
        value = 'chipmunk'
        with self.assertRaises(ValidationError):
            validators.not_unauthorized_word(value)