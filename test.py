from recommendations import critics, sim_distance, sim_pearson
from recommendations import topMatches, getRecommendations

# print critics['Lisa Rose']['Lady in the Water']
#
# critics['Toby']['Snakes on a Plane'] = 4.5
# print critics['Toby']


print 'Euclidean Distance Score of Lisa Rose and Gene Seymour is '
print sim_distance(critics, 'Lisa Rose', 'Gene Seymour')


print 'Pearson Correlation Score of Lisa Rose and Gene Seymour is '
print sim_pearson(critics, 'Lisa Rose', 'Gene Seymour')

print 'TopMatches 3 for Toby is '
print topMatches(critics, 'Toby', n=3)

print 'Recommendations for Toby: '
print getRecommendations(critics, 'Toby')

print 'Recommendations for Toby with sim_distance: '
print getRecommendations(critics, 'Toby', similarity=sim_distance)