# Movie Success Predictor

The Project predicts the success of a movie based on various criteria like actors, directors and genres. It also has ability to predicts its success based on the twitter trend as well.

### Modules required are
* Networkx      
	pip install networkx 
* Imdbpie        
	pip install imdbpie
* Tweepy (To run twitter code)     
	pip install tweepy
* nltk           
	pip install nltk
	then run nltk.download() in python shell to download all the nltk files

### Steps to run the code
1. python main.py shell // _To start the Shell_
2. python main.py predict // _To start the prediction_
3. python main.py predict twitter movie_name // _To enable prediction from twitter. movie_name is the name of the movie that twitter uses 													 to search_


### Commands in Shell
1. GET _attributes_ [ OF _movies_ [ WITH _condition_ ]] // The square brackets indicates optional queries AND ARE NOT THE PART OF QUERY

	* _attributes_ - Any combination of : actors, directors, genres, year, ratings         
	* _movies_ - the movie names that we have to get attributes of      
	* _condition_ - Condition for filtering out the movies. AND is used for `and` operation, OR is used for `or`, AS is used for multiple inputs       
	Eg: GET actors, directors OF "the revenant", "inception" // This would send a graph of movies revenant and inception with just actors and directors            
	Eg: GET ratings OF * WITH actors AS ['christian bale'] AND directors AS ['christopher nolan'] // This sends a graph with just ratings of all movies with christian bale as actor and chritopher nolan as director. 

2. SUGGEST _name_ [ LIMIT _limit_ ] // Suggests _limit_ number of values for input _name_
	Eg: SUGGEST "Christopher"

3. QUIT // To quit the command

