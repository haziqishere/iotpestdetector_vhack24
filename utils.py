import os
import sys
from pathlib import Path

from pymongo import MongoClient

connection_string = "mongodb+srv://kymzul27:kymzul2002@kymcluster.wllwwf2.mongodb.net/?retryWrites=true&w=majority&connectTimeoutMS=60000"
print(f"Connecting to MongoDB: {connection_string}")  # Added for debugging
client = MongoClient(connection_string)
db = client.ricerescue
collection = db.pests


import tkinter as tk
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

        cat_score = None  # Initialize cat_score before the if-elif-else chain

        # Check if "Cat" category is in the classification results
        if "Cat" in label_list:
            cat_index = label_list.index("Cat")
            cat_score = score_list[cat_index]
            if cat_score > 0.8:
                print("Cat detected!")
                data = {
                    "cat": True
                }
                collection.insert_one(data)
                print("Successfully insert database")
        
        # Check if "Bird" category is in the classification results
        elif "Bird" in label_list:
            bird_index = label_list.index("Bird")
            bird_score = score_list[bird_index]
            if bird_score > 0.8:  # Use bird_score instead of cat_score
                print("Bird detected!")
                data = {
                    "bird": True
                }
                collection.insert_one(data)
                print("Successfully alert Bird to database")
                
        # Add other conditional checks for different categories if needed...

        self._axes.barh(label_list[::-1], score_list[::-1])

        # Wait for the UI event.
        plt.pause(self._PAUSE_TIME)
