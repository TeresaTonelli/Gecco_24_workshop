import math

import numpy as np
import tensorflow as tf


class kalecki_eqn_analy:

    def __init__(self, app):
        self.app = app

    def __call__(self, t):

        u = 1 - 1.56*t - 0.4 * (t**2) + 0.0533 * (t**3) + 0.0266 * (t**4)

        return tf.convert_to_tensor([u], dtype=tf.float32)


class kalecki_deriv_eqn_analy:

    def __init__(self, app):
        self.app = app

    def __call__(self, t):
         du_dt = -1.56 - 0.8*t + 0.1599*(t**2) + 0.1064*(t**3)
         return tf.convert_to_tensor([du_dt], dtype=tf.float32)