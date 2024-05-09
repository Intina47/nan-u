# Nanéu
![image](https://github.com/Intina47/nan-u/assets/78519682/af2a686a-42a5-4093-88b9-5a79064176df)

Nanéu is an open-source Discord bot designed to streamline and automate the process of fetching and sharing job postings within Discord communities. Leveraging powerful scraping techniques, Nanéu can be configured to retrieve job listings based on specific criteria such as job title, location, and how recent the postings are. 

# Live Demo

To see Nanéu in action and explore its features firsthand, we've set up a test server on Discord where you can interact with the bot. This server provides a live demonstration of Nanéu's capabilities and offers you a space to test its setup and job scraping functionalities without needing to install it on your own server initially.

[Join our Test Discord Server](https://discord.com/channels/1220811373005508768/1220812061634859148)

Please note that this server is intended for demonstration purposes and to give you a feel of how Nanéu operates in a real Discord environment. Feel free to play around with the bot commands and explore its features. If you have any questions or need assistance, our community and support team are active within the server to help you out.

## Features

- **Customizable Job Searches**: Configure Nanéu to search for job postings based on titles, locations, and other preferences.
- **Easy Setup**: A simple setup process facilitated through Discord commands.
- **Permissions Controlled**: Ensures that only users with administrator privileges can configure the bot, maintaining security and control.

## Getting Started

### Prerequisites

- Python 3.10
- Discord bot token (see Discord's developer portal on how to create a bot and get your token)
- `discord.py` library
- `python-jobspy` for job scrapping more on JobSpy here https://github.com/Bunsly/JobSpy
- `PyYAML` for configuration management

### Installation

1. Clone the repository to your local machine:
    ```bash
    git clone https://github.com/Intina47/nan-u.git
    ```
2. Navigate to the cloned directory:
    ```bash
    cd nan-u
    ```
3. Activate the `jobctl` virtual environment. A virtual environment is a self-contained Python environment that allows you to manage dependencies separately for each project. This makes your work easier by avoiding conflicts between different versions of libraries. The `jobctl` virtual environment comes with the project:
    ```bash
    source jobctl/bin/activate
    ```
Note: This command is for Unix-based systems like Linux. If you're using Windows, use `jobctl\Scripts\activate` instead.

4. Create a `.env` file in the root directory and add your Discord bot token:
    ```plaintext
    DISCORD_TOKEN=your_discord_bot_token_here
    ```

### Running the Bot

1. Start the bot by running:
    ```bash
    python app.py
    ```
2. Once the bot is running and connected to Discord, you can configure it in your server by using the `<@your_bot_@> setup` command in the desired channel.

## Configuration

Nanéu supports configuration through Discord commands. Currently, the bot can be configured to filter job postings by:

- Job titles
- Location
- Maximum age of job postings

These settings can be adjusted by running the setup command in any channel where you want Nanéu to post job listings.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See [LICENSE](https://github.com/Intina47/nan-u/blob/main/LICENSE) for more information.

## Acknowledgements

- [Discord.py](https://github.com/Rapptz/discord.py)
- [PyYAML](https://pyyaml.org/)
- [JobSpy](https://github.com/Bunsly/JobSpy)

---

