#Script per creare tutti i dati relativi a questo problema


from solver.helper_classes import *
import problems.kalecki_eqn_case.kalecki_eqn as kalecki
from problems.kalecki_eqn_case.kalecki_helper_classes import *
from kalecki_analytical_solution import *
from GP_operations import compute_new_t, compute_new_x, compute_new_u, compute_ud, compute_du_dx, compute_du3_dx

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm


args = kalecki.kalecki_args(T=1.0, nt=4001, T_start=0., l=0.4, theta=1, c=0.75, v=0.5, dleft_bv_dt=0, dright_bv_dt=0, dbc_l=1,
                 nbc_l=0, dbc_r=1, nbc_r=0, max_deriv=3, acc=4, acc_advec=1)



#compute times t
t = tf.linspace(args.T_start, args.T, args.nt)
t_df = pd.DataFrame(t)
t_df.to_csv('datasets_2\\t.csv', index=False, header=False)


#compute the analytic solution
kalecki_analytic_inst = kalecki_eqn_analy(args)
u_analytic = []
for i in range(args.nt):
    u_analytic.append(tf.expand_dims(kalecki_analytic_inst(t[i]), axis=1))
u_analytic = tf.concat(u_analytic, axis=0)
print("u analitica", u_analytic)

u_analytic_vector = np.zeros(args.nt)
for i in range(args.nt):
    u_analytic_vector[i] = u_analytic.numpy()[i, 0]

u_df = pd.DataFrame(u_analytic_vector)
u_df.to_csv('datasets_2\\u.csv', index=False, header=False)


#compute partial derivatives
def finite_diff_matrix(grid, m=0, acc=2, axis=1):
    A = FinDiff(axis, grid, m, acc=acc).matrix(grid.shape).toarray()
    if m != 0:
        coefs = coefficients(deriv=m, acc=acc)
        offset_c = coefs['center']['offsets']
        offset_f = coefs['forward']['offsets']
        offset_b = coefs['backward']['offsets']
        for i in range(1, int(len(offset_c) / 2)):
            offset_left = [j - i for j in offset_f]
            offset_right = [j + i for j in offset_b]
            coefs_left = coefficients(deriv=m, offsets=offset_left)['coefficients'] * (
                    1. / (grid[1] - grid[0]) ** (m))
            coefs_right = coefficients(deriv=m, offsets=offset_right)['coefficients'] * (
                    1. / (grid[1] - grid[0]) ** (m))
            offset_left = [i + j for j in offset_left]
            for k in range(len(offset_f)):
                A[i, i + offset_f[k]] = 0.
            A[i, offset_left] = coefs_left
            offset_right = [-i - 1 + j for j in offset_right]
            for k in range(len(offset_b)):
                A[-1 - i, -i - 1 + offset_b[k]] = 0.
            A[-1 - i, offset_right] = coefs_right
    return A

du_dt = np.zeros([args.nt])
for i in range(args.Nx):
    du_dt = np.dot(finite_diff_matrix(t.numpy(), m=1, acc=2, axis=0),  u_analytic_vector)
du_dt_df = pd.DataFrame(du_dt)
du_dt_df.to_csv('datasets_2\\du_dt.csv', index=False, header=False)


#compute delay
u_d = np.zeros(args.nt)
u_d_analytic = []
for i in range(args.nt):
    u_d_analytic.append(tf.expand_dims(kalecki_analytic_inst(t[i]-args.theta), axis=1))
u_d_analytic = tf.concat(u_d_analytic, axis=0)
print("u d analitica", u_d_analytic)

for i in range(args.nt):
    u_d[i] = u_d_analytic.numpy()[i, 0]

u_d_df = pd.DataFrame(u_d)
u_d_df.to_csv('datasets_2\\u_d.csv', index=False, header=False)


#compute the analytic derivative of the solution
#kalecki_analytic_deriv_inst = kalecki_deriv_eqn_analy(args)
#du_analytic = []
#for i in range(args.nt):
 #   du_analytic.append(tf.expand_dims(kalecki_analytic_deriv_inst(t[i]), axis=1))
#du_analytic = tf.concat(du_analytic, axis=0)
#print("du analitica", du_analytic)

#du_analytic_vector = np.zeros(args.nt)
#for i in range(args.nt):
 #   du_analytic_vector[i] = du_analytic.numpy()[i, 0]

#compute distance between du_dt analityc and finite difference du_dt
#plt.scatter(du_dt, du_analytic_vector)
#plt.show()



