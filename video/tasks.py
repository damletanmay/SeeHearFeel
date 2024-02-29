import asyncio
from celery import shared_task
from django.core.files import File
from celery_progress.backend import ProgressRecorder

@shared_task(bind=True)
def process_video(self,json_data):
    progress = ProgressRecorder(self)

    try:
        progress.set_progress(1,100,'Uploading Video ...')
        video = Video()

        video_file_path = json_data['video_file_path']
        subtitles_file_path = json_data['subtitles_file_path']

        progress.set_progress(50,100,'Uploading Video ...')
        with open(video_file_path, 'rb') as file:
            video_file = File(file)
            video.video.save(json_data['video_file_name'], video_file)

        progress.set_progress(70,100,'Uploading Subtitles ...')
        with open(subtitles_file_path, 'rb') as file:
            subtitles_file = File(file)
            video.subtitles.save(json_data['subtitles_file_name'], subtitles_file)

        video.user = User.objects.get(id=json_data['user_id'])

        video.save()
        print("Video saved")
        progress.set_progress(100,100,'Video Uploaded!')
        return True
    except Exception as e:
        progress.set_progress(0,0,'Video Upload Failed!')
        return False
