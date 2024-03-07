import tkinter as tk
from tkinter import ttk
from tkmacosx import Button as button
import requests
import constants
from math_functions import round_half_up

# Lifting page to the top
class Page(tk.Frame):
    # Main content frame
    def __init__(self):
        tk.Frame.__init__(self, bg=constants.MAIN_FRAME_COLOR)

    def show(self):
        self.lift()

# Welcome page! First page of app
class Intro(Page):
    intro_text = (
        "Here you can find recommended foods to eat for dialysis patients as well as which foods to avoid. You can also find nutrition information for individual food items of your choice with the built in API!\n"
        "\nUse the calculator to determine your daily energy and protein intake for a balanced diet.\n"
        "\nCheck out the other tabs for additional useful information that can help you consume your favorite foods in a safe way!"
    )
    # App Header
    def __init__(self):
        Page.__init__(self)
        label = tk.Label(
            self,
            text="Welcome to the Dialysis Nutrition App!",
            bg=constants.MAIN_FRAME_COLOR,
            font=("Arial", 24, "bold"),
        )
        label.pack(pady=30)

        # Border around text body and message generation
        border_frame = tk.LabelFrame(self, bg=constants.MAIN_FRAME_COLOR)
        border_frame.pack()
        message = tk.Message(
            border_frame,
            text=Intro.intro_text,
            font=("Arial", 18),
            bg=constants.MAIN_FRAME_COLOR,
        )
        message.pack(pady=20)


class Calculator(Page):
    def __init__(self):
        Page.__init__(self)
        label = tk.Label(
            self,
            text="Calculate your daily energy and protein intake requirements.",
            font=("Arial", 20),
            bg=constants.MAIN_FRAME_COLOR,
        )
        label.pack(pady=25)

        # Enter weight, label
        weight_label = tk.Label(
            self,
            text="Enter your weight in kg:",
            font=("Arial", 18),
            bg=constants.MAIN_FRAME_COLOR,
        )
        weight_label.pack(pady=10)

        # Weight entry box
        weight_entry = tk.Entry(self)
        weight_entry.pack(pady=10)

        # Weight submit button
        weight_btn = button(
            self,
            text="Submit",
            bg="#5ddeef",
            activebackground="#4285f4",
            font=("Arial", 14),
            command=lambda: self.calculated_values(weight_entry.get()),
        )
        weight_btn.pack(pady=10)

        # additional note marked with '*'
        note = tk.Label(
            self,
            text="*All numbers are rounded to the nearest ones place",
            bg=constants.MAIN_FRAME_COLOR,
        )
        note.place(relx=0.05, rely=0.9)

    def calculated_values(self, weight):
        calories = self.displaying_calories(weight)
        protein = self.displaying_protein(weight)

   # Calculates daily intake and displays them on the screen
    def calculating_calories(self, weight):
        # Converts weight into float for accurate calculation and with the help of round_half_up() function,
        # rounds the outcome to nearest ones place and returns as integer
        daily_calories = int(round_half_up(float(weight.strip().strip("kg")) * 30))
        return daily_calories

    def calculating_protein(self, weight):
        # converts weight to float and rounds to nearest ones place
        daily_protein = int(round_half_up(float(weight.strip().strip("kg")) * 1.2))
        return daily_protein

    def displaying_calories(self, weight):
        daily_calories = self.calculating_calories(weight)
        # Calorie label, but not actual calculated value in number only word
        calories = "Calories per day:"
        calories_result = tk.Label(
            self, text=calories, font=("Arial", 18), bg=constants.MAIN_FRAME_COLOR
        )
        calories_result.place(relx=0.33, rely=0.5, relwidth=0.2, relheight=0.1)

        # Unit labels
        calories_unit = tk.Label(
            self, text="kcal", font=("Arial", 18), bg=constants.MAIN_FRAME_COLOR
        )
        calories_unit.place(relx=0.545, rely=0.5, relwidth=0.2, relheight=0.1)

        # Creates StringVar for calories in order to update value with re-submission
        cal_number = tk.StringVar(value=daily_calories)
        # Automatic self updating StringVar printed to the screen (actual calculated value)
        display_calories = tk.Label(
            self,
            textvariable=cal_number,
            bg=constants.MAIN_FRAME_COLOR,
            font=("Arial", 18),
        )
        display_calories.place(relx=0.52, rely=0.5, relwidth=0.1, relheight=0.1)

    def displaying_protein(self, weight):
        daily_protein = self.calculating_protein(weight)
        # Protein label, not calculated value only 'announcement' label in word
        protein = "Protein per day:"
        protein_result = tk.Label(
            self, text=protein, font=("Arial", 18), bg=constants.MAIN_FRAME_COLOR
        )
        protein_result.place(relx=0.33, rely=0.6, relwidth=0.2, relheight=0.1)

        # Unit labels
        protein_unit = tk.Label(
            self, text="g", font=("Arial", 18), bg=constants.MAIN_FRAME_COLOR
        )
        protein_unit.place(relx=0.54, rely=0.6, relwidth=0.2, relheight=0.1)

        # Calculated value stored in string variables. Updates with re-submission
        prot_number = tk.StringVar(value=daily_protein)
        display_protein = tk.Label(
            self,
            textvariable=prot_number,
            bg=constants.MAIN_FRAME_COLOR,
            font=("Arial", 18),
        )
        display_protein.place(relx=0.52, rely=0.6, relwidth=0.1, relheight=0.1)


