import time
from abc import ABC, abstractmethod
import pydirectinput, win32gui, win32con

# ──────────────────────────────────────────────────────────────────────────────
class CharacterBase(ABC):
    """Base class storing bar percentages instead of raw numbers."""
    def __init__(self, name: str):
        self.name  = name
        self.hp    = 1.0  # 0-1 float
        self.mp    = 1.0
        self.fp    = 1.0
        self.exp   = 0.0  # 0-100 %

    # simple getters
    def hp_pct(self) -> float: return self.hp
    def mp_pct(self) -> float: return self.mp
    def fp_pct(self) -> float: return self.fp

    # keyboard helpers --------------------------------------------------------
    def press_key(self, key: str):
        pydirectinput.press(key)

    def action_slot(self, slot: int):
        if 1 <= slot <= 9:
            self.press_key(str(slot))

    # subclasses decide what to do each tick ----------------------------------
    @abstractmethod
    def tick(self): ...

# ──────────────────────────────────────────────────────────────────────────────
class MainChar(CharacterBase):
    """DPS / tanker"""
    def __init__(self, name: str, pickup_key: str = '0', window_title: str | None = None):
        super().__init__(name)
        self.pickup_key = pickup_key
        self.window_title = window_title
        self._hwnd = None
        self.can_pick_objects = False
        self.last_pickup = 0
        self.pickup_cooldown = 0.5

    def press_key(self, key: str):
        if self.window_title:
            if self._hwnd is None:
                self._hwnd = self._find_window(self.window_title)
            if self._hwnd:
                try:
                    win32gui.SetForegroundWindow(self._hwnd)
                    time.sleep(0.05)
                except Exception:
                    self._hwnd = None
        super().press_key(key)

    @staticmethod
    def _find_window(partial_title: str):
        handle = None
        def cb(hwnd, _):
            nonlocal handle
            if win32gui.IsWindowVisible(hwnd):
                if partial_title.lower() in win32gui.GetWindowText(hwnd).lower():
                    handle = hwnd
        win32gui.EnumWindows(cb, None)
        return handle

    def tick(self):
        if self.can_pick_objects and time.time() - self.last_pickup > self.pickup_cooldown:
            self.press_key(self.pickup_key)
            self.last_pickup = time.time()


# ──────────────────────────────────────────────────────────────────────────────
class Healer(CharacterBase):
    def __init__(self, name: str, heal_slot: int = 1, buff_slot: str = 'c', window_title: str | None = None):
        super().__init__(name)
        self.heal_slot = heal_slot
        self.buff_slot = buff_slot
        self.window_title = window_title
        self._hwnd = None
        self._last_heal = 0
        self.last_buff = 0
        self.cooldown = 2.0  # seconds
        self.buff_cooldown = 420    # (7 minutes)

    def press_key(self, key: str):
        if self.window_title:
            if self._hwnd is None:
                self._hwnd = self._find_window(self.window_title)
            if self._hwnd:
                try:
                    win32gui.SetForegroundWindow(self._hwnd)
                    time.sleep(0.05)
                except Exception:
                    self._hwnd = None
        super().press_key(key)

    def heal(self):
        now = time.time()
        if now - self._last_heal > self.cooldown:
            self.press_key(str(self.heal_slot))
            self._last_heal = now

    def buff_main(self):
        now = time.time()
        if now - self.last_buff > self.buff_cooldown:
            self.press_key(str(7))
            self.press_key(str(self.buff_slot))
            self.last_buff = now

    @staticmethod
    def _find_window(partial_title: str):
        handle = None
        def cb(hwnd, _):
            nonlocal handle
            if win32gui.IsWindowVisible(hwnd):
                if partial_title.lower() in win32gui.GetWindowText(hwnd).lower():
                    handle = hwnd
        win32gui.EnumWindows(cb, None)
        return handle

    def tick(self): pass
