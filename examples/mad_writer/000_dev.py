import numpy as np
from cpymad.madx import Madx
import xtrack as xt
import os

# TODO:
# - handle thick slicing of bends (edges!)
# - handle isolated dipole edges
# - crab cavities
# - rbarc (sps)

# ----- Test sequence -----
# mad = Madx()
# # Element definitions
# mad.input("""

# a = 1.;
# b := sin(3*a) + cos(2*a);

# cav1: rfcavity, freq:=a*10, lag:=a*0.5, volt:=a*6;
# cav2: rfcavity, freq:=10, lag:=0.5, volt:=6;
# testseq: sequence, l=10;
# c1: cav1, at=0.2, apertype=circle, aperture=0.01;
# c2: cav2, at=0.5, apertype=circle, aperture=0.01;
# endsequence;
# """
# )
# # Beam
# mad.input("""
# beam, particle=proton, gamma=1.05, sequence=testseq;
# """)
# mad.use('testseq')
# seq = mad.sequence['testseq']
# line = xt.Line.from_madx_sequence(sequence=seq, deferred_expressions=True)

# ----- Elena -----
# mad = Madx()
# folder = ('../../test_data/elena')
# mad.call(folder + '/elena.seq')
# mad.call(folder + '/highenergy.str')
# mad.call(folder + '/highenergy.beam')
# mad.use('elena')
# seq = mad.sequence.elena
# line = xt.Line.from_madx_sequence(seq)
# line.particle_ref = xt.Particles(gamma0=seq.beam.gamma,
#                                     mass0=seq.beam.mass * 1e9,
#                                     q0=seq.beam.charge)

# line.slice_thick_elements(
#     slicing_strategies=[
#         xt.Strategy(slicing=None), # don't touch other elements
#         xt.Strategy(slicing=xt.Uniform(10, mode='thick'), element_type=xt.Bend)
#     ])

# ----- LHC (thick) -----
line = xt.Line.from_json('../../test_data/hllhc15_thick/lhc_thick_with_knobs.json')
line.build_tracker()

# ----- LHC (thin) -----
# line = xt.Line.from_json('../../test_data/hllhc15_noerrors_nobb/line_w_knobs_and_particle.json')
# line.particle_ref = xt.Particles(mass=xt.PROTON_MASS_EV, p0c=7000e9)
# line.build_tracker()

# ----- LHC (thin) -----
# mad1 = Madx()
# mad1.call('../../test_data/hllhc15_noerrors_nobb/sequence_with_crabs.madx')
# mad1.use('lhcb1')
# seq = mad1.sequence.lhcb1
# line = xt.Line.from_madx_sequence(seq, deferred_expressions=True)
# line.particle_ref = xt.Particles(gamma0=seq.beam.gamma,
#                                     mass0=seq.beam.mass * 1e9,
#                                     q0=seq.beam.charge)

mad_seq = line.to_madx_sequence(sequence_name='seq')


temp_fname = 'temp4madng'
with open(temp_fname+'.madx', 'w') as fid:
    fid.write(mad_seq)

from pymadng import MAD
mad = MAD()
mad.MADX.load(f'"{temp_fname}.madx"', f"'{temp_fname}.madng'")
# os.remove(temp_fname)

# mad2 = Madx()
# mad2.input(mad_seq)
# mad2.use('seq')

# tw = line.twiss(method='4d')
# twmad2 = mad2.twiss()

