from datetime import datetime,timedelta
import sys,csv,os

#returns distance from (0,0) co-ordinates as warehouse to delievry point in grid
def dist(a):
  l=[]
  a=a.lower()
  if('w' in a):
    l=a.split("w")
  elif("e" in a):
    l=a.split("e")
  return int(l[0][1:])+int(l[1])

#Add time to delivery to ordertime,once we deliver the order,this gives us delivery time
def addtime(t,x):
	t = datetime.strptime(t,'%H:%M:%S')
	t = t+timedelta(minutes=x)
	return t.strftime("%H:%M:%S")

def deliver_order(curr,ip):
	d = dict()
	#Sorting dictionary according to order time and calculating the distance from warehouse co ordinates as (0,0) and appending it to 
	#new dictionary as d,key:order_id and value:[distance in number of blocks from warehouse,order_time]
	for i in (sorted(ip.items(), key=lambda x: x[1][1])):
		i[1][0]=dist(i[1][0])
		d[i[0]]=i[1]
	opl=[]#Output List
	dpl=[]#departure List
	while(len(d)):
		nd=dict()
		for k,v in d.items():
			if(v[1]>curr):
				break
			nd[k]=v 								            #Copying values less than curr_time																		
		if(not len(nd)):
			deliv=min(d.items(), key=lambda x: x[1][1])			#If no orders less than curr time, minimum order time available is taken as curr_time
			curr = deliv[1][1]
		else:
			deliv = min(nd.items(), key=lambda x: x[1][0])		#Picking order with min distance
		time_check = addtime(addtime(curr,deliv[1][0]),deliv[1][0])					#from warehouse (0,0)->(X,Y) delivery point
		if(time_check>'22:00:00'):									#No order after 10pm
			break
		opl.append([deliv[0], curr])							#add departure time to to output list
		curr = addtime(curr,deliv[1][0])						#from warehouse (0,0)->(X,Y) delivery point
		dpl.append([deliv[0], curr])							#add delivery time to to departure list
		curr = addtime(curr,deliv[1][0])						#from delivery point (X,Y) -> (0,0) warehouse
		del d[deliv[0]]											#deleting the order from input list
	return opl,dpl

def calculate_nps(ip,dpl):
    prom=0
    det=0
    #Calculating Promoters and Detractors
    for i in dpl:
        tdelta = datetime.strptime(i[1], '%H:%M:%S') - datetime.strptime(ip.get(i[0])[1], '%H:%M:%S')
        if(tdelta < timedelta(hours=2)):
            prom+=1
        elif(tdelta > timedelta(hours=4)):
            det+=1
    #print("NPS:",((prom-det)/len(dpl))*100)
    nps=((prom-det)/len(dpl))*100
    return nps

if __name__ == "__main__":
	filename = sys.argv[1]
	f = open(filename,"r")
	ip=dict()
	#key:order_id and value:[distance in coo-ordinates,order_time]
	for line in f:
		l = line.split(",")
		ip[l[0]]=[l[1],l[2][:-1]]
	#start time of drone in the city
	curr = "06:00:00"
	#Delivering the orders and saving output to a list,later to a file 
	opl,dpl=deliver_order(curr,ip)	
	nps=calculate_nps(ip,dpl)
	opl.append([nps])
	with open("output.csv", "w",newline='') as opfile:
		writer = csv.writer(opfile)
		writer.writerows(opl)
	print("Filepath:",os.getcwd()+"output.csv")
