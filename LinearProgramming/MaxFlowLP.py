
from __future__ import division # safety with double division
from pyomo.environ import *
from pyomo.opt import SolverFactory

# Instantiate and name the model
M = AbstractModel()
M.name = "Max Flow"


M.Node = Set()
M.Arc = Set(within = M.Node*M.Node)

# Parameters
M.Length = Param(M.Arc, within = NonNegativeReals)
M.Demand = Param(M.Node, within = NonNegativeReals)
M.Supply = Param(M.Node, within = NonNegativeReals)
