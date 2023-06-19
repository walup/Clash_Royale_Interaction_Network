import requests
from PIL import Image
from io import BytesIO
from tqdm import tqdm

class ClashRoyaleDataRequest:
    
    def __init__(self, token):
        self.token = token
        self.baseURL = "https://api.clashroyale.com/v1"
        #Header required by the clash royale api 
        authorization = 'Bearer '+self.token
        self.headers = {'Content-type': 'application/json', 'Authorization': authorization}
        
    
    def getLastBattles(self, playerTag):
        
        lastBattlesURL = self.baseURL + "/players/"+playerTag+"/battlelog"
        #lastBattlesURL = self.baseURL + "/cards"
        response = requests.get(lastBattlesURL, headers = self.headers)
        #If the request of data was successful
        responseObject = -1
        if(response.status_code == 200):
            responseObject = response.json()
        else:
            print("nothing to see here")
        
        
        return responseObject
    
    def getCards(self):
        cardURL = self.baseURL + "/cards"
        cards = []
        imSize = (256,256)
        response = requests.get(cardURL, headers = self.headers)
        if(response.status_code == 200):
            cardResp = response.json()
            for i in tqdm(range(0,len(cardResp['items']))):
                cardJSON = cardResp['items'][i]
                cardName = cardJSON['name']
                cardURLImage = cardJSON['iconUrls']['medium']
                
                resp = requests.get(cardURLImage)
                img = Image.open(BytesIO(resp.content))
                img = img.resize(imSize)
                card = Card(cardName, img)
                cards.append(card)
            
            return cards
        else:
            return -1
        

class Card:
    
    def __init__(self, name, image):
        self.name = name
        self.image = image

    
class Battle:
    
    def __init__(self, battleJSON):
        self.teamName = battleJSON['team'][0]['name']
        self.opponentName = battleJSON['opponent'][0]['name']
        
        teamCrowns = int(battleJSON['team'][0]['crowns'])
        opponentCrowns = int(battleJSON['opponent'][0]['crowns'])
        
        if(teamCrowns > opponentCrowns):
            self.winner = self.teamName
        elif(opponentCrowns > teamCrowns):
            self.winner = self.opponentName
        else:
            self.winner = "Draw"
        
        self.teamLeakedElixir = battleJSON['team'][0]['elixirLeaked']
        self.opponentLeakedElixir = battleJSON['opponent'][0]['elixirLeaked']
        
        self.teamDeck = []
        for i in range(0,len(battleJSON['team'][0]['cards'])):
            self.teamDeck.append(battleJSON['team'][0]['cards'][i]['name'])
            
        self.opponentDeck = []
        for i in range(0,len(battleJSON['opponent'][0]['cards'])):
            self.opponentDeck.append(battleJSON['opponent'][0]['cards'][i]['name'])
        
        day = battleJSON['battleTime'][6:8]
        month = battleJSON['battleTime'][4:6]
        year = battleJSON['battleTime'][0:4]
        self.date = day + "-"+month+"-"+year
        
        
    
    def getBattleInfo(self):
        battleString = ""
        battleString = battleString + "Date: "+self.date + "\n"
        #Team name
        battleString = battleString + "Team: "+self.teamName+"\n"
        #Opponent name
        battleString = battleString + "Opponent: "+self.opponentName + "\n"
        #Winner 
        battleString = battleString + "Winner: "+self.winner+"\n"
        #Team elixir leaked
        battleString = battleString + "Team elixir leaked: "+str(self.teamLeakedElixir)+"\n"
        battleString = battleString + "Opponent elixir leaked: "+str(self.opponentLeakedElixir)+"\n"
        
        battleString = battleString + "Team deck: "+"\n"+("-"*10)+"\n"
        for i in range(0,len(self.teamDeck)):
            battleString = battleString + self.teamDeck[i]+"\n"
        
        
        
        battleString = battleString + "\nOpponent deck: "+"\n"+("-"*10)+"\n"
        for i in range(0,len(self.opponentDeck)):
            battleString = battleString + self.opponentDeck[i]+"\n"
        
        return battleString
    
    def printBattleInfo(self):
        battleString = self.getBattleInfo()
        print(battleString)