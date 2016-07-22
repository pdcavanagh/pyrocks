#/usr/local/python
import time
import re
import logging
import urllib2
import numpy as np
import pulp
import CifFile as cif
import pickle
import csv

class Result:
    def __init__(self, name):
        self.opt = name
        self.obj_fun = 0.0
        self.opt_var = ''
        self.var_value = 0.0
        self.obj_fun_result = 0.0

    def add_variable(self, var_name):
        self.opt_var = var_name    

    def add_value(self, var_value):
        self.var_value=var_value
                    
    def add_obj_fun_result(self, objValue):
        self.obj_fun_result = objValue

class Model:
    def __init__(self, name):
        self.name = name
        self.phases = {}
        self.free_variables = {}
        self.bulk = {'SiO2':  0.0,
                     'TiO2':  0.0,
                     'Al2O3': 0.0, 
                     'Cr2O3': 0.0,
                     'Fe':    0.0,
                     'MnO':   0.0,
                     'MgO':   0.0,
                     'CaO':   0.0,
                     'Na2O':  0.0,
                     'K2O':   0.0,
                     'SO3':   0.0,
                     'P2O5':  0.0,
                     'Cl':    0.0}
#                     'H2O':   0,
#                     'F':     0}
 
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

def save_results(model, res):
    fn_out = './output/' + model.name + '_out-test.csv'
    amorph_fn = './output/' + model.name + '_amorph_' + str(time.localtime().tm_year) + \
              '{:02d}'.format(time.localtime().tm_mon) + \
              '{:02d}'.format(time.localtime().tm_mday) + \
              str(time.localtime().tm_hour) + \
              '{:02d}'.format(time.localtime().tm_min) + '.csv'
    abun_fn = './output/' + model.name + '_abun_out_' + str(time.localtime().tm_year) + \
              '{:02d}'.format(time.localtime().tm_mon) + \
              '{:02d}'.format(time.localtime().tm_mday) + \
              str(time.localtime().tm_hour) + \
              '{:02d}'.format(time.localtime().tm_min) + '.csv'

    # create a max and min list
    max_dict = {}
    min_dict = {}
    phase_min_dict = {}
    amorph_comp = {} 
    amorph_all = {} 
 
    # Record the constraints for the mineral phases 
    lowBound ={} 
    upBound ={} 
    for x in model.phases:
        if model.phases[x].qxrd - model.phases[x].qxrd_error >= 0:
            lowBound[x] = model.phases[x].qxrd - model.phases[x].qxrd_error
            upBound[x] = model.phases[x].qxrd + model.phases[x].qxrd_error
        else:
            lowBound[x] = 0.0    
            upBound[x] = model.phases[x].qxrd + model.phases[x].qxrd_error
        #print '%s %f' % (x, lowBound[x])
        #print '%s %f' % (x, upBound[x])
    
    with open(amorph_fn, 'w') as csvfile: 
        fieldnames = ['Opt', 'Oxide', 'Initial', 'Delta', 'Final',  'Wt Percent']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for x in res:
            delta_oxide = str(x.opt_var)[19:] 
            if x.opt=='amorphous':
                print '%-15s%-40s%8f' % (x.opt, x.opt_var, x.var_value)
            if str(x.opt_var)[0:18]=='Phase_DX_amorphous':
                amorph_comp[delta_oxide]=x.var_value
            phase=str(x.opt_var)[8:] #strip phase name from variable, remove 'Phase_X_'
    
            if str(x.opt_var)[0:18]=='Phase_DX_amorphous':
                initial = model.phases['amorphous'].oxide_comp[delta_oxide] 
                delta = model.phases['amorphous'].phase_variables['DX_amorphous_' + delta_oxide]
                final =  amorph_comp[delta_oxide]*delta[delta_oxide]

                wt_perc = initial + final 
                #print '%s%s%s' % (x.opt,str(x.opt_var)[19:],x.var_value)
                writer.writerow({'Opt': x.opt, 'Oxide': delta_oxide, 'Initial': initial, 'Delta': delta[delta_oxide], 'Final': final,  'Wt Percent': wt_perc})
    
            # Encounter optimization value for first time, initialize to first value
            if x.opt_var not in min_dict:
                min_dict[x.opt_var] = x.var_value
    
            # Create list of max values for each phase optimization
            if x.opt==phase:
                max_dict[x.opt]=x.var_value
    
            # Update the list of min results
            if x.var_value < min_dict[x.opt_var]:
                min_dict[x.opt_var] = x.var_value
    
        # Calculate the amorphous component composition from the amorphous maximization
        for y in amorph_comp:
            wt_perc = model.phases['amorphous'].oxide_comp[y] 
            delta = model.phases['amorphous'].phase_variables['DX_amorphous_' + str(y)]
            print '%s \t %5.2f' % (y, wt_perc+amorph_comp[y]*delta[y]) 
        
        for x in min_dict:
            if x[0:8]=='Phase_X_':
                phase_min_dict[x[8:]]=min_dict[x]
        print '%20s%14s%14s%14s%14s' % ('phase','lower bounds','min','max','upper bounds') 
        for x in max_dict:
            print '%20s%14f%14f%14f%14f' % (x, lowBound[x], phase_min_dict[x], max_dict[x], upBound[x])
    
                
        #for x in phase_min_dict:
            #print x, phase_min_dict[x]
    
    with open(fn_out, 'w') as csvfile:
        fieldnames = ['Opt', 'Mineral or Variable', 'Wt Percent']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
            
        for x in res:
            writer.writerow({'Opt': x.opt, 'Mineral or Variable': x.opt_var, 'Wt Percent': x.var_value})

    with open(abun_fn, 'w') as csvfile:
        fieldnames = ['Phase', 'Lower Bound', 'Minimum', 'Maximum', 'Upper Bound']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
            
        for x in max_dict:
            writer.writerow({'Phase': x, 'Lower Bound': lowBound[x], 
                'Minimum': phase_min_dict[x], 'Maximum': max_dict[x], 
                'Upper Bound': upBound[x]})

