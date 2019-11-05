import pyautogui
import threading
from time import sleep
from .directkeys import PressKey, ReleaseKey, W, A, S, D, F, SHIFT_L, LEFT_MOUSE, RIGHT_MOUSE, PressLeftButton, \
    ReleaseLeftButton


# pyautogui.click(980, 530)
class ControlManager:
    def __init__(self):
        self._W = 0
        self._A = 0
        self._S = 0
        self._D = 0
        self._F = 0
        self._right = 0
        self._left = 0
        self._shift = 0

    def clear(self):
        self._A = 0
        self._D = 0
        self._W = 0
        self._S = 0
        self._F = 0
        self._right = 0
        self._left = 0
        self._shift = 0

    def GoAhead(self, key_w):
        if self._W == 0 and key_w == 1:
            PressKey(W)
        if self._W == 1 and key_w == 0:
            ReleaseKey(W)
        self._W = key_w

    def GoBack(self, key_s):
        if self._S == 0 and key_s == 1:
            PressKey(S)
        if self._S == 1 and key_s == 0:
            ReleaseKey(S)
        self._S = key_s

    def TurnLeft(self, key_a):
        if self._A == 0 and key_a == 1:
            PressKey(A)
        if self._A == 1 and key_a == 0:
            ReleaseKey(A)
        self._A = key_a

    def TurnRight(self, key_d):
        if self._D == 0 and key_d == 1:
            PressKey(D)
        if self._D == 1 and key_d == 0:
            ReleaseKey(D)
        self._D = key_d

    def DoF(self, key_f):
        if self._F == 0 and key_f == 1:
            PressKey(F)
        if self._F == 1 and key_f == 0:
            ReleaseKey(F)
        self._F = key_f

    def DoShift(self, key_shift):
        if self._shift == 0 and key_shift == 1:
            PressKey(SHIFT_L)
        if self._shift == 1 and key_shift == 0:
            ReleaseKey(SHIFT_L)
        self._shift = key_shift

    def MouseLeft(self, key_left):
        if self._left == 0 and key_left == 1:
            PressLeftButton()
        if self._left == 1 and key_left == 0:
            ReleaseLeftButton()
        self._left = key_left

    def move(self, w, a, s, d, f, mouse, shift):
        self.GoAhead(w)
        self.GoBack(s)
        self.TurnLeft(a)
        self.TurnRight(d)
        self.DoF(f)
        self.DoShift(shift)
        self.MouseLeft(mouse['left'])
