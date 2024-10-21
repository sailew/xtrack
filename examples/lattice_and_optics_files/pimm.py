import xtrack as xt

env = xt.get_environment(verbose=True)

env.vars.default_to_zero = True

env.new('qf1', 'Quadrupole', length=2*0.175, k1='qf1k1')
env.new('qd',  'Quadrupole', length=2*0.175, k1='qd1k1')
env.new('qf2', 'Quadrupole', length=2*0.175, k1='qf2k1')
env.new('qa',  'Quadrupole', length=0.556,   k1='qa1k1')

env.new('mb',  'Bend', length=1.661, angle=0.3926990817,
        edge_entry_angle=0.19634954085, edge_exit_angle=0.19634954085)

env.new('xcd1', 'Sextupole', length=0.2, k2='k2xcd')
env.new('xcf1', 'Sextupole', length=0.2, k2='k2xcf')
env.new('xcd2', 'Sextupole', length=0.2, k2='k2xcd')
env.new('xcf2', 'Sextupole', length=0.2, k2='k2xcf')
env.new('xrra', 'Sextupole', length=0.2, k2='k2xrr_a')
env.new('xrrb', 'Sextupole', length=0.2, k2='k2xrr_b')

env.new('es_injection', 'Marker')
env.new('es_marker',    'Marker')
env.new('betkick',      'Marker')
env.new('rfkokick',     'Marker')
env.new('pimm_start',  'Marker')

env.new('pimm_cavity',  'Cavity')

pimm = env.new_builder(name='pimm')

# Place elements
pimm.new('end_ring', 'Marker', at=75.24) # defines ring length
pimm.place('pimm_start', at=0)
pimm.place('pimm_cavity', at=0.001)
pimm.place('es_injection', at=1.05)
pimm.place('qf1', at=2.3875)
pimm.place('mb', at=3.8125)
pimm.place('qd', at=5.2925)
pimm.place('mb', at=7.0475)
pimm.place('qf1', at=8.3275)
pimm.place('rfkokick', at= 9.30875)
pimm.place('xcd1', at=10.29)
pimm.place('qf2', at=10.6775)
pimm.place('mb', at=12.1325)
pimm.place('qd', at=14.2625)
pimm.place('mb', at=15.9175)
pimm.place('qf2', at=17.1975)
pimm.place('betkick', at=18.7225)
pimm.place('qf2', at=20.2475)
pimm.place('mb', at=21.7025)
pimm.place('qd', at=23.1825)
pimm.place('xcf1', at=24.045)
pimm.place('mb', at=25.4875)
pimm.place('qf2', at=26.7675)
pimm.place('qa', at=27.9425)
pimm.place('qf1', at=29.1175)
pimm.place('mb', at=30.5725)
pimm.place('qd', at=32.1525)
pimm.place('mb', at=33.8075)
pimm.place('qf1', at=35.0575)
pimm.place('xrra', at=35.0575 + 0.6)
pimm.place('xrrb', at=40.0075 - 0.6)
pimm.place('qf1', at=40.0075)
pimm.place('mb', at=41.4325)
pimm.place('qd', at=42.9125)
pimm.place('mb', at=44.6675)
pimm.place('qf1', at=45.9475)
pimm.place('xcd2', at=47.91)
pimm.place('qf2', at=48.2975)
pimm.place('mb', at=49.7525)
pimm.place('qd', at=51.8825)
pimm.place('mb', at=53.5375)
pimm.place('qf2', at=54.8175)
pimm.place('qf2', at=57.8675)
pimm.place('mb', at=59.3225)
pimm.place('qd', at=60.8025)
pimm.place('xcf2', at=61.665)
pimm.place('mb', at=63.1075)
pimm.place('qf2', at=64.3875)
pimm.place('qf1', at=66.7375)
pimm.place('mb', at=68.1925)
pimm.place('qd', at=69.7725)
pimm.place('mb', at=71.4275)
pimm.place('qf1', at=72.6775)
pimm.place('es_marker', at=73.25225)

pimm = pimm.build() # Becomes a line
env.default_to_zero = False