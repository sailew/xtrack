import numpy as np
from cpymad.madx import Madx
import xtrack as xt

mad_ti2 = Madx()
mad_ti2.call('../../../acc-models-tls/sps_extraction/tt60ti2/ti2.seq')
mad_ti2.call('../../../acc-models-tls/sps_extraction/tt60ti2_q20/line/ti2_liu.str')
mad_ti2.beam()
mad_ti2.use('ti2')

line = xt.Line.from_madx_sequence(mad_ti2.sequence['ti2'])
line.particle_ref = xt.Particles(p0c=450e9, mass0=xt.PROTON_MASS_EV, q0=1)
tt = line.get_table()

# Define elements to be used as monitors for orbit correction
# (in this case all element names starting by "bpm" and not ending by "_entry" or "_exit")
tt_monitors = tt.rows['bpm.*'].rows['.*(?<!_entry)$'].rows['.*(?<!_exit)$']
line.steering_monitors_x = tt_monitors.name
line.steering_monitors_y = tt_monitors.name

# Define elements to be used as correctors for orbit correction
# (in this case all element names starting by "mci.", containing "h." or "v.")
tt_h_correctors = tt.rows['mci.*'].rows['.*h\..*']
line.steering_correctors_x = tt_h_correctors.name
tt_v_correctors = tt.rows['mci.*'].rows['.*v\..*']
line.steering_correctors_y = tt_v_correctors.name

# Initial conditions from upstream ring
init = xt.TwissInit(betx=27.77906807, bety=120.39920690,
                     alfx=0.63611880, alfy=-2.70621900,
                     dx=-0.59866300, dpx=0.01603536)

# Reference twiss (no misalignments)
tw_ref = line.twiss4d(start='ti2$start', end='ti2$end', init=init)

# Introduce misalignments on all quadrupoles
tt = line.get_table()
tt_quad = tt.rows['mqi.*']
rgen = np.random.RandomState(2) # fix seed for random number generator
shift_x = rgen.randn(len(tt_quad)) * 0.1e-3 # 0.1 mm rms shift on all quads
shift_y = rgen.randn(len(tt_quad)) * 0.1e-3 # 0.1 mm rms shift on all quads
for nn_quad, sx, sy in zip(tt_quad.name, shift_x, shift_y):
    line.element_refs[nn_quad].shift_x = sx
    line.element_refs[nn_quad].shift_y = sy

# Twiss before correction
tw_before = line.twiss4d(start='ti2$start', end='ti2$end', init=init)

# Correct trajectory
correction = line.correct_trajectory(twiss_table=tw_ref, start='ti2$start', end='ti2$end')

# Twiss after correction
tw_after = line.twiss4d(start='ti2$start', end='ti2$end', init=init)

# Extract correction strength
s_x_correctors = correction.x_correction.s_correctors
s_y_correctors = correction.y_correction.s_correctors
kicks_x = correction.x_correction.get_kick_values()
kicks_y = correction.y_correction.get_kick_values()

assert tw_before.x.std() > 1.5e-3
assert tw_before.y.std() > 0.5e-3

assert tw_after.x.std() < 0.3e-3
assert tw_after.y.std() < 0.3e-3

assert kicks_x.std() < 2e-5
assert kicks_y.std() < 2e-5
