#/usr/local/python
import re
import logging
import urllib2
import numpy as np
import pulp
import CifFile as cif

class Model:
    def __init__(self, name):
        self.name = name
        self.phases = {} 
 
    # Fuction to add all mineral phases used in model
    def add_phase(self, phase):
        self.phases[phase] = Phase(phase)

    # Function for adding the bulk chemical composition to model
    def add_bulk(self, oxide, wt):
        self.bulk[oxide] = wt

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
        self.oxides = {}
        self.delta_oxides = {}

    def add_formula(self, formula):
        self.formula = formula

    def add_qxrd(self, qxrd):
        self.qxrd = qxrd

    def add_oxide(self, oxide, wt):
        self.oxides[oxide] = wt

    def add_delta(self, delta_oxide, value):
        self.delta_oxides[delta_oxide] = value

# Dictionary of phases in the Rocknest 
phases = ['plagioclase', 
          'olivine', 
          'augite',
          'pigeonite',
          'magnetite',
          'anhydrite',
          'quartz',
          'sanidine',
          'hematite',
          'ilmenite'] 

bulk = ['SiO2',
        'TiO2',
        'Al2O3', 
        'Fe2O3+FeO',
        'MnO',
        'MgO',
        'CaO',
        'Na2O',
        'K2O',
        'SO3', 
        'H2O'] 

# Dictionary of Rietveld phase abundances in Rocknest, Bish 2013
phase_abun = {'plagioclase': 40.8,
              'olivine': 22.4,
              'augite': 14.6,
              'pigeonite': 13.8,
              'magnetite': 2.1,
              'anhydrite': 1.5,
              'quartz': 1.4,
              'sanidine': 1.3,
              'hematite': 1.1,
              'ilmenite': 0.9} 

# Dictionary of Rietveld 2sigma values of Rocknest soil, Bish 2013
phase_2sigma = {'plagioclase': 2.4,
                'olivine': 1.9,
                'augite': 2.8,
                'pigeonite': 2.8,
                'magnetite': 0.8,
                'anhydrite': 0.7,
                'quartz': 0.6,
                'sanidine': 1.3,
                'hematite': 0.9,
                'ilmenite': 0.9} 

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
    return res 

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
    test_array = np.genfromtxt(testAPXSdata, delimiter=',')

    model_name = 'Rocknest'

    # Begin of linear programming code
    prob = pulp.LpProblem(model_name, LpMinimize) 

    # Objective function
    #prob += lpSum([])

    #prob += lpSum([

if __name__ == "__main__":
    import sys
    try:
        fn = sys.argv[1]
    except:
        print "Please provide a filename: python pyrocks.py FILENAME"
    else:
        cf = cif.ReadCif(fn)
        main_loop()