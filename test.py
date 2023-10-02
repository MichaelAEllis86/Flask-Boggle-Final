from unittest import TestCase
from app import app
from flask import session, request
from boggle import Boggle
# import json



class FlaskTests(TestCase):

    def setUp(self):
        """setup! enabling flask testing configs here"""
        app.config['TESTING']=True
        app.config['DEBUG_TB_HOSTS']=['dont-show-debug-toolbar']
        

    def test_root_page(self):
        """Test if root page returns correct status code for GET request and returns included html"""
        with app.test_client() as client:
            response=client.get("/")
            html=response.get_data(as_text=True)
            
            self.assertEqual(response.status_code,200)
            self.assertIn('<a href="/highscores">Highscore & Games Played</a>',html)
    
    def test_homepage_andorthe_gamepage(self):
        """Test if home page returns correct status code for GET request and returns included html, 
        Tests if the board is saved in the session['current-board']"""
        with app.test_client() as client:
            response=client.get("/home")
            html=response.get_data(as_text=True)

            self.assertEqual(response.status_code,200)
            self.assertIn('<h1 id="gamepagewelcome">Welcome to the Game Page</h1>', html)
            self.assertIn('current_board', session)
           
    def test_highscores_page_with_data(self):
        """Test if highscores page returns correct status code for GET request and returns included html, 
        Tests if session is correctly updated with games-played and highscore data if preexisting score and game data is present in session already """
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['highscore']=30
                change_session['games-played']=5
            response=client.get("/highscores")
            html=response.get_data(as_text=True)
            self.assertEqual(response.status_code,200)
            self.assertIn('<h1 id="highscorewelcome">Welcome to the Highscore Page</h1>', html)
            self.assertEqual(session['highscore'],30)
            self.assertEqual(session['games-played'],5)

    def test_highscoresPageWithNoData(self):
        """test if highscores page returns correct status code for GET request and returns included html, 
        Tests if session is correctly updated with games-played and highscore data if there is no previous player data """
        with app.test_client() as client:
            response=client.get("/highscores")
            html=response.get_data(as_text=True)
            self.assertEqual(response.status_code,200)
            self.assertIn('<h1 id="highscorewelcome">Welcome to the Highscore Page</h1>', html)
            self.assertEqual(session['highscore'],0)
            self.assertEqual(session['games-played'],0)

    def test_check_valid(self):
        """test if """
        with app.test_client() as client:
             with client.session_transaction() as change_session:
                change_session['current_board']=[["C","A","T","A","C"],["C","A","T","A","C"],["C","A","T","A","C"],["C","A","T","A","C"],["C","A","T","A","C"]]
        response=client.get('/check?word=cat')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json["result"],"ok")

    def test_check_invalid_not_on_board(self):
        with app.test_client() as client:
             with client.session_transaction() as change_session:
                change_session['current_board']=[["C","A","T","A","C"],["C","A","T","A","C"],["C","A","T","A","C"],["C","A","T","A","C"],["C","A","T","A","C"]]
        response=client.get('/check?word=mellophone')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json["result"],"not-on-board")
    
    def test_check_invalid_not_a_word(self):
        with app.test_client() as client:
             with client.session_transaction() as change_session:
                change_session['current_board']=[["C","A","T","A","C"],["C","A","T","A","C"],["C","A","T","A","C"],["C","A","T","A","C"],["C","A","T","A","C"]]
        response=client.get('/check?word=roomba')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json["result"],"not-word")


    def test_playerdata(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["highscore"]=30
                change_session['games-played']=0
                print("printing the CHANGED highscore session...",change_session["highscore"])
                print("printing the CHANGED gamesplayed session...",change_session['games-played'])

            # Failed solutions for finding the correct data format to send to client route

            # response=client.post('/playerdata', data=json.loads("{\"score\":\"50\"}")) from browser response.config.data in javascript
            # response=client.post("/playerdata",{"score":"0"}) 
            # response=client.post("/playerdata",data={"score":"0"}) using a data parameter
            # response=client.post("/playerdata", json={{ "method":"POST", "url":"/playerdata","data":{"score":"10"}}})


            response=client.post('/playerdata',json={"score":"50"})
            print("printing the NEW games_played session AFTER DATA RECEIVED...",session['games-played'])
            print("printing the NEW highscore session AFTER DATA RECEIVED...",session['highscore'])
            print("printing response.json...",response.json)
            print("printing response.data...",response.data)
            print("printing response.data.score",response.data)
            self.assertEqual(response.status_code,200)
            self.assertEqual(session["games-played"],1)
            self.assertEqual(session["highscore"],50)
            self.assertEqual(response.json["brokeRecord"],True)
            self.assertEqual(response.json["highscore"],50)
            self.assertEqual(response.json['games_played'],1)
            
            
            
    #     const response=await axios({
    #     method:"POST",
    #     url:"/playerdata",
    #     data:{score:`${score}`}
    # })