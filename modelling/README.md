# Exploratory Data Analysis
4 Datasets (FD001-4) consist of multiple multivariate series. Each dataset has 3 operational settings and number of sensor measurements which are contaminated with noise over time.

Taking a look at example of sensor measurements, we can see non-linear trends in some, caused by noises in sensors.

### Measurements visualization of dataset FD001
[<img src="../app/assets/eda.png"/>](app/assets/eda.png) 

## Modelling
We want to build a RNN that can handle a stream of sensor measurements and produce a one-hot-encoded vector in real time.
Each unit has a different number of time cycles. 

We can structure the data such that each unit's data is treated as a separate sequence. 