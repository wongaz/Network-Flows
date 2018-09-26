
from __future__ import division # safety with double division
from pyomo.environ import *
from pyomo.opt import SolverFactory

# Instantiate and name the model
M = AbstractModel()
M.name = "Shorted Path"

# Sets
M.Node = Set()
M.Arc = Set(within = M.Node*M.Node)

# Parameters
M.Length = Param(M.Arc, within = NonNegativeReals)
M.Demand = Param(M.Node, within = NonNegativeReals)
M.Supply = Param(M.Node, within = NonNegativeReals)

# Variables
M.Flow = Var(M.Arc, within=NonNegativeIntegers)

# Objective
def DistanceCalc(M):
	return sum(M.Flow[x]*M.Length[x] for x in M.Arc)
M.Calc = Objective(rule=DistanceCalc, sense=minimize)

def FlowBalance(M,k):
	return M.Supply[k]+sum(M.Flow[i,k] for i in M.Node if (i,k) in M.Arc) == \
          M.Demand[k]+sum(M.Flow[k,j] for j in M.Node if (k,j) in M.Arc)
M.FlowBalance = Constraint(M.Node, rule=FlowBalance)


instance = M.create_instance("Wong2_42.dat")

# Indicate which solver to use
Opt = SolverFactory("gurobi")

# Generate a solution
Soln = Opt.solve(instance)
instance.solutions.load_from(Soln)

# Print the output
print("Termination Condition was "+str(Soln.Solver.Termination_condition))
display(instance)
