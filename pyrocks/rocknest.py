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
model.phases['plagioclase'].add_oxide('SiO2', 53.05)
model.phases['plagioclase'].add_oxide('Al2O3', 30.01)
model.phases['plagioclase'].add_oxide('CaO', 12.38)
model.phases['plagioclase'].add_oxide('Na2O', 4.56)

# Add oxide weight percent delta values, plagioclase defined relative to SiO2
model.phases['plagioclase'].add_delta('SiO2', {'SiO2': -1.5, 'Al2O3': 1.005, 'CaO': 1.2, 'Na2O': -0.69})

# Add olivine oxide weight percent to phases of model
model.phases['olivine'].add_oxide('SiO2', 36.93)
model.phases['olivine'].add_oxide('TiO2', 0.09)
model.phases['olivine'].add_oxide('Al2O3', 1.8)
model.phases['olivine'].add_oxide('Fe2O3+FeO', 30.97)
model.phases['olivine'].add_oxide('MnO', 0.43)
model.phases['olivine'].add_oxide('MgO', 29.2)
model.phases['olivine'].add_oxide('CaO', 0.58)
model.phases['olivine'].add_oxide('Na2O', 0.09)
model.phases['olivine'].add_oxide('K2O', 0.03)

# Add olivine oxide weight percent delta values
model.phases['olivine'].add_delta('SiO2', 1.17)
model.phases['olivine'].add_delta('TiO2', 0.12)
model.phases['olivine'].add_delta('Al2O3', 2.41)
model.phases['olivine'].add_delta('Fe2O3+FeO', 1.99)
model.phases['olivine'].add_delta('MnO', 0.15)
model.phases['olivine'].add_delta('MgO', 2.35)
model.phases['olivine'].add_delta('CaO', 1.16)
model.phases['olivine'].add_delta('Na2O', 0.18)
model.phases['olivine'].add_delta('K2O', 0.01)

# Add augite oxide weight percent to phases of model
model.phases['augite'].add_oxide('SiO2', 48.88)
model.phases['augite'].add_oxide('TiO2', 1.3)
model.phases['augite'].add_oxide('Al2O3', 4.88)
model.phases['augite'].add_oxide('Fe2O3+FeO', 9.11)
model.phases['augite'].add_oxide('MnO', 0.15)
model.phases['augite'].add_oxide('MgO', 15.08)
model.phases['augite'].add_oxide('CaO', 19.23)
model.phases['augite'].add_oxide('Na2O', 0.55)
model.phases['augite'].add_oxide('K2O', 0.11)

# Add augite oxide weight percent delta values
model.phases['augite'].add_delta('SiO2', 0.75)
model.phases['augite'].add_delta('TiO2', 0.45)
model.phases['augite'].add_delta('Al2O3', 0.76)
model.phases['augite'].add_delta('Fe2O3+FeO', 2.69)
model.phases['augite'].add_delta('MnO', 0.3)
model.phases['augite'].add_delta('MgO', 0)
model.phases['augite'].add_delta('CaO', 0.18)
model.phases['augite'].add_delta('Na2O', 0.46)
model.phases['augite'].add_delta('K2O', 0.12)

# Add pigeonite oxide weight percent to phases of model
model.phases['pigeonite'].add_oxide('SiO2', 53.36)
model.phases['pigeonite'].add_oxide('Fe2O3+FeO', 21.69)
model.phases['pigeonite'].add_oxide('MgO', 20.22)
model.phases['pigeonite'].add_oxide('CaO', 4.73)

# Add pigeonite oxide weight percent delta values
model.phases['pigeonite'].add_delta('SiO2', 1.12)
model.phases['pigeonite'].add_delta('Fe2O3+FeO', 0.88)
model.phases['pigeonite'].add_delta('MgO', 1.65)
model.phases['pigeonite'].add_delta('CaO', 3.05)

# Add magnetite oxide weight percent delta values
model.phases['magnetite'].add_oxide('Fe2O3+FeO', 100)

# Add anhydrite oxide weight percent delta values
model.phases['anhydrite'].add_oxide('CaO', 41.19)
model.phases['anhydrite'].add_oxide('SO3', 58.81)

# Add anhydrite oxide weight percent delta values
model.phases['anhydrite'].add_delta('CaO', 0.1)
model.phases['anhydrite'].add_delta('SO3', 0.1)

# Add quartz oxide weight percent delta values
model.phases['quartz'].add_oxide('SiO2', 100)

# Add sanidine oxide weight percent to phases of model
model.phases['sanidine'].add_oxide('SiO2', 64.76)
model.phases['sanidine'].add_oxide('Al2O3', 18.32)
model.phases['sanidine'].add_oxide('K2O', 16.92)

# Add sanidine oxide weight percent delta values
model.phases['sanidine'].add_delta('SiO2', 0.1)
model.phases['sanidine'].add_delta('Al2O3', 0.1)
model.phases['sanidine'].add_delta('K2O', 0.1)

# Add hematite oxide weight percent delta values
model.phases['hematite'].add_oxide('Fe2O3+FeO', 100)

# Add ilmenite oxide weight percent to phases of model
model.phases['ilmenite'].add_oxide('TiO2', 52.65)
model.phases['ilmenite'].add_oxide('Fe2O3+FeO', 47.35)

# Add ilmenite oxide weight percent delta values
model.phases['ilmenite'].add_delta('TiO2', 0.1)
model.phases['ilmenite'].add_delta('Fe2O3+FeO', 0.1)

# Add amorphous oxide weight percent to phases of model
model.phases['amorphous'].add_oxide('SiO2', 37.2)
model.phases['amorphous'].add_oxide('TiO2', 2.06)
model.phases['amorphous'].add_oxide('Al2O3', 6.04)
model.phases['amorphous'].add_oxide('Fe2O3+FeO', 23.14)
model.phases['amorphous'].add_oxide('MnO', 0.91)
model.phases['amorphous'].add_oxide('MgO', 4.86)
model.phases['amorphous'].add_oxide('CaO', 5.61)
model.phases['amorphous'].add_oxide('Na2O', 3.56)
model.phases['amorphous'].add_oxide('K2O', 0.89)
model.phases['amorphous'].add_oxide('SO3', 11.01)

# Add amorphous oxide weight percent delta values
model.phases['amorphous'].add_delta('SiO2', 3.72)
model.phases['amorphous'].add_delta('TiO2', 0.21)
model.phases['amorphous'].add_delta('Al2O3', 0.6)
model.phases['amorphous'].add_delta('Fe2O3+FeO', 2.31)
model.phases['amorphous'].add_delta('MnO', 0.09)
model.phases['amorphous'].add_delta('MgO', 0.49)
model.phases['amorphous'].add_delta('CaO', 0.56)
model.phases['amorphous'].add_delta('Na2O', 0.36)
model.phases['amorphous'].add_delta('K2O', 0.09)
model.phases['amorphous'].add_delta('SO3', 1.1)

#for x in model.phases:
#     print '%s:' % model.phases[x].name
#     print model.phases[x].oxides

for x in model.phases:
#     if model.phases[x].oxides.items() == 'SiO2':
      try:
          print model.phases[x].name, model.phases[x].oxides['SiO2']
          print model.phases[x].name, model.phases[x].deltas['SiO2']
      except:
          print 'Exception'
#         print model.phases[x].oxides['SiO2']