def add_clay_comp(mdl, comp_name):
    if comp_name=='default': 
        # Add smectite
        # saponite data from webmineral.com
        # Add amorphous oxide weight percent to phases of model
        mdl.phases['smectite'].set_oxide_comp('SiO2', 50.79)
        mdl.phases['smectite'].set_oxide_comp('Al2O3', 6.83)
        mdl.phases['smectite'].set_oxide_comp('Fe', 35.61)
        mdl.phases['smectite'].set_oxide_comp('MgO', 1.11)
        mdl.phases['smectite'].set_oxide_comp('CaO', 2.95)
        mdl.phases['smectite'].set_oxide_comp('Na2O', 0.0)
    #    mdl.phases['smectite'].set_oxide_comp('H2O', )
        # Add smectite oxide weight percent delta values
        # random error ranges
        mdl.phases['smectite'].add_phase_variable('DX_smectite_SiO2', 'SiO2', 3.72)
        mdl.phases['smectite'].add_phase_variable('DX_smectite_Al2O3', 'Al2O3', 0.6)
        mdl.phases['smectite'].add_phase_variable('DX_smectite_Fe', 'Fe', 2.31)
        mdl.phases['smectite'].add_phase_variable('DX_smectite_MgO', 'MgO', 0.49)
        mdl.phases['smectite'].add_phase_variable('DX_smectite_CaO', 'CaO', 0.56)
        mdl.phases['smectite'].add_phase_variable('DX_smectite_Na2O', 'Na2O', 0.36)
    #    mdl.phases['smectite'].add_phase_variable('DX_smectite_H2O', 'H2O', 1.1)
        mdl.phases['smectite'].add_phase_variable('smectite_oxides=100.0', 0.0, 0.0)
    
    elif comp_name=='nontronite':
        # Nontronite from Spokane, WA - Manito (Koster, 1999) Clay Minerals
        mdl.phases['smectite'].set_oxide_comp('SiO2', 44.8)
        mdl.phases['smectite'].set_oxide_comp('TiO2', 0.17)
        mdl.phases['smectite'].set_oxide_comp('Al2O3', 7.8)
        mdl.phases['smectite'].set_oxide_comp('Cr2O3', 0.0)
        mdl.phases['smectite'].set_oxide_comp('Fe', 30.52)
        mdl.phases['smectite'].set_oxide_comp('MnO', 0.0)
        mdl.phases['smectite'].set_oxide_comp('MgO', 0.4)
        mdl.phases['smectite'].set_oxide_comp('CaO', 0.03)
        mdl.phases['smectite'].set_oxide_comp('Na2O', 3.17)
        mdl.phases['smectite'].set_oxide_comp('K2O', 0.1)
        mdl.phases['smectite'].set_oxide_comp('P2O5', 0.0)
        mdl.phases['smectite'].set_oxide_comp('SO3', 0.0)
        mdl.phases['smectite'].set_oxide_comp('Cl', 0.0)
    #    mdl.phases['smectite'].set_oxide_comp('H2O', )
        # Add smectite oxide weight percent delta values
        # random error ranges
        mdl.phases['smectite'].add_phase_variable('DX_smectite_SiO2', 'SiO2', 3.72)
        mdl.phases['smectite'].add_phase_variable('DX_smectite_TiO2', 'TiO2', 0.1)
        mdl.phases['smectite'].add_phase_variable('DX_smectite_Al2O3', 'Al2O3', 0.6)
        mdl.phases['smectite'].add_phase_variable('DX_smectite_Fe', 'Fe', 2.31)
        mdl.phases['smectite'].add_phase_variable('DX_smectite_MgO', 'MgO', 0.49)
        mdl.phases['smectite'].add_phase_variable('DX_smectite_CaO', 'CaO', 0.56)
        mdl.phases['smectite'].add_phase_variable('DX_smectite_Na2O', 'Na2O', 0.36)
    #    mdl.phases['smectite'].add_phase_variable('DX_smectite_H2O', 'H2O', 1.1)
        mdl.phases['smectite'].add_phase_variable('smectite_oxides=100.0', 0.0, 0.0)
    
    elif comp_name=='saponite':
        # Add smectite
        # saponite data from Dehouck, 2014 ref. from Treiman AMNH 2014
        # Griffith Saponite 1
        # Add amorphous oxide weight percent to phases of mdl
        mdl.phases['smectite'].set_oxide_comp('SiO2', 50.21)
        mdl.phases['smectite'].set_oxide_comp('TiO2', 0.05)
        mdl.phases['smectite'].set_oxide_comp('Al2O3', 8.91)
        mdl.phases['smectite'].set_oxide_comp('Cr2O3', 0.01)
        mdl.phases['smectite'].set_oxide_comp('Fe', 17.24)
        mdl.phases['smectite'].set_oxide_comp('MnO', 0.1)
        mdl.phases['smectite'].set_oxide_comp('MgO', 20.73)
        mdl.phases['smectite'].set_oxide_comp('CaO', 2.62)
        mdl.phases['smectite'].set_oxide_comp('Na2O', 0.09)
        mdl.phases['smectite'].set_oxide_comp('K2O', 0.03)
        mdl.phases['smectite'].set_oxide_comp('P2O5', 0.0)
        mdl.phases['smectite'].set_oxide_comp('SO3', 0.0)
        mdl.phases['smectite'].set_oxide_comp('Cl', 0.0)
    #    mdl.phases['smectite'].set_oxide_comp('H2O', )
        # Add smectite oxide weight percent delta values
        # random error ranges
        mdl.phases['smectite'].add_phase_variable('DX_smectite_SiO2', 'SiO2', 3.72)
        mdl.phases['smectite'].add_phase_variable('DX_smectite_Al2O3', 'Al2O3', 0.6)
        mdl.phases['smectite'].add_phase_variable('DX_smectite_Fe', 'Fe', 2.31)
        mdl.phases['smectite'].add_phase_variable('DX_smectite_MgO', 'MgO', 0.49)
        mdl.phases['smectite'].add_phase_variable('DX_smectite_CaO', 'CaO', 0.56)
        mdl.phases['smectite'].add_phase_variable('DX_smectite_Na2O', 'Na2O', 0.36)
    #    mdl.phases['smectite'].add_phase_variable('DX_smectite_H2O', 'H2O', 1.1)
        mdl.phases['smectite'].add_phase_variable('smectite_oxides=100.0', 0.0, 0.0)

