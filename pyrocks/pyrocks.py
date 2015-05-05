#/usr/local/python
import re
import logging
import urllib2
import numpy as np
import pulp as lp
import CifFile as cif

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

phase_abun = {'Plagioclase': 40.8,
              'Forsterite': 22.4,
              'Augite': 14.6,
              'Pigeonite': 13.8,
              'Magnetite': 2.1,
              'Anhydrite': 1.5,
              'Quartz': 1.4,
              'Sanidine': 1.3,
              'Hematite': 1.1,
              'Ilmenite': 0.9} 

phase_2sigma = {'Plagioclase': 2.4,
                'Forsterite': 1.9,
                'Augite': 2.8,
                'Pigeonite': 2.8,
                'Magnetite': 0.8,
                'Anhydrite': 0.7,
                'Quartz': 0.6,
                'Sanidine': 1.3,
                'Hematite': 0.9,
                'Ilmenite': 0.9} 

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

if __name__ == "__main__":
    import sys
    try:
        fn = sys.argv[1]
    except:
        print "Please provide a filename: python pyrocks.py FILENAME"
    else:
        cf = cif.ReadCif(fn)
        main_loop()
