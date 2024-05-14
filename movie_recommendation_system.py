# -*- coding: utf-8 -*-
"""movie_recommendation_system.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1RJLCgEbhgdAYh2PlY6WunWLGc1Bsw6j7
"""

import pandas as pd
import re
import sys

"""DataLoader class"""

class DataLoader:
  def __init__(self):
    self.data = pd.read_csv('tmdb_5000_movies.csv')
    self.process_data()

  def process_data(self):
    self.data = self.data[['title', 'genres', 'release_date', 'runtime', 'vote_average']]

  def get_data(self):
    return self.data

"""Movie class"""

class Movie:
  def __init__(self, title, genre, release_date, runtime, rating):
    self.title = title # title of movie
    self.genre = re.findall(r': "(.*?)\"',genre) # genre of movie
    self.release_date = int(str(release_date)[:4]) # year movie was released
    self.runtime = runtime # length of movie in minutes
    self.rating = rating # rating of movie (out of 10)

"""MovieDatabase class"""

class MovieDatabase:
  def __init__(self):
    self.data_loader = DataLoader()
    self.movie_data = self.data_loader.get_data()
    self.allmovies = self.extract_all_movies()

  # extracts all movies from the dataset
  def extract_all_movies(self):
    movies = []
    for index, row in self.movie_data.iterrows():
        title = row['title']
        genre = row['genres']
        release_date = row['release_date']
        runtime = row['runtime']
        rating = row['vote_average']
        movies.append(Movie(title, genre, release_date, runtime, rating))
    return movies

  # creates new movie object and adds movie to list
  def addmovie(self, moviename, moviegenre, moviedate,
               movielength, moviestarrating):
    self.allmovies.append(Movie(moviename, moviegenre, moviedate,
                           movielength, moviestarrating))

  # removes movie from list by movie title and date released
  # edit as needed i dont remember why i added moviedate. maybe i thought there were movies with the same name
  def removemovie(self, moviename, moviedate):
    for i, movie in enumerate(self.allmovies):
      if movie.moviename == moviename and movie.moviedate == moviedate:
        return self.allmovies.pop(i)


  # returns list of movies that match movie title
  def findmoviename(self, moviename):
    matchingtitle = []
    for movie in self.allmovies:
      if movie.moviename == moviename:
        matchingtitle.append(movie)
    return matchingtitle

  # returns list of movies that were released in given year
  def findmoviedate(self, movieyear):
    matchingdate = []
    for movie in self.allmovies:
      if movie.moviedate == movieyear:
        matchingdate.append(movie)
    return matchingdate

  # returns list of movies that match a genre
  def findmoviegenre(self, moviegenre):
    matchinggenre = []
    for movie in self.allmovies:
      if movie.moviegenre == moviegenre:
        matchinggenre.append(movie)
    return matchinggenre

  # returns sorted list of all movies in order of highest to lowest star rating
  def sortstarratings(self):
    starheap = Max_heap()
    starheap.build_max_heap(self.allmovies)
    return starheap.heap_list

