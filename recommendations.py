#!/user/bin/python
# -*- coding: utf-8 -*-

# 用户-电影评分词典
critics={
  'Lisa Rose': {
    'Lady in the Water': 2.5,
    'Snakes on a Plane': 3.5,
    'Just My Luck': 3.0,
    'Superman Returns': 3.5,
    'You, Me and Dupree': 2.5,
    'The Night Listener': 3.0
  },
  'Gene Seymour': {
    'Lady in the Water': 3.0,
    'Snakes on a Plane': 3.5,
    'Just My Luck': 1.5,
    'Superman Returns': 5.0,
    'The Night Listener': 3.0,
    'You, Me and Dupree': 3.5
  },
  'Michael Phillips': {
    'Lady in the Water': 2.5,
    'Snakes on a Plane': 3.0,
    'Superman Returns': 3.5,
    'The Night Listener': 4.0
  },
  'Claudia Puig': {
    'Snakes on a Plane': 3.5,
    'Just My Luck': 3.0,
    'The Night Listener': 4.5,
    'Superman Returns': 4.0,
    'You, Me and Dupree': 2.5
  },
  'Mick LaSalle': {
    'Lady in the Water': 3.0,
    'Snakes on a Plane': 4.0,
    'Just My Luck': 2.0,
    'Superman Returns': 3.0,
    'The Night Listener': 3.0,
    'You, Me and Dupree': 2.0
  },
  'Jack Matthews': {
    'Lady in the Water': 3.0,
    'Snakes on a Plane': 4.0,
    'The Night Listener': 3.0,
    'Superman Returns': 5.0,
    'You, Me and Dupree': 3.5
  },
  'Toby': {
    'Snakes on a Plane': 4.5,
    'You, Me and Dupree': 1.0,
    'Superman Returns': 4.0
  }
}


from math import sqrt

# 返回一个有关 person1 与 person2 的基于距离的相似度评价
# 欧几里得距离评价 Euclidean Distance Score
def sim_distance(prefs, person1, person2):
  # 得到双方都曾评价过的物品列表
  si={}
  for item in prefs[person1]: 
    if item in prefs[person2]:
      si[item]=1

  # 如果两者没有共同之处，返回 0
  if len(si)==0: return 0

  # 计算所有差值的平方和
  sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item], 2)
                      for item in prefs[person1] if item in prefs[person2]])

  return 1/(1+sum_of_squares)


# 返回 p1 和 p2 的皮尔逊相关度评价
def sim_pearson(prefs,p1,p2):
  # 得到双方都曾评价过的物品列表
  si={}
  for item in prefs[p1]: 
    if item in prefs[p2]: si[item]=1

  n = len(si)

  # 如果两者没有共同之处，返回 1
  if n==0: return 1
  
  # Sums of all the preferences 求和
  sum1=sum([prefs[p1][it] for it in si])
  sum2=sum([prefs[p2][it] for it in si])
  
  # Sums of the squares 求平方和
  sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
  sum2Sq=sum([pow(prefs[p2][it],2) for it in si])	
  
  # Sum of the products 求乘积之和
  pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])
  
  # 计算皮尔逊评价值
  num=pSum-(sum1*sum2/n)
  den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
  if den==0: return 0

  r=num/den

  return r


# 从反映偏好的词典中返回最匹配者
# 返回结果的个数和相似度函数均为可选参数
def topMatches(prefs,person,n=5,similarity=sim_pearson):
  scores=[(similarity(prefs,person,other),other) 
                  for other in prefs if other!=person]
  scores.sort()
  scores.reverse()
  return scores[0:n]

# 利用所有他人评价值的加权平均，为某人提供推荐
def getRecommendations(prefs,person,similarity=sim_pearson):
  totals={}
  simSums={}
  for other in prefs:
    # 不和自己作比较
    if other==person: continue
    sim=similarity(prefs,person,other)

    # 忽略评价值 <= 0 的情况
    if sim<=0: continue
    for item in prefs[other]:
	    
      # 只对自己还未曾看过的影评进行评价
      if item not in prefs[person] or prefs[person][item]==0:
        # 相似度 * 评价值
        totals.setdefault(item,0)
        totals[item]+=prefs[other][item]*sim
        # 相似度之和
        simSums.setdefault(item,0)
        simSums[item]+=sim

  # 建立一个归一化的列表
  rankings=[(total/simSums[item],item) for item,total in totals.items()]

  # Return the sorted list
  rankings.sort()
  rankings.reverse()
  return rankings


# 通过查看哪些人喜欢某一特定商品，以及这些人喜欢哪些其他物品来决定相似度
# 这和之前用来决定人与人之间相似度的方法是一样的，只需将人员和物品对换
def transformPrefs(prefs):
  result={}
  for person in prefs:
    for item in prefs[person]:
      result.setdefault(item,{})

      # 将物品和人员对换
      result[item][person]=prefs[person][item]
  return result


def calculateSimilarItems(prefs,n=10):
  # 建立字典，以给出与这些物品最相近的其他所有物品
  result={}

  # 以物品为中心，倒置偏好矩阵（有关物品-用户评价情况的列表）
  itemPrefs=transformPrefs(prefs)
  c=0
  for item in itemPrefs:
    # 对大数据集更新状态变量
    c+=1
    if c%100==0: print "%d / %d" % (c,len(itemPrefs))
    # 寻找最相似的物品
    scores=topMatches(itemPrefs,item,n=n,similarity=sim_distance)
    result[item]=scores
  return result


# 利用反映物品相似度的字典来给出推荐
def getRecommendedItems(prefs,itemMatch,user):
  userRatings=prefs[user]
  scores={}
  totalSim={}

  # 循环遍历由当前用户评分的物品
  for (item,rating) in userRatings.items():

    # 循环遍历与当前物品相近的物品
    for (similarity,item2) in itemMatch[item]:

      # 如果该用户已经对当前物品做过评价，则忽略
      if item2 in userRatings: continue

      # 评价值与相似度的加权之和
      scores.setdefault(item2,0)
      scores[item2]+=similarity*rating

      # 全部相似度之和
      totalSim.setdefault(item2,0)
      totalSim[item2]+=similarity

  # 将每个合计值除以加权和，求平均值
  rankings=[(score/totalSim[item],item) for item,score in scores.items()]

  # 从高到低返回评分结果
  rankings.sort()
  rankings.reverse()
  return rankings