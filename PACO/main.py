# tools library has all the libraries needed for the pipeline
from tools import *
from pdf_gen import create_pdf

# database
cursor = MongoClient(STR_CONN)
db = cursor.final_project

def main():
    # get peaks for each day
    date = datetime.now().replace(day=15, month=11, hour=0, minute=0, second=0, microsecond=0)
    end_date = date.replace(day = 16)

    data_15 = list(db.message.find({'date': {'$gte': date, '$lte': end_date}}))

    high_15, low_15 = peak_mins(data_15)

    date = datetime.now().replace(day=16, month=11, hour=0, minute=0, second=0, microsecond=0)
    end_date = date.replace(day = 17)

    data_16 = list(db.message.find({'date': {'$gte': date, '$lte': end_date},
                                    'timestamp': {'$lte': 250}})) #investiture minute

    high_16, low_16 = peak_mins(data_16)

    # dictionary for day and video

    day_vid = {15: "https://www.youtube.com/watch?v=5jUU1RhZBHw&ab_channel=RTVENoticias",
            16: "https://www.youtube.com/watch?v=jP1teEowYpo&ab_channel=RTVENoticias"}

    day_df = {15: [high_15, low_15],
            16: [high_16, low_16]}

    for key, value in day_vid.items():
        i = 0
        vid_download(value)
        for df in day_df[key]:
            texts = []
            for index, row in df.iterrows():
                end_time = row['timestamp']
                # if there are comments at the beggining, it won't be reacting to anything said
                if end_time <= 0:
                    continue
                start_time = end_time - 2
                # just in case there is a peak at minute 1
                if start_time < 0:
                    start_time = 0
                clip_extraction('video.mp3', start_time, end_time, f'clip_{index}')
                texts.append(transcribe_audio(f'clip_{index}.mp4'))

            summarizer_es = pipeline("summarization", model="facebook/bart-large-cnn")

            summ = []
            # summary of each text transcribed
            for text in texts:
                # first, translate to english
                text = translate_to_english(text)
                # then, summary
                resumen_espanol = summarizer_es(text, max_length=100, min_length=40, do_sample=False)

                # finally, append to summary list
                summ.append(resumen_espanol[0]['summary_text'])
            
            # generate pdf report
            if i == 0:
                temp = 'high'
                i+=1
            else:
                temp = 'low'

            title = f'{temp}_{key}'
            create_pdf(summ, df, title)


        # path of the mp3
        path = "./video.mp3"

        # delete video.mp3
        os.remove(path)

if __name__ == '__main__':
	main()