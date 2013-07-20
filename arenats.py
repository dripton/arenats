#!/usr/bin/env python

"""Calculate TrueSkill rankings for an arena game."""

__copyright__ = "Copyright 2013 David Ripton"
__license__ = "MIT"


from collections import defaultdict
import sys

import trueskill


SIGMA_MULTIPLIER = 3


def explode(li):
    """Convert a list of strings into a list of lists of strings.

    Each inner list is one team.
    """
    result = []
    for el in li:
        li2 = el.split("&")
        inner = [el2.strip() for el2 in li2]
        result.append(inner)
    return result


class Ranker(object):
    def __init__(self, lines):
        self.lines = lines

        # name: Rating
        self.ratings = defaultdict(trueskill.Rating)
        # name: number of wins
        self.wins = defaultdict(int)
        # name: number of losses
        self.losses = defaultdict(int)

    def process(self, line):
        """Process a line denoting one match, and update the ratings."""
        line = line.strip()
        if not line or line.startswith("#"):
            return
        parts = line.split(",")
        assert len(parts) >= 4
        # The first 3 parts are unused for now.
        winners = [parts[3]]
        losers = parts[4:]
        winner_lists = explode(winners)
        loser_lists = explode(losers)

        for winner_list in winner_lists:
            for winner in winner_list:
                self.wins[winner] += 1
        for loser_list in loser_lists:
            for loser in loser_list:
                self.losses[loser] += 1

        # Fetch old ratings for combatants
        all_ratings = []
        for team in winner_lists + loser_lists:
            team_ratings = []
            for name in team:
                team_ratings.append(self.ratings[name])
            team_ratings = tuple(team_ratings)
            all_ratings.append(team_ratings)

        # Calculate new ratings for combatants
        new_ratings = trueskill.transform_ratings(all_ratings)

        # Store new ratings for combatants
        for ii, team in enumerate(winner_lists + loser_lists):
            new_team_ratings = new_ratings[ii]
            for jj, name in enumerate(team):
                self.ratings[name] = new_team_ratings[jj]

    def process_all(self):
        """Process all lines."""
        for line in self.lines:
            self.process(line)

    def output(self):
        ratings = []
        for name, rating in self.ratings.iteritems():
            ts = max(1, rating.mu - SIGMA_MULTIPLIER * rating.sigma)
            ratings.append((ts, rating.mu, rating.sigma, name))
        ratings.sort(reverse=True)

        print "ts    mu      sigma   name (record)"
        for ts, mu, sigma, name in ratings:
            print "%2d %f %f %s (%d-%d)" % (ts, mu, sigma, name,
              self.wins[name], self.losses[name])
        print


def main():
    if len(sys.argv) > 1:
        fn = sys.argv[1]
        fil = open(fn)
    else:
        fil = sys.stdin
    bytes = fil.read()
    fil.close()
    lines = bytes.split("\n")

    ranker = Ranker(lines)
    ranker.process_all()
    ranker.output()


if __name__ == "__main__":
    main()
