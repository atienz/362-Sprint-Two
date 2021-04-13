from django.shortcuts import render, redirect
from .models import MyModel
from .forms import MyForm
from .forms import RegisterForm
from django.http import HttpResponse, HttpResponseRedirect
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
# from django.shortcuts import HttpResponse
import pandas as pd
from matplotlib import pyplot as plt
from Collab_Filter import data2, indices, cosine_sim, movies_list

def mainpage(response):
    return render(response,"main/login_init.html",{})

def login(request):
    return render(request, "main/home.html", {})


# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect("/home")
    else:
        form = RegisterForm()

    return render(response, "main/register.html", {"form": form})


def home(response):
    return render(response, "main/home.html", {})


def logout(request, redirect=None, auth=None):
    auth.logout(request)
    return redirect('home_url')


import pytvmaze
import numpy as np

tvm = pytvmaze.TVMaze()
from tvmaze.api import Api

api = Api()


def display(request):
    def rec(title, cosine_sim=cosine_sim):
        # Find index of the movie that matches the title
        if title in indices:
            idx = indices[title]
            # Get pairwise similarity scores of all movies with that movie
            sim_scores = list(enumerate(cosine_sim[idx]))

            # Sort the movies based on the similarity scores
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

            # Get scores of 10 most similar movies
            sim_scores = sim_scores[1:11]

            # Get movie indices
            movie_indices = [i[0] for i in sim_scores]

            # Return top 10 most similar movies
            return data2['title_x'].iloc[movie_indices]
        else:
            return []

    # Redirects in the display.html page and Outputs the user's recommendations
    # Display IMDB and TVMaze recommendations
    z = []
    res = request.POST['title']
    # Only displays TVMaze Table if not found in IMBD Database
    if len(rec(res)) == 0:
        # Finds shows using TVMaze API
        x = api.search.shows(res)

        for i in range(len(x)):
            # Typecasts the API output into a string
            y = str(x[i])
            # Truncates the string for HTML output
            z.append(y[14:len(y) - 3])
        # Uses the set function to prevent duplicates
        z = list(set(z))

        # Sprint 4 Goal: Sentimental Analysis Algorithm
        # Recommend Title based on mood of the movie
        # Fills in gaps left behind from removed duplicates
        # temp = 0
        # val = rec("Fight")
        # val = val.reset_index()
        # val = val[['title_x']].to_dict()
        # movies = sorted(val.items())
        # if len(z) != 10:
        #     temp = 10 - len(z)
        #     for i in range(temp):
        #         val.append(val[i])
        # 1D vector is transposed into a column vector
        col_vec = np.array(z, ndmin=2)

        return render(request, 'main/display.html', {'result2': col_vec})
    # If the input works for both algorithms, display 2 tables
    else:
        val = rec(res)
        val = val.reset_index()
        val = val[['title_x']].to_dict()
        movies = sorted(val.items())

        # Finds shows using TVMaze API
        x = api.search.shows(res)
        for i in range(len(x)):
            # Typecasts the API output into a string
            y = str(x[i])
            # Truncates the string for HTML output
            z.append(y[14:len(y) - 3])
        # Uses the set function to prevent duplicates
        z = list(set(z))
        # 1D vector is transposed into a column vector
        col_vec = np.array(z, ndmin=2)

        return render(request, 'main/display.html', {'result': movies, 'result2': col_vec})


def my_form(request):
    if request.method == "POST":
        form = MyForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = MyForm()
    return render(request, 'main/cvForm.html', {'my_form': form, 'name': 'Cesar'})

# def operation(request):
# if user clicks to add title, the title info is added to User List Home
# That same title is used to update the UI database and update the recommendations
# if user clicks to delete title, the title will be erased from the user's and UI's list
# Allow the user to navigate the list by clicking or scrolling
# Redirect the user to view more recommendations
