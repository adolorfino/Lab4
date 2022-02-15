# Lab4

In this lab we built a circuit and attached it to our nucleo in order to record data on the step response for the circuit. The goal was to make sure our code was able to correctly display the step response and get a time constant relatively similar to the calculated time constant for the circuit. Below we have the graph that are code generated and also a graph generated from a simulation done in MATLAB to replicate the same step response. One of the main comparisons between the two is that they both follow the same shape of a first order step response however the one generated for my code only has a range from 2 to 3.1 while the MATLAB has one from 0 to 3.3.

![Annotated Graph](/../main/images/annotated_graph.PNG)

![Code](/../main/images/code.PNG)

![MATLAB Graph](/../main/images/code_graph.PNG)

The calculated time constant that we wanted would be equal to the capacitor times the resistor and with a capacitor of 3.3 uF and a resistor of 6k ohm out calculated time constant would be about 0.0198 seconds. However, the calculated time constant that we got from our code was about 0.275 seconds. This means that the type constant generated from our code is about a factor of 10 off however they are fairly similar in number so that I might just be something to do with the fact that our grass starts at two instead of zero.
