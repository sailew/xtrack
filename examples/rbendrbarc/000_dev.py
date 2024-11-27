import numpy as np
import xtrack as xt
import xobjects as xo
from cpymad.madx import Madx

mad = Madx()
mad.input('''
    ang = 0.6;
    lb = 0.5;
    rb: rbend, l=lb, angle=ang;

    beam, particle=proton, energy=1.0;
    seq: sequence, l=2;
    rb, at=1;
    endsequence;
    use, sequence=seq;
''')
tw = xt.Table(mad.twiss(betx=1.0, bety=1.0))

ds_madx = tw['s', 'rb:1'] - tw['s', 'rb:1<<1']

line = xt.Line.from_madx_sequence(mad.sequence.seq)

xo.assert_allclose(ds_madx, line['rb'].length, atol=0, rtol=1e-12)

env = xt.Environment()
env['lb'] = 0.5
env['ang'] = 0.6
env.new('rb_rbarc', xt.Bend)
env.set('rb_rbarc', length='lb', angle='ang', rbend=True, rbarc=True, k0_from_h=True)

xo.assert_allclose(env['rb_rbarc'].length, ds_madx, atol=0, rtol=1e-12)
xo.assert_allclose(env['rb_rbarc'].h * env['rb_rbarc'].length, 0.6, atol=0, rtol=1e-12)
xo.assert_allclose(env['rb_rbarc'].edge_entry_angle, 0.3, atol=0, rtol=1e-12)
xo.assert_allclose(env['rb_rbarc'].edge_exit_angle, 0.3, atol=0, rtol=1e-12)

assert env['rb_rbarc'].get_expr('length') == "(vars['lb'] / f['sinc']((0.5 * vars['ang'])))"
assert env['rb_rbarc'].get_expr('h') == "(f['sin']((0.5 * vars['ang'])) / (0.5 * vars['lb']))"
assert env['rb_rbarc'].get_expr('k0') == env['rb_rbarc'].get_expr('h')
assert env['rb_rbarc'].get_expr('edge_entry_angle') == "(0.0 + (vars['ang'] / 2))"
assert env['rb_rbarc'].get_expr('edge_exit_angle') == "(0.0 + (vars['ang'] / 2))"

env.new('rb_norbarc', xt.Bend)
env.set('rb_norbarc', length='lb', angle='ang', rbend=True, rbarc=False, k0_from_h=True)

xo.assert_allclose(env['rb_norbarc'].length, 0.5, atol=0, rtol=1e-12)
xo.assert_allclose(env['rb_norbarc'].h * env['rb_norbarc'].length, 0.6, atol=0, rtol=1e-12)
xo.assert_allclose(env['rb_norbarc'].k0, env['rb_norbarc'].h, atol=0, rtol=1e-12)
xo.assert_allclose(env['rb_norbarc'].edge_entry_angle, 0.3, atol=0, rtol=1e-12)
xo.assert_allclose(env['rb_norbarc'].edge_exit_angle, 0.3, atol=0, rtol=1e-12)

assert env['rb_norbarc'].get_expr('length') == "vars['lb']"
assert env['rb_norbarc'].get_expr('h') == "(vars['ang'] / vars['lb'])"
assert env['rb_norbarc'].get_expr('k0') == env['rb_norbarc'].get_expr('h')
assert env['rb_norbarc'].get_expr('edge_entry_angle') == "(0.0 + (vars['ang'] / 2))"
assert env['rb_norbarc'].get_expr('edge_exit_angle') == "(0.0 + (vars['ang'] / 2))"

# Check an sbend
env.new('sb', xt.Bend)
env.set('sb', length='lb', angle='ang', rbend=False, rbarc=True, k0_from_h=True)

xo.assert_allclose(env['sb'].length, 0.5, atol=0, rtol=1e-12)
xo.assert_allclose(env['sb'].h * env['sb'].length, 0.6, atol=0, rtol=1e-12)
xo.assert_allclose(env['sb'].edge_entry_angle, 0, atol=1e-12, rtol=0)
xo.assert_allclose(env['sb'].edge_exit_angle, 0, atol=1e-12, rtol=0)

assert env['sb'].get_expr('length') == "vars['lb']"
assert env['sb'].get_expr('h') == "(vars['ang'] / vars['lb'])"
assert env['sb'].get_expr('k0') == env['sb'].get_expr('h')
assert env['sb'].get_expr('edge_entry_angle') == None
assert env['sb'].get_expr('edge_exit_angle') == None