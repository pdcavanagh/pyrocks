#/usr/local/python
import re
import logging
import urllib2
import numpy as np
import pulp
import CifFile as cif
import pickle

class Model:
    def __init__(self, name):
        self.name = name
        self.phases = {}
        self.free_variables = {}
        self.bulk = {'SiO2':  0,
                     'TiO2':  0,
                     'Al2O3': 0, 
                     'Fe':    0,
                     'MnO':   0,
                     'MgO':   0,
                     'CaO':   0,
                     'Na2O':  0,
                     'K2O':   0,
                     'SO3':   0,
                     'Cl':    0,
                     'H2O':   0}
 
    # Fuction to add all mineral phases used in model
    def add_phase(self, phase):
        self.phases[phase] = Phase(phase)

    def add_free_variable(self, fv_name, values):
        self.free_variables[fv_name] =  values

    # Function for adding the bulk chemical composition to model
    def add_bulk(self, oxide, wt):
        self.bulk[oxide] = wt

def save_model(model, fn):
    output = open(fn, 'wb')
    pickle.dump(model, output)
    output.close()

def open_model(fn):
    pkl_file = open(fn, 'rb')
    model = pickle.load(pkl_file)
    pkl_file.close()
    return model

# Minearl Phase Class
# Contains all information relevant for a phase to be added to model
# Attributes:
#   Name 
#   Chemical formula
#   QXRD abundance
#   Oxide composition
#   Variability of individual oxide components
class Phase:
    def __init__(self, name):
        self.name = name
        self.formula = ''
        self.qxrd = 0
        self.qxrd_error = 0
        self.oxide_comp = {'SiO2': 0,
                           'TiO2': 0,
                           'Al2O3': 0, 
                           'Fe': 0,
                           'MnO':  0,
                           'MgO':  0,
                           'CaO':  0,
                           'Na2O': 0,
                           'K2O':  0,
                           'SO3':  0,
                           'Cl':   0,
                           'H2O':  0}
        #self.delta_oxides = {}
        self.phase_variables = {}

    def add_formula(self, formula):
        self.formula = formula

    def add_qxrd(self, qxrd):
        self.qxrd = qxrd

    def add_qxrd_error(self, error):
        self.qxrd_error = error

    def set_oxide_comp(self, oxide, value):
        self.oxide_comp[oxide] = value 

#    def add_delta_oxide(self, oxide, wts):
#        self.delta_oxides[oxide] = Oxides(oxide, wts)

    def add_phase_variable(self, name, constraint, value):
        try:  
            self.phase_variables[name][constraint]=value
        except:
            self.phase_variables[name] = {}
            self.phase_variables[name][constraint]=value


class Oxides:
    def __init__(self, name, oxides):
        self.name = name 
        self.oxides = { 'SiO2': 0,
                        'TiO2': 0,
                        'Al2O3': 0, 
                        'Fe': 0,
                        'MnO':  0,
                        'MgO':  0,
                        'CaO':  0,
                        'Na2O': 0,
                        'K2O':  0,
                        'SO3':  0,
                        'Cl':  0,
                        'H2O':  0}
        for x,y in oxides.items():
            self.oxides[x] = y    
        def set_oxide(self, oxide_name, value):
            self.oxides[oxide_name] = value 

# Example bulk composition oxide components
bulk = ['SiO2',
        'TiO2',
        'Al2O3', 
        'Fe',
        'MnO',
        'MgO',
        'CaO',
        'Na2O',
        'K2O',
        'SO3', 
        'Cl', 
        'H2O'] 


# Dictionary element to oxide 
elem2oxide = {'Si': 'SiO2',
              'Ca': 'CaO',
              'Na': 'Na2O',
              'Al': 'Al2O3', 
              'Mg': 'MgO', 
              'H': 'H2O', 
              'K': 'K2O'}

# Dictionary of atomic weights
atomic_wt = {'Si': 28.086, 
             'Ca': 40.078, 
             'Na': 22.99, 
             'Al': 26.982, 
             'O': 15.999, 
             'Mg': 24.305, 
             'H': 1.00794, 
             'K': 39.0983}

