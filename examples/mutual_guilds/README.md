# Usage

First of all, copy your application's bot token, client ID and client secret from the [Discord Developer Portal](https://discord.com/developers/applications). Don't forget to add `http://127.0.0.1:5000/callback` as redirect URL. Now, replace the placeholders  in `example.env`. You also have to set an `APP_SECRET`. Rename the `example.env` to `.env`. Finally, run `pip install -r requirements.txt`.

Now you should be able to run `python -m dashboard` and `python -m bot` without any errors.