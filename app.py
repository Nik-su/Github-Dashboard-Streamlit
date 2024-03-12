###Most Optimized Final Product
## Still Needed to plot piechart 
## commit_per_repo_top10(), stares_per_repo_top10()
## It will be completed
## Efficiently handle apis requests if possible
import streamlit as st
from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import requests
import time

client = MongoClient("mongodb://localhost:27017/") 
db = client["github_users_file4"]  
collection = db["user_collection"]
def get_user_data(username):
    user_data = collection.find_one({"Login": username})
    return user_data

def get_language_from_repo_url(repo_url):
    try: 
        #headers = {"Authorization": f"token {ACCESS_TOKEN}"}
        response = requests.get(repo_url)#, headers=headers)
        if response.status_code == 200:
            return response.json().get("language")
        elif response.status_code == 403:
            print("Received a 403 error. Retrying after 15 minutes...")
            time.sleep(900)  # Sleep for 15 minutes
            return get_language_from_repo_url(repo_url) 
        else:
            print(f"Error fetching repository data for {repo_url}: {response.status_code}")
    except Exception as e:
        print(f"Error fetching repository data for {repo_url}: {e}")
    return None

def stars_per_language(user_data):
    st.subheader("Stars per Language")
    stars_per_language = defaultdict(int)
    starred_repos = user_data.get("Starred Repositories", "").split(",") if user_data.get("Starred Repositories") else []
    for repo_url in starred_repos:
        repo_url_cleaned = repo_url.strip().strip("'\"").strip("['")
        if isinstance(repo_url_cleaned, list):
            repo_url_cleaned = repo_url_cleaned[0] 
        response = requests.get(repo_url_cleaned)
        if response.status_code == 200:
            repo_data = response.json()
            language = repo_data.get("language")
            stars_per_language[language] += repo_data.get("stargazers_count", 0)
        else:
            print(f"Error fetching repository data for {repo_url_cleaned}: {response.status_code}")
    df = pd.DataFrame(stars_per_language.items(), columns=["Language", "Stars"])
    if not df.empty:
        st.write(df.set_index("Language"))
    else:
        st.write("No repository data available for this user.")

def stars_per_repo_top10(user_data):
    st.subheader("Top 10 Starred Repositories")
    starred_repos = user_data.get("Starred Repositories", "").split(",") if user_data.get("Starred Repositories") else []
    if starred_repos:
        repo_stars = defaultdict(int)
        for repo_url in starred_repos:
            repo_url_cleaned = repo_url.strip().strip("'\"")
            stars = stars_per_language(repo_url_cleaned)  # Assuming you have a function to get stars for a repo
            repo_stars[repo_url_cleaned] += stars
        sorted_repos = sorted(repo_stars.items(), key=lambda x: x[1], reverse=True)[:10]
        df = pd.DataFrame(sorted_repos, columns=["Repository", "Stars"])
        st.write(df.set_index("Repository"))
    else:
        st.write("No starred repository data available for this user.")

def get_repos_per_language(user_data):
    st.subheader("Repositories per Language")
    repos_per_language = defaultdict(int)
    starred_repos = user_data.get("Starred Repositories", "").split(",") if user_data.get("Starred Repositories") else []
    subscriptions = user_data.get("Subscriptions", "").split(",") if user_data.get("Subscriptions") else []
    repositories = starred_repos + subscriptions
    for repo_url in repositories:
        repo_url_cleaned = repo_url.strip().strip("'\"")  
        language = get_language_from_repo_url(repo_url_cleaned)
        if language:
            repos_per_language[language] += 1
    df = pd.DataFrame(repos_per_language.items(), columns=["Language", "Repositories"])
    if not df.empty:
        st.write(df.set_index("Language"))
    else:
        st.write("No repository data available for this user.")

