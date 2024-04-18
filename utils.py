import os
import sys
from pathlib import Path
import pyrebase

config = {
  "apiKey": "VFJ3VLwCQIbttdTOnZBuMoj88OmxAsgUPx0VVCBY",
  "authDomain": "vhack-rice-rescue.firebaseapp.com",
  "databaseURL": "https://vhack-rice-rescue-default-rtdb.firebaseio.com",
  "storageBucket": "vhack-rice-rescue.appspot.com"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

import tkinter as tk  # Importing Tkinter

from mediapipe.tasks.python import audio
from matplotlib import rcParams
import matplotlib.pyplot as plt

rcParams.update({
    # Set the plot left margin so that the labels are visible.
    'figure.subplot.left': 0.3,

    # Hide the bottom toolbar.
    'toolbar': 'None'
})

class Plotter(object):
    """An util class to display the classification results."""

    _PAUSE_TIME = 0.05
    """Time for matplotlib to wait for UI event."""

    def __init__(self) -> None:
        fig, self._axes = plt.subplots()
        fig.canvas.manager.set_window_title('Audio classification')

        # Stop the program when the ESC key is pressed.
        def event_callback(event):
            if event.key == 'escape':
                sys.exit(0)

        fig.canvas.mpl_connect('key_press_event', event_callback)

        plt.show(block=False)

    def plot(self, result: audio.AudioClassifierResult) -> None:
      """Plot the audio classification result.
      Args:
      result: Classification results returned by an audio classification
          model.
      """
      # Clear the axes
      self._axes.cla()
      self._axes.set_title('Press ESC to exit.')
      self._axes.set_xlim((0, 1))

      # Plot the results so that the most probable category comes at the top.
      classification = result.classifications[0]
      label_list = [category.category_name
                  for category in classification.categories]
      score_list = [category.score for category in classification.categories]


      # Check if "Cat" category is in the classification results
      print("Hello")
      flag = True
      if "Background Noise" in label_list:
          background_index = label_list.index("Backgrond Noise")
          background_score = score_list[background_index]
          if background_score > 0.8:
              print("Diam je yak yak ke")
      if "Bird" in label_list:
          bird_index = label_list.index("Bird")
          bird_score = score_list[bird_index]
          if bird_score > 0.8:
              data={
                  "bird" : True
              }
              print("Bebird sape yang bunyi tu")
          else:
              data={
                  "bird" : False
              }
              
      if "Grasshopper" in label_list:
          grasshopper_index = label_list.index("Grasshopper")
          grasshopper_score = score_list[grasshopper_index]
          if grasshopper_score > 0.8:
              print("Belalang kupu kupu")

      if "Rat" in label_list:
          rat_index = label_list.index("Rat")
          rat_score = score_list[rat_index]
          if rat_score > 0.8:
              print("Cit Cit")
      if "Snake" in label_list:
          snake_index = label_list.index("Snake")
          snake_score = score_list[snake_index]
          if snake_score > 0.8:
              print("SSSSSSSSSSSSSSS motherfucker")

      db.child("vhack-rice-rescue").child("1-set").set(data)
      db.child("vhack-rice-rescue").child("2-push").set(data)
              
     


      self._axes.barh(label_list[::-1], score_list[::-1])

      # Wait for the UI event.
      plt.pause(self._PAUSE_TIME)
