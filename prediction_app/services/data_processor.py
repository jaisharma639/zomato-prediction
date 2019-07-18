from prediction_app.models import ActiveMatches
from django.conf import settings
import importlib
from .calculator import Calculator

p = importlib.import_module("prediction_app.interfaces."+settings.PARTNER)


class Processor(object):

    def __init__(self, data):
        self.data = data
        self.partner = p.Reader(data)

    def get_match_id_in_db(self):
        return ActiveMatches.get_all_mid()

    def get_updates(self, deletes=False):
        incoming = self.partner.get_active_matches_id()
        db_count = self.get_match_id_in_db()
        if deletes:
            return db_count - incoming
        return incoming - db_count

    def update_db(self):
        updates = self.get_updates()
        for each_match in updates:
            print 'updating...'
            ActiveMatches.create_entry(
                each_match, self.partner.get_match_title(each_match))
        # Tables keeps on growing?
        # deletes = self.get_updates(True)
        # if deletes:
        #     print 'deleting'
        #     ActiveMatches.delete_entries(deletes)
        return

    def get_answer(self, questions, match_id):
        for q in questions:
            print 'q', q
            correct_ans = self.partner.get_answer(q.question_type, match_id)
            print 'correct answer is', correct_ans
            calculator = Calculator(q, correct_ans)
            done = calculator.calculate()
            if not done:
                return False
            q.correct_ans = correct_ans
            q.save()
        return True

    def update_answers(self):
        completed_matches = self.partner.filter_completed_matches()
        running_matches = ActiveMatches.get_running_matches()
        to_update = [match for match in running_matches
                     if match.match_id in completed_matches]
        print 'to_update', to_update
        for each_match in to_update:
            print 'each_match', each_match
            question_to_update = each_match.question_set.all()
            updated = self.get_answer(question_to_update, each_match.match_id)
            if not updated:
                return
            each_match.match_completed = True
            # each_match.save()
            from .notification import Notification
            print 'triggering notification service', question_to_update
            notification = Notification(question_to_update, each_match.match_text)
            notification.notify()

    def process_updates(self):
        self.update_db()
        self.update_answers()
