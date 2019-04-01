Given file of order_lists [order_id,co-ordinates,order_time] (test.csv)

Note: Timings are taken in 24Hr format (HH:MM:SS)

Distance is calculated from co-ordinates considering ware house as (0,0). As mentioned all orders depart from the warehouse. Drone will pick up
one order at a time, delivers and returns to the warehouse to pick another order. Idea is to follow greedy algorithm to pick the order with minimum 
number of blocks from warehouse (i.e. minimum distance).

Converted into dictionary with key:order_id and value:[distance,order_time]

Dictionary is sorted according to the order_time (Ascending)

Assuming that the drone starts at 06:00:00 (Current_Time)

Step1:
	We filter the order which has minimum distance from (0,0) which are ordered before the Current_Time

	The order is delivered and Current_Time is increased by distance units

	Order_ID, Drone departure time are appended to OUTPUT_list

	Current_Time is increased to distance units to reach (0,0)

Step1 is repeated until it places all possible orders

NPS calculation :
waiting times are claculated by Delivery_Time - Order_Time
One who waits for less than 2 hours are considered as promoters.
One who waits for more than 4 hours are considered as detractors.
NPS is calulated (#Promoters-#Detractors)/#Deliveries * 100

All the contents of Output_list are written into a file (output.csv)

To run : python assignment.py test.csv