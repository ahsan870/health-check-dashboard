# Health Check Dashboard

## Overview

The Health Check Dashboard is a web application built using Streamlit that allows users to monitor the status of various services across different environments (development, staging, user acceptance testing, and production). The application fetches service statuses asynchronously and displays them in a user-friendly format, providing real-time insights into the health of your services.

## Features

- **Asynchronous Service Status Checks**: Utilizes `httpx` for non-blocking HTTP requests to check the status of services.
- **Environment Configuration**: Supports multiple environments with customizable display names.
- **Real-time Updates**: Automatically refreshes the service status every minute.
- **Downloadable Reports**: Users can download CSV reports of the service statuses for each environment.
- **Color-Coded Status Indicators**: Services are visually represented as "UP" (green) or "DOWN" (red) for easy identification.

## Requirements

- Python 3.7 or higher
- Streamlit
- httpx
- pandas
- python-dotenv

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add your environment-specific credentials:

   ```plaintext
   DEV_USERNAME=your_dev_username
   DEV_PASSWORD=your_dev_password
   SIT_USERNAME=your_sit_username
   SIT_PASSWORD=your_sit_password
   UAT_USERNAME=your_uat_username
   UAT_PASSWORD=your_uat_password
   PROD_USERNAME=your_prod_username
   PROD_PASSWORD=your_prod_password
   ```

4. Create a `config.json` file in the root directory with the following structure:

   ```json
   {
       "base_urls": {
           "dev": "http://dev.example.com",
           "sit": "http://sit.example.com",
           "uat": "http://uat.example.com",
           "prod": "http://prod.example.com"
       },
       "env_urls": {
           "dev": [
               {"name": "Service 1", "path": "/service1/status"},
               {"name": "Service 2", "path": "/service2/status"}
           ],
           "sit": [
               {"name": "Service 1", "path": "/service1/status"},
               {"name": "Service 2", "path": "/service2/status"}
           ],
           "uat": [
               {"name": "Service 1", "path": "/service1/status"},
               {"name": "Service 2", "path": "/service2/status"}
           ],
           "prod": [
               {"name": "Service 1", "path": "/service1/status"},
               {"name": "Service 2", "path": "/service2/status"}
           ]
       }
   }
   ```

## Usage

To run the Health Check Dashboard, execute the following command (any one command which one works):

```bash
streamlit run health-check-dashboard.py
python3 -m streamlit run health-check-dashboard.py
```

It will automatically open your browser or Open your web browser and navigate to `http://localhost:8501` to access the dashboard.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Streamlit](https://streamlit.io/) for the framework.
- [httpx](https://www.python-httpx.org/) for asynchronous HTTP requests.
- [pandas](https://pandas.pydata.org/) for data manipulation and analysis.
