from math import sin, acos, sqrt, cos, floor, pi
from random import gauss
import numpy as np
from pandas import DataFrame

def rmse(y_true, y_pred):
    rmse = sqrt(np.square(np.subtract(y_true,y_pred)).mean())
    return rmse

def test(iters=10000, noise_variance_=[0], amplitude_=[1], omega_=[1], periods=1, process_noise=0.5, model_amplitude=1, model_omega=1):
    end = np.pi*2*periods
    step = end/iters
   
    state_prediction = 0
    error_prediction = 1

    excel_df = DataFrame(index=noise_variance_)

    for noise_variance in noise_variance_:
        measurement_noise = noise_variance
        for amplitude in amplitude_:
            for omega in omega_:
                time = [0]
                signal = []
                signal_estimate = []
                true_signal = [0]

                end = floor(periods*((2*pi)/omega)/step)

                #First iteration
                kalman_gain = error_prediction/(error_prediction + measurement_noise)
                measurement = np.random.normal(0, noise_variance, 1)
                signal.append(measurement)
                state_update = state_prediction + kalman_gain*(measurement - state_prediction)
                signal_estimate.append(state_update)
                error_update = error_prediction*(1 - kalman_gain)

                #All iterations after first iteration
                for t in [x*step for x in range(1, end)]:
                    true_value = amplitude*sin(omega*t)
                    measurement = true_value + gauss(0, noise_variance)

                    true_signal.append(true_value)
                    time.append(t)
                    signal.append(measurement)

                    state_prediction = state_update + model_amplitude*sin(model_omega*t) - model_amplitude*sin(model_omega*(t-step))
                    error_prediction = ((model_amplitude*model_omega*cos(model_omega*(t-step)))**2)*error_update + process_noise
                    kalman_gain = error_prediction/(error_prediction + measurement_noise)
                    state_update = state_prediction + kalman_gain*(measurement - state_prediction)
                    error_update = error_prediction*(1 - kalman_gain)

                    signal_estimate.append(state_update)
               
                error = rmse(true_signal, signal_estimate)
                print("Step: %s | Noise Var: %s | Amplitude: %s | Omega: %s | RMSE: %s" % (step, noise_variance, amplitude, omega, error))
                excel_df.at[noise_variance, omega] = error
   
    excel_df.to_excel('results.xlsx', sheet_name="sheet1")