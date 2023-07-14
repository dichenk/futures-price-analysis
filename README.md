# futures-price-analysis
The project is to study futures price analysis using Python

The program monitors the ETHUSDT futures price in real time 
(with minimal delay) and using the method you choose, determines 
your own ETH price movements. If the price changes by 1% over the last 60 minutes, 
the program displays a message in the console.

For training purposes, to demonstrate how the algorithm works, 
the program outputs every 10 seconds the intrinsic change in the price of ETH 
over the last hour. To activate the scheduled output (only when the own price 
change is at least 1 percent), you need to comment out line 38 
and uncomment line 39 of the main.py file.
