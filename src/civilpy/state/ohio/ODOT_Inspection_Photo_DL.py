import requests

from io import BytesIO
from PIL import Image
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
import json
import tkinter as tk
from tkinter import messagebox

# Define the path for the secrets.json file in the user's AppData\Local directory
civilpy_dir = os.path.join(os.getenv("LOCALAPPDATA"), "Civilpy")  # E.g., C:\Users\<Username>\AppData\Local\Civilpy
secrets_file = os.path.join(civilpy_dir, "secrets.json")

def download_assetwise_photos(asset_sfn, target_folder):
    driver, wait = assetwise_authentication(asset_sfn, target_folder)
    # Finish the login process, a users natural instinct is to click the login button after the captcha
    try:
        sign_in_button = driver.find_element(By.ID, 'ContentPlaceHolder1_cmdSubmit')
        sign_in_button.click()
    except:
        pass

    input_element = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "iui-input"))
    )

    input_element.send_keys(asset_sfn)

    link_element = wait.until(
        EC.presence_of_element_located((By.XPATH, "//li[@class='iui-menu-item ']/a"))
    )
    href_value = link_element.get_attribute("href")
    print(f"Navigating to link: {href_value}")

    driver.get(href_value)

    file_tab = wait.until(
        EC.presence_of_element_located((By.XPATH, "//span[text()='Files']"))
    )
    file_tab.click()

    # Wait until the pagination container shows up
    wait = WebDriverWait(driver, 2)
    pagination_container = wait.until(
        EC.presence_of_element_located((By.ID, "divLinks"))
    )

    # This part of the code navigates the photos and downloads them, it could use some work and splitting out
    # A list to store all image links
    all_image_links = []

    def extract_image_links():
        """Optimized function to extract all image links on the page."""
        images = driver.find_elements(By.XPATH,
                                      "//div[@id='ctl01_ContentPlaceHolder1_fileMgr_rptFileTypes_ctl00_ft_container_FileRepeater']//img")
        return [img.get_attribute("datasrc") or img.get_attribute("src") for img in images]

    while True:
        # Extract image links from the current page
        all_image_links.extend(extract_image_links())

        # Check if the "Next" button exists and is clickable
        try:
            next_button = wait.until(EC.element_to_be_clickable((By.ID, "lnkNext")))
            next_button.click()

            # Wait for the page container to reload
            wait.until(EC.invisibility_of_element_located((By.ID, "divLoadingSpinner")))
        except Exception:
            print("No more pages.")
            break

    print(f"Total image links collected: {len(all_image_links)}")

    all_image_links = list(set(all_image_links))

    # Download the images to the specified folder
    for i, url in enumerate(all_image_links):
        # Correct the URL to download
        url = url.replace('~', 'https://ohiodot-it.bentley.com')
        url = url.replace('displaythumb', 'displayfile')

        # Wait until the <img> is available
        image_element = driver.find_element(By.TAG_NAME, "img")

        # Get the `src` attribute from the <img> tag
        image_src = image_element.get_attribute("src")

        # Obtain session id from Selenium cookies
        selenium_cookies = driver.get_cookies()
        cookies = {cookie['name']: cookie['value'] for cookie in selenium_cookies}

        # User agent must match user agent used to create session
        user_agent = driver.execute_script("return navigator.userAgent;")
        headers = {'User-Agent': user_agent}

        response = requests.get(url, cookies=cookies, headers=headers)
        image_data = BytesIO(response.content)
        image = Image.open(image_data)
        file_path = Path(target_folder) / f'image{i + 1}.jpg'
        image.save(file_path)
        print(f"Downloaded {file_path} successfully")

def download_assetwise_inspections(asset_sfn, target_folder):
    pass

# assetwise_authentication function
def assetwise_authentication(asset_sfn, target_folder):
    with open(f'{civilpy_dir}/secrets.json', 'r') as f:
        data = json.load(f)
    driver = webdriver.Chrome()
    driver.get("https://ohiodot-it.bentley.com")
    wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "showLocal")))
    login_button.click()
    WebDriverWait(driver, timeout=5).until(lambda d: d.find_element(By.ID, 'ContentPlaceHolder1_txtUserName'))
    driver.find_element(By.ID, 'ContentPlaceHolder1_txtUserName').send_keys(data['AW_USERNAME'])
    driver.find_element(By.ID, 'ContentPlaceHolder1_txtPassword').send_keys(data['AW_PASSWORD'])

    messagebox.showinfo("Captcha", "Please finishing solving the captcha in the chrome window")

    return driver, wait

