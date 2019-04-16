#!/user/bin/python
# -*- coding: utf-8 -*-

from recommendations import critics, sim_distance, sim_pearson
from recommendations import topMatches, getRecommendations, transformPrefs
from recommendations import calculateSimilarItems, getRecommendedItems

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

# User-Based CF

print '通过按人群与 Toby 相似度，加权重新评分，为影片排名获得推荐: '
print getRecommendations(critics, 'Toby')

print '通过查看哪些人喜欢 Superman Returns，以及这些人喜欢哪些其他物品来确定相似度：'
movies = transformPrefs(critics)
print topMatches(movies, 'Superman Returns')

print '可能最喜欢 Just My Luck 的人群列表（对调人和物不一定能获得有用信息）：'
print getRecommendations(movies, 'Just My Luck')

# Item-Based CF

print '构造物品比较数据集：'
itemsim = calculateSimilarItems(critics)
print itemsim

print '基于物品的推荐为 Toby 提供推荐列表：'
print getRecommendedItems(critics, itemsim, 'Toby')