def add_amorph_comp(mdl, comp_name, scl):
    if comp_name=='general':
        amorph_comp = { 'SiO2': 39.0,
                        'TiO2': 2.0,
                        'Al2O3': 6.0,
                        'Fe': 25.0,
                        'MnO': 1.0,
                        'MgO': 5.0,
                        'CaO': 6.0,
                        'Na2O': 4.0,
                        'K2O': 1.0,
                        'SO3': 10.0,
                        'Cl': 1.0}
        #amorphous oxide component delta scaling value
        amorph_delta = { 'SiO2':   -5.0,
                         'TiO2':   1.0,
                         'Al2O3': -1.0,
                         'Fe':     3.0,
                         'MnO':    -0.1,
                         'MgO':   -1.0,
                         'CaO':   -1.0,
                         'Na2O':  -1.0,
                         'K2O':    0.1,
                         'SO3':    1.0,
                         'Cl':     1.0}

    if comp_name=='general-jk':
        amorph_comp = { 'SiO2': 39.0,
                        'TiO2': 2.0,
                        'Al2O3': 6.0,
                        'Fe': 25.0,
                        'MnO': 1.0,
                        'MgO': 5.0,
                        'CaO': 6.0,
                        'Na2O': 4.0,
                        'K2O': 1.0,
                        'SO3': 10.0,
                        'Cl': 1.0}
        #amorphous oxide component delta scaling value
        amorph_delta = { 'SiO2':   5.0,
                         'TiO2':   5.0,
                         'Al2O3': -5.0,
                         'Fe':     -5.0,
                         'MnO':    -5.1,
                         'MgO':   5.0,
                         'CaO':   5.0,
                         'Na2O':  5.0,
                         'K2O':    -5.0,
                         'SO3':    -5.0,
                         'Cl':     5.0}

    if comp_name=='default':
        amorph_comp = { 'SiO2': 37.2,
                        'TiO2': 2.06,
                        'Al2O3': 6.04,
                        'Fe': 23.14,
                        'MnO': 0.91,
                        'MgO': 4.86,
                        'CaO': 5.61,
                        'Na2O': 3.56,
                        'K2O': 0.89,
                        'SO3': 11.01,
                        'Cl': 0.1}
        #amorphous oxide component delta scaling value
        amorph_delta = { 'SiO2':   3.72,
                         'TiO2':   0.206,
                         'Al2O3': -0.604,
                         'Fe':     2.314,
                         'MnO':    0.091,
                         'MgO':   -0.486,
                         'CaO':   -0.561,
                         'Na2O':  -0.356,
                         'K2O':    0.089,
                         'SO3':    1.101,
                         'Cl':     1.01}
         
    elif comp_name=='default-ch':
        amorph_comp = { 'SiO2': 37.2,
                        'TiO2': 2.06,
                        'Al2O3': 6.04,
                        'Fe': 23.14,
                        'MnO': 0.91,
                        'MgO': 4.86,
                        'CaO': 5.61,
                        'Na2O': 3.56,
                        'K2O': 0.89,
                        'SO3': 11.01,
                        'Cl': 0.1}
        #amorphous oxide component delta scaling value
        amorph_delta = { 'SiO2':   3.72,
                         'TiO2':   0.206,
                         'Al2O3':  0.604,
                         'Fe':     -2.314,
                         'MnO':    0.091,
                         'MgO':    -0.486,
                         'CaO':    -0.561,
                         'Na2O':   0.356,
                         'K2O':    0.089,
                         'SO3':    1.101,
                         'Cl':     1.01}

    elif comp_name=='default-tp':
        amorph_comp = { 'SiO2': 37.2,
                        'TiO2': 2.06,
                        'Al2O3': 6.04,
                        'Fe': 23.14,
                        'MnO': 0.91,
                        'MgO': 4.86,
                        'CaO': 5.61,
                        'Na2O': 3.56,
                        'K2O': 0.89,
                        'SO3': 11.01,
                        'Cl': 0.1}
        #amorphous oxide component delta scaling value
        amorph_delta = { 'SiO2':   3.72,
                         'TiO2':   0.206,
                         'Al2O3':  0.604,
                         'Fe':     -2.314,
                         'MnO':    0.091,
                         'MgO':    0.5, #change from 0.486
                         'CaO':    -0.561,
                         'Na2O':   0.356,
                         'K2O':    0.089,
                         'SO3':    1.101,
                         'Cl':     1.01}

    elif comp_name=='default-bk':
        amorph_comp = { 'SiO2': 77.49,
                        'TiO2': 2.59,
                        'Al2O3': 0.03,
                        'Cr2O3': 0.15,
                        'Fe': 4.29,
                        'MnO': 0.11,
                        'MgO': 1.17,
                        'CaO': 1.53,
                        'Na2O': 1.54,
                        'K2O': 0.72,
                        'P2O5': 2.1,
                        'SO3': 7.28,
                        'Cl': 0.47}
        #amorphous oxide component delta scaling value
        amorph_delta = { 'SiO2': 7.749,
                        'TiO2': .259,
                        'Al2O3': .003,
                        'Cr2O3': .015,
                        'Fe': .429,
                        'MnO': .011,
                        'MgO': .117,
                        'CaO': .153,
                        'Na2O': .154,
                        'K2O': .072,
                        'P2O5': .21,
                        'SO3': .728,
                        'Cl': .047}

    elif comp_name=='dehouck-griffith-sap1-30':
        # Rocknest amorphous componenet added 2/22/16
        # Add amorphous oxide weight percent to phases of model
        amorph_comp = { 'SiO2', 36.1,
                        'TiO2', 2.3,
                        'Al2O3', 1.8,
                        'Cr2O3', 1.4,
                        'Fe', 24.7,
                        'MnO', 0.8,
                        'MgO', 8.8,
                        'CaO', 6.9,
                        'Na2O', 4.8,
                        'K2O', 0.7,
                        'P2O5', 3.2,
                        'SO3', 2.2,
                        'Cl', 4.2}
        # Add amorphous oxide weight percent delta values
        amorph_delta = {'SiO2', 7.8,
                        'TiO2', 0.7,
                        'Al2O3', 2.7,
                        'Fe', 10.0,
                        'MnO', 0.1,
                        'MgO', 5.8,
                        'CaO', 3.7,
                        'Na2O', 1.2,
                        'K2O', 0.5,
                        'P2O5', 0.0,
                        'SO3', 3.0,
                        'Cl', 0.4}
    elif comp_name=='dehouck-griffith-sap1-45':
        # Add amorphous oxide weight percent to phases of model
        amorph_comp = { 'SiO2', 39.4,
                        'TiO2', 1.7,
                        'Al2O3', 5.0,
                        'Cr2O3', 1.0,
                        'Fe', 23.6,
                        'MnO', 0.6,
                        'MgO', 9.1,
                        'CaO', 6.6,
                        'Na2O', 3.9,
                        'K2O', 0.6,
                        'P2O5', 2.1,
                        'SO3', 2.4,
                        'Cl', 2.9}
        # Add amorphous oxide weight percent delta values
        amorph_delta = {'SiO2', 4.4,
                        'TiO2', 0.4,
                        'Al2O3', 2.4,
                        'Fe', 5.2,
                        'MnO', 0.0,
                        'MgO', 3.15,
                        'CaO', 1.95,
                        'Na2O', 0.85,
                        'K2O', 0.25,
                        'P2O5', 0.0,
                        'SO3', 2.15,
                        'Cl', 0.2}
    elif comp_name=='dehouck-griffith-sap2-30':
        # Add amorphous oxide weight percent to phases of model
        amorph_comp = { 'SiO2': 37.2,
                        'TiO2': 2.2, 
                        'Al2O3': 1.0,
                        'Cr2O3': 1.4,
                        'Fe': 24.7,
                        'MnO': 0.7,
                        'MgO': 10.4,
                        'CaO': 5.8,
                        'Na2O': 4.4,
                        'K2O': 0.7,
                        'P2O5': 3.2,
                        'SO3': 2.2,
                        'Cl': 4.2}
        # Add amorphous oxide weight percent delta values
        amorph_delta = {'SiO2': 7.45,
                        'TiO2': 0.7,
                        'Al2O3': 2.25,
                        'Fe': 9.75,
                        'MnO': 0.15,
                        'MgO': 5.1,
                        'CaO': 3.2,
                        'Na2O': 1.05,
                        'K2O': 0.45,
                        'P2O5': 0.0,
                        'SO3': 2.95,
                        'Cl': 0.35}
    elif comp_name=='dehouck-griffith-sap2-45':
        # Add amorphous oxide weight percent to phases of model
        amorph_comp = { 'SiO2': 40.0,
                        'TiO2': 1.6,
                        'Al2O3': 4.6,
                        'Cr2O3': 1.0,
                        'Fe': 24.0,
                        'MnO': 0.5,
                        'MgO': 9.9,
                        'CaO': 6.0,
                        'Na2O': 3.7,
                        'K2O': 0.6,
                        'P2O5': 2.1,
                        'SO3': 2.4,
                        'Cl': 2.9}
        # Add amorphous oxide weight percent delta values
        amorph_delta = {'SiO2': 4.2,
                        'TiO2': 0.4,
                        'Al2O3': 2.3,
                        'Fe': 5.2,
                        'MnO': 0.1,
                        'MgO': 2.9,
                        'CaO': 1.8,
                        'Na2O': 0.8,
                        'K2O': 0.3,
                        'P2O5': 0.0,
                        'SO3': 1.2,
                        'Cl': 0.2}
    elif comp_name=='SapCa-1':
    #    # SapCa-1 Model amorphous
    #    # Add amorphous oxide weight percent to phases of model
        amorph_comp = { 'SiO2': 30.1,
                        'TiO2': 2.03,
                        'Al2O3': 9.08,
                        'Fe': 33.46,
                        'MnO': .66,
                        'MgO': 0.01,
                        'CaO': 6.46,
                        'Na2O': 3.68,
                        'K2O': 0.56,
                        'SO3': 8.72}
        # Add amorphous oxide weight percent delta values
        amorph_delta = {'SiO2': 3.72,
                        'TiO2': 0.21,
                        'Al2O3': 0.6,
                        'Fe': 2.31,
                        'MnO': 0.09,
                        'MgO': 0.49,
                        'CaO': 0.56,
                        'Na2O': 0.36,
                        'K2O': 0.09,
                        'SO3': 1.1}
    
    # Add amorphous oxide weight percent to phases of model
    mdl.phases['amorphous'].set_oxide_comp('SiO2', amorph_comp['SiO2'])
    mdl.phases['amorphous'].set_oxide_comp('TiO2', amorph_comp['TiO2'])
    mdl.phases['amorphous'].set_oxide_comp('Al2O3',amorph_comp['Al2O3'])
    mdl.phases['amorphous'].set_oxide_comp('Fe', amorph_comp['Fe'])
    mdl.phases['amorphous'].set_oxide_comp('MnO', amorph_comp['MnO'])
    mdl.phases['amorphous'].set_oxide_comp('MgO', amorph_comp['MgO'])
    mdl.phases['amorphous'].set_oxide_comp('CaO', amorph_comp['CaO'])
    mdl.phases['amorphous'].set_oxide_comp('Na2O', amorph_comp['Na2O'])
    mdl.phases['amorphous'].set_oxide_comp('K2O', amorph_comp['K2O'])
    mdl.phases['amorphous'].set_oxide_comp('SO3', amorph_comp['SO3'])
    mdl.phases['amorphous'].set_oxide_comp('Cl', amorph_comp['Cl'])
    # Add amorphous oxide weight percent delta values
    mdl.phases['amorphous'].add_phase_variable('DX_amorphous_SiO2', 'SiO2', scl*amorph_delta['SiO2'])
    mdl.phases['amorphous'].add_phase_variable('DX_amorphous_TiO2', 'TiO2', scl*amorph_delta['TiO2'])
    mdl.phases['amorphous'].add_phase_variable('DX_amorphous_Al2O3', 'Al2O3', scl*amorph_delta['Al2O3'])
    mdl.phases['amorphous'].add_phase_variable('DX_amorphous_Fe', 'Fe', scl*amorph_delta['Fe'])
    mdl.phases['amorphous'].add_phase_variable('DX_amorphous_MnO', 'MnO', scl*amorph_delta['MnO'])
    mdl.phases['amorphous'].add_phase_variable('DX_amorphous_MgO', 'MgO', scl*amorph_delta['MgO'])
    mdl.phases['amorphous'].add_phase_variable('DX_amorphous_CaO', 'CaO', scl*amorph_delta['CaO'])
    mdl.phases['amorphous'].add_phase_variable('DX_amorphous_Na2O', 'Na2O', scl*amorph_delta['Na2O'])
    mdl.phases['amorphous'].add_phase_variable('DX_amorphous_K2O', 'K2O', scl*amorph_delta['K2O'])
    mdl.phases['amorphous'].add_phase_variable('DX_amorphous_SO3', 'SO3', scl*amorph_delta['SO3'])
    mdl.phases['amorphous'].add_phase_variable('DX_amorphous_Cl', 'Cl', scl*amorph_delta['Cl'])
    mdl.phases['amorphous'].add_phase_variable('amorphous_oxides=100', 0.0, 0.0)

