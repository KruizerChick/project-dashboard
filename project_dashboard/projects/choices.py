""" Choices common among multiple models """


# Ranking of objects
HIGHEST = 5
HIGH = 4
MEDIUM = 3
LOW = 2
LOWEST = 1

RANK_OPTIONS = [
    (HIGHEST, 'Very High'),
    (HIGH, 'High'),
    (MEDIUM, 'Medium'),
    (LOW, 'Low'),
    (LOWEST, 'Very Low'),
]

# Impact rankings based on category
SCOPE_IMPACT = [
    (HIGHEST, 'Very High - The product does not meet the objectives and is effectively useless.'),
    (HIGH, 'High - The product is deficient in multiple essential requirements.'),
    (MEDIUM, 'Medium - The product is deficient in one major requirement or multiple minor requirements.'),
    (LOW, 'Low - The product is deficient in a few minor requirements.'),
    (LOWEST, 'Very Low - Minimal deviation from requirements.'),
 ]

QUALITY_IMPACT = [
    (HIGHEST, 'Very High - Performance is significantly below objectives and is effectively useless.'),
    (HIGH, 'High - Major aspects of performance do not meet requirements.'),
    (MEDIUM, 'Medium - At least one performance requirement is significantly deficient.'),
    (LOW, 'Low - There is minor deviation in performance.'),
    (LOWEST, 'Very Low - Minimal deviation in performance.'),
 ]

SCHEDULE_IMPACT = [
    (HIGHEST, 'Very High - Greater than 20% overall schedule increase.'),
    (HIGH, 'High - Between 10% and 20% overall schedule increase.'),
    (MEDIUM, 'Medium - Between 5% and 10% schedule increase.'),
    (LOW, 'Low - Noncritical paths have used all of their float or overall schedule increase of 1% to 5%.'),
    (LOWEST, 'Very Low - Slippage on noncritical paths but float remains.'),
]

COST_IMPACT = [
    (HIGHEST, 'Very High - Cost increase of greater than 20%.'),
    (HIGH, 'High - Cost increase of 10% to 20%.'),
    (MEDIUM, 'Medium - Cost increase of 5% to 10%.'),
    (LOW, 'Low - Cost increase that requires use of all contingency funds.'),
    (LOWEST, 'Very Low - Cost increase that requires use of some, but not all contingency funds.'),
]

# Risk Rating explanation:
# High:
#  - Probability of Medium or above and a Very High impact on any objective.
#  - Probability of High or above and a High impact on any objective.
#  - Probability of Very High and a Medium impact on any objective.
#  - Probability of Low or above and Medium impact on more than two objectives.

# Medium:
#  - Probability of Very Low and a High or above impact on any objective.
#  - Probability of Low and a Medium or above impact on any objective.
#  - Probability of Medium and a Low to High impact on any objective.
#  - Probability of High and a Very Low impact on any objective.
#  - Probability of Very High and a Low or Very Low impact on any objective.
#  - Probability of Very Low and a Medium impact on more than two objectives.

# Low:
#  - Probability of Medium and a Very Low impact on any objective.
#  - Probability of Low and a Low or Very Low impact on any objective.
#  - Probability of Very Low and a Medium or less impact on any objective.
