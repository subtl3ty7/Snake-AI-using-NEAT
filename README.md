# Snake-AI-using-NEAT
Snake game with Neural Networks and Genetic Algorithm using NEAT Library on Python

NOTE: The input parameter and output parameter tweaks are absent! That's why the learning rate of the Snake might take longer than usual (over 20-30 Generations). This project's purpose was to program the Snake game in Python and design the Neural Network. (Not efficiency)
You are welcome to tweak it.


CONFIG File contains the NEAT Library parameters to tweak the Neural Network and Genetic Algorithm Settings. 
Link to the NEAT Documentation: https://neat-python.readthedocs.io/en/latest/index.html

In the algorithm I took the following datas as inputs:
-If Snake's left tile contains a node from body
-If Snake's right tile contains a node from body
-If Snake's down tile contains a node from body
-If Snake's up tile contains a node from body
-If Food is on left side
-If Food is on right side
-If Food is on down side
-If Food is on up side

Everytime we move, we increase the Score with 10.
Everytime we eat, we increase the Score with 50.
Then Fitness follows fitness = Score - distanceFromFood

If we get far away from food, fitness drops.