# Mineral Phase Class
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
                           'H2O':  0,
                           'F':    0}
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
                        'H2O':  0,
                        'F':   0}
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
        'H2O', 
        'F']

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

def getAPXSData(url, web_flag):
    if web_flag==True:
        # create a new Urllib2 Request object	
        req = urllib2.Request(url)
        # make the request and print the results
        res = urllib2.urlopen(req)
    else:
        res = url
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

def saveResults(resultVars):
    for v in resultVars:
        #if v.name != '__dummy':
            #if v.name[0:8] == 'Phase_X_':
                logging.debug('%-25s = %6.4f' % (v.name, v.varValue))
    

#------------- Creation of the PuLP optimization -------------------------------
def optimize_phase(model, maxPhase, objFunWt): 
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
            phase_frac[x] = 1.0
        else:
            phase_frac[x] = 0.0
    
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
        if model.phases[x].qxrd - model.phases[x].qxrd_error < 0:
            phase_vars['X_' + x].lowBound = 0.0
        else:
            phase_vars['X_' + x].lowBound = model.phases[x].qxrd - model.phases[x].qxrd_error
        phase_vars['X_' + x].upBound = model.phases[x].qxrd + model.phases[x].qxrd_error
        #print x,phase_vars['X_' + x].lowBound, phase_vars['X_' + x].upBound 

    # Add objective function to 'prob' first
    prob += pulp.lpSum([objfun[i]*phase_vars[i] for i in variables]), "Objective function for maximization of particular phase"
    
    # Add constraints to 'prob'
    prob += pulp.lpSum([phase_frac[i] * phase_vars[i] for i in variables]) == 1, "Phases sum to 100%"

    # Add bulk chemistry
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
    #print prob
    return(pulp.LpStatus[prob.status], prob.variables(), pulp.value(prob.objective))

