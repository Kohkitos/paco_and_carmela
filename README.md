# Live Chat ETL 🔴
test
### Project Description 🚀

This is an important component of your project that many new developers often overlook.

Your description is an extremely important aspect of your project. A well-crafted description allows you to show off your work to other developers as well as potential employers.

The quality of a README description often differentiates a good project from a bad project. A good one takes advantage of the opportunity to explain and showcase:

- **What your application does:** This project revolves around an ETL (Extract, Transform, Load) process in Python. It extracts comments from a live YouTube chat, transforms them to extract relevant information, and analyzes moments with varying comment activity within the video.
  
- **Why you used the technologies you used:** Python was chosen for its versatility and powerful libraries. ChatDownloader comment extraction, since the data extraction was with JSons, MongoDB is a great options for storing our DataBase, while Whisper assists in transcribing and analyzing these comments efficiently.
  
- **Some of the challenges you faced and features you hope to implement in the future:** Discuss the hurdles encountered during development, such as handling large data streams, ensuring accuracy in sentiment analysis, or managing API rate limits. Additionally, highlight future plans, whether it's refining analysis algorithms, implementing user customization, or enhancing data visualization.

This comprehensive description aims to offer a clear overview of the project's purpose, its technical underpinnings, and the roadmap ahead. 📈✨

### How to Install and Run the Project 🛠️

To get started with this project and set up the development environment, follow these steps:

#### 1. Prerequisites

Ensure you have the following installed:

- **Python**: Check that Python is installed on your system. You can download it from [Python's official website](https://www.python.org/downloads/).
- **MongoDB**: Install MongoDB to set up the database. Visit [MongoDB's website](https://www.mongodb.com/) for installation instructions.
- **ChatDownloader**: Use ChatDownloader to extract comments from YouTube. You can find installation details [here](https://github.com/xenova/chat-downloader).
- **NLTK**: For sentiment analysis, install NLTK. You can install it using pip:

    ```bash
    pip install nltk
    ```

#### 2. Clone the Repository

```bash
git clone https://github.com/Kohkitos/live_chat_etl.git
```

#### 3. Install dependencies

```bash
pip install pymongo
```

#### 4. Set up your mongo

-- TBD -- 

#### 5. Run the project

```bash
python main.py
```
