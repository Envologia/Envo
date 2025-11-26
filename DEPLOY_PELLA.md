# Deploying Envo Userbot to Pella.app

This guide will walk you through the process of deploying your Envo userbot to `pella.app`.

## 1. Prerequisites

Before you begin, make sure you have the following:

- A Telegram account.
- Your `API_KEY` and `API_HASH` from `my.telegram.org`.
- Your `BOT_TOKEN` from `@BotFather`.
- Your `OPENROUTER_API_KEY` from `openrouter.ai`.

## 2. Generate Your Session String

You will need a Telethon session string to run your userbot.

-   **If you have a PC**, you can generate the session string by running the `session_generator.py` script locally.
-   **If you do not have a PC**, you can use a free online service called Replit. Please follow the detailed instructions in our **[Replit Session Generation Guide](GENERATE_SESSION_REPLIT.md)**.

Once you have your session string, copy it and save it in a safe place. You will need it for the deployment.

## 3. Prepare Your Project for Upload

To deploy your bot to `pella.app`, you will need to upload your project files. The easiest way to do this is to create a zip archive of your project.

1.  **Create a Zip Archive**:
    - Make sure you are in the root directory of your project.
    - Create a zip archive of all the project files, including the `pyEnvo`, `plugins`, `assistant`, and `resources` directories, as well as the `requirements.txt`, `.env.sample`, and `startup` files.
    - **Important**: Do not include the `session_generator.py` or `envo.db` files in the zip archive.

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

## 5. Testing Your Bot

Since you are deploying without a local PC, you will test your bot once it is live on `pella.app`.

-   **Userbot**: Go to any of your Telegram chats (like "Saved Messages") and type `.ping` or `.alive`. The bot should edit the message to confirm it's running.
-   **Assistant Bot**: Find your assistant bot on Telegram and send it a `/start` command. It should reply to you.
-   **Other Features**: You can now test all the other commands we built, such as `.afk`, `.un`, `.ds`, `.wiki`, `.meme`, etc.

## 6. Troubleshooting

If you encounter any issues, check the application logs on `pella.app` for any error messages. Make sure you have set all the environment variables correctly.