class Guidelines(Page):
    def __init__(self):
        Page.__init__(self)
        # Creating Notebook
        notebook = ttk.Notebook(self, width=1000, height=500)
        notebook.pack()

        # Creating each tab frame
        intake_frame = tk.Frame(
            notebook, width=900, height=500, bg=constants.MAIN_FRAME_COLOR
        )
        good_foods_frame = tk.Frame(
            notebook, width=900, height=500, bg=constants.GOOD_FOOD_COLOR
        )
        bad_foods_frame = tk.Frame(
            notebook, width=900, height=500, bg=constants.BAD_FOOD_COLOR
        )

        # Naming each tab
        frames = [intake_frame, good_foods_frame, bad_foods_frame]
        tab_names = [
            "Daily Intake",
            "Recommended Foods",
            "Foods to Avoid",
        ]
        i = 0
        for frame in frames:
            notebook.add(frame, text=tab_names[i])
            i += 1

        # Header for each tab section
        intake_title = self.tab_titles(intake_frame, "Daily Nutrition Guideline")
        good_foods_title = self.tab_titles(
            good_foods_frame,
            "Low levels of phosphorous and potassium foods",
            constants.GOOD_FOOD_COLOR,
        )
        bad_foods_title = self.tab_titles(
            bad_foods_frame,
            "High levels of phosphorous and potassium foods",
            constants.BAD_FOOD_COLOR,
        )

        # Creating a frame for each tab and its content
        # Daily Intake Tab Frames
        tab1_left = tk.Frame(intake_frame, bg=constants.MAIN_FRAME_COLOR)
        tab1_left.place(relx=0.25, rely=0.25, relwidth=0.2, relheight=0.6)
        tab1_right = tk.Frame(intake_frame, bg=constants.MAIN_FRAME_COLOR)
        tab1_right.place(relx=0.45, rely=0.25, relwidth=0.45, relheight=0.6)

        # Recommended Foods Frames
        tab2_left = self.tab_content_foods(good_foods_frame, constants.GOOD_FOOD_COLOR)
        tab2_right = self.tab_content_foods(
            good_foods_frame, constants.GOOD_FOOD_COLOR, 0.5
        )

        # Foods to Avoid Frames
        avoid_left = self.tab_content_foods(bad_foods_frame, constants.BAD_FOOD_COLOR)
        avoid_right = self.tab_content_foods(
            bad_foods_frame, constants.BAD_FOOD_COLOR, 0.5
        )

        # Defining Actual Tab Contents
        daily_left = self.daily_nutr_text(
            tab1_left, constants.DAILY_NUTR_LEFT, constants.MAIN_FRAME_COLOR, "bold"
        )
        daily_right = self.daily_nutr_text(
            tab1_right, constants.DAILY_NUTR_RIGHT, constants.MAIN_FRAME_COLOR
        )

        good_left = self.tab_body(
            tab2_left, constants.GOOD_LIST_LEFT, constants.GOOD_FOOD_COLOR
        )

        good_right = self.tab_body(
            tab2_right, constants.GOOD_LIST_RIGHT, constants.GOOD_FOOD_COLOR
        )

        bad_left = self.tab_body(
            avoid_left, constants.BAD_LIST_LEFT, constants.BAD_FOOD_COLOR
        )
        bad_right = self.tab_body(
            avoid_right, constants.BAD_LIST_RIGHT, constants.BAD_FOOD_COLOR
        )