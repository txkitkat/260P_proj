# 260P_proj

This repository contains all Project files from CS 260P, especially pertaining to the Final Project.

This Final Project generates a results.txt and a results_not_holding.txt for data comparison against TSP approximation Algorithms
All results will output in CSV format

To generate all results, do the following:
  1. Run python generate_traveling_salesman_problem.py or place previously saved data_set_holding/ and data_set_not_holding/ directories under 260P_Proj/ directory
  2. Run final_project.py
  3. Wait for script to complete

CONSTRAINTS: Numpy must be installed to environment

The difference between holding and not holding data is that holding data follows the triangle inequality and non-holding data does not.

Due to the size of data generated, testcase data cannot be push to the repo but can be regenerated locally to receive similar results.
