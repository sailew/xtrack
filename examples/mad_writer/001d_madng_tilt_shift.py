import numpy as np
import xtrack as xt
import xobjects as xo

line = xt.Line.from_json(
    '../../test_data/hllhc15_thick/lhc_thick_with_knobs.json')

tt = line.get_table()
tt_quads = tt.rows[tt.element_type=='Quadrupole']

# Introduce misalignments on all quadrupoles
tt = line.get_table()
tt_quad = tt.rows['mq\..*']
rgen = np.random.RandomState(1) # fix seed for random number generator
                                # (to have reproducible results)
shift_x = rgen.randn(len(tt_quad)) * 0.01e-3 # 0.01 mm rms shift on all quads
shift_y = rgen.randn(len(tt_quad)) * 0.01e-3 # 0.01 mm rms shift on all quads
rot_s = rgen.randn(len(tt_quad)) * 1e-3 # 1 mrad rms rotation on all quads
k2l = rgen.rand(len(tt_quad)) * 1e-3

line['on_error'] = 1.
for nn_quad, sx, sy, rr, kkk in zip(tt_quad.name, shift_x, shift_y, rot_s, k2l):
    line[nn_quad].shift_x = sx * line.ref['on_error']
    line[nn_quad].shift_y = sy * line.ref['on_error']
    line[nn_quad].rot_s_rad = rr * line.ref['on_error']
    line[nn_quad].knl[2] = kkk * line.ref['on_error']

tw = line.madng_twiss()

xo.assert_allclose(tw.x, tw.x_ng, atol=5e-4*tw.x.std(), rtol=0)
xo.assert_allclose(tw.y, tw.y_ng, atol=5e-4*tw.y.std(), rtol=0)
xo.assert_allclose(tw.betx2, tw.beta12_ng, atol=0, rtol=2e-3)
xo.assert_allclose(tw.bety1, tw.beta21_ng, atol=0, rtol=2e-3)
xo.assert_allclose(tw.wx_chrom, tw.wx_ng, atol=5e-3*tw.wx_chrom.max(), rtol=0)
xo.assert_allclose(tw.wy_chrom, tw.wy_ng, atol=5e-3*tw.wy_chrom.max(), rtol=0)
xo.assert_allclose(tw.ax_chrom, tw.ax_ng, atol=5e-3*tw.wx_chrom.max(), rtol=0)
xo.assert_allclose(tw.ay_chrom, tw.ay_ng, atol=5e-3*tw.wy_chrom.max(), rtol=0)
xo.assert_allclose(tw.bx_chrom, tw.bx_ng, atol=5e-3*tw.wx_chrom.max(), rtol=0)
xo.assert_allclose(tw.by_chrom, tw.by_ng, atol=5e-3*tw.wy_chrom.max(), rtol=0)

line['on_error'] = 0
tw = line.madng_twiss()

xo.assert_allclose(tw.x, tw.x_ng, atol=5e-4*tw.x.std(), rtol=0)
xo.assert_allclose(tw.y, tw.y_ng, atol=5e-4*tw.y.std(), rtol=0)
xo.assert_allclose(tw.betx2, tw.beta12_ng, atol=0, rtol=2e-3)
xo.assert_allclose(tw.bety1, tw.beta21_ng, atol=0, rtol=2e-3)
xo.assert_allclose(tw.wx_chrom, tw.wx_ng, atol=5e-3*tw.wx_chrom.max(), rtol=0)
xo.assert_allclose(tw.wy_chrom, tw.wy_ng, atol=5e-3*tw.wy_chrom.max(), rtol=0)
xo.assert_allclose(tw.ax_chrom, tw.ax_ng, atol=5e-3*tw.wx_chrom.max(), rtol=0)
xo.assert_allclose(tw.ay_chrom, tw.ay_ng, atol=5e-3*tw.wy_chrom.max(), rtol=0)
xo.assert_allclose(tw.bx_chrom, tw.bx_ng, atol=5e-3*tw.wx_chrom.max(), rtol=0)
xo.assert_allclose(tw.by_chrom, tw.by_ng, atol=5e-3*tw.wy_chrom.max(), rtol=0)