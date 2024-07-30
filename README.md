# 📚 Litmos Course Downloader and Analyzer

## 📋 Overview

This project is a Python-based tool designed to automate the process of downloading course data from Litmos, a Learning Management System (LMS). It uses Selenium for web scraping, processes the downloaded data, and imports it into a SQL database for further analysis.

## 🌟 Main Features

- 🔐 Automated login to Litmos
- 📥 Bulk download of course reports
- 🔄 Data processing and transformation
- 📊 SQL database integration for easy analysis
- 🔧 Configurable for different services and courses

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.7+
- Chrome browser
- ChromeDriver (compatible with your Chrome version)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/RicardoR-M/litmos-course-downloader.git
   cd litmos-course-downloader
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   Create a `.env` file in the root directory with the following content:
   ```
   USUARIO_LITMOS=your_litmos_username
   PWD_LITMOS=your_litmos_password
   DB_CONN=your_database_connection_string
   ASESORES_LINK=link_to_asesores_report
   ```

4. Configure the Chrome and ChromeDriver paths in `app.py`:
   ```python
   chrome_dir = r'..\chrome-win_89\chrome.exe'
   driver_dir = cwd + r'\driver\chromedriver.exe'
   ```

5. Update the course configuration in `config/litmos_cursos.py` to match your Litmos structure.

## 🚀 Usage

To run the Litmos Course Downloader:

```
python app.py
```

This will:
1. Log into Litmos
2. Download course reports for configured services and courses
3. Process the downloaded data
4. Import the data into the configured SQL database

## 📁 Project Structure

- `app.py`: Main entry point of the application
- `config/`:
  - `litmos_cursos.py`: Configuration for services and courses
  - `selenium_config.py`: Selenium WebDriver configuration
  - `utils.py`: Utility functions for file handling
- `downloader.py`: Functions for downloading reports from Litmos
- `to_sql.py`: Functions for processing data and importing to SQL

## 📝 Notes

- Ensure your Litmos account has the necessary permissions to access and download the required reports.
- The tool is configured to run headless by default. Modify `selenium_config.py` if you need to see the browser while running.
- Make sure your SQL database is properly set up and accessible with the provided connection string.

## 📜 License

This project is [MIT](https://choosealicense.com/licenses/mit/) licensed.