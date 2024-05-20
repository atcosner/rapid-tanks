# Rapid Tanks

**NOTICE**

Work on this project was suspended in April 2024 due to the release of [EPA TANKS Version 5](https://www.epa.gov/air-emissions-factors-and-quantification/tanks-emissions-estimation-software-version-5). Development may continue in the future as the current beta version of TANKS 5 is limited in its feature set and reporting capabilities.

## Overview

Rapid Tanks is a GUI application that supports calculating emissions from tanks based on the EPA AP 42 Chapter 7 regulations. The current suite of products that can acomplish this are either incorrect based on updated regulations (TANKS 4.09d) or are only avaliable at significant cost (TankESP). An open-source implementation of the emissions calculations will hopefully drive costs down and increase compliance with the Chapter 7 regulations.

## Features
* Calculations for both fixed and floating roof tanks
* Meteorological data for ~300 sites across the US
* Custom mixture and material support
* Granular tank service records (Year, Month, explicit date range)
* In-depth reports over multiple time ranges (yearly, monthly, and custom date ranges)

## Technologies
* PyQT (GUI)
* ReportLab (PDF reports)
* SQLAlchemy (DB)
