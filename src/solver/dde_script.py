import numpy as np
import scipy.integrate
import scipy.interpolate


class ddeVar:

    def __init__(self, g, tc=0):
        """ g(t) = expression of Y(t) for t<tc """

        self.g = g
        self.tc = tc
        # We must fill the interpolator with 2 points minimum

        self.interpolator = scipy.interpolate.interp1d(
            np.array([tc - 1, tc]),  # X
            np.array([self.g(tc), self.g(tc)]).T,  # Y
            kind="linear",
            bounds_error=False,
            fill_value=self.g(tc)
        )

    def update(self, t, Y):
        """ Add one new (ti,yi) to the interpolator """
        Y2 = Y if (Y.size == 1) else np.array([Y]).T
        self.interpolator = scipy.interpolate.interp1d(
            np.hstack([self.interpolator.x, [t]]),  # X
            np.hstack([self.interpolator.y, Y2]),  # Y
            kind="linear",
            bounds_error=False,
            fill_value=Y
        )

    def __call__(self, t=0):
        """ Y(t) will return the instance's value at time t """

        return self.g(t) if (t <= self.tc) else self.interpolator(t)


class dde(scipy.integrate.ode):
    """
    This class overwrites a few functions of ``scipy.integrate.ode``
    to allow for updates of the pseudo-variable Y between each
    integration step.
    """

    def __init__(self, f, jac=None):
        def f2(t, y, args):
            return f(self.Y, t, *args)

        scipy.integrate.ode.__init__(self, f2, jac)
        self.set_f_params(None)

    def integrate(self, t, step=0, relax=0):
        scipy.integrate.ode.integrate(self, t, step, relax)
        self.Y.update(self.t, self.y)
        return self.y

    def set_initial_value(self, Y):
        self.Y = Y  # !!! Y will be modified during integration
        scipy.integrate.ode.set_initial_value(self, Y(Y.tc), Y.tc)


def my_ddeint(func, g, tt, fargs=None):
    dde_ = dde(func)
    dde_.set_initial_value(ddeVar(g, tt[0]))
    dde_.set_f_params(fargs if fargs else [])
    results = [dde_.integrate(dde_.t + dt) for dt in np.diff(tt)]
    print(np.array([g(tt[0])] + results))
    return np.array([g(tt[0])] + results)