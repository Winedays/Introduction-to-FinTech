import csv
import numpy as np
import matplotlib.pyplot as plt
# requirements :
# matplotlib==2.0.1
# numpy==1.15.0
# pandas==0.23.4

# read SPY.csv
def readSPY( file ) :
    adjCloseList = []
    f = open( file , 'r' , encoding='utf-8' )  # read file
    rows = csv.reader( f ) 
    next( rows ) # skip title
    for row in rows :
        adjCloseList.append( float(row[5]) )  # get Adj_Close
    
    return adjCloseList ;

# cal. each day MA
# adjClose : List of adjClose data each day
# maDay : day length of MA
def MA( adjClose , startDay , endDay , maDay ) :
    maList = []
    # MA with day length < day, change to lower dayMA 
    if startDay < maDay :
        for day in range( 1 , maDay ) :
            windowData = adjClose[ :day ]
            ma = np.mean( windowData )
            maList.append( ma )
        startDay = maDay
    # MA with day length > day
    for day in range( startDay , endDay ) :
        windowData = adjClose[ day-maDay : day ]
        ma = np.mean( windowData )
        maList.append( ma )
    
    return maList ;

# cal. all case in diff. MA
def allMA( adjCloseList, startDay, endDay, windowSize ) :
    maResult = [] 
    for window in windowSize :
        ma = MA( adjCloseList , startDay , endDay , window )
        maResult.append( ma )
    return maResult ;

# make result graph
def makeGraph( filename , title , adjClose , maResult, startDay, endDay, labelName ) : 
    plt.switch_backend('agg') # for run on linux without GUI
    # make result graph
    xlabel = np.arange( startDay, endDay )
    plt.plot( xlabel , adjClose, '-', label='Price')
    for i in range(len(maResult)) :
        plt.plot( xlabel , maResult[i], '-', label=labelName[i])
    plt.xlabel( "Data Index" )
    plt.ylabel( "MA" )
    plt.xlim( startDay, endDay-1 )
    # plt.xticks( np.arange(startDay, endDay, 10) )
    plt.title( title )
    plt.legend( loc='lower right' )
    fig = plt.gcf()
    fig.set_size_inches( 12.5, 8.2 )
    fig.savefig( filename, dpi=125 )
    # plt.show()
    plt.close()
    print( "save \"" + title + "\" as \"" + filename + "\"" )
    return ;

if __name__ == "__main__" :
    # read file
    SPYFile = "./SPY.csv"
    adjCloseList = readSPY( SPYFile )
    
    # set windows size
    windowSize = [5, 10, 20, 60, 120, 240]
    labelName = ["5MA", "10MA", "20MA", "60MA", "120MA", "240MA"]
    
    # all data view
    startDay = 1 ; endDay = len(adjCloseList) ;
    maResult = allMA( adjCloseList, startDay, endDay, windowSize )
    makeGraph( "./global.png" , "Global(10-year) view" , adjCloseList[startDay:endDay] , maResult, startDay, endDay, labelName )
    
    # Zoom in 1-year view
    startDay = 1020 ; endDay = startDay + 240 ;
    maResult = allMA( adjCloseList, startDay, endDay, windowSize )
    makeGraph( "./1-year.png" , "1-year view" , adjCloseList[startDay:endDay] , maResult, startDay, endDay, labelName )
    
    # Zoom in 1-quarter(1-season) view
    startDay = 1020 ; endDay = startDay + 60 ;
    maResult = allMA( adjCloseList, startDay, endDay, windowSize )
    makeGraph( "./1-season.png" , "1-season view" , adjCloseList[startDay:endDay] , maResult, startDay, endDay, labelName )
    