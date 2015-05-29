# coding: utf-8

import pyrocks

model = pyrocks.Model('Rocknest')

for x in pyrocks.phases:
    model.add_phase(x)

for x in model.phases:
    model.phases[x].add_qxrd(pyrocks.phase_abun[x])
    print "%20s: %5.2f" % (model.phases[x].name,model.phases[x].qxrd)
 
model.add_phase('amorphous')

# Add plagioclase oxide weight percent to phases of model
model.phases['plagioclase'].set_oxide_comp('SiO2', 53.05)
model.phases['plagioclase'].set_oxide_comp('Al2O3', 30.01)
model.phases['plagioclase'].set_oxide_comp('CaO', 12.38)
model.phases['plagioclase'].set_oxide_comp('Na2O', 4.56)

# Add oxide weight percent delta values, plagioclase defined relative to SiO2
model.phases['plagioclase'].add_delta_oxide('SiO2', {'SiO2': -1.5, 'Al2O3': 1.005, 'CaO': 1.2, 'Na2O': -0.69})

# Add olivine oxide weight percent to phases of model
ol_ox = {'SiO2': 36.93,
           'TiO2': 0.09,
           'Al2O3': 1.8,
           'Fe2O3+FeO': 30.97,
           'MnO': 0.43,
           'MgO': 29.2,
           'CaO': 0.58,
           'Na2O': 0.09,
           'K2O': 0.03}

for x,y in ol_ox.items():
    model.phases['olivine'].set_oxide_comp(x, y)

# Add olivine oxide weight percent delta values
model.phases['olivine'].add_delta_oxide('SiO2',{'SiO2': 1.17})
model.phases['olivine'].add_delta_oxide('TiO2',{'TiO2': 0.12})
model.phases['olivine'].add_delta_oxide('Al2O3', {'Al2O3': 2.41})
model.phases['olivine'].add_delta_oxide('Fe2O3+FeO', {'Fe2O3+FeO': 1.99})
model.phases['olivine'].add_delta_oxide('MnO', {'MnO': 0.15})
model.phases['olivine'].add_delta_oxide('MgO', {'MgO': 2.35})
model.phases['olivine'].add_delta_oxide('CaO', {'CaO': 1.16})
model.phases['olivine'].add_delta_oxide('Na2O',{'Na2O': 0.18})
model.phases['olivine'].add_delta_oxide('K2O', {'K2O': 0.01})

for i in model.phases['olivine'].oxide_comp:
    print i
for x,y in model.phases['olivine'].delta_oxides.items():
    print x,y.oxides 

# Add augite oxide weight percent to phases of model
model.phases['augite'].set_oxide_comp('SiO2', 48.88)
model.phases['augite'].set_oxide_comp('TiO2', 1.3)
model.phases['augite'].set_oxide_comp('Al2O3', 4.88)
model.phases['augite'].set_oxide_comp('Fe2O3+FeO', 9.11)
model.phases['augite'].set_oxide_comp('MnO', 0.15)
model.phases['augite'].set_oxide_comp('MgO', 15.08)
model.phases['augite'].set_oxide_comp('CaO', 19.23)
model.phases['augite'].set_oxide_comp('Na2O', 0.55)
model.phases['augite'].set_oxide_comp('K2O', 0.11)

# Add augite oxide weight percent delta values
model.phases['augite'].add_delta_oxide('SiO2', {'SiO2': 0.75})
model.phases['augite'].add_delta_oxide('TiO2', {'TiO2': 0.45})
model.phases['augite'].add_delta_oxide('Al2O3', {'Al2O3': 0.76})
model.phases['augite'].add_delta_oxide('Fe2O3+FeO', {'Fe2O3+FeO': 2.69})
model.phases['augite'].add_delta_oxide('MnO', {'MnO': 0.3})
model.phases['augite'].add_delta_oxide('MgO', {'MgO': 0})
model.phases['augite'].add_delta_oxide('CaO', {'CaO': 0.18})
model.phases['augite'].add_delta_oxide('Na2O', {'Na2O': 0.46})
model.phases['augite'].add_delta_oxide('K2O', {'K2O': 0.12})


# Add pigeonite oxide weight percent to phases of model
model.phases['pigeonite'].set_oxide_comp('SiO2', 53.36)
model.phases['pigeonite'].set_oxide_comp('Fe2O3+FeO', 21.69)
model.phases['pigeonite'].set_oxide_comp('MgO', 20.22)
model.phases['pigeonite'].set_oxide_comp('CaO', 4.73)

