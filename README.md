
# Sinusoidal State Estimation

## What are noisy signals?

A signal is a function that conveys information about a system. For example, a temperature probe may send a signal - a continuous stream of numbers that convey the temperature of the space around the probe. For this project, I concentrated on signals that change approximately sinusoidally.

So what's noise? Noise is unwanted interference in a signal. When the temperature probe sends a signal, it's not sending the true temperature. It sends the true temperature with additional noise due to both the probe's uncertainties and environmental fluctuations.

Creating algorithms to accurately and efficiently remove unwanted noise and uncover the true values underlying noisy signals is a primary goal in the field of signals processing.

## The Kalman Filter

The Kalman Filter is an algorithm that can be used to estimate the state of a system and remove noise in the process. NASA began using the Kalman Filter in the '60s, and they continue to do so to this day. As part of this project, I wanted to explore how the filter functions and what problems it may have.

## Experimenting

I used a Raspberry Pi and small accelerometer and placed them on a glider that can run on an air track (see the picture below). I conncted my laptop wirelessly to the RPi.

![Experimental Apparatus](https://github.com/AkiraY1/SinusoidalStateEstimation/blob/main/Media/InitialIdeaPhoto.jpg?raw=true)

The glider apparatus slid along the air track and recorded its acceleration, from which I calculated the velocity and displacement in real time (see the file "collision_sim.py").

From this experiment I was able to implement the Kalman Filter to calculating the acceleration and velocity of the apparatus more accurately. It was quite fun.

## The Problem and Solution

After lots of experimentating, thinking and researching, I was able to come up with problems that the Kalman Filter inherently has and ideas to fix them. In the end I created my own filter based on the autocorrelation function to improve upon the Kalman Filter (it kind of worked).
