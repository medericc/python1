import youtube_dl
from urllib.parse import parse_qs

def handler(event, context):
    # Récupération de l'URL YouTube depuis les paramètres de requête
    query = parse_qs(event.get("queryStringParameters", ""))
    video_url = query.get("url", [None])[0]

    if not video_url:
        return {"statusCode": 400, "body": "Please provide a YouTube URL"}

    ydl_opts = {
        'format': 'best',
        'outtmpl': '/tmp/%(title)s.%(ext)s',
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            video_file = ydl.prepare_filename(info)

        # Retourner l'info sur la vidéo
        return {
            "statusCode": 200,
            "body": f"Video downloaded successfully: {video_file}"
        }

    except Exception as e:
        return {"statusCode": 500, "body": str(e)}
