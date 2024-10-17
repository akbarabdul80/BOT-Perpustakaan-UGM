import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from telegram import Bot
from telegram.ext import CommandHandler, Updater, MessageHandler, Filters

import json


# Initialize session and encode authentication
session = requests.Session()

# Telegram bot & Sessions Simaster configuration
TELEGRAM_TOKEN = '{YOUR_TELEGRAM_BOT_TOKEN}'
SESSION_ID = "{YOUR_SESSION_ID}"
GROUP_MENU = "{GROUP_MENU}"
MENU = "469"

# Initialize the Telegram bot
bot = Bot(token=TELEGRAM_TOKEN)
updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Define URLs
URL_UGM = "https://simaster.ugm.ac.id"
URL_COOKIE = f"{URL_UGM}/services/simaster/ongoing?sesId={SESSION_ID}&groupMenu={GROUP_MENU}&menu={MENU}"
URL_VIEW = f"{URL_UGM}/perpustakaan/pemesanan/kursi_view"
URL_BOOKING = f"{URL_UGM}/perpustakaan/pemesanan/kursi_booking"


def set_cookie():
    """Retrieve and set cookies for the session."""
    session.get(URL_COOKIE)


def get_page_content(url):
    """Fetch the content of a page."""
    response = session.get(url)
    return response.content


def parse_select_options(soup, name):
    """Parse select options from the soup object."""
    select_element = soup.find('select', {'name': name})
    options = select_element.find_all('option') if select_element else []
    return [(option.get('value'), option.text) for option in options if option.get('value')]


def get_token(soup):
    """Extract CSRF token from the soup object."""
    token_element = soup.find('input', {'name': 'simasterUGM_token'})
    return token_element.get('value') if token_element else None


def send_message(update, message):
    """Send a message to the Telegram chat."""
    update.message.reply_text(message)


def start(update, context):
    """Handle /start command."""
    send_message(update, "Welcome! Use /booking to start the booking process.")


def booking(update, context):
    """Handle /booking command to start the booking process."""
    set_cookie()

    # Get and parse the page content
    page_content = get_page_content(URL_VIEW)
    soup = BeautifulSoup(page_content, 'html.parser')

    # Parse options
    room_data = parse_select_options(soup, 'dParam[ruangan]')
    period_data = parse_select_options(soup, 'dParam[periode]')

    TOKEN = get_token(soup)

    # Get available dates
    today = datetime.now().strftime("%d-%m-%Y")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%d-%m-%Y")

    # Display options to the user
    send_message(update, "Available Dates:\n1. Today\n2. Tomorrow")
    send_message(update, "Available Rooms:\n" + "\n".join(f"{i + 1}. {text}" for i, (_, text) in enumerate(room_data)))
    send_message(update,
                 "Available Periods:\n" + "\n".join(f"{i + 1}. {text}" for i, (_, text) in enumerate(period_data)))

    # Request user input for date, room, and period
    send_message(update, "Please select a date by number.")
    context.user_data['room_data'] = room_data
    context.user_data['period_data'] = period_data
    context.user_data['date_options'] = [today, tomorrow]
    context.user_data['step'] = 'date'


def handle_message(update, context):
    """Handle user input for date, room, period, and seat selection."""
    user_step = context.user_data.get('step')
    if user_step == 'date':
        date_index = int(update.message.text) - 1
        if 0 <= date_index < len(context.user_data['date_options']):
            selected_date = context.user_data['date_options'][date_index]
            send_message(update, "You selected date. Please select a room by number.")
            context.user_data['selected_date'] = selected_date
            context.user_data['step'] = 'room'
        else:
            send_message(update, "Invalid date selection. Please try again.")
    elif user_step == 'room':
        room_index = int(update.message.text) - 1
        if 0 <= room_index < len(context.user_data['room_data']):
            room_value = context.user_data['room_data'][room_index][0]
            send_message(update, "You selected room. Please select a period by number.")
            context.user_data['selected_room'] = room_value
            context.user_data['step'] = 'period'
        else:
            send_message(update, "Invalid room selection. Please try again.")
    elif user_step == 'period':
        period_index = int(update.message.text) - 1
        if 0 <= period_index < len(context.user_data['period_data']):
            period_value = context.user_data['period_data'][period_index][0]
            send_message(update, "You selected period. Fetching available seats...")
            context.user_data['selected_period'] = period_value
            fetch_seats(update, context)
        else:
            send_message(update, "Invalid period selection. Please try again.")
    elif user_step == 'seat':
        try:
            seat_index = int(update.message.text) - 1
            if 0 <= seat_index < len(context.user_data['available_seats']):
                finalize_booking(update, context, seat_index)
            else:
                send_message(update, "Invalid seat selection. Please try again.")
        except ValueError:
            send_message(update, "Please enter a valid number.")


def fetch_seats(update, context):
    """Fetch available seats based on user selections."""
    formatted_date = context.user_data['selected_date']
    url_room_period = f"https://simaster.ugm.ac.id/perpustakaan/pemesanan/kursi_lokasi/{formatted_date}/{context.user_data['selected_period']}/{context.user_data['selected_room']}"

    page_content = get_page_content(url_room_period)
    soup = BeautifulSoup(page_content, 'html.parser')

    # Find and display available seats
    available_buttons = soup.find_all('button', class_='pesanBookingApproval')
    available_seats = [(button.text.strip(), button.get('onclick', '').split("'")[1]) for button in available_buttons]
    if available_seats:
        send_message(update, "Available Seats:\n" + "\n".join(
            f"{i + 1}. {seat}" for i, (seat, _) in enumerate(available_seats)))
        context.user_data['available_seats'] = available_seats
        send_message(update, "Please select a seat by number.")
        context.user_data['step'] = 'seat'
    else:
        send_message(update, "No available seats found.")


def finalize_booking(update, context, seat_index):
    """Finalize the booking based on selected seat."""
    seat_id = context.user_data['available_seats'][seat_index][1]
    token_value = get_token(BeautifulSoup(get_page_content(URL_VIEW), 'html.parser'))
    data_token = {
        'simasterUGM_token': token_value,
        'dParam[kursiId]': seat_id,
        'dParam[tanggal]': context.user_data['selected_date'],
        'dParam[ruangan]': context.user_data['selected_room'],
        'dParam[periode]': context.user_data['selected_period'],
    }

    response = session.post(URL_BOOKING, data=data_token)

    try:
        response_json = response.json()
        if response_json.get("status") == "danger":
            message = response_json.get("msg", "An error occurred during the booking process.")
        else:
            message = f"Booking Successful! Response: {response.text}"
    except json.JSONDecodeError:
        message = f"Booking Failed. Response Text: {response.text}"

    send_message(update, message)


# Register command and message handlers
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('booking', booking))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

# Start polling
updater.start_polling()
updater.idle()