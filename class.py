import random

AVERAGE_CFB_NUMBER_DRIVES = 12

class Team():

    def __init__(self, name, offRank, defRank, stRank, talentRank, coachRank, turnoverRank):
        self.name = name
        self.offRank = offRank
        self.defRank = defRank
        self.stRank = stRank
        self.talentRank = talentRank
        self.coachRank = coachRank
        self.turnoverRank = turnoverRank
    
    # Getters
    def getName(self):
        return self.name

    def getOffRank(self):
        return self.offRank
    
    def getDefRank(self):
        return self.defRank
    
    def getSTRank(self):
        return self.stRank
    
    def getTalentRank(self):
        return self.talentRank
    
    def getCoachRank(self):
        return self.coachRank
    
    def getTurnoverRank(self):
        return self.turnoverRank
    
    # Setters
    def setOffRank(self, offRank):
        self.offRank = offRank

    def setDefRank(self, defRank):
        self.defRank = defRank

    def setSTRank(self, stRank):
        self.stRank = stRank

    def setTalentRank(self, talentRank):
        self.talentRank = talentRank

    def setCoachRank(self, coachRank):
        self.coachRank = coachRank

    def setTurnoverRank(self, turnoverRank):
        self.turnoverRank = turnoverRank
    

def coinFlip():
    if random.random() > 0.5:
        return True
    else:
        return False


class Game():
    
    def __init__(self, homeTeam, awayTeam, avgNumberDrives):
        self.homeTeam = homeTeam
        self.awayTeam = awayTeam
        self.avgNumberDrives = avgNumberDrives

    def playDrive(self, possTeam, nonPossTeam):
        if possTeam.getOffRank() > nonPossTeam.getDefRank():
            scoreRatio = nonPossTeam.getDefRank() / possTeam.getOffRank()
            print(scoreRatio)
            if scoreRatio > random.random():
                if scoreRatio > random.random():
                    return 7
                else:
                    return 3
            else:
                return 0
        else:
            scoreRatio = 1 - (possTeam.getOffRank() / nonPossTeam.getDefRank())
            print(scoreRatio)
            if scoreRatio > random.random():
                if scoreRatio > random.random():
                    return 7
                else:
                    return 3
            else:
                return 0
        
    def playGame(self):
        self.numberDrives = round(random.uniform(self.avgNumberDrives - 3, self.avgNumberDrives + 3))
        self.homeScore = 0
        self.awayScore = 0
        if coinFlip():
            possTeam = self.homeTeam
        else:
            possTeam = self.awayTeam
        print(f"Initial possession: {possTeam.getName()}")  # print the team that starts with the ball
        for i in range(self.numberDrives):
            print(f"Drive number: {i+1}")  # print the current drive number
            if possTeam == self.homeTeam:
                score = self.playDrive(self.homeTeam, self.awayTeam)
                self.homeScore += score
                print(f"Home team scored: {score}")  # print the score of the home team in this drive
                possTeam = self.awayTeam
            else:
                score = self.playDrive(self.awayTeam, self.homeTeam)
                self.awayScore += score
                print(f"Away team scored: {score}")  # print the score of the away team in this drive
                possTeam = self.homeTeam
        print(f"Final scores - Home: {self.homeScore}, Away: {self.awayScore}")  # print the final scores
        if self.homeScore > self.awayScore: 
            return self.homeTeam.getName(), (self.homeScore, self.awayScore)
        elif self.awayScore > self.homeScore:
            return self.awayTeam.getName(), (self.awayScore, self.homeScore)
        else:
            return "Tie", (self.homeScore, self.awayScore)
        
            
Michigan = Team('Michigan', offRank=53, defRank=2, stRank=3, talentRank=4, coachRank=5, turnoverRank=6)
Alabama = Team('Alabama', offRank=66, defRank=18, stRank=4, talentRank=5, coachRank=6, turnoverRank=1)
Georgia = Team('Georgia',offRank=3, defRank=4, stRank=5, talentRank=6, coachRank=1, turnoverRank=2)

game1 = Game(Michigan, Alabama, AVERAGE_CFB_NUMBER_DRIVES)  # Replace "team2" with "Alabama"
game2 = Game(Alabama, Georgia, AVERAGE_CFB_NUMBER_DRIVES)
game3 = Game(Georgia, Michigan, AVERAGE_CFB_NUMBER_DRIVES)

print(game1.playGame())
# print(game2.playGame())
# print(game3.playGame())

