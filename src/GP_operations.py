from deap import gp
from sympy import Symbol, Derivative, Function, lambdify
import random
import numpy as np
import operator



def protectedDiv(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 1
    except ValueError:
        return 1


def protectedPow(a,b):
    try:
        return operator.pow(a,b)
    except ValueError:
        return 1


def compute_du_dx(u, t, x_grid):
    hx = x_grid[1]-x_grid[0]
    nt = len(t)
    nx = len(x_grid)
    du_dx = np.zeros([nt, nx])
    for i in range(nt):
        for j in range(1, nx-1):
            du_dx[i, j] = (u[i, j+1] - u[i, j-1])/(2*hx)
    return du_dx


def compute_du2_dx(u, t, x_grid):
    hx = x_grid[1] - x_grid[0]
    nt = len(t)
    nx = len(x_grid)
    du2_dx = np.zeros([nt, nx])
    for i in range(nt):
        for j in range(1, nx-1):
            du2_dx[i,j] = (u[i, j+1] - 2*u[i,j] + u[i, j-1])/(hx**2)
    return du2_dx


def compute_du3_dx(u,t,x_grid):
    hx = x_grid[1]-x_grid[0]
    nt = len(t)
    nx = len(x_grid)
    du3_dx = np.zeros([nt, nx])
    for i in range(nt):
        for j in range(2, nx-2):
            du3_dx[i,j] = (-0.5*u[i,j-2] + u[i,j-1] - u[i,j+1] + 0.5*u[i,j+2])/(hx**3)
    return du3_dx


def compute_du_dt(u, t_grid, x_grid):
    ht = t_grid[1]-t_grid[0]
    nt = len(t_grid)
    nx = len(x_grid)
    du_dt = np.zeros([nt, nx])
    for j in range(nx):
        for i in range(1, nt-1):
            du_dt[i, j] = (u[i+1, j] - u[i-1, j])/(2*ht)
    return du_dt


ht = 0.01   #questa è la distanza tra due t consecutivi del vettore tt dei tempi
def compute_ud(u, d):
    nt, nx = u.shape
    u_d = np.ones([nt, nx])
    r = int(d/ht)
    for i in range(nt):
        for j in range(nx):
            if i < r:
                u_d[i, j] = u[i, j]
            else:
                u_d[i, j] = u[i - r, j]
    return u_d


def compute_new_t(t_grid, nx):
    nt = len(t_grid)
    new_t = np.zeros([nt * nx])
    for i in range(nt*nx):
        new_t[i] = t_grid[i//nx]
    return new_t


def compute_new_x(x_grid, nt):
    nx = len(x_grid)
    new_x = np.zeros([nx*nt])
    for j in range(nt):
        for i in range(nx):
            new_x[nt*j + i] = x_grid[i]
    return new_x


def compute_new_u(u):
    nt, nx = u.shape
    new_u = np.zeros([nt*nx])
    for i in range(nt*nx):
        new_u[i] = u[i//nx, i%nx]
    return new_u



