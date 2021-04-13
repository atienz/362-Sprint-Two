# =============================DATA PREPARATION ==============================
# ============================================================================
# Imports dataset
import numpy as np
import pandas as pd
# Load dataset
data = pd.read_csv('tmdb_5000_credits.csv')
data.head()

# Load second dataset
data2 = pd.read_csv('tmdb_5000_movies.csv')
data2.head()

# Merges datasets on id column
data.columns = ['id', 'title', 'cast', 'crew']
data2 = data2.merge(data, on = 'id')
data2.head()

# Using IMDB weighted rating 
# Mean rating for listed movies
avg = data2['vote_average'].mean()

# Minimum threshold for votes listed
min_listed_votes = data2['vote_count'].quantile(0.9)

# Getting the size of the listed movies based on requirement
movies_list = data2.copy().loc[data2['vote_count'] >= min_listed_votes]

# Define the metric function for each qualified movie
def weighted_rating(x, min_listed_votes=min_listed_votes, avg=avg ):
    v = x['vote_count']
    R = x['vote_average']
    # Caclculation based on IMDB formula 
    return (v/(v+min_listed_votes)*R) + (min_listed_votes/(min_listed_votes+v)*avg)

#Defines new feature score and calculate its value with the weighted rating
# Score is computed with a minimal tolerance for vote counts
movies_list['score'] = movies_list.apply(weighted_rating, axis=1)

# Sort the movie list
movies_list = movies_list.sort_values('score', ascending = False)

# =============================COLLABORATIVE FILTER ==========================
# ============================================================================
import matplotlib.pyplot as plt
# Visualize trending movies
pop = data2.sort_values('popularity', ascending = False)
# plt.figure(figsize=(12,4))
# plt.barh(pop['title_x'].head(6), pop['popularity'].head(6), align='center', color='r')
# plt.gca().invert_yaxis()
# plt.xlabel('Popularity')
# plt.title('Popular Trending Movies')


# High Budget Movies
# budget = data2.sort_values('budget', ascending = False)
# plt.figure(figsize=(12,4))
# plt.barh(budget['title_x'].head(6), budget['budget'].head(6), align='center', color='b')
# plt.gca().invert_yaxis()
# plt.xlabel('Popularity')
# plt.title('High Budget Movies')

# Machine Learning stuff
movies_list.drop(['title_y'], axis=1, inplace=True)
# movies_list.shape
# print(data2['overview'].head(10))

from sklearn.feature_extraction.text import TfidfVectorizer
# Define TF-IDF object and remove stop words
tfidf = TfidfVectorizer(stop_words='english')

# Replaces NaN with empty string
data2['overview'] = data2['overview'].fillna('')

# Construct TF-IDF matrix by fitting and transforming data
tfidf_matrix = tfidf.fit_transform(data2['overview'])

# import Linear kernel
from sklearn.metrics.pairwise import linear_kernel

# Compute cosine similarity on the tfidf matrix
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Construct reverse map of indices and movie titles
indices = pd.Series(data2.index, index = data2['title_x']).drop_duplicates()

# =============================USER FUNCTIONS ================================
# ============================================================================

# Function takes in movie title as input and outputs similar movies
def GetRecommendations(title, cosine_sim = cosine_sim):
    # Find index of the movie that matches the title
    idx = indices[title]
    
    # Get pairwise similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse = True)
    
    # Get scores of 10 most similar movies
    sim_scores = sim_scores[1:11]
    
    # Get movie indices
    movie_indices = [i[0] for i in sim_scores]
    
    # Return top 10 most similar movies
    return data2['title_x'].iloc[movie_indices]    

#===========================================
# Add Error Handling
# Do not let user add duplicates
#===========================================
# # Main Page
# import sys
# main = ''
# title = ''
# # userList = ['Inception']
# userList = []
# List = movies_list[['title_x', 'vote_average', 'score']]
# # Work on exit condition
# while True:
#     # Precondition: User's List has to be empty for new user
#     if bool(userList) == False:
#         # First time user is prompted add a movie to their list
#         temp = 0
#         while True:
#             print(f'Select a Movie to begin or type New for more options\n=============================')
#             print(f'Popular Movies:\n\n {List[temp:temp + 9].to_string(index=False)}')
#             title = input('\nType in Movie title to add to list: ')
#             # Updates displayed movies
#             if title.lower() == 'new':
#                 temp += 10
#             elif title.lower() != 'new' and (data2['title_x'] == title).any():
#                 userList.append(title)
#                 break
#             elif title.lower() == 'exit':
#                 raise SystemExit
#
#     while True:
#         # Precondition: User List has to be filled
#         import random
#
#         print('========== Main Menu ==========\n==============================\n')
#         if len(userList) != 0:
#             # Randomly recommends based on list size
#             idx = random.randrange(0, len(userList))
#             print(f'Movies based on your list:\n\n {GetRecommendations(userList[idx]).to_string(index=False)}')
#             # print(f'Movies based on your list:\n\n {GetRecommendations(userList[0]).to_string(index=False)}')
#         else:
#             print(f'Popular Movies: \n {print(List[0:9].to_string(index=False))}')
#         print(f'\nYour Movie List: {userList}\n')
#         print('Type the number of the option')
#         print('1:Search    2:Delete    3:Insert    4:Exit')
#         main = int(input('$\: '))
#
#         # Search algorithm with embedded loop
#         if main == 1:
#             while True:
#                 title = input('\nType in Movie title: ')
#                 user = GetRecommendations(title)
#                 print(f'Recommended based on your Search:\n {user.to_string(index=False)}\n')
#                 print('Type the number of the option')
#                 print('1. Add to list    2. Search  3. Main Menu\n')
#                 option = int(input('$\: '))
#                 # User adds preferred title to their list
#                 if option == 1:
#                     title = input('\nType in Movie title to add to list: ')
#                     # Goes back to main menu if user adds title
#                     if (data2['title_x'] == title).any():
#                         userList.append(title)
#                         break
#                     else:
#                         print('Invalid Title')
#                 # Continue searching
#                 elif option == 2:
#                     print('...')
#                 # Return to Main Menu
#                 elif option == 3:
#                     print('Returning...')
#                     break
#         # Delete title from list
#         elif main == 2:
#             print(f'\nYour Movie List: {userList}\n')
#             title = input('Type movie name to delete from list: ')
#             idx = userList.index(title)
#             del userList[idx]
#         # Add title from recommended list
#         elif main == 3:
#             # If list is empty, show popular movies
#             if len(userList) != 0:
#                 title = input('\nType in Movie title to add to list: ')
#                 if (data2['title_x'] == title).any():
#                     userList.append(title)
#             else:
#                 print(f'Empty List... ')
#         # Logout from main menu
#         elif main == 4:
#             print('Logging out...')
#             raise SystemExit
#         else:
#             raise SystemError
