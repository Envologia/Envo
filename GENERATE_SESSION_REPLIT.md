# How to Generate a Session String with Replit (No PC Required)

If you don't have access to a PC, you can use the free online service [Replit](https://replit.com) to run the session generator script securely. Follow these steps carefully.

## 1. Create a Replit Account

1.  Go to [replit.com](https://replit.com).
2.  Click **Sign Up** and create a free account.

## 2. Create a New Python Repl

1.  Once you are logged in, click the **+ Create Repl** button.
2.  In the template search box, type `Python` and select the official Python template.
3.  Give your Repl a name, for example, `session-generator`.
4.  Click **Create Repl**.

## 3. Add the Session Generator Code

1.  In the project files you have, find and open the `session_generator.py` script.
2.  Copy the entire content of that file.
3.  In your Replit workspace, you will see a file named `main.py`. Click on it.
4.  Delete any existing code in `main.py` and paste the code you copied from `session_generator.py`.

## 4. Install the Required Library

1.  In your Replit workspace, find the **Shell** tab on the right-hand side (next to the "Console" tab).
2.  Click on the **Shell** tab. A command line terminal will appear.
3.  Type the following command and press Enter:
    ```bash
    pip install telethon
    ```
4.  Wait for the installation to complete.

## 5. Run the Script and Get Your Session String

1.  Click the big green **Run** button at the top of the Replit interface.
2.  The script will start running in the **Console** window.
3.  It will now prompt you for your credentials, one by one:
    *   `Enter your API Key:`
    *   `Enter your API Hash:`
    *   `Please enter your phone number:`
    *   `Please enter the code you received:`
    *   `Please enter your two-step verification password:` (if you have one enabled)
4.  Enter each piece of information carefully and press Enter.

Once you have successfully logged in, the script will print a long session string in the console.

**This is your session string!** Copy the entire string (it's very long and might end with an equals sign `=`). Save it somewhere safe, as you will need it to deploy your bot.

## 6. IMPORTANT: Delete the Repl

For your security, once you have your session string, you should delete the Repl to ensure your credentials are not saved online.

1.  Go back to your Replit dashboard.
2.  Find the `session-generator` Repl you created.
3.  Click the three dots (`...`) next to it and select **Delete**.
4.  Confirm the deletion.

You are now ready to proceed with the deployment!
