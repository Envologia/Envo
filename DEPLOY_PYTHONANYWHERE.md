# Deploying Envo Userbot to PythonAnywhere

This guide will walk you through deploying your Envo userbot to [PythonAnywhere](https://www.pythonanywhere.com).

## 1. Important Note About PythonAnywhere

To run a Telegram bot 24/7, you need a task that is always running. On PythonAnywhere, this feature is called an **"Always-on task"**. This is only available on **paid plans**. The free plan is not sufficient to run a bot continuously.

## 2. Generate Your Session String

Before you start, you need your Telethon session string.

-   **If you have a PC**, run the `session_generator.py` script locally.
-   **If you do not have a PC**, follow our **[Replit Session Generation Guide](GENERATE_SESSION_REPLIT.md)** to generate your string using a free online service.

Once you have your session string, copy it and keep it safe.

## 3. Prepare Your Project for Upload

You will need to upload your project files to PythonAnywhere. The easiest way is to create a zip archive.

1.  **Create a Zip Archive**:
    *   On your device, create a zip file containing all the project files and folders.
    *   Make sure to include: `pyEnvo/`, `plugins/`, `assistant/`, `resources/`, `requirements.txt`, `.env.sample`, and `startup`.
    *   **Do not** include `session_generator.py` or `envo.db`.

## 4. Deploy to PythonAnywhere

1.  **Create an Account**:
    *   Go to [pythonanywhere.com](https://www.pythonanywhere.com) and sign up for a paid account.

2.  **Upload Your Project**:
    *   Go to the **"Files"** tab in your PythonAnywhere dashboard.
    *   Click the **"Upload a file"** button and upload the zip archive you created.
    *   Once uploaded, open a **Bash Console** from the "Consoles" tab.
    *   In the console, unzip your project:
        ```bash
        unzip your-project-name.zip
        ```
        (Replace `your-project-name.zip` with the actual name of your file).

3.  **Create a Virtual Environment**:
    *   In the same Bash console, create a virtual environment for your bot. This keeps its dependencies separate.
        ```bash
        mkvirtualenv --python=/usr/bin/python3.9 envo-bot
        ```
    *   Install the required libraries:
        ```bash
        pip install -r requirements.txt
        ```

4.  **Create Your `.env` File**:
    *   You need to create the `.env` file to store your secrets.
    *   In the Bash console, run:
        ```bash
        cp .env.sample .env
        nano .env
        ```
    *   This will open a text editor. Fill in all your credentials:
        *   `API_KEY`
        *   `API_HASH`
        *   `BOT_TOKEN`
        *   `SESSION` (your session string)
        *   `OPENROUTER_API_KEY`
    *   Press **Ctrl + X**, then **Y**, then **Enter** to save and exit.

5.  **Set Up the "Always-on Task"**:
    *   Go to the **"Tasks"** tab in your PythonAnywhere dashboard.
    *   Scroll down to the **"Always-on tasks"** section and click **"Add new Always-on task"**.
    *   In the command box, you need to enter the full path to your startup script. Your project is usually in `/home/YourUsername/your-project-directory`. The command should be:
        ```bash
        /home/YourUsername/your-project-directory/startup
        ```
        (Replace `YourUsername` and `your-project-directory` with your actual PythonAnywhere username and the folder where you unzipped your files).
    *   Click **"Add task"**.

## 6. Launch and Test Your Bot

The task will now start, and your bot will be live.

-   **Userbot**: Go to any Telegram chat and type `.ping` or `.alive` to see if it's working.
-   **Assistant Bot**: Find your assistant bot on Telegram and send it a `/start` command.

If you make any changes to your code, you will need to **reload** the Always-on task from the "Tasks" tab for the changes to take effect. You can also view the task's logs here to check for any errors.