# Function to check and create secrets.json
def credential_manager():
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if not username:
        messagebox.showerror("Error", "Username is required!")
        return

    # Ensure the directory exists
    os.makedirs(civilpy_dir, exist_ok=True)

    # Save credentials based on toggle checkbox
    secrets = {"AW_USERNAME": username}
    if not pw_toggle.get():  # If the "Do not store my PW locally" option is NOT checked
        if not password:
            messagebox.showerror("Error", "Password is required!")
            return
        secrets["AW_PASSWORD"] = password  # Store the password

    # Save the secrets to a JSON file
    try:
        with open(secrets_file, "w") as file:
            json.dump(secrets, file)
        if pw_toggle.get():
            messagebox.showinfo(
                "Success",
                f"Username saved (without password) to {secrets_file}",
            )
        else:
            messagebox.showinfo("Success", f"Credentials saved to {secrets_file}")
        root.destroy()  # Close the credentials entry GUI
        open_download_window()  # Open the next window
    except Exception as e:
        messagebox.showerror("Error", f"Could not save the file: {e}")

# Function to open the second window with text boxes and panes
def open_download_window():
    download_window = tk.Tk()
    download_window.title("Download Options")
    download_window.geometry("400x400")  # Adjust the window size

    # Asset SFN input section
    label_sfn = tk.Label(download_window, text="Enter Asset SFN:", font=("Arial", 12))
    label_sfn.pack(pady=5)
    asset_sfn_entry = tk.Entry(download_window, width=40)
    asset_sfn_entry.pack(pady=5)

    # Target Folder input section
    label_folder = tk.Label(download_window, text="Target Folder for Download:", font=("Arial", 12))
    label_folder.pack(pady=5)
    target_folder_entry = tk.Entry(download_window, width=40)
    target_folder_entry.pack(pady=5)

    # Frame for the two panes
    pane_frame = tk.Frame(download_window)
    pane_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Pane for "Download Inspection"
    inspection_pane = tk.LabelFrame(pane_frame, text="Download Inspection", padx=10, pady=10)
    inspection_pane.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    inspect_button = tk.Button(
        inspection_pane, text="Download", width=15,
        command=lambda: trigger_assetwise_authentication("Inspection", asset_sfn_entry.get(), target_folder_entry.get())
    )
    inspect_button.pack(pady=10)

    # Pane for "Download Photos"
    photos_pane = tk.LabelFrame(pane_frame, text="Download Photos", padx=10, pady=10)
    photos_pane.pack(side="right", fill="both", expand=True, padx=5, pady=5)
    photos_button = tk.Button(
        photos_pane, text="Download", width=15,
        command=lambda: download_assetwise_photos(asset_sfn_entry.get(), target_folder_entry.get())
    )
    photos_button.pack(pady=10)

    download_window.mainloop()

# Check if secrets.json already exists
if os.path.exists(secrets_file):
    # If the file exists, immediately open the second window
    print(f"'secrets.json' already exists in {secrets_file}.")
    open_download_window()
else:
    # Create the GUI window for entering credentials
    root = tk.Tk()
    root.title("Store Credentials")
    root.geometry("400x250")  # Set window size

    # Create a label frame for credentials entry
    frame = tk.LabelFrame(root, text="Enter your credentials", padx=10, pady=10)
    frame.pack(padx=10, pady=10, fill="both", expand=True)

    # Username entry
    username_label = tk.Label(frame, text="Username:")
    username_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
    username_entry = tk.Entry(frame, width=30)
    username_entry.grid(row=0, column=1, padx=10, pady=5)

    # Password entry
    password_label = tk.Label(frame, text="Password:")
    password_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
    password_entry = tk.Entry(frame, width=30, show="*")  # Use "*" for password masking
    password_entry.grid(row=1, column=1, padx=10, pady=5)

    # Toggle checkbox for storing passwords
    pw_toggle = tk.BooleanVar(value=False)  # Default is unchecked (store password)
    pw_checkbox = tk.Checkbutton(
        frame,
        text="Do not store my PW locally",
        variable=pw_toggle,
    )
    pw_checkbox.grid(row=2, column=0, columnspan=2, pady=5)

    # Save button
    save_button = tk.Button(root, text="Save", command=credential_manager, width=15)
    save_button.pack(pady=10)

    # Start the tkinter main loop
    root.mainloop()
