# librerías 
from datetime import datetime

from pymongo import MongoClient
from passwords import STR_CONN

import pandas as pd

from pytube import YouTube
import os
import subprocess

import whisperx
from transformers import pipeline

from googletrans import Translator


# database
cursor = MongoClient(STR_CONN)
db = cursor.final_project

def peak_mins(data):
    """
    Identify high and low activity timestamps based on message counts and calculate percentages of different sentiments.

    Parameters:
    data (DataFrame): DataFrame containing chat message data with 'timestamp' and 'sentiment_analysis' columns.

    Returns:
    tuple: A tuple containing two DataFrames - the first DataFrame includes high activity timestamps with corresponding sentiment percentages,
           the second DataFrame includes low activity timestamps with corresponding sentiment percentages.
    """

    df = pd.DataFrame(data)

    # count of messages per timestamp
    count_df = df['timestamp'].value_counts().reset_index()
    count_df.columns = ['timestamp', 'count']

    # Dictionary for recounts
    sentiment_counts = {'POS_count': 'POS', 'NEG_count': 'NEG', 'NEU_count': 'NEU'}

    # Count sentiment per timestamp
    for key, value in sentiment_counts.items():
        sentiment_counts[key] = df[df['sentiment_analysis'] == value]['timestamp'].value_counts().reset_index()
        sentiment_counts[key].columns = ['timestamp', f'{value}_count']

    # Combine all counts
    merged_counts = count_df.copy()
    for key, value in sentiment_counts.items():
        merged_counts = pd.merge(merged_counts, value, on='timestamp', how='left').fillna(0)

    # Calculate percentage of sentiments
    for key in sentiment_counts.keys():
        total_sentiment = merged_counts[key.split('_')[0] + '_count'].sum()
        merged_counts[f'{key.split("_")[0]}_percentage'] = (merged_counts[key] / total_sentiment) * 100
        merged_counts[f'{key.split("_")[0]}_percentage'] = merged_counts[f'{key.split("_")[0]}_percentage'].round(2)
        merged_counts.drop(columns=key, inplace=True)


    # Filtre above and below boxplot comments
    p_25 = merged_counts['count'].quantile(0.25)
    p_75 = merged_counts['count'].quantile(0.75)

    # create result dataframes
    high_peaks_df = merged_counts[merged_counts['count'] >= p_75].sort_values(by='timestamp')
    low_peaks_df = merged_counts[merged_counts['count'] <= p_25].sort_values(by='timestamp')

    return high_peaks_df, low_peaks_df

def vid_download(url):
    """
    Download audio from a YouTube video given its URL.

    Parameters:
    url (str): URL of the YouTube video.

    Returns:
    str: Success message if the audio extraction is successful, including the video's title saved as 'video.mp3'.
         Error message if there's an issue during the download process.
    """

    try:
        # transform url into a YouTube object
        yt = YouTube(url)

        # filtre only the audio
        video = yt.streams.filter(only_audio=True).first()

        # download the audio in current directory as video.mp3
        destination = '.'
        out_file = video.download(output_path=destination)
        new_file = 'video.mp3'
        os.rename(out_file, new_file)
        # success message
        return f"Audio extracted succesfully: {yt.title} as video.mp3"
    except Exception as e:
        # failiure message
        return f"There was an error downloading the video: {str(e)}"
    
def clip_extraction(audio_file, start, end, clip_name):
    """
    Extract a specific clip from an audio file and save it as an MP4 video file using FFmpeg.

    Parameters:
    audio_file (str): Path to the input audio file.
    start (float): Start time of the clip in minutes.
    end (float): End time of the clip in minutes.
    clip_name (str): Name for the extracted clip without the file extension.

    Returns:
    None: Saves the extracted clip as an MP4 file based on the provided start and end times.
    """
    
    start_seconds = start * 60
    end_seconds = end * 60
    
    # Clip desired selection
    cilp_command = f'ffmpeg -i {audio_file} -ss {start_seconds} -to {end_seconds} -c:v copy -c:a copy {clip_name}.mp4'
    subprocess.run(cilp_command.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def transcribe_audio(audio_file):
    """
    Transcribe the content of an audio file using the WhisperX model and return the transcription.

    Parameters:
    audio_file (str): Path to the audio file to be transcribed.

    Returns:
    str: Transcription of the audio content, separated by new lines for each sentence.
    """


    # Loads whisperX model
    model = whisperx.load_model("base", device="cpu", compute_type="float32")

    # Load audio
    audio = whisperx.load_audio(audio_file)

    # Transcription
    result = model.transcribe(audio, batch_size=16)
    transcription = result["segments"]

    # Deletes clip
    os.remove(audio_file)

    # Add a new line after each sentence
    res = "\n".join(seg['text'] for seg in transcription)

    return res

def translate_to_english(text):
    """
    Translate text from Spanish to English using the Google Translate API.

    Parameters:
    text (str): Text to be translated from Spanish to English.

    Returns:
    str: Translated text in English.
    """
    
    translator = Translator()
    translated = translator.translate(text, src='es', dest='en')
    return translated.text