import yt_dlp
from urllib.parse import parse_qs

def handler(event, context):
    # Récupération de l'URL YouTube depuis les paramètres de requête
    query = parse_qs(event.get("queryStringParameters", ""))
    video_url = query.get("url", [None])[0]

    if not video_url:
        return {"statusCode": 400, "body": "Veuillez fournir une URL YouTube"}

    ydl_opts = {
        'format': 'best',
        'outtmpl': '/tmp/%(title)s.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            video_file = ydl.prepare_filename(info)

        return {
            "statusCode": 200,
            "body": f"Vidéo téléchargée avec succès : {video_file}"
        }

    except Exception as e:
        return {"statusCode": 500, "body": str(e)}
