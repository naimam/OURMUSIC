# CSC 4350 Project 1 Milestone by Naima Mohamed 
A simple webpage that displays a random artist and a random song every time you refresh the page.
Also displays an audio preview (if available) and a link to the genius lyrics of the song.
View the website [here](https://naimsproj1m1.herokuapp.com/ "website link").
 
![Screenshot of website](https://github.com/csc4350-f21/project1-nmohamed6/blob/main/static/project1pg.png "Screenshot of website")


## Technologies, Frameworks, Libraries, and APIs used
* Developed in Azure VM using VS Code. 
* Version tracking using Git & Github.
* Deployed using heroku.
* PYTHON - 
  * os & dotenv (modules) - to get values in .env file and set them as environment variables in spot.py.
  * spotipy (libaray) - simplifies process of accessing music data through Spotify's Web API.
  * flask (framework) - allows the webapp to developed easily / fetches python data and displays it on webpage.
* HTML - displays the data on a webpage.
* CSS - styles the data in a readable way.
* Spotify API - used to get information on: 
   *  artist: name, image, top tracks.
   *  song: name, song image, preview url.
* Genius API - used to get lyrics of the current song.
 
 
## Setup
1. Install: os, dotenv, spotipy, random, requests, flask
2. Create [Spotify APP](https://developer.spotify.com/documentation/web-api/ "Spotify API") and copy the Client ID and Client Secret.
3. Create [Genius APP](https://docs.genius.com/ "Genius API") and copy the genius token.
4. Create .env file in project directory and store your Spotify client id & client secret, and your Genius access token. Do so with the following code:
  ```python
     export CLIENT_ID = "yourclientid"
     export CLIENT_SECRET = "yourclientsecret"
     export GENIUS_TOKEN = "yourgeniustoken"
   ```
 5. If want to run on localhost - comment out the following lines on app.py:
   ```python
   app.run(
    # host='0.0.0.0',
    # port=int(os.getenv('PORT', 8080)),
    debug=True
   )
   ```
  6. Run app.py and follow the link to your browser to view the site!


## Technical Issues / Problems
1. Git was not letting me push to my main branch, so I searched on stack overflow for a solution. I found out I could use the command "git push -f origin main". It worked, however, I lost all of my previous commits.
2. Another issue I found was that when I deployed my app to heroku, I got an "Application Error". When I checked the logs, I found that I had the error "Heroku H10-App crashed". After searching through my code, I found that I had not initialized port to "port=int(os.getenv('PORT', 8080))".
3. An issue I had was figuring out how to return multiple values in my get methods in spot.py, and then access them in my Flask app. By checking out stack overflow, I was able to figure out how to do so. By using methodName[i], you can access the variables the function returns.

## Additional Features To Implement:
1. Using Twitter API to access tweets mentioning the artist name & song - was going to include this but there is an approval application that takes time.
2. Use other languages such as Javascript to make the webpage more visually appealing. For example, creating a custom music player with javascript.
3. Display more information on artists using the Spotify API such as their albums and related artists.



