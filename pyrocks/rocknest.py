# coding: utf-8
import pyrocks

model = pyrocks.Model('Rocknest')

for x in pyrocks.phases:
    model.add_phase(x)

for x in model.phases:
    model.phases[x].add_qxrd(pyrocks.phase_abun[x])
    print "%20s: %5.2f" % (model.phases[x].name,model.phases[x].qxrd)
    
