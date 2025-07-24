import time, cv2, numpy as np, mss, keyboard
import pytesseract
import threading
import pyautogui

from flyff_chars import MainChar, Healer

# ── characters ───────────────────────────────────────────────────────────────
main_char = MainChar("pipiRanger")
healer = Healer("pipiboy", heal_slot=1, buff_slot='c', window_title="pipiboy - Flyff Universe")

# Monster SubSystem
cooldown = 6
cooldown_until = 0

has_clicked = False
monster_hud_detected = False
in_fight = False

# ── bar rectangles on the 2560×1440 monitor (tweak if needed) ───────────────
BARS = {
    "HP":  {"left": 167, "top": 145, "width": 180, "height": 5},
    "MP":  {"left": 167, "top": 170, "width": 180, "height": 5},
    "FP":  {"left": 167, "top": 195, "width": 180, "height": 5},
    "EXP": {"left": 167, "top": 220, "width": 180, "height": 5},
}

MONSTER_HUD_BARS = {
    "HP": {"left": 1180, "top": 140, "width": 260, "height": 15},
    "MP": {"left": 1180, "top": 165, "width": 260, "height": 15},
}


def is_monster_bar_visible(rect, color, threshold=0.1):
    """Returns True if bar is considered filled."""
    with mss.mss() as sct:
        img = np.array(sct.grab(rect))
    fill = pct_from_right(img, color)
    return fill > threshold

def is_monster_hud_active():
    """Checks if both red (HP) and blue (MP) bars are visible."""
    hp_visible = is_monster_bar_visible(MONSTER_HUD_BARS["HP"], "red")
    mp_visible = is_monster_bar_visible(MONSTER_HUD_BARS["MP"], "blue")
    return hp_visible and mp_visible


# ── fill-percent helper (scan from right) ────────────────────────────────────
def pct_from_right(img, color):
    b, g, r = cv2.split(img[:, :, :3])
    if color == "red":
        mask = (r > 120) & (r > g + 40) & (r > b + 40)
    elif color == "blue":
        mask = (b > 130) & (b > g + 20) & (b > r + 20)
    elif color == "green":
        mask = (g > 130) & (g > r + 20) & (g > b + 20)
    elif color == "cyan":
        mask = (b > 170) & (g > 210) & (r < 140)
    else:
        return 0.0

    votes = np.sum(mask, axis=0) > (img.shape[0] // 2)
    empty = 0
    for v in votes[::-1]:
        if v:
            break
        empty += 1
    return 1.0 - empty / img.shape[1]


# ── async OCR monster detector ───────────────────────────────────────────────
def scan_for_enemies(target_names=None):
    global cooldown_until, has_clicked, in_fight
    SCAN_BOX = {
        "left": 100,
        "top": 300,
        "width": 1950,
        "height": 1000
    }

    with mss.mss() as sct:
        while True:
            if not in_fight:
                now = time.time()
                if now < cooldown_until:
                    time.sleep(0.1)
                    continue
                print("Ready to fight!")

                has_clicked = False

                img = np.array(sct.grab(SCAN_BOX))
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                _, thresh = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY)

                # OCR with positional info
                data = pytesseract.image_to_data(thresh, config="--psm 6", output_type=pytesseract.Output.DICT)

                for i in range(len(data["text"])):
                    text = data["text"][i].strip()
                    print(text)
                    if not text:
                        continue

                    for name in target_names or []:
                        if name.lower() in text.lower():
                            # Compute position in screen coordinates
                            x = SCAN_BOX["left"] + data["left"][i] + data["width"][i] // 2
                            y = SCAN_BOX["top"] + data["top"][i] + data["height"][i] + 50  # 30 px below text

                            print(f"\n👾 Enemy spotted: {text} — clicking at ({x}, {y})")

                            pyautogui.moveTo(x, y)
                            pyautogui.click()

                            has_clicked = True

                            break17c11
                    else:
                        continue
                    break

                time.sleep(0.3)


# ── Start OCR thread for monster detection ───────────────────────────────────
threading.Thread(
    target=scan_for_enemies,
    args=(["Rock Muscle", "Rock", "Muscle", "Bang", "Totemia", "Hobo"],),  # pass names to match
    daemon=True
).start()


with mss.mss() as sct:
    try:
        while True:

            monster_hud_detected = is_monster_hud_active()

            if monster_hud_detected and has_clicked:
                in_fight = True
                print("✅ In FIGHT — HUD appeared")
                cooldown_until = time.time() + cooldown  # ⏱ wait before scanning new targets
            else:
                print("X NOT In FIGHT — HUD disappeared")
                in_fight = False

            start = time.perf_counter()

            # grab bar slices
            bar_imgs = {k: np.array(sct.grab(rect)) for k, rect in BARS.items()}

            # update percentages
            main_char.hp  = pct_from_right(bar_imgs["HP"],  "red")
            main_char.mp  = pct_from_right(bar_imgs["MP"],  "blue")
            main_char.fp  = pct_from_right(bar_imgs["FP"],  "green")
            main_char.exp = pct_from_right(bar_imgs["EXP"], "cyan") * 100  # exp in %

            healer.mp = main_char.mp  # (use real healer MP if you capture it)

            # heal check
            if main_char.hp < 0.90:
                healer.heal()

            healer.buff_main()

            time.sleep(0.05)  # 20 FPS capture
    except KeyboardInterrupt:
        print("\nStopped.")
