

from flask import Flask,render_template



params = {} 
app = Flask(__name__)

def execute_python_code():
    
    
    from PIL import Image
    import pytesseract
    import pyautogui
    import speech_recognition as sr
    import pyttsx3 as py
    import os
    import time
    import cv2
    import subprocess
    import concurrent.futures
    import win32gui
    import keyboard
    import threading
    from difflib import get_close_matches
    import inside_features_of_yt as yt 
    import feedback
    import nltk
    from textblob import TextBlob
    import itertools
    import re
    import queue
    import os
    import shutil
    import pygetwindow as gw

    

    def image_noise_reduction(image_path):
        image = cv2.imread(image_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY)
        denoised_image = cv2.fastNlMeansDenoising(binary_image, None, h=10, templateWindowSize=7, searchWindowSize=21)
        preprocessed_image = Image.fromarray(denoised_image)
        return preprocessed_image
    
    def check_percentage(prompt, dest):
        print(dest)
        matched_words = [word for word in prompt if word in dest]
        print('matched words', matched_words)
        percentage = (len(matched_words)/len(prompt))*100
        return round(percentage,1)


    def find_text_and_move_cursor(image_path, text, desired_text):
        try:
            img = image_noise_reduction(image_path)
        except FileNotFoundError:
            voice_assistant(f"Error: File not found at {image_path}")
            print(f"Error: File not found at {image_path}")
            return None

        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        
        results = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        print('text', text)
        if isinstance(text, str):
            text = text.strip()
            word_list = text.split()
        else:
            word_list = text
        word_list = [word.capitalize() for word in word_list]
        seen = sorted(set(word_list), key=word_list.index)
        print(seen)
        print("word list:", word_list)
        try:
            close_words = [get_close_matches(word, results['text'], cutoff=0.7) for word in word_list]
        except IndexError:
            return 'text not found on screen'
        print('close matches:', close_words)
        close_words = [sublist for sublist in close_words if sublist]
        combination_of_close_words = set(itertools.product(*close_words))
        print('combinations', combination_of_close_words)
        if close_words == []:
            return "text not found on screen"
        for i, close_word in enumerate(close_words[0]):
            index = results['text'].index(close_word)
            wordl = [re.sub(r"[^a-zA-Z0-9]", "", results['text'][j]) for j in range(index, len(word_list) + index)]
            print("wordl", wordl)
            percentage = check_percentage(wordl, list(list(combination_of_close_words)[i]))
            print('percentage', percentage)
            if percentage >= 50:
                x, y, w, h = results['left'][index], results['top'][index], results['width'][index], results['height'][index]
                center_x, center_y = x + w // 2, y + h // 2

                print(f"Desired text '{desired_text}' found at center coordinates ({center_x}, {center_y})!")

                if center_y <= 150:
                    print("moving")
                    pyautogui.moveTo(center_x, center_y, duration=0.5)
                    voice_assistant('here we go...')
                    pyautogui.leftClick()
                    return 'success'
                else:
                    print("moving 2")
                    pyautogui.moveTo(center_x, center_y, duration=0.5)
                    cursor_type = win32gui.GetCursorInfo()
                    print("cursor type", cursor_type[1], cursor_type)
                    if cursor_type[1] == 65567:  # cursor type is pointer
                        voice_assistant('here we go...')
                        pyautogui.leftClick()
                        time.sleep(1)
                        return 'success'
                    else:
                        return 'text not found on screen'

        return "text not found on screen"


    def voice_assistant(text):
        engine1 = py.init()
        engine1.say(text)
        engine1.runAndWait()

    def listen_for_command(text):

        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            voice_assistant(text)
            audio = recognizer.listen(source)

        try:
            recognized_text = recognizer.recognize_google(audio)
            voice_assistant(f"You said {recognized_text}")
            print(f"Recognized button name: {recognized_text}")
            return recognized_text
        except sr.UnknownValueError:
            # voice_assistant("Say again, please...")
            print("Speech Recognition could not understand audio")
            return 1
        except sr.RequestError as e:
            voice_assistant(f"Could not request results from Google Speech Recognition service; {e}")
            print(f"Could not request results from Google Speech Recognition service; {e}")

    def input_processing(text):
        stopwords = nltk.corpus.stopwords.words('english')
        blob = TextBlob(text)
        words = blob.words
        keywords = [word for word in words if word.lower() not in stopwords]
        return keywords
    def get_window_title():
        active_window = gw.getActiveWindow()
        title = active_window.title
        title = title.split('-')
        title = [word.strip() for word in title]
        return title


    def find_button_name(text):
        keywords = input_processing(text)
        keywords = [item.lower() for item in keywords]
        print(keywords)
        if any(item.lower() in ['click', 'open', 'press'] for item in keywords) and any(
                item1 in ['button', 'option', 'app'] for item1 in keywords):
            bt = [i for i in keywords if i in ['click', 'open', 'press', 'Click', 'Open', 'Press']]
            bt1 = [i for i in keywords if i in ['button', 'option', 'app']]
            start = keywords.index(bt[0])
            end = keywords.index(bt1[0])
            s = " ".join(keywords[start + 1:end])
            return s
        elif any(item in ['click', 'open', 'press', 'Click', 'Open', 'Press'] for item in keywords) and any(
                item1 in ['button', 'option', 'app'] for item1 in keywords) == False:
            bt = [i for i in keywords if i in ['click', 'open', 'press', 'Click', 'Open', 'Press']]
            start = keywords.index(bt[0])
            s = " ".join(keywords[start + 1:])
            return s
        elif ('close' in keywords) or ('minimise' in keywords):
            close_app(keywords)
            return 'closed'
        else:
            return keywords


    def close_app(keywords):
        if set(['close', 'window']).issubset(keywords) or set(['close', 'app']).issubset(keywords) or set(['close', 'browser']).issubset(keywords):
            pyautogui.hotkey('alt', 'f4')
            
        elif set(['minimise', 'window']).issubset(keywords) or set(['minimise', 'app']).issubset(keywords) or set(['minimise', 'browser']).issubset(keywords):
            pyautogui.hotkey('win', 'm')
        elif set(['maximize', 'window']).issubset(keywords) or set(['maximize', 'app']).issubset(keywords) or set(['maximize', 'browser']).issubset(keywords):
            pyautogui.hotkey('win', 'shift', 'up')
        elif set(['close', 'tab']).issubset(keywords):
            print("cureent tab is closing...")
            pyautogui.hotkey('ctrl', 'w')
        elif set(['create', 'tab']).issubset(keywords) or set(['create', 'new', 'tab']).issubset(keywords) :
            pyautogui.hotkey('ctrl', 't')
        elif 'close' in keywords:
            keywords.remove('close')
            print(get_window_title())
            print(get_close_matches(keywords[keywords.index('close')+1], get_window_title(), cutoff=0.5))
            try:
                if any(word for word in keywords if get_close_matches(word, get_window_title(), cutoff=0.5)[0] in get_window_title()):
                    pyautogui.hotkey('ctrl', 'w')
            except:
                return
            


    def open_app(app_name):
        # Check if the application executable exists
        if shutil.which(app_name) is None:
            print(f"Error: {app_name} not found on the system.")
            return False
        
        try:
            process = subprocess.Popen(["start", "", f"{app_name}"], shell=True)
            # Check if the process has been successfully created
            if process.poll() is None:
                return True  # Application started successfully
            else:
                return False  # Application failed to start
        except Exception as e:
            print(f"Error opening {app_name}: {e}")
            return False  # Error occurred while opening the application


    def open_file_explorer():
        try:
            os.system("explorer")
        except Exception as e:
            print(f"Error opening File Explorer: {e}")


    def open_apps_in_browser(app_name):
        try:
            subprocess.Popen(["start", "", "chrome", f"https://www.{app_name}.com/"], shell=True)
        except Exception as e:
            print(f"Error opening {app_name} in browser: {e}")


    def open_whatsapp_in_browser():
        try:
            subprocess.Popen(["start", "", "chrome", "https://web.whatsapp.com/"], shell=True)
        except Exception as e:
            print(f"Error opening whatsapp in browser: {e}")


    def open_all_apps(app_name):
        apps = feedback.load_apps()
        if app_name in ['file manager', 'file explorer', "files"]:
            open_file_explorer()
            time.sleep(5)
            return
        elif app_name == 'whatsapp':
            open_whatsapp_in_browser()
            time.sleep(5)
            return
        elif open_app(app_name):
            pyautogui.hotkey('win', 'up')
            time.sleep(5)
            return
        
        else:
            if app_name.lower() in apps:
                open_apps_in_browser(app_name)
                print('open open_apps_in_browser function')
                time.sleep(5)
                return
            else:
                user_input= listen_for_command("you didn't mention whether it's app or button name...please say whether it's app or button")
                if user_input == None:
                    return
                elif 'app' in user_input:
                    feedback.update_apps(app_name, apps)
                    open_apps_in_browser(app_name)
                    time.sleep(5)
                    return
                elif 'button' in user_input:
                    voice_assistant("i can't dind button name, say again...")
                    return
                else:
                    search('google', app_name)
                    return

                    
    def control_screen(image_path, text, desired_text):
        print("initial desired text: ", text)
        result = find_text_and_move_cursor(image_path, text, desired_text)
        desired_list = [i.lower() for i in (desired_text.split())]
        print("desired text: ", desired_text)
        print('result:', result)
        if result == 'success':
            return
        elif result == "text not found on screen" and 'open' in desired_list:
            result = open_all_apps(text)
            print("open all apps function")
            if result == None:
                return None
        elif result == "text not found on screen": 
            voice_assistant("i can't find button name, say again")
            return None


    def pause():
        while True:
            if keyboard.read_key() == 'space':
                break
        return
    
    def switch(desired_text):
        if 'tab' in desired_text:
            pyautogui.hotkey('ctrl', 'tab')
        else:
            pyautogui.hotkey('alt', 'tab')


    def inside_features_of_app(image_path, desired_text):
        if desired_text != None:
            keys = input_processing(desired_text)
            print("keys", keys)
            if 'open' in desired_text or 'click' in desired_text or 'press' in desired_text or 'play' in desired_text:
                if 'play' in desired_text:
                    if 'video' in desired_text:
                        if keys.index('play')+1 != keys.index('video'):
                            desired_text = desired_text.replace('play', 'open')
                            print("desired_text", desired_text)
                        else:
                            pyautogui.press('k')
                    elif 'movie' in desired_text:
                        desired_text = desired_text.replace('play', 'open')
                        print("desired_text", desired_text)
                if 'movie' in desired_text or 'video' in desired_text:
                    if 'movie' in desired_text:
                        desired_text = desired_text.replace('movie', "")
                    elif 'video' in desired_text:
                        if keys.index('play')+1 != keys.index('video'):
                            desired_text = desired_text.replace('video', "")   
                        else:
                            pyautogui.press('k')
                text = find_button_name(desired_text)
                results = find_text_and_move_cursor(image_path, text, desired_text)
                if results == 'text not found on screen':
                    print("running app",get_window_title()[-2])
                    if "Google Chrome" in get_window_title():
                        if get_window_title()[-2].split()[-1].lower() in ['youtube', 'hotstar', 'netflix']:
                            print('open youtube features')
                            yt.youtube(keys)
            elif 'switch' in desired_text:
                switch(desired_text)
            else:
                print("running app",  get_window_title()[-2].lower())
                print("running app",  get_window_title()[-2].lower())
                if get_window_title()[-2].split()[-1].lower() in ['youtube', 'hotstar', 'netflix']:
                    yt.youtube(keys)
                    print('open youtube features')
                    


    def search(app_name, ind, query):
        global params
        print(params)
        app_name = app_name.split()[-1].lower()
        if ind == 1:
            if not app_name in params:
                return
            if app_name == 'hotstar':
                subprocess.Popen(["start", "", "chrome", f"https://www.{app_name}.com/{params[app_name][0]}?{params[app_name][1]}=" + query.replace(' ', '+')], shell=True)
                time.sleep(0.5)
                pyautogui.write(query.replace(' ', '+'))
                pyautogui.press('enter')
                return 
            
            pyautogui.hotkey('ctrl', 'k')
            pyautogui.press('backspace')
            time.sleep(0.5)
            pyautogui.write(f"https://www.{app_name}.com/{params[app_name][0]}?{params[app_name][1]}=" + query.replace(' ', '+'))
            pyautogui.press('enter')
        else:
            if app_name == 'chrome':
                app_name = 'google'
            if app_name in list(params.keys()):
                subprocess.Popen(["start", "", "chrome", f"https://www.{app_name}.com/{params[app_name][0]}?{params[app_name][1]}=" + query.replace(' ', '+')], shell=True)


    def scroll_down(stop_scroll_event):
        print("Scrolling thread started.")
        while not stop_scroll_event.is_set():
            pyautogui.scroll(-100)
            time.sleep(0.5)


    def scroll_up(stop_scroll_event):
        print("Scrolling thread started.")
        while not stop_scroll_event.is_set():
            pyautogui.scroll(100)
            time.sleep(0.5)

    def listen_for_stop_command(stop_listen_event, stop_scroll_event):
        print("Listening for voice command to stop scrolling...")
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            while not stop_listen_event.is_set():
                try:
                    audio = recognizer.listen(source, timeout=5)
                    command = recognizer.recognize_google(audio).lower()

                    if 'stop' in command:
                        print("Stopping scrolling...")
                        stop_scroll_event.set()
                        stop_listen_event.set()

                except sr.WaitTimeoutError:
                    print("No voice input detected. Listening for voice command...")
                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    print(f"Error with the speech recognition service: {e}")



    def scroll(desired_text):
        stop_scroll_event = threading.Event()
        stop_listen_event = threading.Event()
        if 'scroll down' in desired_text.lower():
            scrolling_thread = threading.Thread(target=scroll_down, args=(stop_scroll_event, ))
            listening_thread = threading.Thread(target=listen_for_stop_command, args=(stop_listen_event, stop_scroll_event))
            print("Starting scrolling and listening threads...")
            scrolling_thread.start()
            listening_thread.start()
            scrolling_thread.join()
            listening_thread.join()
            print("Main thread exiting.")
        elif 'scroll up' in desired_text.lower():
            scrolling_thread = threading.Thread(target=scroll_up, args=(stop_scroll_event, ))
            listening_thread = threading.Thread(target=listen_for_stop_command, args=(stop_listen_event, stop_scroll_event))
            print("Starting scrolling and listening threads...")
            scrolling_thread.start()
            listening_thread.start()
            scrolling_thread.join()
            listening_thread.join()
            print("Main thread exiting.")


    def main():
        global params 
        params = {'google': ['search', 'q'],
                'youtube': ['results', 'search_query'],
                'netflix': ['search', 'q'],
                'hotstar': ['in/explore', 'search_query']}
        voice_assistant('hii, i am eva')
        desired_text = ""
        text1 = ""
        while True:
            if desired_text != 1:
                text1 = "What do you want"
            desired_text = listen_for_command(text1)
            if desired_text == 1:
                text1 = "Say again please"
                continue
            print('desired text ', desired_text)
            if 'shut your mouth' in desired_text or 'close your self' in desired_text or 'close yourself' in desired_text:
                voice_assistant("i am shutting off...")
                print("i am shut off...")
                break
            elif desired_text == None:
                print("ufff...")
                continue
            elif 'button' in desired_text:
                keyword = find_button_name(desired_text)
                print("keywords: ", keyword)
                sc = pyautogui.screenshot()
                sc.save('vs.png')
                image_path = "vs.png"
                if keyword == 'closed':
                    continue
                result = find_text_and_move_cursor(image_path, keyword, desired_text)
                if result == 'text not found on screen':
                    voice_assistant("I can't see that button.")
                    continue
            elif 'app' in desired_text:
                keyword = find_button_name(desired_text)
                print("keywords: ", keyword)
                if keyword == 'closed':
                    continue
                open_all_apps(keyword)
            elif 'wait' in desired_text or 'Wait' in desired_text:
                voice_assistant("so I will wait for you until you press space bar to continue")
                pause()
                continue
            elif 'type' in desired_text:
                if 'dot' in desired_text:
                    desired_text = desired_text.replace('dot', '.')
                pyautogui.write(desired_text.replace('type', ""))
                pyautogui.press('enter')
            elif 'write' in desired_text:
                if 'dot' in desired_text:
                    desired_text = desired_text.replace('dot', '.')
                pyautogui.write(desired_text.replace('type', ""))
            elif 'search' in desired_text or 'Search' in desired_text:
                current_app = get_window_title()
                query = desired_text.strip()
                lst = query.split()
                if 'in' in lst:
                    ind = lst.index('in')
                    app_name = lst[ind+1]
                    search(app_name,0, query)
                else:
                    if 'Google Chrome' in current_app:
                        search(current_app[-2], 1, query)
                    else:
                        search('google', 0, query)
            elif 'scroll' in desired_text.lower():
                scroll(desired_text)
            elif desired_text != None:
                keyword = find_button_name(desired_text)
                print("keywords: ", keyword)
                sc = pyautogui.screenshot()
                sc.save('vs.png')
                image_path = "vs.png"
                if keyword == 'closed':
                    continue
                if 'button' in desired_text:
                    result = find_text_and_move_cursor(image_path, keyword, desired_text)
                    if result == 'text not found on screen':
                        voice_assistant("I can't see that button.")
                        continue
                elif 'app' in desired_text:
                    open_all_apps(keyword)
                elif ('open' not in desired_text) and ('press' not in desired_text) and ('click' not in desired_text):
                    print('open features')
                    inside_features_of_app(image_path, desired_text)
                else:
                    print("open all apps")
                    control_screen(image_path, keyword, desired_text)


    main()



    
    print('Python code executed!')
    return 'Python code executed successfully', 200

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute_endpoint():
    return execute_python_code()

if __name__ == '__main__':
    app.run(debug=True)




