def optimize_routine(model, objFunWt, all_phases_flag, maxPhase):
    result_output_list=[]
    # Run the optimization for the selected phase to maximize
    if all_phases_flag == True:
        fn_out = './output/' + model.name + '_out.csv'
        with open(fn_out, 'w') as csvfile:
            fieldnames = ['Opt', 'Mineral or Variable', 'Wt Percent']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for x in model.phases:
                print '**********Maximizing %s*********' % x
                status, results, objValue = optimize_phase(model, x, objFunWt)
                # The status of the solution is printed to the screen
                logging.debug("Status: %s" % status)
  
                # Each of the variables is printed with it's resolved optimum value
                for y in results:
                    temp_result = Result(x)     
                    temp_result.add_variable(y.name)
                    temp_result.add_value(y.varValue)
                    #logging.debug('%-25s = %6.4f' % (y.name, y.varValue))
                    result_output_list.append(temp_result)

                try:
                    logging.debug('Objective Function Value: %2.4f' % objValue)
                    temp_result.add_obj_fun_result(objValue)
                except:
                    logging.debug('Objective function value unavailable')
#        for x in result_output_list:
#            print x.opt
#            print x.var_value
#            print x.opt_var
        return result_output_list

    else:
        status, results, objValue = optimize_phase(model, maxPhase, objFunWt)
        # The status of the solution is printed to the screen
        logging.debug("Status: %s" % status)

        # Each of the variables is printed with it's resolved optimum value
        for x in results:
            if x.name[0:8] == "Phase_X_":
                logging.debug('%-25s = %6.4f' % (x.name, x.varValue))
        try:
            logging.debug('Objective Function Value: %2.4f' % objValue)
        except:
            logging.debug('Objective function value unavailable')


if __name__ == "__main__":
    import sys
    try:
        fn = sys.argv[1]
    except:
        print "Please provide a filename: python pyrocks.py FILENAME"
    else:
        cf = cif.ReadCif(fn)
