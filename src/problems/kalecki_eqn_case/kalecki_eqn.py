import numpy as np
import tensorflow as tf

from solver.findiff_general import solver_arguments
from solver.findiff_solver import fd_solve

########################################################
"""
Common along with testcase specific arguments
"""


class kalecki_args(solver_arguments):

    def __init__(self, T, nt, T_start=0., l=0.4, theta=1, c=0.75, v=0.5,  dleft_bv_dt=0, dright_bv_dt=0, dbc_l=1,
                 nbc_l=0, dbc_r=1, nbc_r=0, max_deriv=1, acc=2, acc_advec=1):
        solver_arguments.__init__(self, T=T, nt=nt, T_start=T_start)

        self.l = l
        self.theta = theta
        self.v = v
        self.c = c
        self.a = self.l * self.v / (self.theta * (1 - self.c))
        self.b = self.l * (1 + self.v / (self.theta * (1 - self.c)))

        #self.state_dim = Nx

        self.dleft_bv_dt = dleft_bv_dt
        self.dright_bv_dt = dright_bv_dt
        self.dbc_l = dbc_l
        self.nbc_l = nbc_l
        self.dbc_r = dbc_r
        self.nbc_r = nbc_r
        self.max_deriv = max_deriv
        self.acc = acc
        self.acc_advec = acc_advec


########################################################
"""
Class containign the RHS of the PDE

Everything assumed to be in numpy
"""


class kalecki_rhs(fd_solve):

    def __init__(self, args, deriv_obj, grid_obj):
        fd_solve.__init__(self, args=args, deriv_obj=deriv_obj, grid_obj=grid_obj)

        self.full_vander_dx = self.deriv_obj.vander(self.grid.x_grid, m=1, acc=self.args.acc)
        self.full_vander_dxx = self.deriv_obj.vander(self.grid.x_grid, m=2, acc=self.args.acc)

        #         self.vander_dx = self.full_vander_dx[1:-(self.args.max_deriv - 1), ]
        #         self.vander_dxx = self.full_vander_dxx[1:-(self.args.max_deriv - 1), ]

        self.vander_dx = self.full_vander_dx[self.args.max_deriv - 1:-(self.args.max_deriv - 1), ]
        self.vander_dxx = self.full_vander_dxx[self.args.max_deriv - 1:-(self.args.max_deriv - 1), ]

        self.full_vander_dx_upwind = self.deriv_obj.upwind(self.grid.x_grid, acc=min(self.args.acc, 4))

        #         self.vander_dx_upwind = self.full_vander_dx_upwind[1:-(self.args.max_deriv - 1), ]
        self.vander_dx_upwind = self.full_vander_dx_upwind[self.args.max_deriv - 1:-(self.args.max_deriv - 1), ]

        self.vander_dx_upwind_advec = self.deriv_obj.upwind(self.grid.x_grid, acc=self.args.acc_advec)[
                                      self.args.max_deriv - 1:-(self.args.max_deriv - 1), ]

        self.full_vander = self.get_vander_matrices(self.grid.x_grid, max_deriv=args.max_deriv)

    def get_vander_matrices(self, x, max_deriv=None):

        if max_deriv == None: max_deriv = self.args.max_deriv

        A = []
        for i in range(max_deriv + 1):
            A.append(self.deriv_obj.vander(x, m=i, acc=self.args.acc))

        return A

