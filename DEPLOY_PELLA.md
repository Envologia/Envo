# Deploying Envo Userbot to Pella.app

This guide will walk you through the process of deploying your Envo userbot to `pella.app`.

## 1. Prerequisites

Before you begin, make sure you have the following:

- A Telegram account.
- Your `API_KEY` and `API_HASH` from `my.telegram.org`.
- Your `BOT_TOKEN` from `@BotFather`.
- A Redis database (you can get one for free from `redislabs.com`).
- Your `OPENROUTER_API_KEY` from `openrouter.ai`.
- Python and `pip` installed on your computer.

## 2. Generate Your Session String

You will need a Telethon session string to run your userbot. To generate one, follow these steps:

1.  **Install Telethon**:
    ```bash
    pip install telethon
    ```

2.  **Run the Session Generator**:
    - Run the `session_generator.py` script from the root of the project:
      ```bash
      python session_generator.py
      ```
    - The script will prompt you for your `API_KEY`, `API_HASH`, phone number, login code, and 2FA password (if you have one).
    - Once you have successfully logged in, the script will print your session string. Copy this string and save it in a safe place.

## 3. Prepare Your Project for Upload

To deploy your bot to `pella.app`, you will need to upload your project files. The easiest way to do this is to create a zip archive of your project.

1.  **Create a Zip Archive**:
    - Make sure you are in the root directory of your project.
    - Create a zip archive of all the project files, including the `pyEnvo`, `plugins`, `assistant`, and `resources` directories, as well as the `requirements.txt`, `.env.sample`, `startup`, and `docker-compose.yml` files.
    - **Important**: Do not include the `session_generator.py` script in the zip archive.

## 4. Deploy to Pella.app

Now you are ready to deploy your bot to `pella.app`.

1.  **Create an Account**:
    - Go to `pella.app` and create a new account.

2.  **Create a New Application**:
    - From your dashboard, create a new application.
    - Select the "Telegram Bot" hosting option.

3.  **Upload Your Project**:
    - Upload the zip archive you created in the previous step.

4.  **Configure Environment Variables**:
    - In your application's settings, go to the "Environment Variables" section.
    - Add the following environment variables with their corresponding values:
      - `API_KEY`
      - `API_HASH`
      - `BOT_TOKEN`
      - `SESSION` (the session string you generated earlier)
      - `REDIS_URI`
      - `REDIS_PASSWORD`
      - `OPENROUTER_API_KEY`

5.  **Set the Start Command**:
    - In your application's settings, find the "Start Command" or "Startup Command" section.
    - Set the start command to the following:
      ```bash
      ./startup
      ```

6.  **Launch Your Bot**:
    - Once you have configured everything, launch your application.
    - Your Envo userbot should now be running on `pella.app`.

## 5. Troubleshooting

If you encounter any issues, check the application logs on `pella.app` for any error messages. Make sure you have set all the environment variables correctly and that your Redis database is accessible.
