from math import sin, acos, sqrt, cos, floor, pi
import matplotlib.pyplot as plt
from random import gauss
import pandas as pd
import numpy as np
from numpy import roll
from scipy.signal import correlate

def test(iters=10000, noise_variance_=[0], amplitude_=[1], omega_=[1], periods=1):
    excel_df = pd.DataFrame(index=noise_variance_)
    for noise_variance in noise_variance_:
        for amplitude in amplitude_:
            for omega in omega_:

                #Simulating the signal according to the chosen parameters
                end = np.pi*2*periods
                step = end/iters
                t = np.linspace(0, end, iters)
                realSignal = amplitude*np.sin(omega*t)
                noisySignal = amplitude*np.sin(omega*t) + np.random.normal(0, noise_variance, iters)

                #Measuring the cyclic autocorrelation
                measured_autocorr = []
                for k in range(0, len(t)):
                    measured_autocorr.append(correlate(noisySignal, roll(noisySignal, k), 'valid'))
                autocorr = np.array(measured_autocorr)/len(t)

                #Measuring big lambda
                lam = []
                for i in range(4, len(t)):
                    lam.append(((autocorr[i] - autocorr[i-1] - autocorr[i-2] + autocorr[i-3])/(autocorr[i-1] - 2*autocorr[i-2] + autocorr[i-3]))/2)
                min_pres = min(lam)
                max_pres = max(lam)
               
                #Estimating omega
                w_options = [(x - min_pres)/(max_pres - min_pres) for x in lam]
                estimate_w = np.mean([acos(j) for j in w_options])

                #Estimating the amplitude
                A_options = 0
                for j in range(0, len(autocorr)):
                    A_options += sqrt(abs((2*autocorr[j]) / (cos(estimate_w*step*j))))
                estimate_a = A_options/len(autocorr)

                #Calculating the RMSE
                calcSignal = estimate_a*np.sin(estimate_w*t)
                rmse = sqrt(np.square(np.subtract(realSignal,calcSignal)).mean())

                print("Step: %s | Noise Var: %s | Amplitude: %s | Omega: %s | RMSE: %s" % (step, noise_variance, amplitude, omega, rmse))

                excel_df.at[noise_variance, omega] = rmse

    excel_df.to_excel('results.xlsx', sheet_name="sheet1")