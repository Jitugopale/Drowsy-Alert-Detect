from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock  # Import the Clock module for scheduling tasks
import time
import random
import pyttsx3
import os

# Initialize the text-to-speech engine
engine = pyttsx3.init()

class ToDoApp(App):
    def build(self):
        self.alert_system_running = False  # Flag to indicate if the alert system is running

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Interface elements for ToDoApp
        heading_label = Label(text='Alert System', font_size=20, bold=True)
        start_alert_button = Button(text='Start Alert System', on_press=self.start_alert_system)
        stop_alert_button = Button(text='Stop Alert System', on_press=self.stop_alert_system)

        layout.add_widget(heading_label)
        layout.add_widget(start_alert_button)
        layout.add_widget(stop_alert_button)

        return layout

    def start_alert_system(self, instance):
        if not self.alert_system_running:
            self.alert_system_running = True
            self.start_time_music = time.time()  # Record the current time when the system starts for music alerts
            self.start_time_speech = time.time()  # Record the current time when the system starts for speech alerts
            self.elapsed_time_music = 0
            self.elapsed_time_speech = 0
            self.music_folder = "sounds"
            self.alert_interval_music_seconds = 180  # Change this to the desired number of seconds for music alerts (3 minutes)
            self.alert_interval_speech_seconds = 120  # Change this to the desired number of seconds for speech alerts (2 minutes)
            Clock.schedule_interval(self.random_alert, 1)  # Schedule the random_alert function to run every second

    def stop_alert_system(self, instance):
        if self.alert_system_running:
            self.alert_system_running = False
            Clock.unschedule(self.random_alert)  # Unschedule the random_alert function

    def random_alert(self, dt):
        elapsed_time_music = time.time() - self.start_time_music
        if elapsed_time_music >= self.alert_interval_music_seconds and elapsed_time_music % self.alert_interval_music_seconds < 1:
            self.play_random_music(self.music_folder)

        elapsed_time_speech = time.time() - self.start_time_speech
        if elapsed_time_speech >= self.alert_interval_speech_seconds and elapsed_time_speech % self.alert_interval_speech_seconds < 1:
            self.display_and_speak_time(elapsed_time_speech)

    def play_random_music(self, music_folder):
        music_files = [file for file in os.listdir(music_folder) if file.endswith(('.mp4', '.wav'))]
        if music_files:
            random_music = random.choice(music_files)
            music_path = os.path.join(music_folder, random_music)
            os.system(f"start {music_path}")
        else:
            print("No music files found in the specified folder.")

    def display_and_speak_time(self, elapsed_time):
        minutes, seconds = divmod(elapsed_time, 60)
        time_str = "{:02}:{:02}".format(int(minutes), int(seconds))
        speak_message = f"You have traveled since {int(minutes)} minute{'s' if int(minutes) > 1 else ''} ago. Take some rest."
        print("Time Elapsed: {}".format(time_str))
        engine.say(speak_message)
        engine.runAndWait()

if __name__ == '__main__':
    ToDoApp().run()
