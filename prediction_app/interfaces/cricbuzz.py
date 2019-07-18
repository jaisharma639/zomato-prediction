# All data fetch operations from cricbuzz endpoint

'''
Rules for type of questions:
a : Who will win the match?
b : Who will win the toss?
'''

class Reader(object):

    def __init__(self, data):
        self.data = data['matches']

    def get_active_matches_id(self):
        return set((map(int, self.data.keys())))

    def get_winner(self):
        pass

    def get_match_title(self, match_id):
        if isinstance(match_id, int):
            match_id = str(match_id)
        match_data = self.data[match_id]
        return match_data['team1']['name'] + " vs "+match_data['team2']['name']

    def filter_completed_matches(self):
        return {match_id for match_id in self.get_active_matches_id() if self.data[str(match_id)]['state']=="complete"}

    def get_answer(self, q_type, match_id):
        match_data = self.data[str(match_id)]
        if q_type == "a":
            win_id = str(match_data['winning_team_id'])
            if match_data['team1']['id'] == win_id:
                return match_data['team1']['name']
            else:
                return match_data['team2']['name']
        elif q_type == "b":
            return match_data['toss']['winner']
        elif q_type == "c":
            return ",".join(match_data['top3_scorers'])
