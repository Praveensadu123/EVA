
# Function to load app names from file
def load_apps():
    try:
        with open("Eva\\applist.txt", "r") as file:
            apps = file.read().splitlines()
    except FileNotFoundError:
        apps = []
    return apps

# Function to save app names to file
def save_apps(apps):
    with open("Eva\\applist.txt", "w") as file:
        for app in apps:
            file.write(app + "\n")

# Function to update app list with user feedback
def update_apps(user_feedback, apps):
    if user_feedback not in apps:
        apps.append(user_feedback)
        save_apps(apps)
        print(f"App '{user_feedback}' added successfully!")
    else:
        print("App already exists in the list.")

