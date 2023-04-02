from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()

#uvicorn main:app --host 0.0.0.0 --port 5050 --reload

@app.get("/new_movies")
async def new_movies_list():
    return new_movies()


def new_movies():
    response = requests.get("http://www.cgv.co.kr/movies/?lt=1&ft=0")
    result_list = []
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        section = soup.select(".sect-movie-chart")
        movie_section = section[0]
        movies = movie_section.find_all("li")
        for movie in movies:
            result = {}
            print(movie.find("img")["src"])
            result['img'] = movie.find("img")["src"]
            print(movie.select_one(".title").text)
            result['title'] = movie.select_one('.title').text
            result_list.append(result)
    else:
        print("오류 발생")

    return result_list


@app.get("/search_movie_poster")
async def movie_poster(movie_name):
    return search_movie_poster(movie_name)


def search_movie_poster(movie_name):
    result_list = []
    response = requests.get("http://www.cgv.co.kr/search/?query=" + movie_name)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        section = soup.select(".searchingMovieResult_list")
        movie_section = section[0]
        movies = movie_section.find_all("li")

        for movie in movies:
            movieNameList = str(movie.select_one(".searchingMovieName").text).split("\n")
            movieName = movieNameList[0].split('\r')[0]
            movieAge = movieNameList[2]
            result = {'img': movie.find("img")["src"], 'movie_name': movieName, 'movie_age': movieAge}
            if 'movieState' in movie.find("span").parent.get("class"):
                result['open-date'] = movie.find_all("span")[1].text
            else :
                result['open-date'] = movie.find("span").text
            result_list.append(result)

        print(result_list)
    else:
        print("오류 발생")

    return result_list
