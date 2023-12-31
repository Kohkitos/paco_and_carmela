# PACO and CARMELA

PACO (Phonetic Analysis by Comment Outburst) and CARMELA (Content Analyser Reading Media Engagement with a Linguistic Approach) are two integrated functions designed to analyze live YouTube videos in real-time. These functions aim to provide a comprehensive understanding of viewer engagement through linguistic analysis and sentiment evaluation of live chat interactions.

This project is part of the final project for IronHack, a data analysis bootcamp. Developed within a limited timeframe of one and a half weeks, PACO and CARMELA offer an innovative approach to analyzing live YouTube video content, enabling deeper insights into audience engagement and content reception.

## Project Overview

### CARMELA
CARMELA focuses on extracting comments from the live video stream, performing sentiment analysis on each comment, and storing the analyzed data in a MongoDB database hosted on Mongo Atlas. By processing the comments in real-time, CARMELA provides insights into the sentiment and engagement levels throughout the live video.

### PACO
PACO operates by identifying peak comment moments and periods with minimal interaction in the live chat. During these intervals, PACO automatically downloads corresponding video audio clips. It transcribes the audio content and generates concise summaries. These summaries provide a comprehensive overview of the significant portions of the video, highlighting crucial points discussed during high engagement moments and key information during low interaction periods.

## Workflow


1. **CARMELA:**
   - Extracts comments from the live video stream.
   - Performs sentiment analysis on each comment.
   - Stores analyzed data into a MongoDB database on Mongo Atlas.

2. **PACO:**
   - Identifies peak and low interaction moments in the live chat.
   - Downloads video audio clips during these intervals.
   - Transcribes audio content and generates summarized data.

### Automatic PDF Generation

The project culminates in an automated PDF report that consolidates the summarized content generated by PACO with corresponding chat reactions. This report provides a cohesive overview of the video's significant moments, interlinked with viewer engagement patterns derived from the live chat.

The integration of CARMELA and PACO offers a comprehensive approach to analyzing live YouTube video content, enabling a deeper understanding of audience engagement and video content reception.

## Technologies Used

### CARMELA
- **chat_downloader**: Install with `pip install chat-downloader`
- **datetime**: (Python Standard Library)
- **pymongo**: Install with `pip install pymongo`
- **selenium**: Install with `pip install selenium`
- **pysentimiento**: Install with `pip install pysentimiento`

### PACO
- **datetime**: (Python Standard Library)
- **pymongo**: Install with `pip install pymongo`
- **pandas**: Install with `pip install pandas`
- **pytube**: Install with `pip install pytube`
- **transformers**: Install with `pip install transformers`
- **googletrans**: Install with `pip install googletrans`

Please follow the installation instructions for **whisperx** available at [whisperX GitHub](https://github.com/m-bain/whisperX).

## Setup

### Prerequisites
- Python 3.x installed
- Git installed

### Initial Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/Kohkitos/paco_and_carmela.git
   cd your_repository
1. Create a passwords.py file in the root directory of the project. Inside passwords.py, add your MongoDB connection string:
    ```python
    # passwords.py

    STR_CONN = "your_mongodb_connection_string_here"

    ```

### Setting Up CARMELA and PACO

1. **CARMELA**:
   - Ensure the necessary libraries are installed. If not, follow the installation steps mentioned in the Technologies section.
   - Create a `passwords.py` file in the root directory of the project as stated before.

2. **PACO**:
   - Install the required dependencies following the instructions provided in the Technologies section.
   - Follow the instructions at [whisperX GitHub](https://github.com/m-bain/whisperX) to install whisperx.

## Limitations

The development of PACO and CARMELA was constrained not only by the time limitations of the project, completed within a brief period of one and a half weeks as part of IronHack's data analysis bootcamp, but also by certain limitations within the AI models utilized. These limitations include:

- **Sentiment Analysis Accuracy**: The sentiment analysis utilized in CARMELA relies on pre-trained models that might lack contextual intelligence. For instance, certain emojis, like the rose emoji in the context of Spanish politics representing PSOE (the Spanish Socialist Party), might be incorrectly analyzed as neutral rather than positive.

- **Transcription Errors**: Due to the utilization of pre-trained models, transcription errors were encountered, particularly in recognizing names, especially when in Catalan (e.g., "Puigdemont"). WhisperX, the transcription tool, had difficulties capturing certain Spanish and Catalan names accurately.

- **Translation and Summarization Challenges**: As Spanish language summarization AI models are not as robust, the process involved translation from Spanish to English before using an English summarizer. However, this intermediary translation resulted in some summaries appearing awkward or less coherent due to imperfect translation.

## Future Work

To address these limitations and enhance the capabilities of PACO and CARMELA, the following improvements and future work are planned:

- **Re-training Summarization AI**: Developing and re-training a summarization AI model specifically tailored for Spanish political content to improve accuracy and coherence in summarizing relevant information.

- **Error Correction for Transcription**: Implementing a mechanism to "correct" transcription errors in WhisperX specifically related to Spanish and Catalan names, ensuring better accuracy in capturing names and terms.

- **Re-training Sentiment Analysis AI**: Retraining the sentiment analysis AI model to include a more nuanced understanding of sentiments expressed through emojis in the context of Spanish politics, enhancing its accuracy and contextual intelligence.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

This project acknowledges the following articles and projects for their contributions:

- **WhisperX: Time-Accurate Speech Transcription of Long-Form Audio**
  - *Authors*: Max Bain, Jaesung Huh, Tengda Han, Andrew Zisserman
  - *Published in*: INTERSPEECH 2023

- **pysentimiento: A Python Toolkit for Opinion Mining and Social NLP tasks**
  - *Authors*: Juan Manuel Pérez, Mariela Rajngewerc, Juan Carlos Giudici, et al.
  - *Year*: 2023
  - [Paper Link](https://arxiv.org/abs/2106.09462)

- **BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension**
  - *Authors*: Mike Lewis, Yinhan Liu, Naman Goyal, et al.
  - *Published in*: CoRR, 2019
  - [Paper Link](https://arxiv.org/abs/1910.13461)




