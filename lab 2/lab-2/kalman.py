# File: kalman.py
# Source: https://github.com/vincent-rou/simple-kalman-filter
# Author: Vincent R.
# License: MIT License

class KalmanFilter:
    def __init__(self, error_est_x, error_est_y, error_mea_x):
        """
        Initialise the kalman filter
        :param error_est_x:
        :param error_est_y:
        :param error_mea_x:
        """
        # Here, error_est_x and error_est_y are analogous to the process variance (Q)
        # and error_mea_x is analogous to the measurement variance (R).
        self.err_est_x = error_est_x
        self.err_est_y = error_est_y
        self.err_mea_x = error_mea_x
        self.current_x = 0
        self.current_y = 0
        self.last_x = 0
        self.last_y = 0
        self.kalman_gain_x = 0
        self.kalman_gain_y = 0

    def get_filtered_value(self, mea_x):
        """
        Get the filtered value from the kalman filter
        :param mea_x: Mea x
        :return: Current x
        """
        # Calculate the kalman gain
        self.kalman_gain_x = self.err_est_x / (self.err_est_x + self.err_mea_x)
        # Calculate the current estimation
        self.current_x = self.last_x + self.kalman_gain_x * (mea_x - self.last_x)
        # Update the error estimation
        self.err_est_x = (1 - self.kalman_gain_x) * self.err_est_x
        # Update the last estimation
        self.last_x = self.current_x

        return self.current_x

    def get_filtered_value_y(self, mea_y):
        """
        Get the filtered value y from the kalman filter
        :param mea_y: Mea y
        :return: Current y
        """
        # Calculate the kalman gain
        self.kalman_gain_y = self.err_est_y / (self.err_est_y + self.err_mea_x)
        # Calculate the current estimation
        self.current_y = self.last_y + self.kalman_gain_y * (mea_y - self.last_y)
        # Update the error estimation
        self.err_est_y = (1 - self.kalman_gain_y) * self.err_est_y
        # Update the last estimation
        self.last_y = self.current_y

        return self.current_y