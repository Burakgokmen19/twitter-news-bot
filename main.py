import requests
import time
import os
import pywhatkit as kit

BEARER_TOKEN = "twitter_bearer_token"

# Kullanıcı adı
USERNAME = "twitter_username"

# Son tweetin ID'sini kaydetmek için dosya yolu
LAST_TWEET_FILE = "last_tweet_id.txt"

# WhatsApp Grubunun Adı
WHATSAPP_GROUP_NAME = "whatsapp_group_name"


def load_last_tweet_id():
    """Önceki tweet ID'sini dosyadan yükler."""
    if os.path.exists(LAST_TWEET_FILE):
        with open(LAST_TWEET_FILE, "r", encoding="utf-8") as file:
            return file.read().strip()
    return None


def save_last_tweet_id(tweet_id):
    """Yeni tweet ID'sini dosyaya kaydeder."""
    with open(LAST_TWEET_FILE, "w", encoding="utf-8") as file:
        file.write(tweet_id)


def get_latest_tweet():
    """Twitter API'den son tweetin ID'sini alır, sadece yeni tweet varsa içeriğini çeker."""

    url = f"https://api.twitter.com/2/tweets/search/recent?query=from:{USERNAME}&tweet.fields=id"
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        tweets = response.json()
        if "data" in tweets and len(tweets["data"]) > 0:
            latest_tweet_id = tweets["data"][0]["id"]

            # Önceki tweet ID'sini oku
            last_tweet_id = load_last_tweet_id()

            # Eğer tweet ID'si değiştiyse yeni tweet var demektir
            if latest_tweet_id != last_tweet_id:
                print("Yeni tweet tespit edildi, içeriği çekiliyor...")
                tweet_text = fetch_tweet_text(latest_tweet_id)
                save_last_tweet_id(latest_tweet_id)

                # Yeni tweeti WhatsApp grubuna gönder
                send_whatsapp_message(tweet_text)

            else:
                print("Yeni tweet yok, istek atılmadı.")
        else:
            print("Tweet bulunamadı.")
    elif response.status_code == 429:
        print("⚠️ Rate limit aşıldı! 2 dakika bekleniyor...")
        time.sleep(120)  # 2 dakika bekle
    else:
        print(f"Hata Kodu: {response.status_code}")
        print("Hata Detayı:", response.json())


def fetch_tweet_text(tweet_id):
    """Eğer yeni tweet varsa, içeriğini çeker."""

    url = f"https://api.twitter.com/2/tweets/{tweet_id}?tweet.fields=text"
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        tweet_data = response.json()
        return tweet_data["data"]["text"]
    elif response.status_code == 429:
        print("⚠️ Rate limit aşıldı! 15 dakika bekleniyor...")
        time.sleep(120)  # 2 dakika bekle
        return None
    else:
        print(f"Hata Kodu: {response.status_code}")
        print("Hata Detayı:", response.json())
        return None


def send_whatsapp_message(tweet_text):
    """Yeni tweeti WhatsApp grubuna gönderir."""
    try:
        if tweet_text:
            message = f"📢 Yeni Tweet: {tweet_text}"  # Mesaj formatı
            kit.sendwhatmsg_to_group(WHATSAPP_GROUP_NAME, message, time.localtime().tm_hour,
                                     time.localtime().tm_min + 1)
            print(f"Tweet WhatsApp grubuna gönderildi: {message}")
    except Exception as e:
        print(f"WhatsApp mesaj gönderme hatası: {e}")


if __name__ == "__main__":
    while True:
        get_latest_tweet()
        time.sleep(900)  # 1 dakika bekle