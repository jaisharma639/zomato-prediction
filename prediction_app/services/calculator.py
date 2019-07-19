from prediction_app.models import Participants, Eligibility, Activity


class Calculator(object):

    def __init__(self, question, correct_ans):
        self.question = question
        self.correct_ans = set(correct_ans.split(','))
        self.default_eligibility = {"1.00": 100}

    def get_entries_to_update(self):
        return self.question.participants_set.all()

    def get_eligibility(self):
        return self.question.eligibility_set.all()

    def percentage_calculate(self, chosen, correct):
        fraction = len(chosen.intersection(correct))/float(len(chosen))
        return "{:.2f}".format(fraction)


    def calculate(self):
        try:
            eligibility = self.get_eligibility()[0].eligibility
        except IndexError:
            print 'Please update eligibility for the question ', self.question
            return False
        print 'The eligibility for given question is : ', eligibility
        print 'Correct answer for given question is : ', self.correct_ans
        print 'Updating the following entires : ', self.get_entries_to_update()
        for entry in self.get_entries_to_update():
            chosen_ans = set(entry.chosen_ans.split(','))
            print 'The answer chosen by the user was : ', chosen_ans
            percentage = self.percentage_calculate(
                chosen_ans, self.correct_ans)
            print 'User scored percentage : ', percentage
            try:
                reward = eligibility[percentage]
            except KeyError:
                reward = 0
            entry.reward = reward
            Activity.objects.create(
                user_field=entry.user_field,
                information="Q: " + self.question.question_text + ", A: " + str(chosen_ans),
                reward=reward)
            entry.save()
        return True
