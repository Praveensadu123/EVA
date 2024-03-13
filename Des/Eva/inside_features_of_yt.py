import pyautogui
def youtube(desired_text):
    actions = [['play', 'video'], ['pause', 'video'], ['start', 'video'], ['stop', 'video'], ['end', 'video']]
    actions1 = [['home'], ['homepage'], ['go', 'homepage'], ['go', 'back', 'homepage'], ['minimise']]
    actions2 = [['full', 'screen'], ['maximize']]
    actions3 = [['raise', 'volume'], ['increase', 'volume'], ['raise', 'sound'], ['increase', 'sound']]
    actions4 = [['skip', 'video'], ['forward', 'video'], ['forward'], ['skip']]
    actions5 = [['backward', 'video'], ['backward']]
    print(desired_text)
    if any(set(action).issubset(desired_text) for action in actions):
        pyautogui.press('k')
        return
    elif any(set(action).issubset(desired_text) for action in actions1):
        pyautogui.press('i')
        return
    elif any(set(action).issubset(desired_text) for action in actions2):
        pyautogui.press('f')
        return
    elif any(set(action).issubset(desired_text) for action in actions4):
        ind = desired_text.index('seconds' or 'second')
        for i in range(int(desired_text[ind-1])//5):
            pyautogui.press('right')
        return
    elif any(set(action).issubset(desired_text) for action in actions5):
        if 'seconds' in desired_text or 'second' in desired_text: 
            ind = desired_text.index('seconds' or 'second')
        for i in range(int(desired_text[ind-1])//5):
            pyautogui.press('left')
        return
    elif set(['go', 'back']).issubset(desired_text):
        pyautogui.hotkey('alt', 'left')
        return
    elif 'sound' in desired_text or 'volume' in desired_text:
        if any(set(action).issubset(desired_text) for action in actions3):
            pyautogui.press('up')
            pyautogui.press('up')
            return
        else:
            pyautogui.press('down')
            pyautogui.press('down')
            return
    elif 'refresh' in desired_text or 'restart' in desired_text:
        pyautogui.hotkey('ctrl', 'r')
        return
    elif set(['close', 'youtube']).issubset(desired_text):
        print("closing youtube...")
        pyautogui.hotkey('ctrl', 'w')
    elif set(['close', 'hotstar']).issubset(desired_text):
        print("closing hotstar...")
        pyautogui.hotkey('ctrl', 'w')
    elif set(['close', 'netflix']).issubset(desired_text):
        print("closing netflix...")
        pyautogui.hotkey('ctrl', 'w')
        