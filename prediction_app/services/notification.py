from prediction_app.models import Participants
from django.db.models import Sum
from django.template.loader import get_template
from prediction_app.utils.email_utils import send_email

class Notification(object):

    def __init__(self, questions, match):
        self.questions = questions
        self.match = match
        self.subject = "Result for ZPL"

    def notify(self):
        user_rewards = Participants.objects.filter(question__in=self.questions).values('user_field__email').annotate(reward=Sum('reward'))
        for user_entry in user_rewards:
                
                email = [user_entry['user_field__email']]
                print email, 'email', type(email)
                if email[0] == '':
                    email = ['jai.sharma8693@gmail.com']
                template = get_template('reward_email.txt')
                context = {
                  'reward': user_entry['reward'],
                  'match': self.match
                }
                message = template.render(context)
                print 'mail sent', send_email(self.subject, message, email)