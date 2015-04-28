# DangerAndProblem
*Methods to access avalanche danger and avalanche problems on regObs and Varsom*

In this repository you will find methods to:
* access data on the regObs OData api in ´getRegObs.py´
* access data on the forecast api for Varsom in ´getForecastApi.py´
* retrieve all avalanche problems forecasted and observed since 2012 and save to file in ´runForAvalancheProblems.py´
* retrieve and plot danger levels an avalanche problems forecasted 2014/15 ´runForMatrix.py´

There are two classes used to structure data. ´AvalancheDanger.py´ and ´AvalancheProblem.py´. This is helpful because the structure of the data in regObs and on Varsom has changed over the past fiew years and this way datasets can be compared.