#max_heap class for sorting star ratings
class Max_heap:
    def __init__(self):
        self.heap_list = [sys.maxsize]

    def size(self):
        return len(self.heap_list) - 1

    def parent(self, index):
        ''' Return the parent of a node at index'''
        return index // 2

    def l_child(self, index):
        '''Return the position of the left child node of a given index'''
        return 2 * index

    def r_child(self, index):
        '''Return the position of the right child node of a given index'''
        return (2 * index) + 1

    def is_leaf(self, index):
        ''' Returns true if the given index is a leaf node'''
        return index * 2 > self.size

    def swap(self, from_pos, to_pos):
        '''A helper function to swap two nodes of the heap'''
        self.heap_list[from_pos], self.heap_list[to_pos] = self.heap_list[to_pos], self.heap_list[from_pos]


    def insert(self, element):
        '''
        It inserts an element to the heap structure and maintain the heap property.
        '''
        self.heap_list.append(element)
        current = self.size
        while (self.heap_list[current].rating > self.heap_list[self.parent(current)].rating):
            self.swap(current, self.parent(current))
            current = self.parent(current)

    def max_heapify(self, i):
        '''
        # Function to heapify the node at index
        '''
        l = self.l_child(i)
        r = self.r_child(i)

        if l <= self.size() and self.heap_list[l].rating > self.heap_list[i].rating:
            largest = l
        else:
            largest = i

        if r <= self.size() and self.heap_list[r].rating > self.heap_list[largest].rating:
            largest = r

        if largest != i :
            self.swap(i, largest)
            self.max_heapify(largest)


    def build_max_heap(self, unsorted_list):
        self.heap_list = unsorted_list
        for i in range(len(unsorted_list) // 2 , 1, -1):
            self.max_heapify(i)

    def extract_max(self):
        '''Extracts the max of this heap'''

        # 1. pop the root of the tree which is on the index 1 of the list
        popped = self.heap_list.pop(1)

        # 2. Insert the last element of the heap list which is a leaf node and insert it to the root
        if(self.size > 1):
            self.insert(self.heap_list.pop())
        # 3. Call heapify() on the root to fix the error it may have caused.
            self.max_heapify(1)

        return popped

"""UserProfile class"""

class UserProfile:
    def __init__(self):
        self.seen_movies = []

    def add_seen_movie(self, movie):
        self.seen_movies.append(movie)

    def remove_seen_movie(self, movie):
        self.seen_movies.remove(movie)

"""Recommender class"""

class Recommender:
    def __init__(self, movie_database):
        self.movie_database = movie_database

    def recommend_movie(self, genre2, min_runtime, max_runtime, start_year, end_year, user_profile):
        filtered_movies = self.movie_database.allmovies

        # Filter movies based on user preferences
        if genre2:
            filtered_movies = [movie for movie in filtered_movies if genre2 in movie.genre]

        if min_runtime is not None:
            filtered_movies = [movie for movie in filtered_movies if movie.runtime >= min_runtime]

        if max_runtime is not None:
            filtered_movies = [movie for movie in filtered_movies if movie.runtime <= max_runtime]

        if start_year is not None:
            filtered_movies = [movie for movie in filtered_movies if movie.release_date >= start_year]

        if end_year is not None:
            filtered_movies = [movie for movie in filtered_movies if movie.release_date <= end_year]

        # Remove movies the user has already seen
        filtered_movies = [movie for movie in filtered_movies if movie not in user_profile.seen_movies]

        # Sort filtered movies by rating
        sorted_movies = self.movie_database.sortstarratings()

        for movie in sorted_movies:
            if movie in filtered_movies:
                recommended_movie = movie
                #user_profile.add_recommended_movie(recommended_movie)
                return recommended_movie

        return None

"""Main"""

def main():
    # Create instances of the required classes
    movie_database = MovieDatabase()
    user_profile = UserProfile()
    recommender = Recommender(movie_database)

    # Prompt user for preferred genre
    genre_input = input("Enter your preferred genre (or leave blank for any genre): ").strip().title()

    # Prompt user for runtime range
    min_runtime = input("Enter minimum runtime in minutes (or leave blank for any): ")
    max_runtime = input("Enter maximum runtime in minutes (or leave blank for any): ")

    # Prompt user for release date range
    start_year = input("Enter the earliest release year (or leave blank for any): ")
    end_year = input("Enter the latest release year (or leave blank for any): ")

    # Convert runtime and release year inputs to integers if provided
    try:
        min_runtime = int(min_runtime) if min_runtime else None
        max_runtime = int(max_runtime) if max_runtime else None
        start_year = int(start_year) if start_year else None
        end_year = int(end_year) if end_year else None
    except ValueError:
        print("Invalid input for runtime or release year. Please enter valid integers.")
        return

    # Recommend a movie based on user preferences
    recommended_movie = recommender.recommend_movie(genre_input, min_runtime, max_runtime, start_year, end_year, user_profile)

    if recommended_movie:
        while True:
            print("Recommended Movie:", recommended_movie.title)
            seen_input = input("Have you already seen this movie? (yes/no): ").strip().lower()
            if seen_input == "yes":
                user_profile.add_seen_movie(recommended_movie)
                print("Movie removed from recommendations.")
                # Get the next recommended movie
                recommended_movie = recommender.recommend_movie(genre_input, min_runtime, max_runtime, start_year, end_year, user_profile)
                if not recommended_movie:
                    print("Sorry, no more movies found matching your criteria.")
                    break
            elif seen_input == "no":
                print("Enjoy watching the movie!")
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
    else:
        print("Sorry, no movie found matching your criteria.")

if __name__ == "__main__":
    main()
    