# Add pigeonite oxide weight percent delta values
model.phases['pigeonite'].add_delta_oxide('SiO2', {'SiO2': 1.12})
model.phases['pigeonite'].add_delta_oxide('Fe2O3+FeO', {'Fe2O3+FeO': 0.88})
model.phases['pigeonite'].add_delta_oxide('MgO', {'MgO': 1.65})
model.phases['pigeonite'].add_delta_oxide('CaO', {'CaO': 3.05})

# Add magnetite oxide weight percent delta values
model.phases['magnetite'].set_oxide_comp('Fe2O3+FeO', 100)

# Add anhydrite oxide weight percent delta values
model.phases['anhydrite'].set_oxide_comp('CaO', 41.19)
model.phases['anhydrite'].set_oxide_comp('SO3', 58.81)

# Add anhydrite oxide weight percent delta values
model.phases['anhydrite'].add_delta_oxide('CaO', {'CaO': 0.1})
model.phases['anhydrite'].add_delta_oxide('SO3', {'SO3': 0.1})

# Add quartz oxide weight percent delta values
model.phases['quartz'].set_oxide_comp('SiO2', 100)

# Add sanidine oxide weight percent to phases of model
model.phases['sanidine'].set_oxide_comp('SiO2', 64.76)
model.phases['sanidine'].set_oxide_comp('Al2O3', 18.32)
model.phases['sanidine'].set_oxide_comp('K2O', 16.92)

# Add sanidine oxide weight percent delta values
model.phases['sanidine'].add_delta_oxide('SiO2', {'SiO2': 0.1})
model.phases['sanidine'].add_delta_oxide('Al2O3', {'Al2O3': 0.1})
model.phases['sanidine'].add_delta_oxide('K2O', {'K2O': 0.1})

# Add hematite oxide weight percent delta values
model.phases['hematite'].set_oxide_comp('Fe2O3+FeO', 100)

# Add ilmenite oxide weight percent to phases of model
model.phases['ilmenite'].set_oxide_comp('TiO2', 52.65)
model.phases['ilmenite'].set_oxide_comp('Fe2O3+FeO', 47.35)

# Add ilmenite oxide weight percent delta values
model.phases['ilmenite'].add_delta_oxide('TiO2', {'TiO2': 0.1})
model.phases['ilmenite'].add_delta_oxide('Fe2O3+FeO', {'Fe2O3+FeO': 0.1})

# Add amorphous oxide weight percent to phases of model
model.phases['amorphous'].set_oxide_comp('SiO2', 37.2)
model.phases['amorphous'].set_oxide_comp('TiO2', 2.06)
model.phases['amorphous'].set_oxide_comp('Al2O3', 6.04)
model.phases['amorphous'].set_oxide_comp('Fe2O3+FeO', 23.14)
model.phases['amorphous'].set_oxide_comp('MnO', 0.91)
model.phases['amorphous'].set_oxide_comp('MgO', 4.86)
model.phases['amorphous'].set_oxide_comp('CaO', 5.61)
model.phases['amorphous'].set_oxide_comp('Na2O', 3.56)
model.phases['amorphous'].set_oxide_comp('K2O', 0.89)
model.phases['amorphous'].set_oxide_comp('SO3', 11.01)

# Add amorphous oxide weight percent delta values
model.phases['amorphous'].add_delta_oxide('SiO2', {'SiO2': 3.72})
model.phases['amorphous'].add_delta_oxide('TiO2', {'TiO2': 0.21})
model.phases['amorphous'].add_delta_oxide('Al2O3', {'Al2O3': 0.6})
model.phases['amorphous'].add_delta_oxide('Fe2O3+FeO', {'Fe2O3:FeO': 2.31})
model.phases['amorphous'].add_delta_oxide('MnO', {'MnO': 0.09})
model.phases['amorphous'].add_delta_oxide('MgO', {'MgO': 0.49})
model.phases['amorphous'].add_delta_oxide('CaO', {'CaO': 0.56})
model.phases['amorphous'].add_delta_oxide('Na2O', {'Na2O': 0.36})
model.phases['amorphous'].add_delta_oxide('K2O', {'K2O': 0.09})
model.phases['amorphous'].add_delta_oxide('SO3', {'SO3':1.1})

for j in pyrocks.bulk:
    for x in model.phases:
        print '%s %s %f' % (j, model.phases[x].name, model.phases[x].oxide_comp[j])
        for k in model.phases[x].delta_oxides:
            print '%5s d%10s:%5.2f' % (j, k, model.phases[x].delta_oxides[k].oxides[k])
    
        #if model.phases[x].delta_oxides.get('SiO2') is not None:
        #    print model.phases[x].delta_oxides.get('SiO2').oxides['SiO2']