# Dictionary of number of oxygens per oxide component
num_oxy =   {'Si': 2, 
             'Ca': 1, 
             'Na': 0.5, 
             'Al': 3/2, 
             'O': 1, 
             'Mg': 1, 
             'H': 0.5, 
             'K': 0.5}

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def getAPXSData(url):
    # create a new Urllib2 Request object	
    req = urllib2.Request(url)
    # make the request and print the results
    res = urllib2.urlopen(req)
    data_array = np.genfromtxt(res, delimiter=',', skip_header=True, names=True, dtype=None )
    for x in data_array:
        x[0] = x[0].strip()
    return data_array 

# Functions for seperating a chemical forumla into atom components
# Returns list of elements and list of stoiciometric coefficients
def form_split(form_str):
    element = []
    elem_num = []

    flag=False

    s = re.split('\s',form_str)
    for j in s:
        temp_elem=str(j).strip('()')
        temp_elem2 = re.split('([A-Z][a-z])|([A-Z])', temp_elem)
        for k in temp_elem2:
          if k != None:
            if str(k).isalpha():
                element.append(k)
                if flag==False:
                    flag=True
                else:
                    elem_num.append(1)
                    flag=False
            if is_number(str(k)):
                elem_num.append(float(k))
                flag=False
    return element, elem_num

def main_loop():
    logging.basicConfig(level=logging.DEBUG, 
                        format='%(asctime)s - %(levelname)s - %(message)s')
    
    # retrieve .CIF filename from command line
    name = cf['global']['_chemical_name_mineral']
    formula = cf['global']['_chemical_formula_sum']
    
    logging.debug('test: %s %s' % (name, formula))
    
    # Parse formula string from CIF
    [element, stoich_coeff] = form_split(formula)
    formula = dict(zip(element, stoich_coeff))
    
    logging.debug('elements: %s' % element)
    logging.debug('stoich: %s' % stoich_coeff)
    logging.debug('%s' % formula)
    
    # Element dictionary template
    element_temp = dict.fromkeys(['Si','Ca','Na','Al','O','Mg','H','K'])
    oxide = dict.fromkeys(['SiO2','CaO','Na2O','Al2O3'])
    
    # Calculate the weight percent of each oxide in phase
    sum = 0
    
    for x,y in formula.items():
        temp1 = atomic_wt[x] * y 
        element_temp[x] = atomic_wt['O'] * num_oxy[x] + temp1
        if x != 'O':
            sum = element_temp[x] + sum
    
    for x in element_temp:
        if x != 'O' and element_temp[x]!=None: 
            oxide[elem2oxide[x]] = element_temp[x]/sum
    
    for x,y in oxide.items():
        if y!=None: 
            print '%5s: %8.3f' % (x,y*100)
    
    apxs_url = 'http://pds-geosciences.wustl.edu/msl/msl-m-apxs-4_5-rdr-v1/mslapx_1xxx/data/sol00288/apb_423020067rwp02880060082_______p1.csv'
    
    testAPXSdata = getAPXSData(apxs_url)

    model_name = 'Rocknest'

    # Begin of linear programming code
    prob = pulp.LpProblem(model_name, LpMinimize) 

    # Objective function
    #prob += lpSum([])

    #prob += lpSum([

#------------- Creation of the PuLP optimization -------------------------------
def optimize_model(model, maxPhase, objFunWt): 
    variables = []   # List of all optimization variables
    phase_abun = {}  # Dictionary of QXRD abudances 
    constraints = {} # Dictionary of all constraints (rows)
    objfun = {}      # Create a dictionary for objective function 
    phase_frac = {}  # Create a dictionary for all variables for phase fractions 
    
    #Build the variables list for the PuLP model
    for x in model.phases:
        variables.append('X_' + model.phases[x].name)
        phase_abun[x] = model.phases[x].qxrd
        for j in model.phases[x].phase_variables:
            variables.append(j)
    for x,y in model.free_variables.items():
        variables.append(x)
    
    # Build the constraint dictionaries
    for j in bulk:
        constraints[j] = {}
        for x in model.phases:
            constraints[j]['X_' + model.phases[x].name] = model.phases[x].oxide_comp[j]
            #print '%s %s %f' % (j, model.phases[x].name, model.phases[x].oxide_comp[j])
            for k in model.phases[x].phase_variables:
                try:
                    constraints[j][k] = model.phases[x].phase_variables[k][j]
                except:
                    constraints[j][k] = 0 
                    continue
        for x in model.free_variables:
            try:
                constraints[j][x] = model.free_variables[x][j] 
            except:
                constraints[j][x] = 0
                continue
    
    # Initialize all variables to 0
    for x in variables:
        objfun[x] = 0
    # Set initial phase to 10, will be a variable later
    objfun['X_' + maxPhase] = objFunWt
    for x in model.free_variables:
        objfun[x]=model.free_variables[x]['objfun']
        #print model.free_variables[x]['objfun']
    
    # Initialize all phases to 1 and other variables to 0
    # Constraint for phase fraction is that all phases add to 1
    for x in variables:
        if x[0] == 'X':
            phase_frac[x] = 1
        else:
            phase_frac[x] = 0
    
    # Create the 'prob' variable to contain the problem data
    prob = pulp.LpProblem(model.name, pulp.LpMaximize)
    
    # A dictionary called 'phase_vars' is created to contain the referenced Variables
    phase_vars = pulp.LpVariable.dicts("Phase",variables,0,1)
    
