import API_CALL
from pprint import pprint
import cfbd
import json


##### ------- This file is used to calculate the success rate of a team at various distances from the end zone. It presently is slightly inaccurate and requires a few big fixes. ------- #####

# Call particular APIs
playsAPI = cfbd.PlaysApi(cfbd.ApiClient(API_CALL.configuration))
gamesAPI = cfbd.GamesApi(cfbd.ApiClient(API_CALL.configuration))
drivesAPI = cfbd.DrivesApi(cfbd.ApiClient(API_CALL.configuration))


# Test info
TEAM = 'Michigan'
YEAR = 2023
WEEK = 1


# Get data from APIs
gamesInfo = gamesAPI.get_games(year=YEAR, team=TEAM, season_type='regular')


def compileDrives(plays, drives):
    """
    This function takes in a list of plays of the type play object and a list of drives of the type drive object 
    and returns a list of tuples of the form (driveResult, seriesList) where driveResult is a string of the drive
    result and seriesList is a list of the yards to goal for each play in the drive.
    """

    # Assign a driveID ticker
    driveID = None
    driveResult = None

    # Create drive and series list
    drivesList = []
    seriesList = []

    # Iterate over play and pull desired offense plays (excluding kickoffs)
    for play in plays:
        if play.offense == TEAM and 'Kickoff' not in play.play_type:

            # Check for changes in driveID and add result and series info to drivesList if changed
            if play.drive_id != driveID:
                if driveID != None:
                    drivesList.append((driveResult, seriesList))
                    seriesList = []
                driveID = play.drive_id
                for drive in drives:
                    if drive.id == driveID:
                        driveResult = drive.drive_result
            
            # Add yards to goal to seriesList
            seriesList.append(play.yards_to_goal)
    
    # Add final drive to drivesList
    drivesList.append((driveResult, seriesList))
    return drivesList

# week8Drives = drivesAPI.get_drives(year=YEAR, week=8, team=TEAM)
# print(week8Drives[0])
# firstDrivePlays = playsAPI.get_plays(year=YEAR, week=8, team=TEAM)
# for play in firstDrivePlays:
#     if play.offense == TEAM and 'Kickoff' not in play.play_type:
#         if play.drive_id == week8Drives[0].id:
#             print(play)
#             print('\n')

# for week in range(8, 13):
#     playByPlay = playsAPI.get_plays(year=YEAR, week=week, team=TEAM)
#     drivesInfo = drivesAPI.get_drives(year=YEAR, week=week, team=TEAM)
#     drives = compileDrives(playByPlay, drivesInfo)
#     print(f'Week {week}:')
#     for drive in drives:
#         print(drive)
#     print('\n')




def distanceCalc(drives, distances=[25, 35, 50]):
    """
    This function takes in a list of drives of the form (driveResult, seriesList) and a list of distances of the form
    [25, 35, 50] and returns a list of tuples of the form (distance, TD%, FG%) where distance is the distance to goal
    """
    successRateDict = {}
    for drive in drives:
        for distance in distances:
            distanceFlag = False
            for actualDistance in drive[1]:
                if actualDistance <= distance:
                    distanceFlag = True
                    break
            if distanceFlag:
                if distance not in successRateDict:
                    successRateDict[distance] = {'TD': 0, 'FG': 0, 'Trips': 1}
                else:
                    successRateDict[distance]['Trips'] += 1
                if drive[0] == 'TD':
                    successRateDict[distance]['TD'] += 1
                elif drive[0] == 'FG':
                    successRateDict[distance]['FG'] += 1
    for distance, results in successRateDict.items():
        successRateDict[distance]['TD%'] = results['TD'] / results['Trips']
        successRateDict[distance]['FG%'] = results['FG'] / results['Trips']
        successRateDict[distance]['PTS%'] = (results['TD'] + results['FG']) / results['Trips']
    return successRateDict




# for i in range(1, 13):
#     playByPlay = playsAPI.get_plays(year=YEAR, week=i, team=TEAM)
#     drivesInfo = drivesAPI.get_drives(year=YEAR, week=i, team=TEAM)
#     drives = compileDrives(playByPlay, drivesInfo)
#     distanceDict = distanceCalc(drives, distances=[25, 20])
#     print(f'Week {i}:')
#     for k, v in distanceDict.items():
#         print(f"{k}: {v}")
#     print('\n')



def teamDistanceSuccessRateCalc(year, team, distances=[100, 95, 90, 85, 80, 75, 70, 65, 60, 55, 50, 45, 40, 35, 30, 25, 20, 15, 10, 5]):
    """
    This function takes in a year, team, and distances and returns a dictionary of the form {distance: successRate}
    """
    # Get data from APIs
    gamesInfo = gamesAPI.get_games(year=year, team=team)
    weeks = []
    allDrives = []
    for game in gamesInfo:
        weeks.append(game.week)
    for week in weeks:
        playByPlay = playsAPI.get_plays(year=year, team=team, week=week)
        drivesInfo = drivesAPI.get_drives(year=year, team=team, week=week)
        for drive in compileDrives(playByPlay, drivesInfo):
            allDrives.append(drive)
    successRateDict = distanceCalc(allDrives, distances)
    return successRateDict













successRateDict = teamDistanceSuccessRateCalc(YEAR, TEAM, distances=[25, 20])
# for distance, results in successRateDict.items():
#     print(f"{distance}yds to goal: {round((results['PTS%'] * 100), 2)}% chance of scoring")
# print('Year Totals:')
for k, v in successRateDict.items():
    print(f"{k}: {v}")