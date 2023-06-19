import random
from tqdm import tqdm
import numpy as np

class CRNode:
    
    def __init__(self, card):
        self.card = card
        self.name = card.name
    
    def __eq__(self, other):
        return self.name == other.name
    
    def displayNode(self, ax, x, y, imWidth, imHeight,zOrder):
        ax.imshow(self.card.image, extent=(x, x + imWidth, y, y + imHeight), zorder = zOrder)
    

class CRConnection:
    
    def __init__(self, card1Name, card2Name):
        self.fromCard = card1Name
        self.toCard = card2Name
        self.weight = 1
        
    def __eq__(self, other):
        return self.fromCard == other.fromCard and self.toCard == other.toCard
    
    def incrementWeight(self):
        self.weight = self.weight + 1
    
    def getWeight(self):
        return weight


class CRInteractionNetwork:
    def __init__(self):
        self.nodes = []
        self.connections = {}
        
    def addNode(self, card):
        node = CRNode(card)
        if (not node in self.nodes):
            self.nodes.append(node)
            self.connections[node.name] = []
    
    def existsNode(self, cardName):
        for i in range(0,len(self.nodes)):
            if(self.nodes[i].name == cardName):
                return True
        
        return False
    
    def getConnectionIndex(self, card1Name, card2Name):
        for i in range(0,len(self.connections[card1Name])):
            conn = self.connections[card1Name][i]
            if(conn.toCard == card2Name):
                return i
        
        return -1
    
    def incrementConnection(self, card1Name, card2Name):
        if(self.existsNode(card1Name) and self.existsNode(card2Name)):
            #If the connection does not exist yet 
            if(not CRConnection(card1Name, card2Name) in self.connections[card1Name]):
                newConnection = CRConnection(card1Name, card2Name)
                self.connections[card1Name].append(newConnection)
            
            else:
                index = self.getConnectionIndex(card1Name, card2Name)
                self.connections[card1Name][index].incrementWeight()
                
    
    def getAllConnections(self):
        allConnections = []
        for i in range(0,len(self.nodes)):
            nodeConnections = self.connections[self.nodes[i].name]
            allConnections.extend(nodeConnections)
        
        return allConnections
    
    def drawGraph(self, ax, maxWeight,nIters = 10):
        nNodes = len(self.nodes)
        nodeX = {}
        nodeY = {}
        nodeDispX = {}
        nodeDispY = {}

        imgWidth = 30
        imgHeight = 30
        
        width = 1000
        height = 1000
        area = width*height
        C = 1
        k = C*np.sqrt(area/nNodes)
        t = 10
        
        connectionColor = "#249de3"
        
        for i in range(0,nNodes):
            node = self.nodes[i]
            nodeX[node.name] = random.random()*height
            nodeY[node.name] = random.random()*width
        
        for s in tqdm(range(0,nIters)):
        
            #Repulsive forces
            for i in range(0,nNodes):
                node = self.nodes[i]
                nodeDispX[node.name] = 0
                nodeDispY[node.name] = 0
                
                for j in range(0,nNodes):
                    node2 = self.nodes[j]
                    if(i != j):
                        delta = np.array([nodeX[node.name] - nodeX[node2.name], nodeY[node.name] - nodeY[node2.name]])
                        deltaNorm = np.sqrt((delta[1])**2 + (delta[0])**2)
                        if(deltaNorm != 0):
                            repulsiveForce = (k**2)/deltaNorm
                            nodeDispX[node.name] = nodeDispX[node.name] + repulsiveForce*(delta[0]/deltaNorm)
                            nodeDispY[node.name] = nodeDispY[node.name] + repulsiveForce*(delta[1]/deltaNorm)
        
            #Attractive forces with the edges
            for i in range(0,nNodes):
                node = self.nodes[i]
                for j in range(0,nNodes):
                    node2 = self.nodes[j]
                    connectionIndex = self.getConnectionIndex(node.name, node2.name)
                    if(i != j and connectionIndex != -1):
                        delta = np.array([nodeX[node.name] - nodeX[node2.name], nodeY[node.name] - nodeY[node2.name]])
                        deltaNorm = np.sqrt((delta[1])**2 + (delta[0])**2)
                        if(deltaNorm != 0):
                            attractiveForce = -(deltaNorm**2)/k
                            nodeDispX[node.name] = nodeDispX[node.name] + attractiveForce*(delta[0]/deltaNorm)
                            nodeDispY[node.name] = nodeDispY[node.name] + attractiveForce*(delta[1]/deltaNorm)
            
            #Adjust the positions
            for i in range(0,nNodes):
                node = self.nodes[i]
                normDisp = np.sqrt(nodeDispX[node.name]**2 + nodeDispY[node.name]**2)
                nodeX[node.name] = nodeX[node.name] + (nodeDispX[node.name]/normDisp)*np.min([normDisp, t])
                nodeY[node.name] = nodeY[node.name] + (nodeDispY[node.name]/normDisp)*np.min([normDisp, t])
                #nodeX[node.name] = np.min([width/2, np.max([nodeX[node.name], -width/2])])
                #nodeY[node.name] = np.min([height/2, np.max([nodeY[node.name], -height/2])])
            
            t = (1/(s + 1))*t 
                
        #Draw the connections
        allConnections = self.getAllConnections()
        zOrder = 0
        for i in range(0,len(allConnections)):
            connection = allConnections[i]
            xFrom = nodeX[connection.fromCard]+imgWidth/2
            xTo = nodeX[connection.toCard]+imgWidth/2
            yFrom = nodeY[connection.fromCard]+imgHeight/2
            yTo = nodeY[connection.toCard]+imgHeight/2
            ax.plot([xFrom, xTo], [yFrom, yTo], color = connectionColor, alpha = connection.weight/maxWeight, linewidth = 0.4, zorder = zOrder)
            zOrder = zOrder + 1
        
        xValsArr = []
        yValsArr = []
        #Draw the nodes
        zOrder = zOrder + 100000
        for i in range(0,len(self.nodes)):
            node = self.nodes[i]
            xVal = nodeX[node.name]
            yVal = nodeY[node.name]
            xValsArr.append(xVal)
            yValsArr.append(yVal)
            node.displayNode(ax, xVal, yVal, imgWidth, imgHeight, zOrder)  
            zOrder = zOrder + 1
        
        ax.set_xlim([min(xValsArr) - imgWidth, max(xValsArr) + imgWidth])
        ax.set_ylim([min(yValsArr) - imgHeight, max(yValsArr) + imgHeight])
        