# File: utils/errors.py

class DiscordTokenErrors:
    @staticmethod
    def token_not_set_error():
        """
        Error raised when DISCORD_TOKEN is not set.
        """
        print("DISCORD_TOKEN is not set in either environment variables or .env file.")
        print("\nTo fix this issue, please follow these steps:")
        print("1. If you haven't already, create a .env file in your project's root directory.")
        print("2. Open the .env file and add the following line:")
        print("   DISCORD_TOKEN=your_token_here")
        print("   Replace 'your_token_here' with your actual Discord bot token.")
        print("3. To get the discord token, go to https://discord.com/developers/applications, create a new application, and create a bot.")
        print("4. Save the .env file and restart your application.")
        print("\nAlternatively, you can set the DISCORD_TOKEN environment variable directly in your environment.")
        print("This approach might be more suitable for production environments or platforms that support environment variables.")
    
    @staticmethod
    def invalid_token_error():
        """
        Error raised when the bot token is invalid.
        """
        print("The provided Discord token is invalid.")
        print("\nTo fix this issue, please follow these steps:")
        print("1. Go to https://discord.com/developers/applications, select your application, and navigate to the bot tab.")
        print("2. Copy the token and replace the existing token in your .env file.")
        print("3. Save the .env file and restart your application.")