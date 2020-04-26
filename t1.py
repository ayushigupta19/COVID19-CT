from simulation import simulate

output = []
init_cond = [[56], [84], [13], [12], [88]]
simulate(init_cond, output, path="output1.csv", algo_mode='level3', population=300, days=100, tstamp_per_day=40)
print("Final output: ", output)