def commit_per_repo_top10(user_data):
    st.subheader("Top 10 Repositories by Commits")
    starred_repos = user_data.get("Starred Repositories", "").split(",") if user_data.get("Starred Repositories") else []
    subscriptions = user_data.get("Subscriptions", "").split(",") if user_data.get("Subscriptions") else []
    repositories = starred_repos + subscriptions
    if repositories:
        repo_commits = defaultdict(int)
        for repo_url in repositories:
            repo_url_cleaned = repo_url.strip().strip("'\"").strip("['")
            commits = commits_per_repository(repo_url_cleaned)  # Corrected function name
            repo_commits[repo_url_cleaned] += commits
        sorted_repos = sorted(repo_commits.items(), key=lambda x: x[1], reverse=True)[:10]
        df = pd.DataFrame(sorted_repos, columns=["Repository", "Commits"])
        st.write(df.set_index("Repository"))
    else:
        st.write("No repository data available for this user.")
def commits_per_repository(repo_url):
    try: 
        #headers = {"Authorization": f"token {ACCESS_TOKEN}"}
        response = requests.get(repo_url)#, headers=headers)
        if response.status_code == 200:
            return response.json().get("commits_count", 0)  
        elif response.status_code == 403:
            print("Received a 403 error. Retrying after 15 minutes...")
            time.sleep(900)  # Sleep for 15 minutes
            return commits_per_repository(repo_url) 
        else:
            print(f"Error fetching commits data for {repo_url}: {response.status_code}")
    except Exception as e:
        print(f"Error fetching commits data for {repo_url}: {e}")
    return 0


def commits_per_language(user_data):
    st.subheader("Commits per Language")
    commits_per_language = defaultdict(int)
    starred_repos = user_data.get("Starred Repositories", "").split(",") if user_data.get("Starred Repositories") else []
    subscriptions = user_data.get("Subscriptions", "").split(",") if user_data.get("Subscriptions") else []
    repositories = starred_repos + subscriptions
    for repo_url in repositories:
        repo_url_cleaned = repo_url.strip().strip("'\"")  
        language = get_language_from_repo_url(repo_url_cleaned)
        if language:
            commits_per_language[language] += 1
    languages = list(commits_per_language.keys())
    commits = list(commits_per_language.values())
    plt.figure(figsize=(8, 8))
    plt.pie(commits, labels=languages, autopct='%1.1f%%', startangle=140)
    plt.axis('equal') 
    plt.title("Commits per Language")
    st.pyplot(plt)

def display_user_statistics(user_data):
    st.subheader("User Statistics")
    st.write("Number of Public Repositories:", user_data.get("Public Repositories", 0))
    st.write("Total Commits:", user_data.get("Total Commits", 0))
    st.write("Languages Used:", user_data.get("Languages",))

def display_popular_languages(user_data):
    st.subheader("Popular Languages")
    languages_string = user_data.get("Languages", "")
    languages_dict = {}
    if languages_string:
        pairs = languages_string.split(", ")
        for pair in pairs:
            language, bytes = pair.split(":")
            languages_dict[language.strip()] = bytes.strip()
    if languages_dict:
        df = pd.DataFrame(list(languages_dict.items()), columns=["Language", "Bytes"])
        st.bar_chart(df.set_index("Language"))
    else:
        st.write("No language data available for this user.")

def display_average_commits(user_data):
    st.subheader("Average Commits")
    followers_count = user_data.get("Followers Count", 0)
    following_count = user_data.get("Following Count", 0)
    average_commits = user_data.get("Total Commits", 0) / max(followers_count, 1)
    st.write("Average Commits per Follower:", average_commits)

def display_profile_analytics(user_data):
    st.subheader("Profile Analytics")
    st.write("User Bio:", user_data.get("Bio", ""))
    
def search_and_display_profile():
    st.sidebar.header("Search GitHub Profile")
    username = st.sidebar.text_input("Enter GitHub Username:")
    if st.sidebar.button("Search"):
        user_data = get_user_data(username)
        if user_data:
            st.header(f"Analytics for GitHub User: {username}")
            display_user_statistics(user_data)
            display_popular_languages(user_data)
            display_average_commits(user_data)
            display_profile_analytics(user_data)
            get_repos_per_language(user_data)
            stars_per_language(user_data)
            commits_per_language(user_data)
            commit_per_repo_top10(user_data)
            stars_per_repo_top10(user_data)

        else:
            st.error("User not found. Please enter a valid GitHub username.")

def main():
    st.title("GitHub User Analytics Dashboard")
    search_and_display_profile()

if __name__ == "__main__":
    main()