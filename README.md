# 🧠 FlyffBot – Automated OCR & Combat Assistant for Flyff Universe

FlyffBot is a lightweight automation assistant for **Flyff Universe**, built in Python. It uses **OCR, pixel color detection, and input control** to assist gameplay with:

- Real-time HP/MP/EXP monitoring  
- Auto-healing using a dedicated support character  
- Spell-based buffing  
- Intelligent monster targeting using text recognition  
- Combat state detection using monster HUD bars (red/blue)  
- Cooldown-aware target switching after monsters die  

> ⚠️ **Note**: This project is for educational use only. Use it at your own risk and with respect to Flyff Universe's terms of service.

## 📁 Features

- 🎯 Monster Detection via `pytesseract` scanning
- ❤️ Player stat tracking using pixel color bars
- 🧙 Healer class casts heals and buffs based on player's HP
- ⚔️ Monster defeat detection using HUD red/blue bars
- ⏱️ Prevents premature retargeting with cooldowns
- Automatic object pick up after defeating monster

## ⚙️ Requirements

Install Python 3.10+ and install dependencies with:


Dependencies include:
- `opencv-python`
- `pytesseract`
- `mss`
- `pyautogui`
- `pydirectinput`
- `keyboard`
- `pywin32`

## 🖥️ Setup Instructions

1. **Clone the repository**


2. **Install Tesseract OCR**

Install [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) and add it to your system PATH.  
Windows users can use Chocolatey:


Or download from: https://github.com/UB-Mannheim/tesseract/wiki

3. **Set your healer’s Flyff window title**

In `Main.py`, modify the line:

python
```healer = Healer("HealerName", heal_slot=1, buff_slot='c', window_title="HealerName - Flyff Universe")```


🔭 Roadmap
 Enemy HP decay detection (to skip unresponsive mobs)

 Adaptive healing thresholds

 Configuration GUI for setting bar regions and options

 Debug overlay with real-time parsing output

 Reference image calibration

 Buff rotation improvements

 Emergency auto-pause

Author
Pierre-Luc Marcotte
