# Instructions

## Installation
1. Install [Poetry](https://python-poetry.org/)
2. Clone the repository `git clone https://github.com/hatonlee/indolent.git`
3. Run `poetry install`

### Usage
1. Start the app: `poetry run invoke start`
2. The main window will open. Currently there are no habits.
3. Click "Add Habit" to open the New Habit View.
4. Enter the required details (name, description, start time, frequency) and click "Create".
5. The new habit will appear in the main view. On the right side you can see whether the habit is completed in the current interval.
7. Mark the habit as completed by clicking the "Complete" button next to it.
8. The habit will now show as completed for the current interval. It will reset in the next interval based on its frequency.
9. If you add enough habits, they will overflow and a scrollbar will appear. Using the mouse wheel or the scrollbar, you can scroll through the list of habits.
