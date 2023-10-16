import pyautogui
from time import sleep

for i in range(4):
    print("Starting in "+str(3-i))
    sleep(1)
"""
for i in range(1,2):
    for j in range(2):
        pyautogui.press('tab')
        pyautogui.write(str(i),interval = 0.5)
    pyautogui.press("tab")
    pyautogui.press("spacebar")
    pyautogui.press("spacebar")
     """
vals = []
for i in range(27,101):
    vals.append(str(i))
print(vals)
for val in vals:
    pyautogui.click()
    for i in range(2):     
        pyautogui.write(val,interval = 0.1)
        pyautogui.press("tab")
    pyautogui.write(" ")
    sleep(0.2)
    pyautogui.write(" ")
    pyautogui.press("tab")