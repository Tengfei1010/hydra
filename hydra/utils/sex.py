# _*_ coding: utf-8 _*_
# This project is fllowing Pedram Amini's sulley, the core part is sully,
#  some part overwrite by me.
# See detail sulley form https://github.com/OpenRCE/sulley
# If there is a problem, please contact tutengfei.kevin@gmail.com
# Thank you!
"""
@the first author: Pedram Amini
@the second author: tutengfei.kevin
@contact: tutengfei.kevin@gmail.com
@source: https://github.com/tutengfei/hydra
"""


class Error(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