#    Bounding conditions for free variables
#    for x in model.free_variables:
#        phase_vars[x].upBound = 1 
#        phase_vars[x].lowBound = 0

    # Set the bounding conditions for all phases based on QXRD error
    for x in model.phases:
        if model.phases[x].qxrd - model.phases[x].qxrd_error >= 0:
            phase_vars['X_' + x].lowBound = model.phases[x].qxrd - model.phases[x].qxrd_error
        phase_vars['X_' + x].upBound = model.phases[x].qxrd + model.phases[x].qxrd_error
        #print x,phase_vars['X_' + x].lowBound, phase_vars['X_' + x].upBound 
    # The objective function is added to 'prob' first
    prob += pulp.lpSum([objfun[i]*phase_vars[i] for i in variables]), "Objective function for maximization of particular phase"
    
    # The constraints are added to 'prob'
    prob += pulp.lpSum([phase_frac[i] * phase_vars[i] for i in variables]) == 1, "Phases sum to 100%"

    for x,y in model.bulk.items():
        try:
            prob += pulp.lpSum([constraints[x][i] * phase_vars[i] for i in variables]) == y, "%s APXS" % x
        except:
            continue

#    prob += pulp.lpSum([constraints['SiO2'][i] * phase_vars[i] for i in variables]) == 42.88, "SiO2 APXS"
#    prob += pulp.lpSum([constraints['TiO2'][i] * phase_vars[i] for i in variables]) == 1.19, "TiO2 APXS"
#    prob += pulp.lpSum([constraints['Al2O3'][i] * phase_vars[i] for i in variables]) == 9.43, "Al2O3 APXS"
#    prob += pulp.lpSum([constraints['Fe'][i] * phase_vars[i] for i in variables]) == 19.19, "Fe2O3+FeO APXS"
#    prob += pulp.lpSum([constraints['MnO'][i] * phase_vars[i] for i in variables]) == 0.41, "MnO APXS"
#    prob += pulp.lpSum([constraints['MgO'][i] * phase_vars[i] for i in variables]) == 8.69, "MgO APXS"
#    prob += pulp.lpSum([constraints['CaO'][i] * phase_vars[i] for i in variables]) == 7.28, "CaO APXS"
#    prob += pulp.lpSum([constraints['Na2O'][i] * phase_vars[i] for i in variables]) == 2.72, "Na2O APXS"
#    prob += pulp.lpSum([constraints['K2O'][i] * phase_vars[i] for i in variables]) == 0.49, "K2O APXS"
#    prob += pulp.lpSum([constraints['SO3'][i] * phase_vars[i] for i in variables]) == 5.45, "SO3 APXS"
    
    # The problem data is written to an .lp file
    prob.writeLP(model.name + ".lp")
    
    # The problem is solved using PuLP's choice of Solver
    prob.solve()
    
    # The status of the solution is printed to the screen
    print "Status:", pulp.LpStatus[prob.status]
    
    # Each of the variables is printed with it's resolved optimum value
    for v in prob.variables():
        if v.name != '__dummy':
            if v.name[0:8] == 'Phase_X_':
                print '%-25s = %6.4f' % (v.name, v.varValue)
    
    # The optimised objective function value is printed to the screen    
    print "optimised objective function value = ", pulp.value(prob.objective)


if __name__ == "__main__":
    import sys
    try:
        fn = sys.argv[1]
    except:
        print "Please provide a filename: python pyrocks.py FILENAME"
    else:
        cf = cif.ReadCif(fn)
        main_loop()
