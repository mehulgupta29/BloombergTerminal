"""
This is the starting point of the project. It is equivalent to the main() in C / Java
"""
import sys
import Constants as const
import csv
import statistics
import matplotlib.pyplot as plt
import numpy as np

TAG = 'Code/Python/Main :'

def inputParams(argv):
	params={}

	if ('--index' or '-i') in argv:
		params['index']=argv[argv.index('--index')+1]
	else:
		params['index']='snp500'

	if ('--noofweeksa' or '-wsa') in argv:
		params['noofweeksa']=int(argv[argv.index('--noofweeksa')+1])
	else:
		params['noofweeksa']=int(19)

	if ('--bistartbalance' or '-bi') in argv:
		params['bistartbalance']=int(argv[argv.index('--bistartbalance')+1])
	else:
		params['bistartbalance']=int(1000)

	if ('--startweekbi' or '-wbi') in argv:
		params['startweekbi']=int(argv[argv.index('--startweekbi')+1])
	else:
		params['startweekbi']=int(31)

	if ('--multiplier' or '-m') in argv:
		params['multiplier']=float(argv[argv.index('--multiplier')+1])
	else:
		params['multiplier']=float(0.1)

	if ('--periods' or '-p') in argv:
		params['periods']=float(argv[argv.index('--periods')+1])
	else:
		params['periods']=float(20)

	return params

def loadDataCSV(fname):
	hds=[]
	dataset=csv.reader(open(fname, 'r'))
	for data in dataset:
		hds.append(data)
	return hds[1:]

def preprocessing(dataset):
	hds=[]
	dataset=sorted(dataset)
	for data in dataset:
		l=[]
		l.append(data[0])
		for item in data[1:]:
			l.append(float(item))

		hds.append(l)
	return hds

def movingAverage(currentClose, prevEMA, multiplier):
	return round(((currentClose - prevEMA) * multiplier) + prevEMA, 2)

def calculateEMA(dataset, params):
	ema=[]
	sa=statistics.mean([round(item[4], 2) for item in dataset[:params['noofweeksa']]])

	for i in range(len(dataset)):
		if i < (params['noofweeksa']-1):
			ema.append([dataset[i][0], round(dataset[i][4], 2), None])
		elif i == (params['noofweeksa']-1):
			ema.append([dataset[i][0], round(dataset[i][4], 2), round(sa, 2)])
		else:
			ema.append([dataset[i][0], round(dataset[i][4], 2), movingAverage(round(dataset[i][4], 2), ema[i-1][2], params['multiplier'])])
	return ema

def buyIndex(currClose, prevClose, prevBI):
	return int((currClose/prevClose)*prevBI)

def calculateBUYINDEX(dataset, params):
	bi=[]

	for i in range(len(dataset)):
		if i < (params['startweekbi']-1):
			bi.append([dataset[i][0], dataset[i][1], dataset[i][2], None])
		elif i == (params['startweekbi']-1):
			bi.append([dataset[i][0], dataset[i][1], dataset[i][2], params['bistartbalance']])
		else:
			bi.append([dataset[i][0], dataset[i][1], dataset[i][2], buyIndex(dataset[i][1], dataset[i-1][1], bi[i-1][3])])

	return bi

def BUYAboveIndex(prevClose, prevEMA, currClose, prevBIaboveEMA):
	#if(Previous CLOSE > Previous EMA, (Current CLOSE / Previous CLOSE) * Previous BUY above EMA, Previous BUY above EMA)

	if prevClose > prevEMA:
		return int((currClose/prevClose)*prevBIaboveEMA)
	else:
		return int(prevBIaboveEMA)


def calculateBUYAboveEMA(dataset, params):
	"""
	dataset=[Date, Close, EMA, BUYINDEX]
	"""
	buyAboveEMA=[]
	for i in range(len(dataset)):
		if i < (params['startweekbi']-1):
			buyAboveEMA.append([dataset[i][0], dataset[i][1], dataset[i][2], dataset[i][3], None])
		elif i == (params['startweekbi']-1):
			buyAboveEMA.append([dataset[i][0], dataset[i][1], dataset[i][2], dataset[i][3], params['bistartbalance']])
		else:
			buyAboveEMA.append([dataset[i][0], dataset[i][1], dataset[i][2], dataset[i][3], BUYAboveIndex(dataset[i-1][1], dataset[i-1][2], dataset[i][1], buyAboveEMA[i-1][4] )])

	return buyAboveEMA

def plotGraph(buyAboveEMA, params):
	"""
		blue = BUY INDEX
		green = BUY Above INDEX
	"""
	xlabel=[]
	line1y=[]
	line2y=[]
	for i in range(len(buyAboveEMA)):
		xlabel.append(buyAboveEMA[i][0])
		line1y.append(buyAboveEMA[i][3])
		line2y.append(buyAboveEMA[i][4])

	# red dashes, blue squares and green triangles
	#plt.plot(line1x, line1y, 'bs', line2x, line2y, 'g^')
	
	plt.plot(line1y[params['startweekbi']-1 :], 'b')
	plt.plot(line2y[params['startweekbi']-1 :], 'g')
	plt.legend(['Buy and Hold Index', 'Buy Above EMA'], loc='upper left')
	plt.show()


if __name__ == "__main__":
	"""
	run command: 
		python Main.py --index snp500 --noofweeksa 19 --periods 20 --multiplier 0.1 --bistartbalance 1000 --startweekbi 31

	csv data=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']
	"""
	print(TAG, "STARTING")

	params=inputParams(sys.argv)
	#print(params)

	#Load data from csv
	hds=loadDataCSV(const.HistoricalDataSet[params['index']])
	hds=preprocessing(hds)
	#print(hds)

	#calculate EMA
	ema=calculateEMA(hds, params)
	#print(ema[-1:])

	#calculate BUYINDEX
	bi=calculateBUYINDEX(ema, params)
	#print(bi[29: 32])

	#calculate BUYaboveEMA
	buyAboveEMA=calculateBUYAboveEMA(bi, params)
	#print(buyAboveEMA[30:32])
	#print(buyAboveEMA[-1:])

	#plot graph
	plotGraph(buyAboveEMA, params)

	print(TAG, "ENDING")