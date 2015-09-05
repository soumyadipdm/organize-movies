#!/usr/bin/python2
'''organize_movie.py
a script to organize movies according to
the imdb specified genre
'''

import os
import os.path
import argparse

import imdb

def get_genre(movie_name):
    '''get the genre of the movie from imdb
    :param movie_name string name of the movie
    '''
    my_imdb = imdb.IMDb()
    result = my_imdb.search_movie(movie_name)

    # if we have provided the exact name of the movie,
    # we should expect the movie to be the first in the
    # result list
    movie = result[0]

    # now update info about movie
    my_imdb.update(movie)

    # let's get the genre of the movie
    # we will get only the first genre in the list
    genre = movie['genre'][0]

    return genre


def list_movies(local_movie_directoy):
    '''prepares a list of movie names by
    parsing the directory specified
    :param local_movie_directoy string path to the movies directory
    '''

    # get a list of movie names stored in the local dir
    # this assumes that the movies are not stored in nested dir
    return os.listdir(local_movie_directoy)


def organize_movies(local_movie_directoy, organized_movie_directory, movie_name, genre):
    '''organized movies folders/files by placing them in
    organized_movie_directory/genre/genre
    :param local_movie_directoy string path to locally stored movie directory
    :param organized_movie_directory string path to organized movies folder
    :param movie_name string name of the movie
    :param genre genre of the movie
    '''

    move_from = os.path.join(local_movie_directoy, movie_name)
    move_to = os.path.join(organized_movie_directory, genre)

    # create a directory structure for like:
    # organized_movie_directory/genre
    # ignore exception if the directory already exists
    if not os.path.exists(move_to):
        if not os.path.isdir(move_to):
            os.mkdir(move_to)
        else:
            print "Error: {0} exists but it's not a directory"

    # now move the movie to the new genre
    destination = os.path.join(move_to, movie_name)
    os.rename(move_from, destination)


def main():
    '''main function, does all the work'''
    parser = argparse.ArgumentParser(description='A script to organize movies per genre')
    parser.add_argument('movie_dir', help='Existing directory full of uncategoried movies')
    parser.add_argument('new_dir', help='New directory for movies to be put into')
    args = parser.parse_args()

    local_movie_directoy = args.movie_dir
    organized_movie_directory = args.new_dir

    for movie_name in list_movies(local_movie_directoy):
        try:
            genre = get_genre(movie_name)
        except Exception:
            continue  # no matter what, we did not get the genre

        organize_movies(local_movie_directoy, organized_movie_directory, movie_name, genre)
        move_from = os.path.join(local_movie_directoy, movie_name)
        move_to = os.path.join(organized_movie_directory, genre, movie_name)
        print "{0} -> {1}".format(move_from, move_to)


if __name__ == '__main__':
    main()

