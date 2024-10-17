# UGM Library Seat Booking Bot

Welcome to the **UGM Library Seat Booking Bot**! This bot allows users to easily book seats at the UGM library through Telegram.

## Features
- **Reserve seats** in the UGM library.
- **Check availability** of seats.

## Requirements
- Python 3.x
- Libraries:
  - `python-telegram-bot`
  - Other dependencies (if any)

## Setup Instructions

### 1. Clone the Repository
To get started, clone the repository using the following command:
```bash
git clone https://github.com/your-username/ugm-library-seat-booking-bot.git
cd ugm-library-seat-booking-bot
```

### 2. Install Dependencies
Make sure you have `pip` installed, then run the following command to install the necessary libraries:
```bash
pip install -r requirements.txt
```

### 3. Configuration
Before running the bot, you'll need to set your Telegram bot token and other configuration variables.

Open the `config.py` file (or wherever you have your configuration) and modify the following variables:
```python
TELEGRAM_TOKEN = '{YOUR_TELEGRAM_BOT_TOKEN}'  # Replace with your Telegram Bot Token
SESSION_ID = "{YOUR_SESSION_ID}"                # Replace with your session ID
GROUP_MENU = "{GROUP_MENU}"                      # Replace with your group menu ID
```

### 4. Run the Bot
After setting up your configuration, you can run the bot using the following command:
```bash
python bot.py
```

### 5. Usage
- Start the bot in Telegram by searching for its username and clicking 'Start'.
- Follow the prompts to book a seat at the UGM library.

## Contributing
Contributions are welcome! If you have suggestions or improvements, feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
If you have any questions or feedback, feel free to reach out at [your-email@example.com].
