# Dondo.ai

Inspired by the tonality of the Dondo drum, **Dondo.ai** is a project designed to help Africans access the internet in their native language. By utilizing audio-based interactions through WhatsApp, Dondo.ai enables users to participate in surveys and polls simply by sending a message. The system responds with an audio message, making it accessible even in regions where English is not the primary language of communication.

## 🎯 Target Audience

- **Developers**: Build voice-based surveys and interactions in non-English languages.
- **Businesses**: Conduct surveys and gather data from a wider audience in their native tongue, particularly in regions where English isn't the language of commerce.

## 🚀 Installation Instructions

### 1. Database Setup

This project requires a MySQL database to store user responses. Although user responses are also stored through the Twilio integration, setting up a MySQL database is recommended for additional storage and data management.

1. **Install MySQL**: Set up a MySQL host on a platform of your choice.
2. **Configure Environment Variables**: Create a `.env` file in the project directory with the following keys:

    ```bash
    MYSQL_HOST=host
    MYSQL_USER=user
    MYSQL_PASSWORD=password
    MYSQL_DB=dondo
    TWILIO_ID=123
    TWILIO_TOKEN=123
    WHATSAPP_NUMBER=1234
    ```

### 2. Python Dependencies

Dondo.ai is a Python application built with Flask. Install the necessary libraries by running:

```bash
pip install -r requirements.txt
