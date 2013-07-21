This is a simple TrueSkill ranker for an online arena game.

Require Python 2.7.

It uses the trueskill module from PyPI.  "pip install trueskill"

There's a sample file that shows the format to use.

Usage:
$ python arenats.py ZuddhaYuddha2.csv

(or substitute your own data file)

If you want house rankings instead of player rankings, you can add
a house file, and do
$ python arenats.py --house-file Houses.csv ZuddhaYuddha2.csv
