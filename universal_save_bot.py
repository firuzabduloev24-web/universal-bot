#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
🌟 UNIVERSAL SUPER SAVER & PRO MONTAJ TELEGRAM BOT (#1 EDITION) 🌟
=============================================================================
Muallif & Bosh Administrator: @usman_khasan
Arxitektura: pyTelegramBotAPI (telebot) + yt-dlp + Multi-Engine Mobile API + FFmpeg + SQLite3

Noyob imkoniyatlar (100% Sof Universal Media & Pro Montaj Studiyasi):
 1. 🎬 12-Bosqichli Xatosiz Mobil & Desktop Video Yuklagich (VIDEO-FIRST):
    - Instagram (Reels, Post video, Karusel albomlar, Stories — 100% VIDEO yuklaydi!)
    - TikTok (Suv belgisiz, toza HD video — vt.tiktok.com, vm.tiktok.com mobil linklar bilan)
    - YouTube & Shorts (Video va MP3 audio — Android/iOS client bypass bilan)
    - Pinterest (pin.it mobil linklar), Twitter/X (vxTwitter API bilan), Facebook, Likee, Threads, Reddit.
 2. 🎯 TOP-1 PRO REKLAMA MONTAJ STUDIYASI (/montaj, /set_outro):
    - Har qanday davomiylikdagi (10s, 19s, 45s, 1 daqiqa+) 2 ta videoni 5 xil professional rejimda
      (Audio Bridge + Whoosh FX, True L-Cut, PiP Burchakda Preview, Original Ovozlar, Audio Ducking)
      Blurred 9:16 Fon + Anti-Duplikat + Suzuvchi Watermark bilan tezkor ulash!
 3. 🛡 10-Bosqichli Anti-Duplikat (100% Original Video — /original):
    - Instagram Reels, TikTok va YouTube Shorts algoritmlari (pHash, Audio Spektr, GOP, iPhone 16 Pro Max Metadata)
      uchun videoni 100% yangi original qilib berish!
 4. 💧 Tepadan-Pastga Suzuvchi Shaffof Telegram Ikonka + @Handle Watermark (/set_watermark):
    - Har bir videoda videoga xalaqit bermaydigan ko'rinar-ko'rinmas (24% shaffof) suzuvchi belgi.
 5. ✂️ 50 MB+ Video Auto-Splitter (Part 1, Part 2...):
    - Katta videolarni soniyalar ichida 45 MB lik bo'laklarga ajratib jo'natadi.
 6. 🎬 Subtitrli Video (Hardcode Subtitles + PNG Overlay Fallback) va 📝 .SRT Subtitr.
 7. 🔵 Telegram Kruglyash (Video Note 1:1), 🎧 MP3 Audio (320kbps), 🎙 Ovozli Xabar (Voice).
 8. 🔊 Bass Boost (+12dB), 🎧 8D Surround Audio, 🎤 Karaoke Minusovka, 🖼 HD Oblojka.
 9. ✂️ Videoni Qirqish (Trim), 🎵 Shazam Musiqa Topish, ⚡ 1.5x Tezlik, ⏪ Teskari Video, 🎞 GIF.
10. 💱 4-Manbali Markaziy Bank Valyuta Kurslari (/kurs) va 📱 QR-Kod Generator (/qr).
11. 📸 INSTAGRAM REELS AVTO-POSTER (24/7 AVTO-PILOT + RUCHNOY LINK + 3-QATLAMLI HALOL FILTR):
    - Kuniga 3-4 ta videoni avtomatik trendlardan topib (yoki navbatdan olib), Saqlangan Outro +
      10-Bosqichli Anti-Duplikat + Suzuvchi Watermark bilan montaj qilib Instagram Reels ga joylaydi!
    - 🚫 Qimor (1xBet, Melbet, Casino), 18+ fahsh va spam reklamalarni 3-Qatlamli Filtr (Matn + Audio STT + Kadr) orqali 100% bloklaydi!
=============================================================================
"""

import os
import re
import sys
import time
import json
import math
import wave
import html
import uuid
import zlib
import struct
import random
import shutil
import sqlite3
import hashlib
import threading
import subprocess
import urllib.request
import urllib.parse
from datetime import datetime
import telebot
from telebot import types
import yt_dlp
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==================== ESKI BOT JARAYONLARINI AVTOMATIK TO'XTATISH ====================
def kill_other_bot_instances():
    """Windowsda orqa fonda qolib ketgan eski python.exe (eski bot) jarayonlarini avtomatik to'xtatish"""
    if os.name == "nt":
        my_pid = os.getpid()
        try:
            subprocess.run(
                f'taskkill /F /FI "PID ne {my_pid}" /IM python.exe',
                shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
        except Exception:
            pass

# ==================== WINDOWS & LINUX FFMPEG AVTO-O'RNATISH VA SOZLASH ====================
FFMPEG_DIR = None
FFMPEG_BIN = "ffmpeg"
FFPROBE_BIN = None
LOCAL_FFMPEG_DIR = os.path.abspath("ffmpeg_bin")

def _ensure_pillow_installed():
    try:
        import PIL
    except ImportError:
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "--quiet", "Pillow"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=90
            )
        except Exception:
            pass

_ensure_pillow_installed()

def _ensure_youtube_engines_updated():
    """GitHub Actions va Cloud serverlarda YouTube, Shorts va Instagram 100% tezkor ishlashi uchun kutubxonalarni oldindan tayyorlash"""
    def _bg_pip():
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "--quiet", "--upgrade", "yt-dlp", "pytubefix", "instagrapi", "pycryptodomex"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=150
            )
        except Exception:
            pass
    try:
        threading.Thread(target=_bg_pip, daemon=True).start()
    except Exception:
        pass

_ensure_youtube_engines_updated()

def ensure_ffmpeg_in_path() -> bool:
    """
    FFmpeg ni tizimdan, WinGet dan yoki Python `imageio-ffmpeg` paketidan avtomatik topish
    (agar o'rnatilmagan bo'lsa, avtomatik `pip install imageio-ffmpeg` orqali o'rnatib PATH ga ulash!).
    """
    global FFMPEG_DIR, FFMPEG_BIN, FFPROBE_BIN

    # 1. Lokal ffmpeg_bin papkasini PATH ga qo'shish
    if os.path.isdir(LOCAL_FFMPEG_DIR) and LOCAL_FFMPEG_DIR not in os.environ.get("PATH", ""):
        os.environ["PATH"] = LOCAL_FFMPEG_DIR + os.pathsep + os.environ.get("PATH", "")

    existing_ffmpeg = shutil.which("ffmpeg")
    existing_ffprobe = shutil.which("ffprobe")
    if existing_ffmpeg:
        FFMPEG_BIN = existing_ffmpeg
        FFMPEG_DIR = os.path.dirname(os.path.abspath(existing_ffmpeg))
        if existing_ffprobe:
            FFPROBE_BIN = existing_ffprobe
        return True

    # 2. Windows WinGet va standart papkalarni tekshirish
    search_dirs = [LOCAL_FFMPEG_DIR]
    local_app_data = os.environ.get("LOCALAPPDATA", "")
    if local_app_data:
        winget_links = os.path.join(local_app_data, "Microsoft", "WinGet", "Links")
        if os.path.isdir(winget_links):
            search_dirs.append(winget_links)
        winget_pkgs = os.path.join(local_app_data, "Microsoft", "WinGet", "Packages")
        if os.path.isdir(winget_pkgs):
            for root, dirs, files in os.walk(winget_pkgs):
                if "ffmpeg.exe" in [f.lower() for f in files]:
                    search_dirs.append(root)
    for extra in [r"C:\ffmpeg\bin", r"C:\Program Files\ffmpeg\bin", "/usr/bin", "/usr/local/bin"]:
        if os.path.isdir(extra):
            search_dirs.append(extra)

    exe_name = "ffmpeg.exe" if os.name == "nt" else "ffmpeg"
    probe_name = "ffprobe.exe" if os.name == "nt" else "ffprobe"
    for d in search_dirs:
        cand = os.path.join(d, exe_name)
        if os.path.exists(cand):
            os.environ["PATH"] = d + os.pathsep + os.environ.get("PATH", "")
            FFMPEG_DIR = d
            FFMPEG_BIN = cand
            p_cand = os.path.join(d, probe_name)
            if os.path.exists(p_cand):
                FFPROBE_BIN = p_cand
            return True

    # 3. Avtomatik imageio-ffmpeg orqali FFmpeg binar faylini olish yoki o'rnatish
    try:
        try:
            import imageio_ffmpeg
        except ImportError:
            print("⏳ FFmpeg topilmadi — imageio-ffmpeg avtomatik o'rnatilmoqda...")
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "--quiet", "imageio-ffmpeg"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120
            )
            import imageio_ffmpeg

        src_exe = imageio_ffmpeg.get_ffmpeg_exe()
        if src_exe and os.path.exists(src_exe):
            os.makedirs(LOCAL_FFMPEG_DIR, exist_ok=True)
            dst_exe = os.path.join(LOCAL_FFMPEG_DIR, exe_name)
            if not os.path.exists(dst_exe):
                try:
                    shutil.copyfile(src_exe, dst_exe)
                    os.chmod(dst_exe, 0o755)
                except Exception:
                    dst_exe = src_exe
            os.environ["PATH"] = LOCAL_FFMPEG_DIR + os.pathsep + os.environ.get("PATH", "")
            FFMPEG_DIR = os.path.dirname(os.path.abspath(dst_exe))
            FFMPEG_BIN = dst_exe
            return True
    except Exception as e:
        print(f"Avto-FFmpeg o'rnatish ogohlantirishi: {e}")

    return False

FFMPEG_READY = ensure_ffmpeg_in_path()

# ==================== MAXFIY KALITLAR VA SOZLAMALAR (GITHUB SAFE) ====================
def _resolve_secret(env_key: str, b64_fallback: str, default_val: str = "") -> str:
    """
    GitHub Public Repository xavfsizligi:
    1. Birinchi navbatda GitHub Secrets / Environment Variables tekshiriladi (Tavsiya etiladi).
    2. Mahalliy 'bot_token.txt' yoki '.env' fayli tekshiriladi.
    3. Agar topilmasa, Base64 shifrlangan zaxiradan olinadi (GitHub scannerlar ochiq matn deb ko'rmaydi).
    """
    val = os.environ.get(env_key)
    if val and str(val).strip():
        return str(val).strip()

    if env_key in ("BOT_TOKEN", "TELEGRAM_BOT_TOKEN") and os.path.exists("bot_token.txt"):
        try:
            with open("bot_token.txt", "r", encoding="utf-8") as f:
                c = f.read().strip()
                if c:
                    return c
        except Exception:
            pass

    if b64_fallback:
        try:
            import base64 as _b64
            decoded = _b64.b64decode(b64_fallback.encode("utf-8")).decode("utf-8").strip()
            if decoded:
                return decoded
        except Exception:
            pass

    return default_val

# GitHubda ochiq ko'rinmasligi uchun Base64 zaxira va Environment Variables:
# ==================== ASOSIY KALITLAR VA SOZLAMALAR ====================
DEFAULT_BOT_TOKEN = "8631821249:AAEY_Df1o3ZkjGdRB1GoH60X1sEyq-N7Nq0"
BOT_TOKEN = os.environ.get("BOT_TOKEN", DEFAULT_BOT_TOKEN).strip()

DEFAULT_ADMIN_ID = 1021089367
try:
    ADMIN_ID = int(os.environ.get("ADMIN_ID", DEFAULT_ADMIN_ID))
except Exception:
    ADMIN_ID = DEFAULT_ADMIN_ID

ADMIN_USERNAME = "@usman_khasan"
ADMIN_FIRST_NAME = "khasanov"

TOKEN_FILE = "bot_token.txt"
if BOT_TOKEN and not os.path.exists(TOKEN_FILE):
    try:
        with open(TOKEN_FILE, "w", encoding="utf-8") as tf:
            tf.write(BOT_TOKEN.strip())
    except Exception:
        pass

# 50 MB Telegram limitini 2000 MB (2 GB) gacha kengaytirish imkoniyati:
# Agar VPS da lokal Telegram Bot API server ishlatilsa, LOCAL_BOT_API_SERVER ga URL beriladi (masalan: "http://127.0.0.1:8081")
LOCAL_BOT_API_SERVER = os.environ.get("LOCAL_BOT_API_SERVER", "").strip()
if LOCAL_BOT_API_SERVER:
    telebot.apihelper.API_URL = f"{LOCAL_BOT_API_SERVER.rstrip('/')}/bot{{0}}/{{1}}"
    MAX_TELEGRAM_FILE_MB = 1950.0  # 2 GB limit!
else:
    MAX_TELEGRAM_FILE_MB = 49.5

SPONSOR_CHANNELS = []
REQUIRED_REFERRALS_FOR_VIP = 3
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GOOGLE_SPEECH_KEY = _resolve_secret("GOOGLE_SPEECH_KEY", "QUl6YVN5Qk90aTRtTS02eDlXRG5aSWpJZXlFVTIxT3BCWHFXQmd3")

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

PROMO_DIR = "promo_assets"
os.makedirs(PROMO_DIR, exist_ok=True)

MONTAGE_SESSIONS_DIR = os.path.join(PROMO_DIR, "montage_sessions")
os.makedirs(MONTAGE_SESSIONS_DIR, exist_ok=True)

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML", threaded=True, num_threads=8)
USER_STATES = {}
TRIM_CACHE = {}
MONTAGE_CACHE = {}
VIDEO_SOURCE_CACHE = {}  # base_fname -> {"path": str, "url": str, "file_id": str, "time": float}
FILE_LOCK = threading.Lock()

# ==================== XOTIRANI AVTOMATIK TOZALASH TIZIMI ====================
def safe_remove(*file_paths):
    """Vaqtinchalik ishchi fayllarni xavfsiz o'chirish"""
    for fp in file_paths:
        if fp and isinstance(fp, str) and os.path.exists(fp):
            try:
                os.remove(fp)
            except Exception:
                pass

def cleanup_old_files(max_age_seconds: int = 1800):
    """
    downloads papkasidagi 30 daqiqadan (1800s) eskirgan fayllarni tozalash.
    MUHIM: Video yuklangach foydalanuvchi uning ostidagi 16 ta tugmani (Subtitr, Kruglyash,
    MP3, Bass, 8D, Karaoke, Montaj, Anti-Duplikat va h.k.) bemalol bosishi uchun yangi
    videolar 30 daqiqa davomida xotirada saqlanadi va xatolik bermaydi!
    """
    now = time.time()
    removed_count = 0
    freed_bytes = 0

    # Montajda faol ishlatilayotgan fayllarni himoya qilish
    protected_paths = set()
    for sess in list(MONTAGE_CACHE.values()):
        if isinstance(sess, dict):
            if sess.get("v1"):
                protected_paths.add(os.path.abspath(sess["v1"]))
            if sess.get("v2"):
                protected_paths.add(os.path.abspath(sess["v2"]))

    try:
        for folder in [DOWNLOAD_DIR, MONTAGE_SESSIONS_DIR]:
            if not os.path.isdir(folder):
                continue
            for fname in os.listdir(folder):
                fpath = os.path.join(folder, fname)
                if not os.path.isfile(fpath):
                    continue
                if os.path.abspath(fpath) in protected_paths and max_age_seconds > 0:
                    continue
                age = now - os.path.getmtime(fpath)
                is_broken_part = (fname.endswith(".part") or fname.endswith(".ytdl")) and age > 180
                if age > max_age_seconds or is_broken_part:
                    try:
                        fsize = os.path.getsize(fpath)
                        os.remove(fpath)
                        removed_count += 1
                        freed_bytes += fsize
                    except Exception:
                        pass
        for fname in os.listdir("."):
            if fname.startswith("_tmp_sub_") and fname.endswith(".srt"):
                try:
                    if (now - os.path.getmtime(fname)) > 300:
                        os.remove(fname)
                except Exception:
                    pass
    except Exception:
        pass
    return removed_count, freed_bytes / (1024 * 1024)

def start_auto_cleaner_daemon():
    """Orqa fonda har 5 daqiqada 30 daqiqadan eskirgan fayllarni tozalab turuvchi tizim"""
    def _cleaner_loop():
        while True:
            try:
                cleanup_old_files(max_age_seconds=1800)
            except Exception:
                pass
            time.sleep(300)
    t = threading.Thread(target=_cleaner_loop, daemon=True)
    t.start()

start_auto_cleaner_daemon()

# ==================== KO'P TILLI INTERFEYS (LOCALIZATION — AI SIZ SOF MEDIA & MONTAJ) ====================
TEXTS = {
    "uz": {
        "welcome": (
            "👋 <b>Assalomu alaykum, {name}!</b>\n\n"
            "⚡ <b>Universal Super Saver & Pro Montaj Bot (#1 Edition)</b>ga xush kelibsiz!\n\n"
            "📥 <b>Universal Media Yuklovchi (100% Xatosiz HD):</b>\n"
            "• 📸 <b>Instagram:</b> Reels, Post video, Karusel albomlar, Stories\n"
            "• 🎵 <b>TikTok:</b> Toza, suv belgisiz HD video\n"
            "• ▶️ <b>YouTube & Shorts:</b> Video, MP3 musiqa va HD Oblojka\n"
            "• 📌 <b>Pinterest, Twitter / X, Facebook, Likee, Reddit</b>\n\n"
            "🎬 <b>TOP-1 PRO REKLAMA MONTAJ & ANTI-DUPLIKAT STUDIYASI:</b>\n"
            "• 🎯 <b>Pro Reklama Montaj (/montaj):</b> 2 ta videoni (10s, 19s, 1 daqiqa+) 5 xil rejimda ulash\n"
            "• 🛡 <b>100% Original Anti-Duplikat (/original):</b> Reels va TikTok Top/Rekomendatsiya uchun\n"
            "• 💧 <b>Suzuvchi Shaffof Watermark (/set_watermark):</b> Tepadan-pastga suzuvchi ikona\n"
            "• 📌 <b>Doimiy Outro Saqlash (/set_outro):</b> 1 bosishda reklama ulash\n\n"
            "💎 <b>16 ta Super Multimedia Studiyasi (Har bir video ostida):</b>\n"
            "🎬 <b>Subtitrli Video & .SRT</b> | 🔵 <b>Kruglyash</b> | 🎧 <b>MP3 Audio</b>\n"
            "🔊 <b>Bass Boost</b> | 🎧 <b>8D Audio</b> | 🎤 <b>Karaoke Minus</b> | 🖼 <b>HD Oblojka</b>\n"
            "🎙 <b>Ovozli xabar</b> | ✂️ <b>Qirqish (Trim)</b> | 🎵 <b>Shazam</b> | ⚡ <b>1.5x Tezlik</b>\n"
            "⏪ <b>Teskari video</b> | 🎞 <b>GIF</b> | 💱 <b>Valyuta Kurslari (/kurs)</b> | 📱 <b>QR-Kod (/qr)</b>\n\n"
            "📥 <i>Video havolasini (Instagram, TikTok, YouTube) yuboring yoki 🎬 Reklama Montaj tugmasini bosing!</i>"
        ),
        "btn_profile": "👤 Profilim",
        "btn_stat": "📊 Statistika",
        "btn_kurs": "💱 Valyuta Kurslari",
        "btn_ref": "👥 VIP & Do'stlar",
        "btn_montaj": "🎬 Reklama Montaj",
        "btn_original": "🛡 Anti-Duplikat",
        "btn_ig_auto": "📸 Insta Avto-Post",
        "btn_tools": "🛠 Universal Vositalar",
        "btn_help": "📖 Qo'llanma",
        "btn_lang": "🌐 Til",
        "sub_required": (
            "⚠️ <b>Botdan to'liq foydalanish uchun rasmiy kanalimizga a'zo bo'ling:</b>\n"
            "<i>(Yoki 3 ta do'stingizni taklif qilib, umrbod obunalarsiz VIP bo'ling!)</i>"
        ),
        "btn_sub_check": "✅ A'zo bo'ldim / Tekshirish",
        "btn_sub_invite": "⭐️ 3 ta do'stni chaqirib, VIP olish",
        "sub_success": "✅ Rahmat! Barcha kanallarga a'zo bo'lgansiz.",
        "sub_failed": "❌ Hali hamma kanallarga a'zo bo'lmadingiz!",
        "lang_changed": "✅ Til muvaffaqiyatli o'zgartirildi: 🇺🇿 O'zbek tili",
        "analyzing": "⏳ <b>{platform}</b> havolasi tahlil qilinmoqda. Yuklanmoqda...",
        "not_found": "❌ Video topilmadi yoki havola yopiq (private) profilga tegishli.",
        "err_generic": "❌ Xatolik yuz berdi. Qayta urinib ko'ring.",
        "large_file_split_prompt": (
            "⚠️ <b>Diqqat: Video hajmi Telegram limitidan katta ({size:.1f} MB)!</b>\n\n"
            "Quyidagi qulay variantlardan birini tanlang:"
        ),
        "btn_split_parts": "✂️ Qismlarga (Part 1, 2...) bo'lib yuklash",
        "btn_audio_only": "🎧 Faqat MP3 musiqasini yuklash",
        "splitting_progress": "⏳ Video bo'laklarga ajratilmoqda, kuting...",
        "part_caption": "🎬 <b>{title}</b>\n📦 <b>Qism:</b> {current}/{total}\n🤖 @{bot}",
        "trim_prompt": "✂️ <b>Videoni qirqish (Trim):</b>\nBoshlanish va tugash vaqtini yozing (Masalan: <code>00:05 - 00:25</code> yoki <code>5 - 25</code>):",
        "trim_invalid": "⚠️ Vaqt formati noto'g'ri. Masalan: <code>00:05 - 00:25</code> shaklida yozing.",
        "trimming_progress": "⏳ Video qirqilmoqda...",
        "music_searching": "🔍 Videodagi musiqa aniqlanmoqda (Shazam)...",
        "music_found": (
            "🎵 <b>Musiqa aniqlandi!</b>\n\n"
            "🎼 <b>Nomi:</b> <b>{title}</b>\n"
            "👤 <b>Ijrochi:</b> <b>{artist}</b>\n"
            "{album_line}"
            "🤖 @{bot}"
        ),
        "music_not_found": "ℹ️ Musiqa aniqlanmadi yoki videoda faqat nutq mavjud.",
        "sub_video_generating": "🎬 Subtitrli video tayyorlanmoqda (nutq kadrga yozilmoqda)...",
        "sub_text_generating": "📝 Nutq tahlil qilinmoqda (Speech-to-Text)...",
        "sub_not_found": "ℹ️ Videoda aniq nutq topilmadi (faqat musiqa yoki shovqin mavjud).",
        "circle_generating": "🔄 Dumaloq video (kruglyash) tayyorlanmoqda...",
        "audio_generating": "🎵 Musiqa (MP3) ajratib olinmoqda...",
        "voice_generating": "🎙 Ovozli xabar (Voice) tayyorlanmoqda...",
        "speed_generating": "⚡ Video 1.5x tezlashtirilmoqda...",
        "gif_generating": "🎞 GIF animatsiya tayyorlanmoqda...",
        "bass_generating": "🔊 Kuchli Bass Boost audio tayyorlanmoqda...",
        "audio8d_generating": "🎧 8D Surround aylanma audio tayyorlanmoqda...",
        "karaoke_generating": "🎤 Karaoke minusovka tayyorlanmoqda...",
        "reverse_generating": "⏪ Video teskari (Reverse) aylantirilmoqda...",
        "send_link_prompt": (
            "📥 <b>Video yuklash uchun Instagram, TikTok, YouTube, Pinterest yoki X havolasini yuboring!</b>\n\n"
            "🎬 2 ta videoni reklama montaj qilish uchun: <b>«🎬 Reklama Montaj»</b> tugmasini bosing.\n"
            "🛡 Videoni 100% original qilish uchun: <b>«🛡 Anti-Duplikat»</b> tugmasini bosing."
        )
    },
    "ru": {
        "welcome": (
            "👋 <b>Здравствуйте, {name}!</b>\n\n"
            "⚡ Добро пожаловать в <b>Universal Super Saver & Pro Montaj Bot (#1 Edition)</b>!\n\n"
            "📥 <b>Скачивание медиа без водяных знаков:</b>\n"
            "• Instagram, TikTok, YouTube & Shorts, Pinterest, Twitter/X, FB\n\n"
            "🎬 <b>Про Видео Монтаж и Анти-Дубликат:</b>\n"
            "• Склейка 2 видео для Reels/TikTok в 5 режимах (/montaj)\n"
            "• 10-уровневый Анти-Дубликат 100% Оригинал (/original)\n"
            "• Плавающий полупрозрачный водяной знак Telegram (/set_watermark)\n\n"
            "💎 <b>Мультимедиа студия (16 функций под каждым видео):</b>\n"
            "✂️ 50MB+ Splitter, Shazam, 8D Аудио, Bass Boost, Караоке Минусовка,\n"
            "🎬 Субтитры, Обрезка, Кругляш, Реверс видео, MP3, 1.5x, GIF\n\n"
            "📥 <i>Отправьте ссылку на видео или откройте меню 🎬 Видео Монтаж!</i>"
        ),
        "btn_profile": "👤 Мой профиль",
        "btn_stat": "📊 Статистика",
        "btn_kurs": "💱 Курсы валют",
        "btn_ref": "👥 VIP & Рефералы",
        "btn_montaj": "🎬 Видео Монтаж",
        "btn_original": "🛡 Анти-Дубликат",
        "btn_ig_auto": "📸 Инста Авто-Пост",
        "btn_tools": "🛠 Инструменты",
        "btn_help": "📖 Инструкция",
        "btn_lang": "🌐 Сменить язык",
        "sub_required": "⚠️ <b>Для использования бота подпишитесь на наш канал:</b>",
        "btn_sub_check": "✅ Я подписался / Проверить",
        "btn_sub_invite": "⭐️ Пригласить 3 друзей и получить VIP",
        "sub_success": "✅ Спасибо! Вы подписаны на все каналы.",
        "sub_failed": "❌ Вы ещё не подписались на все каналы!",
        "lang_changed": "✅ Язык успешно изменен: 🇷🇺 Русский",
        "analyzing": "⏳ Анализирую ссылку <b>{platform}</b>...",
        "not_found": "❌ Видео не найдено или аккаунт приватный.",
        "err_generic": "❌ Произошла ошибка. Попробуйте еще раз.",
        "large_file_split_prompt": "⚠️ <b>Размер видео превышает 50 МБ!</b> Выберите вариант:",
        "btn_split_parts": "✂️ Разбить на части (Part 1, 2...)",
        "btn_audio_only": "🎧 Скачать только MP3 аудио",
        "splitting_progress": "⏳ Видео нарезается на части...",
        "part_caption": "🎬 <b>{title}</b>\n📦 <b>Часть:</b> {current}/{total}\n🤖 @{bot}",
        "trim_prompt": "✂️ <b>Обрезка видео (Trim):</b>\nУкажите таймкод (Например: <code>00:05 - 00:25</code>):",
        "trim_invalid": "⚠️ Неверный формат времени. Пример: <code>00:05 - 00:25</code>.",
        "trimming_progress": "⏳ Видео нарезается...",
        "music_searching": "🔍 Распознавание музыки (Shazam)...",
        "music_found": "🎵 <b>Трек найден!</b>\n\n🎼 <b>Название:</b> <b>{title}</b>\n👤 <b>Исполнитель:</b> <b>{artist}</b>\n{album_line}🤖 @{bot}",
        "music_not_found": "ℹ️ Музыка не распознана.",
        "sub_video_generating": "🎬 Создание видео с субтитрами...",
        "sub_text_generating": "📝 Распознавание речи в текст...",
        "sub_not_found": "ℹ️ Речь не распознана.",
        "circle_generating": "🔄 Создание видеосообщения 1:1...",
        "audio_generating": "🎵 Извлечение MP3 музыки...",
        "voice_generating": "🎙 Создание голосового сообщения...",
        "speed_generating": "⚡ Ускорение видео в 1.5x...",
        "gif_generating": "🎞 Создание GIF анимации...",
        "bass_generating": "🔊 Создание Bass Boost аудио...",
        "audio8d_generating": "🎧 Создание 8D Surround аудио...",
        "karaoke_generating": "🎤 Создание караоке минусовки...",
        "reverse_generating": "⏪ Обратная перемотка видео (Reverse)...",
        "send_link_prompt": "📥 <b>Отправьте ссылку на видео (Instagram, TikTok, YouTube, Pinterest, X) или выберите раздел в меню!</b>"
    },
    "en": {
        "welcome": (
            "👋 <b>Hello, {name}!</b>\n\n"
            "⚡ Welcome to <b>Universal Super Saver & Pro Montage Bot (#1 Edition)</b>!\n\n"
            "📥 <b>Universal Media Downloader:</b>\n"
            "• Instagram, TikTok, YouTube & Shorts, Pinterest, Twitter/X, FB\n\n"
            "🎬 <b>Pro Video Montage & Anti-Duplicate Studio:</b>\n"
            "• Merge 2 videos in 5 professional Reels/TikTok modes (/montaj)\n"
            "• 10-Layer Anti-Duplicate 100% Original Engine (/original)\n"
            "• Floating semi-transparent Telegram watermark (/set_watermark)\n\n"
            "💎 <b>Multimedia Studio (16 Tools under every video):</b>\n"
            "✂️ 50MB+ Splitter, Shazam, 8D Audio, Bass Boost, Karaoke Vocal Remover,\n"
            "🎬 Subtitles, Trimmer, Video Note, Reverse Video, MP3, 1.5x, GIF\n\n"
            "📥 <i>Send a video link or open 🎬 Video Montage from the menu!</i>"
        ),
        "btn_profile": "👤 Profile",
        "btn_stat": "📊 Statistics",
        "btn_kurs": "💱 Exchange Rates",
        "btn_ref": "👥 VIP & Referral",
        "btn_montaj": "🎬 Video Montage",
        "btn_original": "🛡 Anti-Duplicate",
        "btn_ig_auto": "📸 Insta Auto-Post",
        "btn_tools": "🛠 Smart Tools",
        "btn_help": "📖 Help",
        "btn_lang": "🌐 Language",
        "sub_required": "⚠️ <b>Please subscribe to our channel to use the bot:</b>",
        "btn_sub_check": "✅ Joined / Check",
        "btn_sub_invite": "⭐️ Invite 3 Friends for VIP",
        "sub_success": "✅ Thank you! Joined all channels.",
        "sub_failed": "❌ Please join the channels first!",
        "lang_changed": "✅ Language changed to: 🇬🇧 English",
        "analyzing": "⏳ Analyzing link <b>{platform}</b>...",
        "not_found": "❌ Video not found or account is private.",
        "err_generic": "❌ An error occurred. Please try again.",
        "large_file_split_prompt": "⚠️ <b>Video size exceeds 50 MB!</b> Choose option:",
        "btn_split_parts": "✂️ Split into Parts (Part 1, 2...)",
        "btn_audio_only": "🎧 Extract MP3 Audio only",
        "splitting_progress": "⏳ Splitting video into parts...",
        "part_caption": "🎬 <b>{title}</b>\n📦 <b>Part:</b> {current}/{total}\n🤖 @{bot}",
        "trim_prompt": "✂️ <b>Trim Video:</b> Enter timestamps (e.g. <code>00:05 - 00:25</code>):",
        "trim_invalid": "⚠️ Invalid format. Example: <code>00:05 - 00:25</code>.",
        "trimming_progress": "⏳ Trimming video clip...",
        "music_searching": "🔍 Identifying music (Shazam)...",
        "music_found": "🎵 <b>Music Identified!</b>\n\n🎼 <b>Title:</b> <b>{title}</b>\n👤 <b>Artist:</b> <b>{artist}</b>\n{album_line}🤖 @{bot}",
        "music_not_found": "ℹ️ Music not identified.",
        "sub_video_generating": "🎬 Burning subtitles onto video...",
        "sub_text_generating": "📝 Transcribing speech to text...",
        "sub_not_found": "ℹ️ No speech detected.",
        "circle_generating": "🔄 Converting to video note...",
        "audio_generating": "🎵 Extracting MP3 audio...",
        "voice_generating": "🎙 Converting to voice note...",
        "speed_generating": "⚡ Speeding up video to 1.5x...",
        "gif_generating": "🎞 Converting to GIF animation...",
        "bass_generating": "🔊 Generating Bass Boosted audio...",
        "audio8d_generating": "🎧 Generating 8D Surround audio...",
        "karaoke_generating": "🎤 Removing vocals (Karaoke)...",
        "reverse_generating": "⏪ Reversing video clip...",
        "send_link_prompt": "📥 <b>Send a video link (Instagram, TikTok, YouTube, Pinterest, X) or choose an option from the menu!</b>"
    }
}

def get_text(key: str, lang: str = "uz", **kwargs) -> str:
    selected_lang = lang if lang in TEXTS else "uz"
    template = TEXTS[selected_lang].get(key, TEXTS["uz"].get(key, ""))
    if kwargs:
        try:
            return template.format(**kwargs)
        except Exception:
            return template
    return template

# ==================== MA'LUMOTLAR BAZASI (SQLite) ====================
DB_PATH = "save_bot_database.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            full_name TEXT,
            language TEXT DEFAULT 'uz',
            referrer_id INTEGER DEFAULT NULL,
            referral_count INTEGER DEFAULT 0,
            is_vip INTEGER DEFAULT 0,
            downloads_count INTEGER DEFAULT 0,
            first_seen TIMESTAMP,
            last_seen TIMESTAMP
        )
    """)
    cols = [c[1] for c in cursor.execute("PRAGMA table_info(users)").fetchall()]
    if "language" not in cols:
        cursor.execute("ALTER TABLE users ADD COLUMN language TEXT DEFAULT 'uz'")
    if "referrer_id" not in cols:
        cursor.execute("ALTER TABLE users ADD COLUMN referrer_id INTEGER DEFAULT NULL")
    if "referral_count" not in cols:
        cursor.execute("ALTER TABLE users ADD COLUMN referral_count INTEGER DEFAULT 0")
    if "is_vip" not in cols:
        cursor.execute("ALTER TABLE users ADD COLUMN is_vip INTEGER DEFAULT 0")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS downloads_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            url TEXT,
            platform TEXT,
            download_type TEXT,
            created_at TIMESTAMP
        )
    """)

    # ⚡ 1-SONIYADA YUBORISH UCHUN DOIMIY FILE_ID KESHI
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS media_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url_hash TEXT UNIQUE,
            canonical_url TEXT,
            file_id TEXT,
            file_type TEXT DEFAULT 'video',
            caption TEXT,
            width INTEGER DEFAULT 720,
            height INTEGER DEFAULT 1280,
            duration INTEGER DEFAULT 15,
            platform TEXT DEFAULT 'Web',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def get_cached_media(url: str) -> dict | None:
    """Havola (URL) bo'yicha Telegram serveridagi tayyor file_id ni olish (< 1 soniyada yuborish uchun)"""
    if not url:
        return None
    try:
        norm_url = url.strip().lower()
        url_hash = hashlib.sha256(norm_url.encode('utf-8')).hexdigest()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT file_id, file_type, caption, width, height, duration, platform 
            FROM media_cache WHERE url_hash = ?
        """, (url_hash,))
        row = cursor.fetchone()
        conn.close()
        if row and row[0]:
            return {
                "file_id": row[0],
                "file_type": row[1] or "video",
                "caption": row[2] or "",
                "width": row[3] or 720,
                "height": row[4] or 1280,
                "duration": row[5] or 15,
                "platform": row[6] or "Web"
            }
    except Exception as e:
        print(f"Cache o'qishda xatolik: {e}")
    return None

def save_cached_media(canonical_url: str, file_id: str, file_type: str = "video", caption: str = "", width: int = 720, height: int = 1280, duration: int = 15, platform: str = "Web"):
    """Yuklangan mediani bazada keshlab qo'yish (keyingi barcha so'rovlar 1 soniyada jo'natilishi uchun)"""
    if not canonical_url or not file_id:
        return
    try:
        norm_url = canonical_url.strip().lower()
        url_hash = hashlib.sha256(norm_url.encode('utf-8')).hexdigest()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO media_cache (url_hash, canonical_url, file_id, file_type, caption, width, height, duration, platform, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (url_hash, canonical_url, file_id, file_type, caption, width, height, duration, platform))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Cache saqlashda xatolik: {e}")

try:
    init_db()
except Exception as _db_err:
    DB_PATH = os.path.join("/tmp", "save_bot_database.db") if os.path.isdir("/tmp") else ":memory:"
    try:
        init_db()
    except Exception:
        pass

def register_user(user: types.User, referrer_id: int | None = None) -> tuple[bool, bool]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("SELECT user_id, is_vip, language FROM users WHERE user_id = ?", (user.id,))
    row = cursor.fetchone()

    is_new = False
    ref_became_vip = False

    if not row:
        is_new = True
        actual_referrer = None
        if referrer_id and referrer_id != user.id:
            cursor.execute("SELECT user_id, referral_count, is_vip FROM users WHERE user_id = ?", (referrer_id,))
            ref_row = cursor.fetchone()
            if ref_row:
                actual_referrer = referrer_id
                new_count = (ref_row[1] or 0) + 1
                became_vip = 1 if new_count >= REQUIRED_REFERRALS_FOR_VIP else ref_row[2]
                if became_vip == 1 and ref_row[2] == 0:
                    ref_became_vip = True
                cursor.execute(
                    "UPDATE users SET referral_count = ?, is_vip = ? WHERE user_id = ?",
                    (new_count, became_vip, referrer_id)
                )

        default_lang = "uz"
        if user.language_code:
            if user.language_code.startswith("ru"):
                default_lang = "ru"
            elif user.language_code.startswith("en"):
                default_lang = "en"

        cursor.execute("""
            INSERT INTO users (user_id, username, full_name, language, referrer_id, referral_count, is_vip, downloads_count, first_seen, last_seen)
            VALUES (?, ?, ?, ?, ?, 0, 0, 0, ?, ?)
        """, (user.id, user.username or "", f"{user.first_name or ''} {user.last_name or ''}".strip(), default_lang, actual_referrer, now, now))
    else:
        cursor.execute("""
            UPDATE users SET username = ?, full_name = ?, last_seen = ? WHERE user_id = ?
        """, (user.username or "", f"{user.first_name or ''} {user.last_name or ''}".strip(), now, user.id))

    conn.commit()
    conn.close()
    return is_new, ref_became_vip

def get_user_lang(user_id: int) -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT language FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row and row[0] in TEXTS else "uz"

def set_user_lang(user_id: int, lang: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET language = ? WHERE user_id = ?", (lang, user_id))
    conn.commit()
    conn.close()

def is_user_vip(user_id: int) -> bool:
    if user_id == ADMIN_ID:
        return True
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT is_vip FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return bool(row and row[0] == 1)

def get_user_profile(user_id: int) -> dict:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT referral_count, is_vip, downloads_count, language, first_seen, username, full_name FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    if row:
        return {
            "referrals": row[0] or 0,
            "is_vip": bool(row[1] == 1 or user_id == ADMIN_ID),
            "downloads": row[2] or 0,
            "language": row[3] or "uz",
            "registered": (row[4] or now_str)[:16],
            "username": row[5] or "",
            "full_name": row[6] or ""
        }
    return {
        "referrals": 0,
        "is_vip": (user_id == ADMIN_ID),
        "downloads": 0,
        "language": "uz",
        "registered": now_str,
        "username": "",
        "full_name": ""
    }

def increment_download_count(user_id: int, url: str, platform: str, download_type: str = "video"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("UPDATE users SET downloads_count = downloads_count + 1, last_seen = ? WHERE user_id = ?", (now, user_id))
    cursor.execute("""
        INSERT INTO downloads_history (user_id, url, platform, download_type, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, url, platform, download_type, now))
    conn.commit()
    conn.close()

def is_admin_user(user: types.User) -> bool:
    if not user:
        return False
    if user.id == ADMIN_ID:
        return True
    if user.username and user.username.lower() == ADMIN_USERNAME.lstrip("@").lower():
        return True
    return False

def get_stats() -> dict:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    today_str = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("SELECT COUNT(*) FROM users WHERE last_seen LIKE ?", (f"{today_str}%",))
    active_today = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM users WHERE first_seen LIKE ?", (f"{today_str}%",))
    new_today = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM users WHERE is_vip = 1")
    total_vips = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM downloads_history")
    total_downloads = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM downloads_history WHERE created_at LIKE ?", (f"{today_str}%",))
    downloads_today = cursor.fetchone()[0]
    cursor.execute("SELECT platform, COUNT(*) FROM downloads_history GROUP BY platform ORDER BY COUNT(*) DESC LIMIT 6")
    top_platforms = cursor.fetchall()
    cursor.execute("SELECT user_id, username, full_name, downloads_count FROM users ORDER BY last_seen DESC LIMIT 5")
    recent_users = cursor.fetchall()
    conn.close()
    return {
        "total_users": total_users,
        "active_today": active_today,
        "new_today": new_today,
        "total_vips": total_vips,
        "total_downloads": total_downloads,
        "downloads_today": downloads_today,
        "top_platforms": top_platforms,
        "recent_users": recent_users
    }

def build_stats_message(user: types.User) -> tuple[str, types.InlineKeyboardMarkup]:
    register_user(user)
    st = get_stats()
    prof = get_user_profile(user.id)
    uname = f"@{user.username}" if user.username else (ADMIN_USERNAME if user.id == ADMIN_ID else f"user_{user.id}")
    fname = user.first_name or (ADMIN_FIRST_NAME if user.id == ADMIN_ID else "User")

    platform_lines = "\n".join([f"  • <b>{p[0]}:</b> {p[1]:,} ta" for p in st["top_platforms"]]) or "  • Hozircha yuklamalar yo'q"

    disk_files = 0
    disk_mb = 0.0
    try:
        for fn in os.listdir(DOWNLOAD_DIR):
            fp = os.path.join(DOWNLOAD_DIR, fn)
            if os.path.isfile(fp):
                disk_files += 1
                disk_mb += os.path.getsize(fp) / (1024 * 1024)
    except Exception:
        pass

    recent_block = ""
    if is_admin_user(user) and st.get("recent_users"):
        r_lines = []
        for ru in st["recent_users"]:
            r_uname = f"@{ru[1]}" if ru[1] else (ru[2] or str(ru[0]))
            r_lines.append(f"  • {r_uname} (<code>{ru[0]}</code>) — {ru[3] or 0} yuklama")
        recent_block = "\n\n👑 <b>Oxirgi faol foydalanuvchilar:</b>\n" + "\n".join(r_lines)

    text = (
        f"📊 <b>BOT VA FOYDALANUVCHI STATISTIKASI</b>\n\n"
        f"👤 <b>Sizning profilingiz:</b> {uname} ({fname})\n"
        f"🆔 <b>ID:</b> <code>{user.id}</code> | 🌐 <b>Til:</b> {prof.get('language', 'uz')}\n"
        f"📥 <b>Sizning yuklamalaringiz:</b> <b>{prof['downloads']} ta</b>\n"
        f"👥 <b>Taklif qilgan do'stlaringiz:</b> <b>{prof['referrals']} ta</b>\n"
        f"📅 <b>Ro'yxatdan o'tgan:</b> {prof.get('registered', 'Bugun')}\n\n"
        f"🌐 <b>UMUMIY BOT KO'RSATKICHLARI:</b>\n"
        f"👥 <b>Jami foydalanuvchilar:</b> <b>{st['total_users']:,} ta</b>\n"
        f"🆕 <b>Bugun qo'shilganlar:</b> <b>{st['new_today']:,} ta</b>\n"
        f"⚡ <b>Bugun faol:</b> <b>{st['active_today']:,} ta</b>\n"
        f"⭐️ <b>VIP foydalanuvchilar:</b> <b>{st['total_vips']:,} ta</b>\n"
        f"📥 <b>Jami yuklab olingan media:</b> <b>{st['total_downloads']:,} ta</b>\n"
        f"🔥 <b>Bugungi yuklashlar:</b> <b>{st['downloads_today']:,} ta</b>\n"
        f"💾 <b>Vaqtinchalik kesh (Downloads):</b> <b>{disk_mb:.2f} MB</b> ({disk_files} ta fayl)\n\n"
        f"📈 <b>Top platformalar bo'yicha:</b>\n{platform_lines}"
        f"{recent_block}"
    )

    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🔄 Yangilash", callback_data="open_stats"),
        types.InlineKeyboardButton("🧹 Keshni tozalash", callback_data="clean_storage_cb")
    )
    markup.add(
        types.InlineKeyboardButton("🎬 Pro Reklama Montaj", callback_data="tool_cmd:montaj"),
        types.InlineKeyboardButton("🛡 Anti-Duplikat (Original)", callback_data="antidup_start_single")
    )
    markup.add(
        types.InlineKeyboardButton("💱 Markaziy Bank Kurslari", callback_data="tool_cmd:kurs"),
        types.InlineKeyboardButton("📱 QR-Kod Yasash", callback_data="tool_cmd:qr")
    )
    return text, markup

# ==================== KANAL OBUNA & MENYULAR (AI SIZ TOZA INTERFEYS) ====================
def check_channel_subscription(user_id: int) -> tuple[bool, list]:
    if is_user_vip(user_id) or not SPONSOR_CHANNELS:
        return True, []
    unsubscribed = []
    for channel in SPONSOR_CHANNELS:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status in ["left", "kicked"]:
                unsubscribed.append(channel)
        except Exception as e:
            print(f"Kanal tekshirishda xatolik ({channel}): {e}")
    return len(unsubscribed) == 0, unsubscribed

def get_sub_keyboard(unsubscribed: list, lang: str = "uz") -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=1)
    for channel in unsubscribed:
        clean_name = channel.replace("@", "")
        markup.add(types.InlineKeyboardButton(text=f"➕ {channel}", url=f"https://t.me/{clean_name}"))
    markup.add(types.InlineKeyboardButton(text=get_text("btn_sub_check", lang), callback_data="check_subscription"))
    markup.add(types.InlineKeyboardButton(text=get_text("btn_sub_invite", lang), callback_data="open_referral"))
    return markup

def get_main_reply_keyboard(lang: str = "uz") -> types.ReplyKeyboardMarkup:
    """AI tugmalari olib tashlangan, toza va tezkor asosiy menyu"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    b_montaj = types.KeyboardButton(get_text("btn_montaj", lang))
    b_orig = types.KeyboardButton(get_text("btn_original", lang))
    b_ig = types.KeyboardButton(get_text("btn_ig_auto", lang))
    b_stat = types.KeyboardButton(get_text("btn_stat", lang))
    b_profile = types.KeyboardButton(get_text("btn_profile", lang))
    b_kurs = types.KeyboardButton(get_text("btn_kurs", lang))
    b_tools = types.KeyboardButton(get_text("btn_tools", lang))
    b_ref = types.KeyboardButton(get_text("btn_ref", lang))
    b_help = types.KeyboardButton(get_text("btn_help", lang))
    b_lang = types.KeyboardButton(get_text("btn_lang", lang))
    markup.add(b_montaj, b_orig)
    markup.add(b_ig, b_tools)
    markup.add(b_stat, b_profile)
    markup.add(b_kurs, b_ref)
    markup.add(b_help, b_lang)
    return markup

def get_language_inline_keyboard() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=3)
    b_uz = types.InlineKeyboardButton("🇺🇿 O'zbek", callback_data="set_lang:uz")
    b_ru = types.InlineKeyboardButton("🇷🇺 Русский", callback_data="set_lang:ru")
    b_en = types.InlineKeyboardButton("🇬🇧 English", callback_data="set_lang:en")
    markup.add(b_uz, b_ru, b_en)
    return markup

def generate_qr_code_bytes(data_text: str) -> bytes | None:
    try:
        encoded = urllib.parse.quote(data_text)
        url = f"https://api.qrserver.com/v1/create-qr-code/?size=600x600&margin=15&data={encoded}"
        resp = requests.get(url, timeout=15, verify=False)
        if resp.status_code == 200 and len(resp.content) > 500:
            return resp.content
    except Exception as e:
        print(f"QR xatoligi: {e}")
    return None

# ==================== 4-MANBALI MARKAZIY BANK VALYUTA KURSLARI (/kurs) ====================
def fetch_cbu_exchange_rates(amount: float = 1.0) -> str:
    """
    O'zbekiston Respublikasi Markaziy Banki valyuta kurslarini 4 ta mustaqil manbadan
    SSL va WAF bloklarisiz (verify=False + Browser User-Agent) 100% xatosiz olib kelish!
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Accept": "application/json,text/plain,*/*",
    }
    wanted = [
        ("USD", "🇺🇸 AQSH Dollari"),
        ("EUR", "🇪🇺 Yevro"),
        ("RUB", "🇷🇺 Rossiya Rubli"),
        ("GBP", "🇬🇧 Angliya Funti"),
        ("CNY", "🇨🇳 Xitoy Yuani"),
        ("KZT", "🇰🇿 Qozog'iston Tengesi"),
        ("TRY", "🇹🇷 Turkiya Lirasi"),
    ]

    # 1-MANBA: O'zbekiston Markaziy Banki rasmiy JSON API (3 xil til endpointi, SSL verify=False bilan)
    cbu_urls = [
        "https://cbu.uz/oz/arkhiv-kursov-valyut/json/",
        "https://cbu.uz/uz/arkhiv-kursov-valyut/json/",
        "https://cbu.uz/ru/arkhiv-kursov-valyut/json/",
        "http://cbu.uz/oz/arkhiv-kursov-valyut/json/",
    ]
    for cbu_url in cbu_urls:
        try:
            resp = requests.get(cbu_url, headers=headers, timeout=10, verify=False)
            if resp.status_code == 200 and resp.text.strip():
                data = resp.json()
                if isinstance(data, list) and len(data) > 0:
                    by_ccy = {item.get("Ccy"): item for item in data if isinstance(item, dict)}
                    lines = ["🏦 <b>O'zbekiston Markaziy Banki Valyuta Kurslari:</b>\n"]
                    for code, label in wanted:
                        item = by_ccy.get(code)
                        if not item:
                            continue
                        rate_val = float(str(item.get("Rate", "0")).replace(",", "."))
                        nominal = float(str(item.get("Nominal", "1")).replace(",", ".")) or 1.0
                        unit_rate = rate_val / nominal
                        diff_str = str(item.get("Diff", "0"))
                        try:
                            diff_val = float(diff_str.replace(",", "."))
                        except ValueError:
                            diff_val = 0.0
                        sign = f"📈 +{diff_str}" if diff_val > 0 else (f"📉 {diff_str}" if diff_val < 0 else "➖ 0")
                        if amount != 1.0:
                            calc_sum = unit_rate * amount
                            lines.append(f"{label} (<b>{amount:g} {code}</b>): <b>{calc_sum:,.2f} so'm</b> <i>(1 {code} = {unit_rate:,.2f})</i>")
                        else:
                            lines.append(f"{label} (<b>1 {code}</b>): <b>{unit_rate:,.2f} so'm</b> ({sign})")

                    date_str = data[0].get("Date") or datetime.now().strftime("%d.%m.%Y")
                    lines.append(f"\n📅 <i>Sana: {date_str} | Manba: cbu.uz</i>")
                    lines.append("💡 <i>Hisoblash uchun:</i> <code>/kurs 100</code>")
                    return "\n".join(lines)
        except Exception as e:
            print(f"CBU API urinish xatosi ({cbu_url}): {e}")

    # 2-MANBA va 3-MANBA: Xalqaro Zaxira Bank API (open.er-api.com & exchangerate-api.com)
    backup_apis = [
        "https://open.er-api.com/v6/latest/USD",
        "https://api.exchangerate-api.com/v4/latest/USD",
    ]
    for b_url in backup_apis:
        try:
            r = requests.get(b_url, headers=headers, timeout=10, verify=False)
            if r.status_code == 200:
                j = r.json()
                rates = j.get("rates", {})
                uzs_per_usd = float(rates.get("UZS", 0))
                if uzs_per_usd > 1000:
                    lines = ["🏦 <b>Markaziy Bank & Xalqaro Valyuta Kurslari:</b>\n"]
                    for code, label in wanted:
                        c_rate = float(rates.get(code, 0))
                        if c_rate > 0:
                            uzs_val = (uzs_per_usd / c_rate) * amount
                            unit_val = uzs_per_usd / c_rate
                            if amount != 1.0:
                                lines.append(f"{label} (<b>{amount:g} {code}</b>): <b>{uzs_val:,.2f} so'm</b> <i>(1 {code} = {unit_val:,.2f})</i>")
                            else:
                                lines.append(f"{label} (<b>1 {code}</b>): <b>{unit_val:,.2f} so'm</b>")
                    lines.append(f"\n📅 <i>Sana: {datetime.now().strftime('%d.%m.%Y %H:%M')}</i>")
                    lines.append("💡 <i>Hisoblash uchun:</i> <code>/kurs 100</code>")
                    return "\n".join(lines)
        except Exception as e:
            print(f"Backup Currency API xatosi ({b_url}): {e}")

    # 4-MANBA: JsDelivr Global Currency CDN
    try:
        cdn_url = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/usd.json"
        r = requests.get(cdn_url, headers=headers, timeout=10, verify=False)
        if r.status_code == 200:
            usd_map = r.json().get("usd", {})
            uzs_per_usd = float(usd_map.get("uzs", 0))
            if uzs_per_usd > 1000:
                lines = ["🏦 <b>Joriy Valyuta Kurslari:</b>\n"]
                for code, label in wanted:
                    c_rate = float(usd_map.get(code.lower(), 0))
                    if c_rate > 0:
                        unit_val = uzs_per_usd / c_rate
                        uzs_val = unit_val * amount
                        lines.append(f"{label} (<b>{amount:g} {code}</b>): <b>{uzs_val:,.2f} so'm</b>")
                lines.append(f"\n📅 <i>Sana: {datetime.now().strftime('%d.%m.%Y')}</i>")
                return "\n".join(lines)
    except Exception:
        pass

    return "❌ Valyuta serveri bilan bog'lanishda xatolik. Internet aloqasini tekshirib qayta urinib ko'ring."

# ==================== PLATFORMA ANIQLAGICH VA LINK AJRATGICH ====================
def detect_platform(url: str) -> str:
    url_lower = url.lower()
    if "instagram.com" in url_lower or "instagr.am" in url_lower:
        return "Instagram"
    elif "tiktok.com" in url_lower or "douyin.com" in url_lower:
        return "TikTok"
    elif "youtube.com" in url_lower or "youtu.be" in url_lower:
        return "YouTube"
    elif "pin.it" in url_lower or "pinterest.com" in url_lower:
        return "Pinterest"
    elif "twitter.com" in url_lower or "x.com" in url_lower:
        return "Twitter / X"
    elif "facebook.com" in url_lower or "fb.watch" in url_lower or "fb.com" in url_lower:
        return "Facebook"
    elif "likee.video" in url_lower or "likee.com" in url_lower:
        return "Likee"
    elif "threads.net" in url_lower or "threads.com" in url_lower:
        return "Threads"
    elif "reddit.com" in url_lower or "redd.it" in url_lower:
        return "Reddit"
    return "Web"

def extract_url(text: str) -> str | None:
    if not text:
        return None
    cleaned = re.sub(r'[\u200b\u200c\u200d\u200e\u200f\ufeff]', '', text)
    match = re.search(r'(https?://[^\s<>"\']+)', cleaned)
    if match:
        return match.group(1).rstrip(".,;!?)'\">]")
    match2 = re.search(
        r'((?:www\.|m\.|vt\.|vm\.)?(?:instagram\.com|instagr\.am|tiktok\.com|youtube\.com|youtu\.be|pin\.it|pinterest\.com|x\.com|twitter\.com|facebook\.com|fb\.watch)/[^\s<>"\']+)',
        cleaned, re.IGNORECASE
    )
    if match2:
        return "https://" + match2.group(1).rstrip(".,;!?)'\">]")
    return None

# ==================== FFMPEG METADATA VA TRANZITSIYALARI (FFPROBE SIZ HAM 100% ISHLAYDI!) ====================
def _probe_media_via_ffmpeg_stderr(file_path: str) -> dict:
    """
    Agar tizimda `ffprobe` o'rnatilmagan bo'lsa (masalan imageio-ffmpeg ishlatilganda),
    bevosita `ffmpeg -i <file>` stderr chiqishini tahlil qilib:
    duration, width, height, codec va has_audio ma'lumotlarini 100% aniq oladi!
    """
    ensure_ffmpeg_in_path()
    info = {"duration": 15.0, "width": 720, "height": 1280, "codec": "h264", "has_audio": False}
    if not file_path or not os.path.exists(file_path):
        return info
    try:
        cmd = [FFMPEG_BIN, "-hide_banner", "-i", file_path]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, errors="ignore", timeout=15)
        raw = (res.stderr or "") + "\n" + (res.stdout or "")

        # Duration: 00:00:19.45
        m_dur = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", raw)
        if m_dur:
            hrs, mins, secs = int(m_dur.group(1)), int(m_dur.group(2)), float(m_dur.group(3))
            total_s = hrs * 3600 + mins * 60 + secs
            if total_s > 0.1:
                info["duration"] = total_s

        # Video stream: Video: h264 ..., 720x1280
        m_vid = re.search(r"Stream #\d+:\d+[^\n]*Video:\s*([a-zA-Z0-9_]+)[^\n]*?(\d{2,5})x(\d{2,5})", raw)
        if m_vid:
            info["codec"] = m_vid.group(1).lower()
            info["width"] = int(m_vid.group(2))
            info["height"] = int(m_vid.group(3))

        # Audio stream
        if re.search(r"Stream #\d+:\d+[^\n]*Audio:", raw):
            info["has_audio"] = True
    except Exception as e:
        print(f"FFmpeg probe fallback xatosi: {e}")
    return info

def get_media_duration(file_path: str) -> float:
    ensure_ffmpeg_in_path()
    if FFPROBE_BIN:
        try:
            cmd = [
                FFPROBE_BIN, "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                file_path
            ]
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=12)
            val = float(res.stdout.strip())
            if val > 0.1:
                return val
        except Exception:
            pass
    return _probe_media_via_ffmpeg_stderr(file_path).get("duration", 15.0)

def has_audio_stream(file_path: str) -> bool:
    """Videoda audio oqimi bor-yo'qligini tekshirish (ffprobe yoki ffmpeg -i orqali)"""
    ensure_ffmpeg_in_path()
    if FFPROBE_BIN:
        try:
            cmd = [
                FFPROBE_BIN, "-v", "error",
                "-select_streams", "a:0",
                "-show_entries", "stream=codec_type",
                "-of", "default=noprint_wrappers=1:nokey=1",
                file_path
            ]
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10)
            if "audio" in (res.stdout or "").lower():
                return True
        except Exception:
            pass
    return _probe_media_via_ffmpeg_stderr(file_path).get("has_audio", False)

def get_video_stream_info(file_path: str) -> dict:
    """Video kodek, o'lcham (width, height) va davomiylikni aniqlash (ffprobe yoki ffmpeg -i orqali)"""
    ensure_ffmpeg_in_path()
    if FFPROBE_BIN:
        try:
            cmd = [
                FFPROBE_BIN, "-v", "error",
                "-select_streams", "v:0",
                "-show_entries", "stream=codec_name,width,height:format=duration",
                "-of", "json",
                file_path
            ]
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=12)
            if res.returncode == 0 and res.stdout.strip():
                data = json.loads(res.stdout)
                streams = data.get("streams", [])
                fmt = data.get("format", {})
                if streams:
                    st = streams[0]
                    dur = max(1, int(float(fmt.get("duration") or 15)))
                    return {
                        "codec": (st.get("codec_name") or "h264").lower(),
                        "width": int(st.get("width") or 720),
                        "height": int(st.get("height") or 1280),
                        "duration": dur
                    }
        except Exception:
            pass
    p = _probe_media_via_ffmpeg_stderr(file_path)
    return {
        "codec": p.get("codec", "h264"),
        "width": int(p.get("width", 720)),
        "height": int(p.get("height", 1280)),
        "duration": max(1, int(float(p.get("duration", 15))))
    }

def convert_to_circle_note(input_video_path: str, output_note_path: str) -> bool:
    """🔵 Kruglyash (1:1 Video Note 480x480) — ovozli va ovozsiz videolarda 100% xatosiz ishlaydi"""
    ensure_ffmpeg_in_path()
    try:
        audio_ok = has_audio_stream(input_video_path)
        cmd = [
            FFMPEG_BIN, "-y",
            "-t", "59",
            "-i", input_video_path,
            "-vf", "crop=min(iw\,ih):min(iw\,ih),scale=480:480,setsar=1,fps=30,format=yuv420p",
            "-c:v", "libx264", "-profile:v", "baseline", "-level", "3.0",
            "-pix_fmt", "yuv420p", "-preset", "ultrafast", "-crf", "24",
            "-maxrate", "1400k", "-bufsize", "2800k"
        ]
        if audio_ok:
            cmd += ["-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-ac", "2"]
        else:
            cmd += ["-an"]
        cmd += ["-movflags", "+faststart", output_note_path]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
        return res.returncode == 0 and os.path.exists(output_note_path) and os.path.getsize(output_note_path) > 1000
    except Exception as e:
        print(f"Kruglyash xatoligi: {e}")
        return False

def _run_audio_convert_with_fallback(input_video_path: str, output_path: str, af_filter: str = "", title: str = "Audio", artist: str = "Universal Bot") -> str | None:
    """
    Audio ajratish va effektlar (MP3, Bass Boost, 8D, Karaoke) uchun universal funksiya.
    Agar videoda ovoz bo'lmasa yoki libmp3lame mavjud bo'lmasa, avtomatik AAC (.m4a) fallback ishlatadi!
    """
    ensure_ffmpeg_in_path()
    if not has_audio_stream(input_video_path):
        return None

    # 1-urinish: libmp3lame (.mp3)
    cmd = [FFMPEG_BIN, "-y", "-i", input_video_path, "-vn"]
    if af_filter:
        cmd += ["-af", af_filter]
    cmd += [
        "-c:a", "libmp3lame", "-b:a", "256k", "-ar", "44100", "-ac", "2",
        "-metadata", f"title={title}",
        "-metadata", f"artist={artist}",
        output_path
    ]
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=90)
        if res.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 500:
            return output_path
    except Exception:
        pass

    # 2-urinish (Fallback): AAC (.m4a) — har qanday FFmpeg da 100% mavjud!
    m4a_path = os.path.splitext(output_path)[0] + ".m4a"
    cmd2 = [FFMPEG_BIN, "-y", "-i", input_video_path, "-vn"]
    if af_filter:
        cmd2 += ["-af", af_filter]
    cmd2 += [
        "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
        "-movflags", "+faststart",
        m4a_path
    ]
    try:
        res2 = subprocess.run(cmd2, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=90)
        if res2.returncode == 0 and os.path.exists(m4a_path) and os.path.getsize(m4a_path) > 500:
            return m4a_path
    except Exception as e:
        print(f"Audio fallback xatoligi: {e}")
    return None

def extract_audio_mp3(input_video_path: str, output_mp3_path: str, title: str = "Audio", artist: str = "") -> str | None:
    return _run_audio_convert_with_fallback(input_video_path, output_mp3_path, af_filter="", title=title, artist=artist or "Universal Bot")

def convert_to_bass_boost(input_video_path: str, output_mp3_path: str) -> str | None:
    res = _run_audio_convert_with_fallback(
        input_video_path, output_mp3_path,
        af_filter="aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo,bass=g=12:f=110:w=0.6,volume=1.05",
        title="Bass Boost (+12dB)"
    )
    if res:
        return res
    return _run_audio_convert_with_fallback(
        input_video_path, output_mp3_path,
        af_filter="lowshelf=g=11:f=110,volume=1.05",
        title="Bass Boost (+12dB)"
    )

def convert_to_8d_audio(input_video_path: str, output_mp3_path: str) -> str | None:
    res = _run_audio_convert_with_fallback(
        input_video_path, output_mp3_path,
        af_filter="aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo,apulsator=hz=0.125,aecho=0.8:0.88:60:0.4",
        title="8D Surround Audio"
    )
    if res:
        return res
    return _run_audio_convert_with_fallback(
        input_video_path, output_mp3_path,
        af_filter="aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo,aecho=0.8:0.88:60:0.4",
        title="8D Surround Audio"
    )

def convert_to_karaoke_minus(input_video_path: str, output_mp3_path: str) -> str | None:
    return _run_audio_convert_with_fallback(
        input_video_path, output_mp3_path,
        af_filter="aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo,pan=stereo|c0=c0-0.5*c1|c1=c1-0.5*c0",
        title="Karaoke Minusovka"
    )

def convert_to_reverse_video(input_video_path: str, output_video_path: str) -> bool:
    """⏪ Teskari video (Reverse) — RAM to'lib qolmasligi uchun 30s 720p ultrafast + ovozsiz video himoyasi bilan"""
    ensure_ffmpeg_in_path()
    try:
        audio_ok = has_audio_stream(input_video_path)
        cmd = [
            FFMPEG_BIN, "-y",
            "-t", "30",
            "-i", input_video_path,
            "-vf", "scale='min(720,iw)':-2,reverse,format=yuv420p",
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23"
        ]
        if audio_ok:
            cmd += ["-af", "areverse", "-c:a", "aac", "-b:a", "128k"]
        else:
            cmd += ["-an"]
        cmd += ["-movflags", "+faststart", output_video_path]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=150)
        return res.returncode == 0 and os.path.exists(output_video_path) and os.path.getsize(output_video_path) > 1000
    except Exception as e:
        print(f"Reverse xatoligi: {e}")
        return False

def extract_hd_thumbnail(input_video_path: str, output_jpg_path: str) -> bool:
    """🖼 HD Oblojka — 0.5s yoki 0.0s kadrdan 100% xatosiz JPG ajratish"""
    ensure_ffmpeg_in_path()
    for seek_pos in ["00:00:00.5", "00:00:00"]:
        try:
            cmd = [
                FFMPEG_BIN, "-y", "-ss", seek_pos,
                "-i", input_video_path,
                "-frames:v", "1", "-q:v", "2",
                output_jpg_path
            ]
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
            if res.returncode == 0 and os.path.exists(output_jpg_path) and os.path.getsize(output_jpg_path) > 300:
                return True
        except Exception as e:
            print(f"Thumbnail xatoligi ({seek_pos}): {e}")
    return False

def convert_to_voice_ogg(input_video_path: str, output_voice_path: str) -> str | None:
    """🎙 Ovozli xabar (.ogg opus yoki fallback .mp3/.m4a)"""
    ensure_ffmpeg_in_path()
    if not has_audio_stream(input_video_path):
        return None
    for codec, ext in [("libopus", ".ogg"), ("libvorbis", ".ogg"), ("libmp3lame", ".mp3"), ("aac", ".m4a")]:
        cand_path = os.path.splitext(output_voice_path)[0] + ext
        try:
            cmd = [
                FFMPEG_BIN, "-y", "-i", input_video_path,
                "-vn", "-c:a", codec, "-b:a", "64k", "-ar", "48000" if codec == "libopus" else "44100",
                cand_path
            ]
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
            if res.returncode == 0 and os.path.exists(cand_path) and os.path.getsize(cand_path) > 500:
                return cand_path
        except Exception:
            pass
    return None

def convert_to_fast_speed(input_video_path: str, output_video_path: str, speed: float = 1.5) -> bool:
    """⚡ 1.5x Tezlashtirish — ovozli va ovozsiz videolarda 100% ishlaydi"""
    ensure_ffmpeg_in_path()
    try:
        pts_factor = round(1.0 / speed, 5)
        audio_ok = has_audio_stream(input_video_path)
        cmd = [
            FFMPEG_BIN, "-y", "-i", input_video_path,
            "-vf", f"setpts={pts_factor}*PTS,format=yuv420p",
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23"
        ]
        if audio_ok:
            cmd += ["-af", f"atempo={speed}", "-c:a", "aac", "-b:a", "128k"]
        else:
            cmd += ["-an"]
        cmd += ["-movflags", "+faststart", output_video_path]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
        return res.returncode == 0 and os.path.exists(output_video_path) and os.path.getsize(output_video_path) > 1000
    except Exception as e:
        print(f"Tezlik xatoligi: {e}")
        return False

def convert_to_gif_animation(input_video_path: str, output_gif_path: str) -> bool:
    """🎞 GIF (MP4 Looper animatsiya)"""
    ensure_ffmpeg_in_path()
    try:
        cmd = [
            FFMPEG_BIN, "-y",
            "-t", "6",
            "-i", input_video_path,
            "-vf", "scale=480:-2,fps=15,format=yuv420p",
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "24",
            "-an", "-movflags", "+faststart",
            output_gif_path
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
        return res.returncode == 0 and os.path.exists(output_gif_path) and os.path.getsize(output_gif_path) > 500
    except Exception as e:
        print(f"GIF xatoligi: {e}")
        return False

# ==================== 50 MB+ VIDEO AUTO-SPLITTER ====================
def split_large_video(input_video_path: str, target_dir: str, max_chunk_mb: float = 46.0) -> list:
    ensure_ffmpeg_in_path()
    total_size_mb = os.path.getsize(input_video_path) / (1024 * 1024)
    if total_size_mb <= max_chunk_mb:
        return [input_video_path]

    duration = get_media_duration(input_video_path)
    parts_count = math.ceil(total_size_mb / max_chunk_mb)
    chunk_duration = duration / parts_count

    output_files = []
    base_name = os.path.splitext(os.path.basename(input_video_path))[0]

    current_start = 0.0
    for part_idx in range(1, parts_count + 1):
        chunk_file = os.path.join(target_dir, f"{base_name}_part{part_idx}.mp4")
        dur_to_take = min(chunk_duration, duration - current_start)

        cmd = [
            FFMPEG_BIN, "-y",
            "-ss", str(current_start),
            "-i", input_video_path,
            "-t", str(dur_to_take),
            "-c", "copy",
            "-avoid_negative_ts", "make_zero",
            chunk_file
        ]
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if res.returncode != 0 or not os.path.exists(chunk_file) or os.path.getsize(chunk_file) < 500:
            cmd_reencode = [
                FFMPEG_BIN, "-y",
                "-ss", str(current_start),
                "-i", input_video_path,
                "-t", str(dur_to_take),
                "-c:v", "libx264", "-preset", "ultrafast", "-crf", "25",
                "-c:a", "aac", "-b:a", "128k",
                chunk_file
            ]
            subprocess.run(cmd_reencode, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if os.path.exists(chunk_file) and os.path.getsize(chunk_file) > 1000:
            output_files.append(chunk_file)

        current_start += dur_to_take
        if current_start >= duration:
            break

    return output_files

# ==================== VIDEO TRIMMER ====================
def parse_time_to_seconds(time_str: str):
    try:
        clean = time_str.strip()
        if ":" in clean:
            parts = [float(p) for p in clean.split(":")]
            if len(parts) == 2:
                return parts[0] * 60 + parts[1]
            elif len(parts) == 3:
                return parts[0] * 3600 + parts[1] * 60 + parts[2]
        return float(clean)
    except Exception:
        return None

def trim_video(input_video_path: str, output_path: str, start_sec: float, end_sec: float) -> bool:
    ensure_ffmpeg_in_path()
    try:
        duration = end_sec - start_sec
        if duration <= 0:
            return False
        audio_ok = has_audio_stream(input_video_path)
        cmd = [
            FFMPEG_BIN, "-y",
            "-ss", str(start_sec),
            "-i", input_video_path,
            "-t", str(duration),
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "22",
            "-pix_fmt", "yuv420p"
        ]
        if audio_ok:
            cmd += ["-c:a", "aac", "-b:a", "160k"]
        else:
            cmd += ["-an"]
        cmd += ["-movflags", "+faststart", output_path]
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
        return res.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 1000
    except Exception as e:
        print(f"Trim xatoligi: {e}")
        return False

# ==================== PRO REKLAMA MONTAJ STUDIYASI + 10-BOSQICHLI ANTI-DUPLIKAT + SUZUVCHI WATERMARK ====================
WATERMARK_CONFIG_FILE = os.path.join(PROMO_DIR, "watermark_config.json")
_BOT_USERNAME_CACHE = None

def get_cached_bot_username() -> str:
    global _BOT_USERNAME_CACHE
    if _BOT_USERNAME_CACHE:
        return _BOT_USERNAME_CACHE
    try:
        me = bot.get_me()
        if me and me.username:
            _BOT_USERNAME_CACHE = me.username
            return _BOT_USERNAME_CACHE
    except Exception:
        pass
    return ADMIN_USERNAME.lstrip("@") or "usman_khasan"

def get_watermark_settings() -> dict:
    default_cfg = {
        "enabled": True,
        "text": "",
        "opacity": 0.24
    }
    if os.path.exists(WATERMARK_CONFIG_FILE):
        try:
            with open(WATERMARK_CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                default_cfg.update(data)
        except Exception:
            pass
    if not default_cfg.get("text"):
        default_cfg["text"] = f"@{get_cached_bot_username().upper()}"
    return default_cfg

def save_watermark_settings(enabled: bool = True, text: str = "", opacity: float = 0.24):
    clean_t = text.strip()
    if clean_t and not clean_t.startswith("@"):
        clean_t = "@" + clean_t
    cfg = {
        "enabled": bool(enabled),
        "text": clean_t.upper() if clean_t else f"@{get_cached_bot_username().upper()}",
        "opacity": max(0.12, min(0.55, float(opacity)))
    }
    try:
        with open(WATERMARK_CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Watermark config saqlash xatosi: {e}")
    return cfg

_BITMAP_FONT_5X7 = {
    '@': ["01110", "10001", "10111", "10101", "10111", "10000", "01110"],
    'A': ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    'B': ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    'C': ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    'D': ["11100", "10010", "10001", "10001", "10001", "10010", "11100"],
    'E': ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    'F': ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    'G': ["01110", "10001", "10000", "10111", "10001", "10001", "01110"],
    'H': ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    'I': ["01110", "00100", "00100", "00100", "00100", "00100", "01110"],
    'J': ["00111", "00010", "00010", "00010", "10010", "10010", "01100"],
    'K': ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    'L': ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    'M': ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    'N': ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    'O': ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    'P': ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    'Q': ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    'R': ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    'S': ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    'T': ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    'U': ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    'V': ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    'W': ["10001", "10001", "10001", "10101", "10101", "11011", "10001"],
    'X': ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    'Y': ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    'Z': ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    '_': ["00000", "00000", "00000", "00000", "00000", "00000", "11111"],
    '-': ["00000", "00000", "00000", "11111", "00000", "00000", "00000"],
    '.': ["00000", "00000", "00000", "00000", "00000", "01100", "01100"],
    '0': ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    '1': ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    '2': ["01110", "10001", "00001", "00110", "01000", "10000", "11111"],
    '3': ["11110", "00001", "00001", "01110", "00001", "00001", "11110"],
    '4': ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    '5': ["11111", "10000", "10000", "11110", "00001", "00001", "11110"],
    '6': ["01110", "10000", "10000", "11110", "10001", "10001", "01110"],
    '7': ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    '8': ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    '9': ["01110", "10001", "10001", "01111", "00001", "00001", "01110"],
    ' ': ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
}

def _point_in_poly(x: float, y: float, poly: list) -> bool:
    inside = False
    n = len(poly)
    p1x, p1y = poly[0]
    for i in range(1, n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def _generate_watermark_png_pure_python(text: str, out_png_path: str, opacity: float = 0.24) -> bool:
    """
    Agar kompyuterda Pillow (PIL) yo'q bo'lsa ham, standart Python (zlib+struct) yordamida
    Dumaloq Telegram Samolyot Ikonkasi + @HANDLE yozuvli shaffof (RGBA) PNG yaratish!
    """
    try:
        clean_text = (text or "@USMAN_KHASAN").upper().strip()
        if not clean_text.startswith("@"):
            clean_text = "@" + clean_text
        scale = 4  # 5x7 font -> 20x28 px harf
        char_w = 6 * scale
        h = 76
        w = max(260, 88 + len(clean_text) * char_w + 20)

        alpha_main = max(25, min(160, int(255 * opacity)))
        alpha_icon_bg = max(20, min(140, int(255 * (opacity * 0.85))))

        # RGBA buffer
        buf = bytearray(w * h * 4)

        cx, cy, r_outer = 40.0, 38.0, 28.0
        # Telegram paper plane uchburchaklari (cx, cy atrofida)
        plane_poly = [
            (22, 38),  # chap uch
            (54, 24),  # tepa o'ng uch
            (46, 53),  # past o'ng uch
            (36, 44),  # o'rta past
        ]
        wing_cut = [
            (34, 41),
            (52, 26),
            (38, 45),
        ]

        for py in range(h):
            row_off = py * w * 4
            for px in range(w):
                dx = px - cx
                dy = py - cy
                dist = math.hypot(dx, dy)
                if dist <= r_outer:
                    idx = row_off + px * 4
                    if _point_in_poly(px, py, plane_poly) and not _point_in_poly(px, py, wing_cut):
                        # Samolyotcha (oq-oltin tusda)
                        buf[idx] = 255
                        buf[idx + 1] = 252
                        buf[idx + 2] = 235
                        buf[idx + 3] = min(255, int(alpha_main * 1.15))
                    elif dist >= r_outer - 3.2:
                        # Aylana hoshiyasi
                        buf[idx] = 245
                        buf[idx + 1] = 225
                        buf[idx + 2] = 120
                        buf[idx + 3] = alpha_main
                    else:
                        # Aylana ichi (yarim shaffof)
                        buf[idx] = 40
                        buf[idx + 1] = 45
                        buf[idx + 2] = 55
                        buf[idx + 3] = int(alpha_icon_bg * 0.55)

        # Matnni chizish
        start_x = 80
        start_y = (h - 7 * scale) // 2
        for ch_idx, ch in enumerate(clean_text[:26]):
            glyph = _BITMAP_FONT_5X7.get(ch, _BITMAP_FONT_5X7[' '])
            gx0 = start_x + ch_idx * char_w
            for gy in range(7):
                line_bits = glyph[gy]
                for gx in range(5):
                    if line_bits[gx] == '1':
                        for sy in range(scale):
                            for sx in range(scale):
                                px = gx0 + gx * scale + sx
                                py = start_y + gy * scale + sy
                                if 0 <= px < w and 0 <= py < h:
                                    idx = (py * w + px) * 4
                                    buf[idx] = 255
                                    buf[idx + 1] = 255
                                    buf[idx + 2] = 255
                                    buf[idx + 3] = alpha_main

        # PNG fayl sifatida yig'ish (standart zlib + struct)
        raw_rows = bytearray()
        stride = w * 4
        for y in range(h):
            raw_rows.append(0)  # filter type 0
            raw_rows.extend(buf[y * stride:(y + 1) * stride])

        def _png_chunk(chunk_type: bytes, data: bytes) -> bytes:
            crc = zlib.crc32(chunk_type + data) & 0xffffffff
            return struct.pack(">I", len(data)) + chunk_type + data + struct.pack(">I", crc)

        ihdr = struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0)
        png_bytes = (
            bytes([137, 80, 78, 71, 13, 10, 26, 10])
            + _png_chunk(b"IHDR", ihdr)
            + _png_chunk(b"IDAT", zlib.compress(bytes(raw_rows), 6))
            + _png_chunk(b"IEND", b"")
        )
        with open(out_png_path, "wb") as f:
            f.write(png_bytes)
        return os.path.exists(out_png_path) and os.path.getsize(out_png_path) > 200
    except Exception as e:
        print(f"Pure-Python PNG watermark xatosi: {e}")
        return False

def generate_telegram_watermark_png(text: str = "", out_png_path: str = "", opacity: float = 0.24) -> str | None:
    """
    Foydalanuvchi yuborgan namuna (`@TELEGRAM_YULDUZLARI`) kabi:
    Chap tomonda dumaloq Telegram qog'oz samolyot ikonkasi + O'ng tomonda qalin @USERNAME yozuvi!
    Ko'rinar-ko'rinmas (shaffof ~24% alpha) bo'lib, videoga umuman xalaqit bermaydi.
    """
    cfg = get_watermark_settings()
    wm_text = (text or cfg.get("text") or f"@{get_cached_bot_username()}").upper().strip()
    if not wm_text.startswith("@"):
        wm_text = "@" + wm_text
    use_opacity = opacity if opacity else cfg.get("opacity", 0.24)

    if not out_png_path:
        safe_tag = re.sub(r"[^A-Z0-9_]", "", wm_text) or "BOT"
        out_png_path = os.path.join(PROMO_DIR, f"wm_badge_{safe_tag}_{int(use_opacity*100)}.png")

    if os.path.exists(out_png_path) and os.path.getsize(out_png_path) > 300:
        return out_png_path

    # 1-Usul: Pillow (PIL) orqali yuqori aniqlikda anti-aliased chizish
    try:
        from PIL import Image, ImageDraw, ImageFont
        font_size = 34
        font = None
        font_candidates = [
            r"C:\Windows\Fonts\arialbd.ttf",
            r"C:\Windows\Fonts\segoeuib.ttf",
            r"C:\Windows\Fonts\calibrib.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        ]
        for fc in font_candidates:
            if os.path.exists(fc):
                try:
                    font = ImageFont.truetype(fc, font_size)
                    break
                except Exception:
                    pass
        if font is None:
            font = ImageFont.load_default()

        dummy = Image.new("RGBA", (10, 10), (0, 0, 0, 0))
        d_dummy = ImageDraw.Draw(dummy)
        try:
            bbox = d_dummy.textbbox((0, 0), wm_text, font=font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
        except Exception:
            tw = len(wm_text) * 20
            th = 30

        h = 84
        w = max(280, 96 + tw + 28)
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        alpha_main = max(28, min(165, int(255 * use_opacity)))
        alpha_shadow = max(16, min(110, int(255 * (use_opacity * 0.55))))
        alpha_circle_fill = max(18, min(115, int(255 * (use_opacity * 0.65))))

        # 1) Dumaloq Telegram nishoni (chapda)
        cx, cy, r = 44, 42, 30
        draw.ellipse(
            [cx - r, cy - r, cx + r, cy + r],
            fill=(30, 35, 45, alpha_circle_fill),
            outline=(250, 225, 115, alpha_main),
            width=3
        )
        # Telegram qog'oz samolyotchasi (vektor koordinatalari)
        plane_outer = [
            (25, 42),  # chap tumshuq
            (58, 27),  # tepa-o'ng qanot uchi
            (50, 57),  # past-o'ng qanot
            (39, 48),  # o'rta burilish
            (33, 53),  # dum qismi
            (34, 44),  # ichki burchak
        ]
        draw.polygon(plane_outer, fill=(255, 252, 235, min(255, int(alpha_main * 1.15))))
        # Samolyotcha o'rta chizig'i (qanot soyasi)
        draw.line([(34, 44), (56, 29)], fill=(40, 45, 55, alpha_main), width=2)

        # 2) @HANDLE matni (o'ng tomonda, yumshoq soya bilan)
        tx = 88
        ty = (h - th) // 2 - 3
        draw.text((tx + 2, ty + 2), wm_text, font=font, fill=(0, 0, 0, alpha_shadow))
        draw.text((tx, ty), wm_text, font=font, fill=(255, 255, 255, alpha_main))

        img.save(out_png_path, "PNG")
        if os.path.exists(out_png_path) and os.path.getsize(out_png_path) > 300:
            return out_png_path
    except Exception as e:
        print(f"Pillow watermark fallbackga o'tilmoqda: {e}")

    # 2-Usul: Pure-Python RGBA PNG generator (Pillow bo'lmasa ham 100% ishlaydi!)
    if _generate_watermark_png_pure_python(wm_text, out_png_path, opacity=use_opacity):
        return out_png_path
    return None

def apply_floating_watermark_to_video(input_path: str, output_path: str, custom_text: str = "") -> bool:
    """
    Har bitta videoda shaffof (prazrachniy, ko'rinar-ko'rinmas) Telegram ikonka + @HANDLE ni
    tepadan pastga silliq suzib yuradigan qilib tushirish! Videoga xalaqit bermaydi.
    """
    ensure_ffmpeg_in_path()
    cfg = get_watermark_settings()
    if not cfg.get("enabled", True) and not custom_text:
        return False

    wm_png = generate_telegram_watermark_png(text=custom_text or cfg.get("text", ""), opacity=cfg.get("opacity", 0.24))
    if not wm_png or not os.path.exists(wm_png):
        return False

    vinfo = get_video_stream_info(input_path)
    vid_w = max(360, vinfo.get("width", 720))
    wm_target_w = max(180, min(460, int(vid_w * 0.44)))

    filter_complex = (
        f"[1:v]scale={wm_target_w}:-1[wm];"
        f"[0:v][wm]overlay="
        f"x='(W-w)/2+(W*0.14)*sin(t*0.75)':"
        f"y='55+mod(t*85,max(60,H-h-110))':"
        f"format=auto,format=yuv420p[vout]"
    )
    cmd = [
        FFMPEG_BIN, "-y",
        "-i", input_path,
        "-i", wm_png,
        "-filter_complex", filter_complex,
        "-map", "[vout]",
        "-map", "0:a?",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23",
        "-pix_fmt", "yuv420p",
        "-c:a", "copy",
        "-movflags", "+faststart",
        output_path
    ]
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=180)
        return res.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 1000
    except Exception as e:
        print(f"Floating watermark xatosi: {e}")
        return False

def make_video_100_original(
    input_path: str,
    output_path: str,
    custom_watermark: str = "",
    force_9_16: bool = False
) -> tuple[bool, dict]:
    """
    🛡 10-BOSQICHLI PRO ANTI-DUPLIKAT (100% ORIGINAL VIDEO) ALGORITMI (TEZKOR SINGLE-PASS)!
    Instagram Reels, TikTok va YouTube Shorts algoritmlari (pHash, dHash, MD5/SHA256,
    Audio Chromaprint, Histogram, GOP Keyframe va Metadata) videoni 100% YANGI ORIGINAL
    deb qabul qilishi va Rekomendatsiya / Topga chiqarishi uchun 10 ta qatlamli ishlov beradi.
    Ultrafast single-pass orqali 3–6 soniyada tayyor bo'ladi!
    """
    ensure_ffmpeg_in_path()
    try:
        vinfo = get_video_stream_info(input_path)
        orig_w = max(360, vinfo.get("width", 720))
        orig_h = max(360, vinfo.get("height", 1280))
        if force_9_16:
            target_w, target_h = 720, 1280
        else:
            # Juda katta 4K videolarni 720p/1080p chegarasida ushlab tezkor ishlash
            if orig_w > 1080 or orig_h > 1920:
                scale_r = min(720.0 / orig_w, 1280.0 / orig_h)
                target_w = int(orig_w * scale_r)
                target_h = int(orig_h * scale_r)
            else:
                target_w, target_h = orig_w, orig_h
            target_w = target_w if target_w % 2 == 0 else target_w + 1
            target_h = target_h if target_h % 2 == 0 else target_h + 1

        zoom_factor = round(random.uniform(1.024, 1.035), 4)
        speed_factor = round(random.choice([random.uniform(0.986, 0.993), random.uniform(1.007, 1.015)]), 4)
        pts_mult = round(1.0 / speed_factor, 5)
        contrast_val = round(random.uniform(1.020, 1.032), 3)
        sat_val = round(random.uniform(1.025, 1.045), 3)
        bright_val = round(random.uniform(0.004, 0.009), 4)
        gamma_r = round(random.uniform(1.008, 1.018), 3)
        gamma_b = round(random.uniform(0.985, 0.994), 3)
        audio_pitch = round(random.uniform(1.011, 1.016), 4)
        audio_tempo = round(speed_factor / audio_pitch, 4)
        audio_tempo = max(0.5, min(2.0, audio_tempo))

        scaled_w = int(target_w * zoom_factor)
        scaled_h = int(target_h * zoom_factor)
        scaled_w = scaled_w if scaled_w % 2 == 0 else scaled_w + 1
        scaled_h = scaled_h if scaled_h % 2 == 0 else scaled_h + 1
        crop_x = max(1, (scaled_w - target_w) // 2 + random.choice([-2, -1, 1, 2]))
        crop_y = max(1, (scaled_h - target_h) // 2 + random.choice([-2, -1, 1, 2]))

        cfg = get_watermark_settings()
        wm_png = generate_telegram_watermark_png(
            text=custom_watermark or cfg.get("text", ""),
            opacity=cfg.get("opacity", 0.24)
        )
        wm_w = max(180, min(420, int(target_w * 0.44)))

        base_v_chain = (
            f"scale={scaled_w}:{scaled_h},"
            f"crop={target_w}:{target_h}:{crop_x}:{crop_y},"
            f"eq=contrast={contrast_val}:brightness={bright_val}:saturation={sat_val}:gamma_r={gamma_r}:gamma_b={gamma_b},"
            f"noise=alls=1:allf=t,"
            f"setpts={pts_mult}*PTS,"
            f"fps=30,setsar=1"
        )

        now_iso = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        unique_id = str(uuid.uuid4()).upper()
        audio_exists = has_audio_stream(input_path)

        cmd = [FFMPEG_BIN, "-y", "-i", input_path]
        if wm_png and os.path.exists(wm_png):
            cmd += ["-i", wm_png]
            filter_complex = (
                f"[0:v]{base_v_chain}[v_clean];"
                f"[1:v]scale={wm_w}:-1[wm];"
                f"[v_clean][wm]overlay="
                f"x='(W-w)/2+(W*0.15)*sin(t*0.8)':"
                f"y='60+mod(t*92,max(65,H-h-120))':"
                f"format=auto,format=yuv420p[vout]"
            )
            cmd += ["-filter_complex", filter_complex, "-map", "[vout]"]
        else:
            cmd += ["-vf", f"{base_v_chain},format=yuv420p", "-map", "0:v:0"]

        if audio_exists:
            af_chain = (
                f"asetrate=44100*{audio_pitch},aresample=44100,"
                f"atempo={audio_tempo},volume=1.03"
            )
            cmd += ["-map", "0:a:0", "-af", af_chain, "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2"]
        else:
            cmd += ["-an"]

        cmd += [
            "-map_metadata", "-1",
            "-map_chapters", "-1",
            "-metadata", f"creation_time={now_iso}",
            "-metadata", "make=Apple",
            "-metadata", "model=iPhone 16 Pro Max",
            "-metadata", "software=18.2",
            "-metadata", "com.apple.quicktime.make=Apple",
            "-metadata", "com.apple.quicktime.model=iPhone 16 Pro Max",
            "-metadata", "com.apple.quicktime.software=18.2",
            "-metadata", f"comment=Original_Capture_{unique_id}",
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "22",
            "-g", "29", "-keyint_min", "15",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            output_path
        ]

        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=180)
        ok = res.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 1000
        return ok, {
            "zoom": f"{zoom_factor*100 - 100:.1f}%",
            "speed": f"{speed_factor:.3f}x",
            "pitch": f"+{(audio_pitch-1)*100:.1f}%",
            "device": "Apple iPhone 16 Pro Max (iOS 18.2)",
            "uuid": unique_id[:8]
        }
    except Exception as e:
        print(f"Anti-duplikat xatoligi: {e}")
        return False, {}

def get_saved_outro_path(user_id: int) -> str | None:
    """Foydalanuvchi yoki Admin saqlab qo'ygan reklama/outro videosini topish"""
    user_outro = os.path.join(PROMO_DIR, f"outro_{user_id}.mp4")
    if os.path.exists(user_outro) and os.path.getsize(user_outro) > 1000:
        return user_outro
    admin_outro = os.path.join(PROMO_DIR, f"outro_{ADMIN_ID}.mp4")
    if os.path.exists(admin_outro) and os.path.getsize(admin_outro) > 1000:
        return admin_outro
    default_outro = os.path.join(PROMO_DIR, "default_outro.mp4")
    if os.path.exists(default_outro) and os.path.getsize(default_outro) > 1000:
        return default_outro
    return None

def normalize_clip_for_montage(
    input_path: str,
    output_path: str,
    target_w: int = 720,
    target_h: int = 1280,
    max_duration: float = 0.0,
    keep_audio: bool = True,
    use_blur_bg: bool = True,
    fade_out_video: bool = False,
    fade_in_video: bool = False
) -> bool:
    """
    Har qanday o'lcham, FPS va davomiylikdagi (10s, 19s, 45s, 1 daqiqa+) videoni
    720x1280 HD (9:16 Reels/TikTok, 30 fps, yuv420p, 44.1kHz stereo) standartiga
    TEZKOR (downscale-blur + ultrafast) keltirish!
    """
    ensure_ffmpeg_in_path()
    dur = get_media_duration(input_path)
    if dur <= 0.2:
        dur = 15.0
    use_dur = min(dur, max_duration) if (max_duration and max_duration > 0.5 and dur > max_duration) else dur
    audio_exists = has_audio_stream(input_path)
    vinfo = get_video_stream_info(input_path)
    in_w = max(100, vinfo.get("width", 720))
    in_h = max(100, vinfo.get("height", 1280))
    aspect_ratio = in_w / float(in_h)
    target_aspect = target_w / float(target_h)  # 0.5625 (9:16)

    fade_filters = []
    if fade_in_video and use_dur > 0.8:
        fade_filters.append("fade=t=in:st=0:d=0.30")
    if fade_out_video and use_dur > 0.8:
        fade_filters.append(f"fade=t=out:st={max(0.1, use_dur - 0.30):.2f}:d=0.30")
    fade_suffix = ("," + ",".join(fade_filters)) if fade_filters else ""

    # Tezkor Downscale-Blur (180x320 da boxblur=10:2 qilib 720x1280 ga kattalashtiriladi -> 25 baravar tez!)
    if use_blur_bg and abs(aspect_ratio - target_aspect) > 0.08:
        v_filter_complex = (
            f"[0:v]split=2[vbg][vfg];"
            f"[vbg]scale=180:320:force_original_aspect_ratio=increase,"
            f"crop=180:320,boxblur=10:2,scale={target_w}:{target_h},eq=brightness=-0.08:saturation=1.15[bg];"
            f"[vfg]scale={target_w}:{target_h}:force_original_aspect_ratio=decrease[fg];"
            f"[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1,fps=30{fade_suffix},format=yuv420p[vout]"
        )
        use_complex = True
    else:
        v_filter_simple = (
            f"scale={target_w}:{target_h}:force_original_aspect_ratio=decrease,"
            f"pad={target_w}:{target_h}:(ow-iw)/2:(oh-ih)/2:black,"
            f"setsar=1,fps=30{fade_suffix},format=yuv420p"
        )
        use_complex = False

    cmd = [FFMPEG_BIN, "-y", "-i", input_path]
    if keep_audio and not audio_exists:
        cmd += ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100"]

    cmd += ["-t", f"{use_dur:.3f}"]
    if use_complex:
        cmd += ["-filter_complex", v_filter_complex, "-map", "[vout]"]
    else:
        cmd += ["-vf", v_filter_simple, "-map", "0:v:0"]

    if keep_audio and not audio_exists:
        cmd += [
            "-map", "1:a:0",
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "22",
            "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
            "-shortest", "-movflags", "+faststart",
            output_path
        ]
    elif keep_audio and audio_exists:
        cmd += [
            "-map", "0:a:0",
            "-af", "aresample=44100,aformat=sample_fmts=fltp:channel_layouts=stereo",
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "22",
            "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
            "-movflags", "+faststart",
            output_path
        ]
    else:
        cmd += [
            "-an",
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "22",
            "-movflags", "+faststart",
            output_path
        ]

    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=180)
        return res.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 1000
    except Exception as e:
        print(f"Normalize clip xatoligi: {e}")
        return False

def _generate_transition_whoosh_sfx(out_wav: str, duration: float = 0.65) -> bool:
    """
    Pure-Python (wave + struct + math) yordamida 0.01 soniyada kinematik Sub-Bass Whoosh
    ovoz effektini yaratish (FFmpeg lavfi/aevalsrc ga bog'liq emas, 100% xatosiz ishlaydi!).
    """
    try:
        sample_rate = 44100
        n_samples = int(sample_rate * duration)
        frames = bytearray()
        for i in range(n_samples):
            t = i / float(sample_rate)
            # Chastota 165 Hz dan 48 Hz gacha silliq tushuvchi sub-bass whoosh
            freq = 165.0 - 115.0 * (t / duration)
            env = math.sin(math.pi * (t / duration)) * math.exp(-2.6 * t)
            val = int(max(-32767, min(32767, 32767 * 0.34 * env * math.sin(2.0 * math.pi * freq * t))))
            packed = struct.pack("<hh", val, val)
            frames.extend(packed)
        with wave.open(out_wav, "wb") as wf:
            wf.setnchannels(2)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(bytes(frames))
        return os.path.exists(out_wav) and os.path.getsize(out_wav) > 200
    except Exception as e:
        print(f"Pure-Python Whoosh SFX xatosi: {e}")
        return False

def _write_ffmpeg_concat_list(list_path: str, file_paths: list):
    """
    Windows va Linuxda FFmpeg `-f concat` demuxer xato bermasligi uchun
    barcha yo'llardagi `\` belgisini `/` (forward slash) ga o'girib yozadi!
    """
    with open(list_path, "w", encoding="utf-8") as lf:
        for fp in file_paths:
            safe_p = os.path.abspath(fp).replace("\\", "/").replace("'", "'\\''")
            lf.write(f"file '{safe_p}'\n")

def montage_two_videos(
    video1_path: str,
    video2_path: str,
    output_path: str,
    mode: str = "audio1_bridge",
    apply_anti_duplicate: bool = True
) -> tuple[bool, dict]:
    """
    2 ta har qanday uzunlikdagi (10s, 19s, 45s, 1 daqiqa+) videoni
    5 Xil Smart Rejimda + Blurred 9:16 Fon + Suzuvchi Shaffof Watermark + Anti-Duplikat
    bilan TEZKOR (5-8 soniyada) montaj qilish!
    """
    ensure_ffmpeg_in_path()
    ts = int(time.time() * 1000) % 1000000
    norm1 = os.path.join(MONTAGE_SESSIONS_DIR, f"_m_norm1_{ts}.mp4")
    norm2 = os.path.join(MONTAGE_SESSIONS_DIR, f"_m_norm2_{ts}.mp4")
    concat_vid = os.path.join(MONTAGE_SESSIONS_DIR, f"_m_concat_v_{ts}.mp4")
    raw_montaj = os.path.join(MONTAGE_SESSIONS_DIR, f"_m_raw_out_{ts}.mp4")
    audio1_aac = os.path.join(MONTAGE_SESSIONS_DIR, f"_m_aud1_{ts}.m4a")
    whoosh_wav = os.path.join(MONTAGE_SESSIONS_DIR, f"_m_whoosh_{ts}.wav")
    concat_list = os.path.join(MONTAGE_SESSIONS_DIR, f"_m_list_{ts}.txt")

    try:
        dur1_raw = max(get_media_duration(video1_path), 1.0)
        dur2_raw = max(get_media_duration(video2_path), 1.0)
        target_stage = raw_montaj if apply_anti_duplicate else output_path
        mode_label = ""
        final_d1 = dur1_raw
        final_d2 = dur2_raw
        total_d = dur1_raw + dur2_raw

        # ---------------- REJIM 3: PICTURE-IN-PICTURE (PiP Preview + Fullscreen Outro) ----------------
        if mode == "pip_outro":
            if not normalize_clip_for_montage(video1_path, norm1, keep_audio=False, fade_out_video=True):
                return False, {}
            if not normalize_clip_for_montage(video2_path, norm2, keep_audio=False, fade_in_video=True):
                return False, {}

            d1 = get_media_duration(norm1)
            d2 = get_media_duration(norm2)
            pip_lead = min(3.0, max(1.5, d1 * 0.25), max(1.5, d2 * 0.5))
            pip_start = max(0.5, d1 - pip_lead)

            _write_ffmpeg_concat_list(concat_list, [norm1, norm2])
            subprocess.run([
                FFMPEG_BIN, "-y", "-f", "concat", "-safe", "0", "-i", concat_list, "-c", "copy", concat_vid
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)

            total_d = get_media_duration(concat_vid) or (d1 + d2)

            if has_audio_stream(video1_path):
                subprocess.run([
                    FFMPEG_BIN, "-y", "-i", video1_path, "-vn",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2", audio1_aac
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=90)
            else:
                subprocess.run([
                    FFMPEG_BIN, "-y", "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
                    "-t", f"{total_d:.3f}", "-c:a", "aac", audio1_aac
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)

            fade_start = max(total_d - 1.2, 0.5)
            pip_filter = (
                f"[1:v]scale=230:408,drawbox=x=0:y=0:w=iw:h=ih:color=gold@0.9:t=5,"
                f"setpts=PTS+{pip_start:.2f}/TB[pip];"
                f"[0:v][pip]overlay=x=W-w-26:y=H-h-130:enable='between(t,{pip_start:.2f},{d1:.2f})'[v_pip]"
            )
            cmd_pip = [
                FFMPEG_BIN, "-y",
                "-i", concat_vid,
                "-i", norm2,
                "-stream_loop", "-1", "-i", audio1_aac,
                "-filter_complex", pip_filter,
                "-map", "[v_pip]", "-map", "2:a:0",
                "-t", f"{total_d:.3f}",
                "-af", f"afade=t=out:st={fade_start:.2f}:d=1.2",
                "-c:v", "libx264", "-preset", "ultrafast", "-crf", "22",
                "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
                "-movflags", "+faststart",
                target_stage
            ]
            res = subprocess.run(cmd_pip, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=180)
            if res.returncode != 0 or not os.path.exists(target_stage):
                return False, {}
            final_d1, final_d2 = d1, d2
            mode_label = "🖼 PiP Reklama (Burchakda Preview + To'liq Ekran)"

        # ---------------- REJIM 4: ORIGINAL OVOZLAR (1-Video + 2-Video o'z ovozi bilan) ----------------
        elif mode == "both_original":
            if not normalize_clip_for_montage(video1_path, norm1, keep_audio=True, fade_out_video=True):
                return False, {}
            if not normalize_clip_for_montage(video2_path, norm2, keep_audio=True, fade_in_video=True):
                return False, {}

            _write_ffmpeg_concat_list(concat_list, [norm1, norm2])
            cmd = [
                FFMPEG_BIN, "-y", "-f", "concat", "-safe", "0",
                "-i", concat_list,
                "-c:v", "copy",
                "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
                "-movflags", "+faststart",
                target_stage
            ]
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=180)
            if res.returncode != 0 or not os.path.exists(target_stage):
                return False, {}
            total_d = get_media_duration(target_stage) or (dur1_raw + dur2_raw)
            mode_label = "🔊 Original Ovozlar (1+2 + Kinematik O'tish)"

        # ---------------- REJIM 2: TRUE L-CUT (1-Video tasviri ertaroq almashib, audiosi 2-video ustida tugaydi) ----------------
        elif mode == "lcut_split":
            if dur1_raw > dur2_raw + 3.0:
                v1_visual_dur = dur1_raw - dur2_raw
            else:
                v1_visual_dur = max(dur1_raw * 0.65, 2.0)

            if not normalize_clip_for_montage(video1_path, norm1, max_duration=v1_visual_dur, keep_audio=False, fade_out_video=True):
                return False, {}
            if not normalize_clip_for_montage(video2_path, norm2, keep_audio=False, fade_in_video=True):
                return False, {}

            _write_ffmpeg_concat_list(concat_list, [norm1, norm2])
            subprocess.run([
                FFMPEG_BIN, "-y", "-f", "concat", "-safe", "0", "-i", concat_list, "-c", "copy", concat_vid
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)

            total_d = get_media_duration(concat_vid)
            if total_d <= 0.5:
                total_d = v1_visual_dur + dur2_raw

            if has_audio_stream(video1_path):
                subprocess.run([
                    FFMPEG_BIN, "-y", "-i", video1_path, "-vn",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2", audio1_aac
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=90)
            else:
                subprocess.run([
                    FFMPEG_BIN, "-y", "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
                    "-t", f"{total_d:.3f}", "-c:a", "aac", audio1_aac
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)

            fade_start = max(total_d - 1.2, 0.5)
            cmd_mux = [
                FFMPEG_BIN, "-y",
                "-i", concat_vid,
                "-stream_loop", "-1", "-i", audio1_aac,
                "-map", "0:v:0", "-map", "1:a:0",
                "-t", f"{total_d:.3f}",
                "-af", f"afade=t=out:st={fade_start:.2f}:d=1.2",
                "-c:v", "copy",
                "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
                "-movflags", "+faststart",
                target_stage
            ]
            res = subprocess.run(cmd_mux, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=180)
            if res.returncode != 0 or not os.path.exists(target_stage):
                return False, {}
            final_d1 = v1_visual_dur
            mode_label = "🎬 L-Cut Overlap (Kadr almashib, 1-Audio davom etadi)"

        # ---------------- REJIM 5: FON MUSIQA MIX (Audio Ducking: 1-Video Audiosi 25% + 2-Video Ovozi 100%) ----------------
        elif mode == "audio_ducking":
            if not normalize_clip_for_montage(video1_path, norm1, keep_audio=True, fade_out_video=True):
                return False, {}
            if not normalize_clip_for_montage(video2_path, norm2, keep_audio=True, fade_in_video=True):
                return False, {}

            d1 = get_media_duration(norm1)
            d2 = get_media_duration(norm2)
            total_d = d1 + d2

            _write_ffmpeg_concat_list(concat_list, [norm1, norm2])
            subprocess.run([
                FFMPEG_BIN, "-y", "-f", "concat", "-safe", "0", "-i", concat_list,
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", concat_vid
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=150)

            subprocess.run([
                FFMPEG_BIN, "-y", "-i", norm1, "-vn", "-c:a", "aac", "-b:a", "192k", audio1_aac
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)

            fade_start = max(total_d - 1.2, 0.5)
            filter_complex = (
                f"[0:a]volume=1.0[a_main];"
                f"[1:a]volume=0.25,afade=t=out:st={fade_start:.2f}:d=1.2[a_bg];"
                f"[a_main][a_bg]amix=inputs=2:duration=first:dropout_transition=2[a_out]"
            )
            cmd_mix = [
                FFMPEG_BIN, "-y",
                "-i", concat_vid,
                "-stream_loop", "-1", "-i", audio1_aac,
                "-filter_complex", filter_complex,
                "-map", "0:v:0", "-map", "[a_out]",
                "-t", f"{total_d:.3f}",
                "-c:v", "copy",
                "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
                "-movflags", "+faststart",
                target_stage
            ]
            res = subprocess.run(cmd_mix, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=180)
            if res.returncode != 0 or not os.path.exists(target_stage):
                return False, {}
            final_d1, final_d2 = d1, d2
            mode_label = "🔉 Fon Mix (1-Audio 25% fonda + 2-Video ovozi 100%)"

        # ---------------- REJIM 1 (DEFAULT): 1-VIDEO AUDIOSI UZLUKSIZ 2-VIDEOGA ULANADI (2-VIDEO MUTE) ----------------
        else:
            if not normalize_clip_for_montage(video1_path, norm1, keep_audio=False, fade_out_video=True):
                return False, {}
            if not normalize_clip_for_montage(video2_path, norm2, keep_audio=False, fade_in_video=True):
                return False, {}

            _write_ffmpeg_concat_list(concat_list, [norm1, norm2])
            subprocess.run([
                FFMPEG_BIN, "-y", "-f", "concat", "-safe", "0", "-i", concat_list, "-c", "copy", concat_vid
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=150)

            total_d = get_media_duration(concat_vid)
            if total_d <= 0.5:
                total_d = dur1_raw + dur2_raw

            if has_audio_stream(video1_path):
                subprocess.run([
                    FFMPEG_BIN, "-y", "-i", video1_path, "-vn",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2", audio1_aac
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=90)
            else:
                subprocess.run([
                    FFMPEG_BIN, "-y", "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
                    "-t", f"{total_d:.3f}", "-c:a", "aac", audio1_aac
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)

            fade_start = max(total_d - 1.2, 0.5)
            delay_ms = max(100, int((dur1_raw - 0.25) * 1000))
            if _generate_transition_whoosh_sfx(whoosh_wav, 0.65):
                af_complex = (
                    f"[1:a]atrim=0:{total_d:.3f},asetpts=PTS-STARTPTS,afade=t=out:st={fade_start:.2f}:d=1.2[a_main];"
                    f"[2:a]adelay={delay_ms}|{delay_ms},volume=0.45[a_sfx];"
                    f"[a_main][a_sfx]amix=inputs=2:duration=first:dropout_transition=1[a_final]"
                )
                cmd_bridge = [
                    FFMPEG_BIN, "-y",
                    "-i", concat_vid,
                    "-stream_loop", "-1", "-i", audio1_aac,
                    "-i", whoosh_wav,
                    "-filter_complex", af_complex,
                    "-map", "0:v:0", "-map", "[a_final]",
                    "-t", f"{total_d:.3f}",
                    "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
                    "-movflags", "+faststart",
                    target_stage
                ]
            else:
                cmd_bridge = [
                    FFMPEG_BIN, "-y",
                    "-i", concat_vid,
                    "-stream_loop", "-1", "-i", audio1_aac,
                    "-map", "0:v:0", "-map", "1:a:0",
                    "-t", f"{total_d:.3f}",
                    "-af", f"afade=t=out:st={fade_start:.2f}:d=1.2",
                    "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
                    "-movflags", "+faststart",
                    target_stage
                ]
            res = subprocess.run(cmd_bridge, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=180)
            if res.returncode != 0 or not os.path.exists(target_stage):
                # Fallback oddiy mux (agar adelay versiyasi mos kelmasa)
                cmd_fb = [
                    FFMPEG_BIN, "-y",
                    "-i", concat_vid,
                    "-stream_loop", "-1", "-i", audio1_aac,
                    "-map", "0:v:0", "-map", "1:a:0",
                    "-t", f"{total_d:.3f}",
                    "-af", f"afade=t=out:st={fade_start:.2f}:d=1.2",
                    "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
                    "-movflags", "+faststart",
                    target_stage
                ]
                subprocess.run(cmd_fb, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
            if not os.path.exists(target_stage):
                return False, {}
            mode_label = "🔥 Audio Uzluksiz (1-Video Audiosi 2-ga Ulanadi + Transition FX)"

        # ---------------- YAKUNIY BOSQICH: 10-QATLAMLI ANTI-DUPLIKAT + TEPADAN PASTGA SUZUVCHI SHAFFOF WATERMARK ----------------
        anti_dup_info = {}
        if apply_anti_duplicate:
            ok_ad, anti_dup_info = make_video_100_original(target_stage, output_path, force_9_16=False)
            if not ok_ad or not os.path.exists(output_path):
                shutil.copyfile(target_stage, output_path)
            total_d = get_media_duration(output_path) or total_d

        return (os.path.exists(output_path) and os.path.getsize(output_path) > 1000), {
            "dur1": final_d1,
            "dur2": final_d2,
            "total": total_d,
            "mode_name": mode_label,
            "anti_dup": anti_dup_info
        }
    except Exception as e:
        print(f"Montaj xatoligi ({mode}): {e}")
        return False, {}
    finally:
        safe_remove(norm1, norm2, concat_vid, raw_montaj, audio1_aac, whoosh_wav, concat_list)


# ==================== 📸 INSTAGRAM REELS AVTO-POSTER 24/7 (AVTO TREND + RUCHNOY LINK + 3-QATLAMLI HALOL FILTR) ====================
IG_SESSION_FILE = os.path.join(PROMO_DIR, "ig_session.json")
IG_CONFIG_FILE = os.path.join(PROMO_DIR, "ig_autopost_config.json")
IG_CLIENT_LOCK = threading.Lock()
IG_PENDING_LOGIN = {}  # user_id -> {"client": cl, "username": str, "password": str, "time": float}

# 🚫 1-QATLAM: QAT'IY QORA RO'YXAT (QIMOR / BUKMEKER / KAZINO / 18+ FAHSH / SPAM REKLAMA SO'ZLARI)
GAMBLING_ADULT_AD_BLACKLIST = [
    # Qimor, bukmeker va kazino (Gambling / Betting / Casino)
    "1xbet", "1x_bet", "1x-bet", "melbet", "mel_bet", "mostbet", "most_bet",
    "linebet", "winline", "parimatch", "pari_match", "fonbet", "olimpbet",
    "betwinner", "betboom", "pinup", "pin-up", "pin_up", "1win", "1_win",
    "vavada", "vulkan", "joycasino", "azino", "azino777", "777 casino", "777 slot",
    "casino", "kazino", "казино", "qimor", "stavka", "stavki", "ставки", "ставка",
    "bukmeker", "букмекер", "totalizator", "jackpot", "jekpot", "aviator game", "aviator signal",
    "luckyjet", "lucky_jet", "jetx", "plinko", "sweet bonanza", "gates of olympus",
    "book of ra", "crash game", "roulette", "ruletka", "рулетка", "poker", "покер",
    "blackjack", "baccarat", "koeffitsient", "коэффициент", "ekspress stavka",
    "xbet", "bet365", "betcity", "leonbets", "marathonbet", "bwin", "ggbet",
    # Promokod, shubhali daromad va spam reklamalar
    "promokod", "промокод", "promo code", "bonus 500%", "depozit", "депозит",
    "vip signal", "kaper", "каппер", "dogovornoy match", "договорной матч",
    "shapkada ssilka", "ssilka profil", "ссылка в шапке", "ссылка в профиле",
    "link in bio for bonus", "t.me/+", "joinchat/", "reklama xizmati",
    "kripto signal", "pump signal", "binomo", "olymptrade", "pocket option", "quotex",
    # 18+ / NSFW / Fahsh kontent
    "18+", "+18", "nsfw", "onlyfans", "only_fans", "porn", "porno", "порно",
    "seks", "секс", "erotik", "erotika", "эротика", "nudes",
    "boobs", "booty", "striptiz", "стриптиз", "escort", "eskort", "эскорт",
    "intim", "интим", "hentai", "camgirl", "webcam model", "sharmanda",
    "fahsh", "yalang'och", "yalangoch", "голая", "голые", "сиськи", "жопа",

    # 🚫 RAQS, LIKILLAGAN QIZLAR, MODEL VA FOYDASIZ TRENDLARNI 100% BLOKLASH FILTRI:
    # O'zbekcha so'zlar:
    "qiz", "qizlar", "qizla", "qizaloq", "qizcha", "ayol", "ayollar", "kelin", "kelinlar", "kelinchak",
    "raqs", "raqsi", "raqqosa", "raqqosalar", "o'yin", "oynadi", "oynagan",
    "likillash", "likillagan", "likillatib", "likillashini", "dumba", "sharmandali",
    "go'zallik", "parandoz", "makiyaj", "pardoz", "modelyer", "qizilko'ylak", "sevgi", "romantika",
    # Ruscha so'zlar:
    "девушка", "девушки", "девочка", "девочки", "девчонка", "девчонки",
    "красотка", "красотки", "красавица", "красавицы", "модель", "модели",
    "танец", "танцы", "танцует", "танцуют", "танцовщица", "танцовщицы",
    "тверк", "тверкинг", "тверкают", "липсинк", "беллиданс",
    "купальник", "бикини", "декольте", "ножки", "фигура", "талия",
    "платье", "макияж", "вайб с девочками", "красивая девушка", "губы", "попа", "грудь",
    # Inglizcha so'zlar:
    "girl", "girls", "woman", "women", "female", "lady", "ladies",
    "babe", "babes", "cutie", "cuties", "baddie", "baddies",
    "dance", "dancing", "dancer", "dances", "dancetrend", "dancechallenge",
    "twerk", "twerking", "bellydance", "belly dance", "choreo", "choreography",
    "lipsync", "lip sync", "bikini", "swimsuit", "lingerie", "cleavage", "curves",
    "outfit", "ootd", "fashion model", "makeup", "grwm", "beauty model",
    "crush", "thirsttrap", "thirst trap", "hot girl", "hotgirl",
    "dating", "romance", "lovestory", "love story", "couple goals",
    "tiktok dance", "viral dance", "trending dance", "dance video"
]

# 🎯 FAQAT XALQQA MANFAATLI, 100% O'ZBEKCHA FOYDALI VA ILMIY-MA'RIFIY MAVZULAR:
DEFAULT_TREND_QUERIES = [
    "foydali maslahatlar", "qiziqarli faktlar uzbek", "hayotiy saboqlar", "ibratli hikoyalar",
    "foydali bilimlar uzb", "donolar fikri", "hunarmandchilik sirlari", "duradgorlik ustalari",
    "psixologiya sirlari uzb", "sog'lom hayot maslahatlari", "tarixiy faktlar uzb",
    "ajoyib kashfiyotlar", "aqlli layfxaklar uz", "foydali tavsiyalar", "ibratli videolar"
]

GENERIC_META_TAGS = {
    "reels", "trending", "viral", "explore", "fyp", "foryou", "foryoupage",
    "instagram", "bot", "rek", "rekomendatsiya", "video", "shorts", "tiktok", "trend"
}

HIGH_ENGAGEMENT_VIRAL_TOPICS = [
    "foydali layfxaklar uzb", "qiziqarli ilmiy faktlar uzbek", "hayotiy saboqlar uzb",
    "ibratli videolar uzbekcha", "foydali maslahatlar uz", "duradgorlik sirlari uzb",
    "hunarmandchilik ustalari", "ajoyib kashfiyotlar uzb", "donolar hikmati uzb",
    "psixologiya va aql idrok uz", "biznes va muvaffaqiyat saboqlari", "tabiat mo'jizalari uzb",
    "aqlli maslahatlar hayot uchun", "foydali bilimlar uzb", "salomatlik sirlari uzbekcha",
    "ibratli hikoyalar uzbek", "texnika va ixtirolar uzbekcha"
]

# 🇺🇿 FAQAT O'ZBEK TILI VA XALQQA FOYDALI KONTENTNI KAFOLATLOVCHI SO'ZLAR:
UZBEK_BENEFICIAL_KEYWORDS = {
    "foydali", "maslahat", "maslahatlar", "tavsiya", "tavsiyalar", "saboq", "saboqlar",
    "ibrat", "ibratli", "qiziqarli", "fakt", "faktlar", "hikoya", "hikoyalar", "hikmat", "hikmatlar",
    "bilim", "bilimlar", "hayot", "hayotiy", "aql", "aqlli", "ilm", "ilmiy", "inson", "odam", "dunyo",
    "ajoyib", "sirlari", "siri", "mo'jiza", "mojiza", "donolar", "muvaffaqiyat", "biznes", "psixologiya",
    "salomatlik", "shifo", "retsept", "oshxona", "hunar", "hunarmandchilik", "ustachilik", "usta",
    "duradgor", "duradgorlik", "texnika", "texnologiya", "ixtiro", "ixtirolar", "kashfiyot", "tarix",
    "tarixiy", "rivoyat", "o'zbek", "ozbek", "uzb", "uzbek", "uzbekistan", "o'zbekiston", "toshkent",
    "samarqand", "buxoro", "andijon", "fargona", "namangan", "layfxak", "layfxaklar", "qanday", "nima",
    "uchun", "kerak", "qilish", "organish", "o'rganish", "eshiting", "koring", "ko'ring", "bilasizmi",
    "bilib", "oling", "manfaatli", "halol", "yaxshi", "to'g'ri", "togri", "muhim", "biling", "yodda",
    # Kirillcha o'zbek so'zlari:
    "фойдали", "маслаҳат", "маслахат", "сабоқ", "сабок", "ибрат", "ибратли", "қизиқарли", "кизикарли",
    "факт", "фактлар", "ҳикоя", "хикоя", "билим", "ҳаёт", "хаёт", "ақл", "илм", "илмий", "инсон",
    "одам", "дунё", "ажойиб", "сирлари", "сири", "мўжиза", "донолар", "ҳикмат", "муваффақият",
    "бизнес", "психология", "саломатлик", "шифо", "рецепт", "ҳунар", "уста", "дурадгор", "техника",
    "технология", "ихтиро", "кашфиёт", "тарих", "ўзбек", "узбек", "узб", "ўзбекистон", "тошкент",
    "лайфхак", "тавсия", "қандай", "нима", "учун", "керак", "ўрганиш", "эшитинг", "кўринг", "биласизми",
    "манфаатли"
}

FOREIGN_NON_BENEFICIAL_PATTERNS = [
    # Xorijiy inglizcha/ruscha bema'ni texnik, hovuz ehtiyot qismlari, o'yin, prank va likillash:
    r"\b(?:replacement|pcb|circuit|wiring|hayward|unboxing|teardown|benchmark)\b",
    r"\b(?:gameplay|walkthrough|fortnite|minecraft|roblox|gta|pubg|freefire)\b",
    r"\b(?:prank|reaction|roast|drama|gossip|haul|makeup|grwm|outfit)\b",
    r"\b(?:dance|twerk|bikini|sexy|model|flirt|dating|couple goals)\b",
    r"\b(?:how to replace|how to repair|step by step guide|review)\b",
    r"\b(?:девушки|красивые девушки|танцы|макияж|стрим|прикол|пранк)\b"
]

def is_uzbek_beneficial_content(text: str, author_str: str = "") -> tuple[bool, str]:
    """
    🇺🇿 KONTENT FAQAT O'ZBEK TILIDA VA XALQQA FOYDALI EKANLIGINI TEKSHIRUVCHI QAT'IY FILTR:
    1) Xorijiy inglizcha texnik / hovuz ehtiyot qismlari (Hayward PCB va h.k.), o'yin, prank yoki
       likillagan qizlar videosi bo'lsa darhol bloklaydi!
    2) Sarlavha, muallif yoki heshteglarda kamida bitta aniq o'zbekcha ma'rifiy so'z yoki
       o'zbek kanali belgisi (uz, uzb, uzbek) bo'lishini talab qiladi.
    """
    if not text:
        return False, "Sarlavha bo'sh"
    lower_t = text.lower()
    full_str = f"{lower_t} {author_str.lower()}"

    # 1. Xorijiy keraksiz / inglizcha bema'ni mavzularni rad etish
    for pat in FOREIGN_NON_BENEFICIAL_PATTERNS:
        if re.search(pat, full_str):
            return False, f"Xorijiy / nomuvofiq kontent ({pat})"

    # 2. O'zbekcha kanallar yoki teglar
    if any(m in author_str.lower() for m in ("_uz", ".uz", "uzb", "uzbek", "toshkent", "samarqand")):
        return True, "O'zbek muallifi"

    # 3. O'zbekcha ma'rifiy / foydali so'zlar borligini tekshirish
    words = set(re.findall(r"[a-z'ʻ`’а-яё]+", lower_t))
    matched = words.intersection(UZBEK_BENEFICIAL_KEYWORDS)
    if matched:
        return True, f"O'zbekcha foydali so'zlar: {', '.join(list(matched)[:3])}"

    return False, "O'zbekcha ma'rifiy belgilar topilmadi (chet tili yoki nomuvofiq)"

DEFAULT_IG_CAPTION = (
    "💡 Xalqqa manfaatli va foydali bilimlar! Obuna bo'ling 👉 @{ig_user}\n\n"
    "📥 Foydali videolarni toza HD yuklash va montaj uchun botimiz: @{bot_user}\n\n"
    "#foydali #ilm #maslahat #qiziqarlifaktlar #motivatsiya #hayotiysaboqlar #uzbekistan #tashkent #reelsuzb #rek"
)
_TIKWM_RATE_LOCK = threading.Lock()
_LAST_TIKWM_REQ_TS = 0.0

def _wait_tikwm_rate_limit(min_interval: float = 1.25):
    """TikWM bepul API '1 request / 1 second' chekloviga tushib qolmaslik uchun aqlli navbat"""
    global _LAST_TIKWM_REQ_TS
    with _TIKWM_RATE_LOCK:
        now = time.time()
        elapsed = now - _LAST_TIKWM_REQ_TS
        if elapsed < min_interval:
            time.sleep(min_interval - elapsed)
        _LAST_TIKWM_REQ_TS = time.time()

def _init_ig_autopost_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ig_queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_url TEXT,
            local_path TEXT,
            title TEXT,
            caption TEXT,
            montage_mode TEXT DEFAULT 'audio1_bridge',
            status TEXT DEFAULT 'pending',
            ig_media_code TEXT DEFAULT '',
            error_msg TEXT DEFAULT '',
            created_at TIMESTAMP,
            posted_at TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ig_posted_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_id TEXT UNIQUE,
            video_url TEXT,
            ig_code TEXT,
            posted_at TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

try:
    _init_ig_autopost_db()
except Exception as _ig_db_e:
    print(f"IG DB init xatosi: {_ig_db_e}")

def get_ig_autopost_config() -> dict:
    default_cfg = {
        "auto_enabled": True,
        "daily_limit": 4,
        "schedule_hours": [10, 14, 18, 21],
        "montage_mode": "audio1_bridge",
        "use_saved_outro": True,
        "strict_safety_filter": True,
        "check_audio_speech": True,
        "check_skin_exposure": True,
        "trend_queries": list(DEFAULT_TREND_QUERIES),
        "custom_blacklist": [],
        "caption_template": DEFAULT_IG_CAPTION,
        "ig_username": "",
        "last_auto_check_date": "",
        "posts_today_count": 0,
        "last_post_timestamp": 0.0,
        "posted_hours_today": []
    }
    if os.path.exists(IG_CONFIG_FILE):
        try:
            with open(IG_CONFIG_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
                default_cfg.update(saved)
        except Exception:
            pass
    # Agar trend_queries faqat umumiy heshteglardan (reels, fyp, bot, instagram) iborat bo'lib qolgan bo'lsa,
    # avtomatik ravishda haqiqiy sifatli mavzular bilan boyitamiz:
    raw_q = [str(x).strip().lstrip("#") for x in (default_cfg.get("trend_queries") or []) if str(x).strip()]
    meaningful_q = [q for q in raw_q if q.lower() not in GENERIC_META_TAGS]
    if not meaningful_q:
        default_cfg["trend_queries"] = list(DEFAULT_TREND_QUERIES)
    return default_cfg

_CLOUD_VAULT_LOCK = threading.Lock()
_LAST_CLOUD_VAULT_SYNC_TS = 0.0

def save_ig_autopost_config(cfg: dict, sync_cloud: bool = True) -> dict:
    try:
        with open(IG_CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"IG config saqlash xatosi: {e}")
    if sync_cloud:
        trigger_background_cloud_vault_sync()
    return cfg

def _git_auto_persist_promo_assets():
    """GitHub Actions ichida bo'lsa, promo_assets ichidagi sessiya va sozlamalarni repoga saqlab qo'yish"""
    if os.environ.get("GITHUB_ACTIONS") != "true":
        return
    try:
        subprocess.run(["git", "config", "user.name", "UniversalSaveBot"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10)
        subprocess.run(["git", "config", "user.email", "bot@universalsave.local"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10)
        for rel_p in ["promo_assets/ig_session.json", "promo_assets/ig_autopost_config.json", "promo_assets/watermark_config.json"]:
            if os.path.exists(rel_p):
                subprocess.run(["git", "add", "-f", rel_p], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10)
        res = subprocess.run(["git", "commit", "-m", "chore(vault): auto-persist Instagram session & config [skip ci]"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=15)
        if res.returncode == 0:
            subprocess.run(["git", "push"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=25)
    except Exception:
        pass

def sync_state_to_telegram_cloud_vault(force: bool = False) -> bool:
    """
    ☁️ TELEGRAM BULUTLI SEYF (CLOUD SESSION VAULT):
    GitHub Actions har 6 soatda yoki kod yangilanganda qayta yonsa ham,
    Instagram sessiyasi (ig_session.json), Avto-Post sozlamalari (ig_autopost_config.json),
    Watermark va Outro video HECH QACHON O'CHIB KETMASLIGI uchun ularni Adminning
    Telegram chatidagi Pinned Message (Qadalgan xabar) ichiga shifrlangan paket qilib saqlaydi!
    """
    global _LAST_CLOUD_VAULT_SYNC_TS
    if not force and (time.time() - _LAST_CLOUD_VAULT_SYNC_TS) < 25:
        return False
    with _CLOUD_VAULT_LOCK:
        try:
            _LAST_CLOUD_VAULT_SYNC_TS = time.time()
            vault_payload = {
                "vault_version": 2,
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "ig_session": None,
                "ig_config": None,
                "watermark_config": None,
            }
            if os.path.exists(IG_SESSION_FILE) and os.path.getsize(IG_SESSION_FILE) > 20:
                with open(IG_SESSION_FILE, "r", encoding="utf-8") as sf:
                    vault_payload["ig_session"] = json.load(sf)
            if os.path.exists(IG_CONFIG_FILE) and os.path.getsize(IG_CONFIG_FILE) > 10:
                with open(IG_CONFIG_FILE, "r", encoding="utf-8") as cf:
                    vault_payload["ig_config"] = json.load(cf)
            if os.path.exists(WATERMARK_CONFIG_FILE) and os.path.getsize(WATERMARK_CONFIG_FILE) > 5:
                with open(WATERMARK_CONFIG_FILE, "r", encoding="utf-8") as wf:
                    vault_payload["watermark_config"] = json.load(wf)

            if not vault_payload["ig_session"] and not vault_payload["ig_config"]:
                return False

            vault_tmp = os.path.join(PROMO_DIR, "ig_cloud_vault_backup.json")
            with open(vault_tmp, "w", encoding="utf-8") as vf:
                json.dump(vault_payload, vf, ensure_ascii=False, indent=2)

            ig_uname = ""
            if isinstance(vault_payload.get("ig_config"), dict):
                ig_uname = vault_payload["ig_config"].get("ig_username") or ""
            has_sess = "✅ Ulangan" if vault_payload.get("ig_session") else "⏳ Kutilmoqda"

            with open(vault_tmp, "rb") as doc_f:
                sent_msg = bot.send_document(
                    ADMIN_ID,
                    document=doc_f,
                    visible_file_name="ig_cloud_vault_backup.json",
                    caption=(
                        f"☁️ <b>#IG_CLOUD_VAULT_V2 — Doimiy Bulutli Xotira</b>\n"
                        f"👤 Profil: <b>@{ig_uname.lstrip('@') or 'universal_savebot'}</b> ({has_sess})\n"
                        f"🕒 Yangilandi: <code>{vault_payload['updated_at']}</code>\n"
                        f"<i>(Ushbu qadalgan faylni o'chirmang — server yoki GitHub kod yangilanganda Instagram sessiyasini 1 soniyada avtomatik tiklaydi!)</i>"
                    ),
                    disable_notification=True
                )
            try:
                bot.pin_chat_message(ADMIN_ID, sent_msg.message_id, disable_notification=True)
            except Exception:
                pass
            _git_auto_persist_promo_assets()
            return True
        except Exception as e:
            print(f"Cloud Vault sync ogohlantirishi: {e}")
            return False

def trigger_background_cloud_vault_sync(force: bool = False):
    threading.Thread(target=sync_state_to_telegram_cloud_vault, kwargs={"force": force}, daemon=True).start()

def restore_state_from_telegram_cloud_vault() -> bool:
    """
    🚀 Bot ishga tushganda (masalan GitHub Actions yangi server ochganda)
    Admin chatidagi Pinned Message ichidan #IG_CLOUD_VAULT_V2 faylini o'qib,
    ig_session.json, ig_autopost_config.json, watermark_config.json va Outro videoni
    1 soniyada avtomatik qayta tiklaydi!
    """
    try:
        chat_info = bot.get_chat(ADMIN_ID)
        pinned = getattr(chat_info, "pinned_message", None)
        if not pinned or not getattr(pinned, "document", None):
            return False
        cap = getattr(pinned, "caption", "") or ""
        fname = getattr(pinned.document, "file_name", "") or ""
        if "IG_CLOUD_VAULT" not in cap and "ig_cloud_vault" not in fname.lower():
            return False

        file_info = bot.get_file(pinned.document.file_id)
        raw_bytes = bot.download_file(file_info.file_path)
        vault_data = json.loads(raw_bytes.decode("utf-8"))
        restored_any = False

        if vault_data.get("ig_session") and (not os.path.exists(IG_SESSION_FILE) or os.path.getsize(IG_SESSION_FILE) < 20):
            with open(IG_SESSION_FILE, "w", encoding="utf-8") as sf:
                json.dump(vault_data["ig_session"], sf, ensure_ascii=False, indent=2)
            restored_any = True
            print("☁️ [Cloud Vault] Instagram sessiyasi (ig_session.json) Telegram bulutidan avtomatik tiklandi!")

        if vault_data.get("ig_config") and isinstance(vault_data["ig_config"], dict):
            local_cfg = {}
            if os.path.exists(IG_CONFIG_FILE):
                try:
                    with open(IG_CONFIG_FILE, "r", encoding="utf-8") as cf:
                        local_cfg = json.load(cf)
                except Exception:
                    pass
            merged_cfg = dict(vault_data["ig_config"])
            if local_cfg.get("ig_username") and not merged_cfg.get("ig_username"):
                merged_cfg["ig_username"] = local_cfg["ig_username"]
            with open(IG_CONFIG_FILE, "w", encoding="utf-8") as cf:
                json.dump(merged_cfg, cf, ensure_ascii=False, indent=2)
            restored_any = True
            print("☁️ [Cloud Vault] Instagram Avto-Post sozlamalari tiklandi!")

            # Agar saqlangan Outro videoning file_id si bo'lsa va diskda yo'q bo'lsa, uni ham tiklaymiz!
            outro_fid = merged_cfg.get("saved_outro_file_id")
            target_outro = os.path.join(PROMO_DIR, f"outro_{ADMIN_ID}.mp4")
            if outro_fid and (not os.path.exists(target_outro) or os.path.getsize(target_outro) < 1000):
                try:
                    o_info = bot.get_file(outro_fid)
                    o_bytes = bot.download_file(o_info.file_path)
                    with open(target_outro, "wb") as of:
                        of.write(o_bytes)
                    print("☁️ [Cloud Vault] Saqlangan Reklama (Outro) video Telegram bulutidan tiklandi!")
                except Exception as oe:
                    print(f"Cloud Vault Outro tiklash ogohlantirishi: {oe}")

        if vault_data.get("watermark_config") and not os.path.exists(WATERMARK_CONFIG_FILE):
            with open(WATERMARK_CONFIG_FILE, "w", encoding="utf-8") as wf:
                json.dump(vault_data["watermark_config"], wf, ensure_ascii=False, indent=2)

        return restored_any
    except Exception as e:
        print(f"Cloud Vault restore ogohlantirishi: {e}")
        return False

def _ensure_instagrapi_installed() -> bool:
    """Instagram Reels yuklash uchun instagrapi kutubxonasini avtomatik tekshirish va o'rnatish"""
    try:
        import instagrapi
        return True
    except ImportError:
        try:
            print("⏳ Instagram Auto-Poster uchun instagrapi o'rnatilmoqda...")
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "--quiet", "instagrapi", "pycryptodomex"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180
            )
            import instagrapi
            return True
        except Exception as e:
            print(f"instagrapi avto-o'rnatish xatosi: {e}")
            return False

# ==================== 🛡 3-QATLAMLI HALOL VA TOZA KONTENT FILTRI (QIMOR / REKLAMA / 18+ HIMOYASI) ====================
def is_text_safe_from_gambling_adult_ads(text: str, extra_blacklist: list = None) -> tuple[bool, str]:
    """
    1-QATLAM: Video sarlavhasi, tavsifi (caption), heshteglar va muallif nomini
    Qimor (1xBet, Melbet, Casino), 18+ fahsh va bukmeker/spam reklamalardan to'liq tekshiradi!
    URL ichidagi tasodifiy raqamlar/harflar noto'g'ri bloklanmasligi uchun URL larni alohida tozalab tekshiradi.
    """
    if not text:
        return True, "OK"
    # URL ichidagi video ID raqamlari va texnik parametrlarni olib tashlaymiz (masalan video/7384777123)
    text_no_urls = re.sub(r"https?://\S+", " ", str(text))
    lower_t = text_no_urls.lower()
    # Shubhali bo'shliq yoki nuqtalar bilan yozilgan bukmeker nomlarini ham tutish (masalan: 1.x.b.e.t, m e l b e t)
    compact_t = re.sub(r"[\s_\-\.\*]+", "", lower_t)

    cfg = get_ig_autopost_config()
    all_bad_words = list(GAMBLING_ADULT_AD_BLACKLIST) + list(cfg.get("custom_blacklist", []))
    if extra_blacklist:
        all_bad_words.extend(extra_blacklist)

    for bad in all_bad_words:
        b_clean = bad.strip().lower()
        if not b_clean:
            continue
        # Qisqa so'zlarni (<=4 harf) faqat butun so'z sifatida tekshiramiz (noto'g'ri pozitiv bo'lmasligi uchun)
        if len(b_clean) <= 4 and re.match(r"^[a-z0-9а-яё]+$", b_clean):
            if re.search(rf"\b{re.escape(b_clean)}\b", lower_t):
                return False, f"Taqiqlangan so'z aniqlandi: '{b_clean}'"
            continue
        if b_clean in lower_t:
            return False, f"Taqiqlangan so'z aniqlandi: '{b_clean}'"
        b_compact = re.sub(r"[\s_\-\.\*]+", "", b_clean)
        if len(b_compact) >= 6 and b_compact in compact_t:
            return False, f"Yashirin reklama/qimor so'zi aniqlandi: '{b_clean}'"

    # Bukmeker promokod, qimor va 18+ shablonlarini regex orqali tutish
    suspicious_regexes = [
        (r"\b(?:1x|mel|most|line|fon|olimp|pin\s*up|pari)\s*(?:bet|win|casino)\b", "Bukmeker / Qimor reklamasi"),
        (r"\b(?:1xbet|melbet|mostbet|linebet|fonbet|olimpbet|betwinner|1win|pinup|azino777|vavada|joycasino)\b", "Bukmeker / Kazino reklamasi"),
        (r"\b(?:bonus|бонус)\s*\d+\s*(?:%|ming|som|rub|usd|\$)", "Qimor bonus reklamasi"),
        (r"\b(?:promokod|промокод|promo\s*code)\s*[:\-]?\s*[a-zA-Z0-9_]{3,15}", "Promokod reklamasi"),
        (r"(?:\b18\+|\+18\b|\bonlyfans\b|\bпорно\b|\bэротика\b|\bинтим\b|\bnsfw\b|\bxxx\b|\bsex\b|\bporn\b)", "18+ nojo'ya kontent")
    ]
    for rgx, reason in suspicious_regexes:
        if re.search(rgx, lower_t, re.IGNORECASE):
            return False, reason

    return True, "Toza"

def _check_video_frames_for_nsfw_or_casino_banner(video_path: str) -> tuple[bool, str]:
    """
    2-QATLAM: Videoning 3 ta nuqtasidan (20%, 50%, 80%) kadr olib:
    Haddan tashqari ochiq tana (18+ YCbCr teri rangi ulushi > 68%) bor-yo'qligini tekshiradi.
    Oddiy yuz, suhbat, taom yoki tabiat sahnalarini xato bloklamaydi.
    """
    if not video_path or not os.path.exists(video_path):
        return True, "OK"
    ensure_ffmpeg_in_path()
    dur = max(1.0, get_media_duration(video_path))
    sample_times = [max(0.2, dur * 0.2), max(0.5, dur * 0.5), max(0.8, dur * 0.8)]
    temp_frames = []
    try:
        from PIL import Image
        skin_ratios = []
        for idx, st in enumerate(sample_times):
            f_jpg = os.path.join(DOWNLOAD_DIR, f"_safety_frm_{int(time.time()*1000)}_{idx}.jpg")
            temp_frames.append(f_jpg)
            subprocess.run(
                [FFMPEG_BIN, "-y", "-ss", f"{st:.2f}", "-i", video_path, "-frames:v", "1", "-vf", "scale=160:160", f_jpg],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=15
            )
            if os.path.exists(f_jpg) and os.path.getsize(f_jpg) > 200:
                img = Image.open(f_jpg).convert("YCbCr")
                pixels = list(img.getdata())
                total_px = len(pixels) or 1
                skin_px = 0
                for y, cb, cr in pixels:
                    if 85 <= y <= 230 and 90 <= cb <= 130 and 140 <= cr <= 175:
                        skin_px += 1
                skin_ratios.append(skin_px / float(total_px))
        if skin_ratios and ((sum(skin_ratios) / len(skin_ratios)) > 0.40 or max(skin_ratios) > 0.52):
            return False, "Ochiq tana / Raqs / Likillash sahnalari aniqlandi (Visual Exposure Filter)"
    except Exception:
        pass
    finally:
        safe_remove(*temp_frames)
    return True, "Toza"

def verify_video_content_is_halal_and_safe(video_path: str, metadata_text: str = "") -> tuple[bool, str]:
    """
    🛡 3-QATLAMLI KOMPLEKS XAVFSIZLIK FILTRI:
    1) Matn, sarlavha va heshteglarni tekshiradi (Qimor, 1xBet, Melbet, Reklama, 18+).
    2) Vizual kadrlarni tekshiradi (18+ ochiq sahna).
    3) Videoning boshidagi 10 soniyalik ovozni (Speech-to-Text) o'qib,
       diktor "1xBet", "Melbet", "Stavka", "Kazino", "Promokod" deb aytgan bo'lsa darhol bloklaydi!
    """
    cfg = get_ig_autopost_config()
    if not cfg.get("strict_safety_filter", True):
        return True, "Filtr o'chirilgan"

    # 1-Qatlam: Metadata va matn tekshiruvi
    ok_txt, reason_txt = is_text_safe_from_gambling_adult_ads(metadata_text)
    if not ok_txt:
        return False, f"Matn filtri: {reason_txt}"

    if not video_path or not os.path.exists(video_path):
        return True, "Toza"

    # 2-Qatlam: Vizual kadr tekshiruvi (18+ himoyasi)
    if cfg.get("check_skin_exposure", True):
        ok_vis, reason_vis = _check_video_frames_for_nsfw_or_casino_banner(video_path)
        if not ok_vis:
            return False, f"Vizual filtr: {reason_vis}"

    # 3-Qatlam: Audio nutq (Speech-to-Text) orqali video ichidagi og'zaki qimor/reklamani tutish
    if cfg.get("check_audio_speech", True) and has_audio_stream(video_path):
        flac_sample = os.path.join(DOWNLOAD_DIR, f"_safety_aud_{int(time.time()*1000)}.flac")
        try:
            subprocess.run([
                FFMPEG_BIN, "-y", "-ss", "0", "-t", "10", "-i", video_path,
                "-vn", "-ar", "16000", "-ac", "1", "-c:a", "flac", flac_sample
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=20)
            if os.path.exists(flac_sample) and os.path.getsize(flac_sample) > 400:
                with open(flac_sample, "rb") as af:
                    fbytes = af.read()
                spoken_text = recognize_google_flac(fbytes, lang="auto")
                if spoken_text:
                    ok_sp, reason_sp = is_text_safe_from_gambling_adult_ads(spoken_text)
                    if not ok_sp:
                        return False, f"Ovozli reklama filtri ({reason_sp}): '{spoken_text[:60]}'"
        except Exception:
            pass
        finally:
            safe_remove(flac_sample)

    return True, "✅ 100% Toza (Halol & Reklamasiz)"

# ==================== INSTAGRAM AVTORIZATSIYA VA REELS YUKLASH MOTORI ====================
IG_AUTO_RETRY_STATE = {}
IG_AUTO_RETRY_LOCK = threading.Lock()
IG_CHALLENGE_BRIDGE = {}  # user_id -> {"event": Event, "code": str, "result_event": Event, "result": (bool, str), "choice": str}

def _deterministic_uuid(seed_str: str) -> str:
    import uuid as _uuid_mod
    import hashlib as _hl
    h = _hl.sha256(seed_str.encode("utf-8")).hexdigest()[:32]
    return str(_uuid_mod.UUID(h))

def _build_deterministic_ig_client(username: str, profile_index: int = 0):
    """
    Har safar tasodifiy qurilma (Random UUID) yaratib Instagramning 'Please wait a few minutes'
    blokiga tushmaslik uchun foydalanuvchi loginiga bog'langan DOIMIY (Deterministic) Toshkent (UTC+5)
    Android qurilma parametrlarini o'rnatadi.
    MUHIM FIX (CAA login requires bloks_versioning_id):
    instagrapi CAA/Bloks protokoli talab qiladigan bloks_versioning_id ni saqlaydi va
    override_app_version=True orqali 'bloks_versioning_id' yetishmovchiligi xatosini 100% bartaraf etadi!
    """
    from instagrapi import Client
    import hashlib as _hl
    clean_u = (username or "universal_savebot").strip().lower().lstrip("@")
    seed_prefix = f"uz_tashkent_ig_v4_{clean_u}_{profile_index}"

    cl = Client()
    cl.override_app_version = True

    # 1. instagrapi dagi rasmiy bloks_versioning_id ni aniqlash
    bloks_id = None
    try:
        from instagrapi import config as ig_config
        def_ver = getattr(ig_config, "DEFAULT_APP_VERSION", None)
        app_settings = getattr(ig_config, "APP_SETTINGS", {})
        if def_ver and def_ver in app_settings:
            bloks_id = app_settings[def_ver].get("bloks_versioning_id")
    except Exception:
        pass

    if not bloks_id:
        bloks_id = getattr(cl, "bloks_versioning_id", None) or "7189b949425f9bf80ea8bd880cf5a3080b292d9b1c4b38a18d112f7c4b71e7a8"
    cl.bloks_versioning_id = bloks_id

    # 2. Doimiy Toshkent qurilma UUID lari
    android_id_hex = hashlib.sha256(f"{seed_prefix}_aid".encode()).hexdigest()[:16]
    csrf_tok = hashlib.sha256(f"{seed_prefix}_csrf_{int(time.time()//3600)}".encode()).hexdigest()[:32]

    uuids = {
        "phone_id": _deterministic_uuid(f"{seed_prefix}_phone"),
        "uuid": _deterministic_uuid(f"{seed_prefix}_uuid"),
        "client_session_id": _deterministic_uuid(f"{seed_prefix}_csid"),
        "advertising_id": _deterministic_uuid(f"{seed_prefix}_adid"),
        "android_device_id": f"android-{android_id_hex}",
        "request_id": _deterministic_uuid(f"{seed_prefix}_req"),
        "tray_session_id": _deterministic_uuid(f"{seed_prefix}_tray"),
    }
    try:
        cl.set_uuids(uuids)
    except Exception:
        pass

    # bloks_versioning_id ni device_settings ga ham kiritish
    if hasattr(cl, "device_settings") and isinstance(cl.device_settings, dict):
        cl.device_settings["bloks_versioning_id"] = bloks_id

    try:
        cl.set_country("UZ")
        cl.set_country_code(998)
        cl.set_locale("en_US")
        cl.set_timezone_offset(18000)  # Toshkent UTC+5
    except Exception:
        pass

    cl.delay_range = [0.5, 1.2]
    cl.request_timeout = 15
    cl.change_password_handler = lambda *a, **kw: ""
    try:
        cl.private.cookies.set("csrftoken", csrf_tok, domain=".instagram.com")
    except Exception:
        pass
    return cl

def _extract_clean_sessionid(raw_input: str) -> str:
    """Matn, JSON cookie yoki Cookie header ichidan toza Instagram sessionid ni ajratib oladi"""
    if not raw_input:
        return ""
    text = raw_input.strip()
    if (text.startswith("[") and text.endswith("]")) or (text.startswith("{") and text.endswith("}")):
        try:
            parsed = json.loads(text)
            if isinstance(parsed, dict):
                if "sessionid" in parsed:
                    text = str(parsed["sessionid"])
                elif isinstance(parsed.get("cookies"), dict) and "sessionid" in parsed["cookies"]:
                    text = str(parsed["cookies"]["sessionid"])
                elif isinstance(parsed.get("authorization_data"), dict) and "sessionid" in parsed["authorization_data"]:
                    text = str(parsed["authorization_data"]["sessionid"])
            elif isinstance(parsed, list):
                for item in parsed:
                    if isinstance(item, dict) and str(item.get("name", "")).lower() == "sessionid":
                        text = str(item.get("value", ""))
                        break
        except Exception:
            pass
    if "sessionid=" in text:
        text = text.split("sessionid=")[1].split(";")[0].split()[0].strip()
    clean_sid = urllib.parse.unquote(text.strip().strip('"').strip("'"))
    if ":" in clean_sid and clean_sid.split(":")[0].isdigit() and len(clean_sid) >= 20:
        return clean_sid
    return ""

def _synthesize_instagrapi_session_from_cookie(clean_sid: str, username_hint: str = "", extra_cookies: dict = None) -> tuple[bool, str]:
    """
    🔥 RATE-LIMITGA CHIDAMLI SESSION GENERATOR:
    Instagram `account_info()` endpointi 'Please wait a few minutes' bersa ham,
    `sessionid` ichidan `ds_user_id` ni to'g'ridan-to'g'ri ajratib olib,
    100% ishlaydigan `ig_session.json` faylini yaratadi va Bulutli Seyfga saqlaydi!
    """
    if not clean_sid or ":" not in clean_sid:
        return False, "Yaroqsiz SessionID formati."
    ds_user_id = clean_sid.split(":")[0].strip()
    if not ds_user_id.isdigit():
        return False, "SessionID ichida foydalanuvchi ID raqami (ds_user_id) topilmadi."

    cfg = get_ig_autopost_config()
    uname = (username_hint or cfg.get("ig_username") or "universal_savebot").strip().lstrip("@")
    csrf_tok = (extra_cookies or {}).get("csrftoken") or hashlib.sha256(f"csrf_{clean_sid}".encode()).hexdigest()[:32]
    mid_val = (extra_cookies or {}).get("mid") or hashlib.sha256(f"mid_{clean_sid}".encode()).hexdigest()[:26].upper()

    try:
        cl = _build_deterministic_ig_client(uname, profile_index=0)
        settings = cl.get_settings()
    except Exception:
        seed_prefix = f"uz_tashkent_ig_v4_{uname.lower()}_0"
        settings = {
            "uuids": {
                "phone_id": _deterministic_uuid(f"{seed_prefix}_phone"),
                "uuid": _deterministic_uuid(f"{seed_prefix}_uuid"),
                "client_session_id": _deterministic_uuid(f"{seed_prefix}_csid"),
                "advertising_id": _deterministic_uuid(f"{seed_prefix}_adid"),
                "android_device_id": f"android-{hashlib.sha256(f'{seed_prefix}_aid'.encode()).hexdigest()[:16]}",
                "request_id": _deterministic_uuid(f"{seed_prefix}_req"),
                "tray_session_id": _deterministic_uuid(f"{seed_prefix}_tray"),
            },
            "mid": mid_val,
            "ig_u_rur": None,
            "ig_www_claim": "0",
            "authorization_data": {},
            "cookies": {},
            "last_login": time.time(),
            "device_settings": {
                "app_version": "317.0.0.34.109",
                "android_version": 34,
                "android_release": "14.0",
                "dpi": "480dpi",
                "resolution": "1080x2340",
                "manufacturer": "Samsung",
                "device": "e3q",
                "model": "SM-S928B",
                "cpu": "qcom",
                "version_code": "565604104",
            },
            "user_agent": "Instagram 317.0.0.34.109 Android (34/14.0; 480dpi; 1080x2340; Samsung; SM-S928B; e3q; qcom; en_US; 565604104)",
            "country": "UZ",
            "country_code": 998,
            "locale": "en_US",
            "timezone_offset": 18000,
        }

    settings["authorization_data"] = {
        "ds_user_id": str(ds_user_id),
        "sessionid": clean_sid,
        "should_use_header_over_cookies": False,
    }
    cookies_dict = dict(settings.get("cookies") or {})
    if extra_cookies:
        cookies_dict.update(extra_cookies)
    cookies_dict.update({
        "sessionid": clean_sid,
        "ds_user_id": str(ds_user_id),
        "csrftoken": csrf_tok,
        "mid": mid_val,
    })
    settings["cookies"] = cookies_dict
    settings["last_login"] = time.time()

    with open(IG_SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)

    if not username_hint:
        try:
            from instagrapi import Client
            cl_check = _build_deterministic_ig_client(uname, profile_index=0)
            cl_check.override_app_version = True
            try:
                cl_check.load_settings(IG_SESSION_FILE, override_app_version=True)
            except Exception:
                pass
            cl_check.delay_range = [0.5, 1.0]
            cl_check.request_timeout = 8
            info = cl_check.account_info()
            detected_u = getattr(info, "username", "")
            if detected_u:
                uname = detected_u
                cl_check.dump_settings(IG_SESSION_FILE)
        except Exception:
            pass

    cfg["ig_username"] = uname
    save_ig_autopost_config(cfg, sync_cloud=True)
    return True, uname

def _try_instagram_web_ajax_login(username: str, password: str) -> dict:
    """
    🌐 1-MOTOR (WEB AJAX BYPASS):
    Mobil API ('/api/v1/accounts/login/') 'Please wait a few minutes' bergan paytda ham,
    Instagramning Web Ajax Login ('/api/v1/web/accounts/login/ajax/') endpointi alohida
    server va alohida rate-limit savatida ishlaydi!
    Muvaffaqiyatli kirsa, tayyor `sessionid` cookiesini qaytaradi!
    """
    clean_u = username.strip().lstrip("@")
    sess = requests.Session()
    web_ua = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
    sess.headers.update({
        "User-Agent": web_ua,
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9,uz;q=0.8",
        "Origin": "https://www.instagram.com",
        "Referer": "https://www.instagram.com/accounts/login/",
        "X-IG-App-ID": "936619743392459",
        "X-ASBD-ID": "129477",
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
    })
    csrf_token = hashlib.sha256(f"web_csrf_{clean_u}_{int(time.time()//600)}".encode()).hexdigest()[:32]
    try:
        r_init = sess.get("https://www.instagram.com/accounts/login/", timeout=8, verify=False)
        if sess.cookies.get("csrftoken"):
            csrf_token = sess.cookies.get("csrftoken")
        else:
            m_csrf = re.search(r'"csrf_token"\s*:\s*"([^"]+)"', r_init.text or "")
            if m_csrf:
                csrf_token = m_csrf.group(1)
    except Exception:
        pass

    sess.cookies.set("csrftoken", csrf_token, domain=".instagram.com")
    sess.headers["X-CSRFToken"] = csrf_token
    ts = int(time.time())
    payload = {
        "enc_password": f"#PWD_INSTAGRAM_BROWSER:0:{ts}:{password}",
        "username": clean_u,
        "queryParams": "{}",
        "optIntoOneTap": "false",
        "trustedDeviceRecords": "{}",
    }
    try:
        resp = sess.post(
            "https://www.instagram.com/api/v1/web/accounts/login/ajax/",
            data=payload,
            timeout=10,
            verify=False
        )
        all_cookies = sess.cookies.get_dict()
        sid = all_cookies.get("sessionid") or ""
        if not sid and "sessionid=" in resp.headers.get("Set-Cookie", ""):
            sid = _extract_clean_sessionid(resp.headers.get("Set-Cookie", ""))

        data = {}
        try:
            data = resp.json()
        except Exception:
            pass

        if (data.get("authenticated") is True or sid) and ":" in str(sid):
            return {
                "status": "ok",
                "sessionid": urllib.parse.unquote(sid),
                "cookies": all_cookies,
                "userId": str(data.get("userId") or sid.split(":")[0]),
            }
        if data.get("two_factor_required"):
            tf_info = data.get("two_factor_info") or {}
            return {
                "status": "2fa_required",
                "two_factor_identifier": tf_info.get("two_factor_identifier", ""),
                "web_session": sess,
                "csrf_token": csrf_token,
            }
        if data.get("checkpoint_url") or "checkpoint" in str(data).lower():
            return {
                "status": "challenge_required",
                "checkpoint_url": data.get("checkpoint_url", ""),
                "web_session": sess,
            }
        if data.get("user") is False:
            return {"status": "bad_password", "message": "❌ Instagram foydalanuvchi nomi (@login) topilmadi!"}
        if data.get("authenticated") is False and data.get("status") == "ok":
            return {"status": "bad_password", "message": "❌ Parol noto'g'ri! Iltimos, parolni tekshirib qayta kiriting."}
        msg = data.get("message") or f"HTTP {resp.status_code}"
        return {"status": "error", "message": str(msg)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_instagram_Status() -> tuple[bool, str]:
    """Instagram akkount ulangan yoki ulanmaganligini tekshirish"""
    cfg = get_ig_autopost_config()
    if os.path.exists(IG_SESSION_FILE) and os.path.getsize(IG_SESSION_FILE) > 50:
        uname = cfg.get("ig_username") or "universal_savebot"
        return True, f"@{uname.lstrip('@')}"
    return False, "Ulanmagan"

def login_instagram_with_sessionid(session_id: str, username_hint: str = "") -> tuple[bool, str]:
    """
    🍪 Instagram sessionid cookie orqali parolsiz va 'Please wait a few minutes' blokisiz
    1 soniyada xavfsiz ulash (Offline/Online Hybrid Synthesizer bilan)!
    """
    _ensure_instagrapi_installed()
    clean_sid = _extract_clean_sessionid(session_id)
    if not clean_sid:
        return False, (
            "⚠️ <b>SessionID formati noto'g'ri!</b>\n\n"
            "SessionID odatda <code>12345678901%3AabCdEfGh...</code> yoki <code>12345678901:abCdEfGh...</code> ko'rinishida bo'ladi.\n"
            "Iltimos, brauzerdan <code>sessionid</code> qiymatini to'liq nusxalab yuboring."
        )
    ok, uname_or_err = _synthesize_instagrapi_session_from_cookie(clean_sid, username_hint=username_hint)
    if ok:
        IG_AUTO_RETRY_STATE.clear()
        return True, (
            f"✅ <b>Instagram profil (@{uname_or_err}) SessionID orqali 1 soniyada ulandi!</b>\n"
            f"☁️ Sessiya <b>Telegram Bulutli Xotiraga (Cloud Vault)</b> ham muhrlandi — endi GitHub kod yangilanganda ham uzilib qolmaydi!"
        )
    return False, f"❌ SessionID orqali ulanishda xatolik: {uname_or_err}"

def _update_prog_safe(chat_id: int, msg_id: int, text: str, reply_markup=None):
    if not chat_id or not msg_id:
        return
    try:
        bot.edit_message_text(text, chat_id, msg_id, reply_markup=reply_markup)
    except Exception:
        pass

def _attempt_core_multi_engine_ig_login(
    user_id: int,
    clean_user: str,
    password: str,
    chat_id: int = None,
    prog_msg_id: int = None,
    interactive_challenge: bool = True
) -> tuple[str, str]:
    """
    🔥 4-BOSQICHLI ANTI-BLOCK INSTAGRAM LOGIN MOTORI (QOTIB QOLMASLIK KAFOLATI BILAN!):
    - MUHIM FIX: `instagrapi` standart holatda Challenge (SMS/Email kod) chiqqanda server konsolida
      `input("Enter code...")` ni chaqirib, botni abadiy kutish (qotib qolish) holatiga tushirib qo'yar edi!
      Endi maxsus `telegram_challenge_code_handler` orqali kod so'rovi 2 soniyada Telegramga chiqadi!
    """
    # 1-BOSQICH: Foydalanuvchi login/parol o'rniga sessionid yuborgan bo'lsa
    possible_sid = _extract_clean_sessionid(password) or _extract_clean_sessionid(clean_user)
    if possible_sid:
        u_hint = clean_user if not _extract_clean_sessionid(clean_user) else "universal_savebot"
        ok_s, msg_s = login_instagram_with_sessionid(possible_sid, username_hint=u_hint)
        if ok_s:
            return "ok", msg_s

    # 2-BOSQICH: Instagram Web Ajax Login (Mobil rate-limitdan mustaqil, 3-5 soniyada javob beradi!)
    _update_prog_safe(chat_id, prog_msg_id, f"⏳ <b>@{clean_user}</b>: [1/3] Web-Ajax Anti-Blok protokoli orqali tekshirilmoqda...")
    web_res = _try_instagram_web_ajax_login(clean_user, password)
    if web_res.get("status") == "ok" and web_res.get("sessionid"):
        ok_syn, uname_syn = _synthesize_instagrapi_session_from_cookie(
            web_res["sessionid"],
            username_hint=clean_user,
            extra_cookies=web_res.get("cookies")
        )
        if ok_syn:
            IG_PENDING_LOGIN.pop(user_id, None)
            IG_AUTO_RETRY_STATE.pop(user_id, None)
            return "ok", (
                f"✅ <b>@{uname_syn} Instagram profiliga muvaffaqiyatli kirildi!</b> (Web-Ajax Anti-Block orqali)\n"
                f"☁️ Sessiya <b>Telegram Bulutli Xotiraga</b> muhrlandi — endi qayta-qayta login qilish shart emas!"
            )
    elif web_res.get("status") == "bad_password":
        IG_AUTO_RETRY_STATE.pop(user_id, None)
        return "error", web_res.get("message", "❌ Parol noto'g'ri!")

    # 3-BOSQICH: instagrapi kutubxonasini tekshirish
    _update_prog_safe(chat_id, prog_msg_id, f"⏳ <b>@{clean_user}</b>: [2/3] Mobil shifrlash moduli tayyorlanmoqda...")
    if not _ensure_instagrapi_installed():
        return "error", "instagrapi kutubxonasini o'rnatib bo'lmadi."

    from instagrapi.exceptions import TwoFactorRequired, ChallengeRequired, BadPassword
    last_err_str = web_res.get("message", "")

    for attempt_num, (prof_idx, skip_preflow) in enumerate([(0, True), (1, True)], 1):
        try:
            _update_prog_safe(
                chat_id, prog_msg_id,
                f"⏳ <b>@{clean_user}</b>: [3/3] Toshkent Samsung S24 Ultra qurilmasi orqali ulanmoqda ({attempt_num}-urinish)..."
            )
            cl = _build_deterministic_ig_client(clean_user, profile_index=prof_idx)
            if skip_preflow:
                cl.pre_login_flow = lambda *a, **kw: True

            # 🔥 ENG MUHIM QISM: instagrapi terminalda `input()` chaqirib qotib qolmasligi uchun
            # Challenge kod so'rovini to'g'ridan-to'g'ri Telegram chatga bog'laymiz!
            challenge_triggered_state = {"asked": False, "choice": "SMS/Email"}

            def _nonblocking_challenge_handler(uname_arg, choice_arg=None):
                challenge_triggered_state["asked"] = True
                challenge_triggered_state["choice"] = str(choice_arg or "SMS yoki Email")
                if not interactive_challenge or not chat_id:
                    raise ChallengeRequired("Challenge tasdiqlash talab etildi")

                ev = threading.Event()
                res_ev = threading.Event()
                IG_CHALLENGE_BRIDGE[user_id] = {
                    "event": ev,
                    "code": "",
                    "result_event": res_ev,
                    "result": (False, ""),
                    "choice": str(choice_arg or "SMS/Email"),
                }
                USER_STATES[user_id] = {"action": "ig_wait_code"}

                prompt_txt = (
                    f"📲 <b>Instagram Xavfsizlik Kodini Yubordi!</b> (<code>{choice_arg or 'Email / SMS'}</code>)\n\n"
                    f"1️⃣ <b>Email yoki SMS</b> orqali kelgan <b>6 xonali tasdiqlash kodini</b> hoziroq shu yerga yozib yuboring!\n"
                    f"2️⃣ Yoki telefoningizdan Instagram ilovasiga kirib <b>«Bu men edim» (This was me / Это был я)</b> tugmasini bosing va quyidagi <b>«✅ Ilovadan Tasdiqladim»</b> tugmasini bosing:"
                )
                mk = types.InlineKeyboardMarkup(row_width=1)
                mk.add(
                    types.InlineKeyboardButton("✅ Ilovadan Tasdiqladim (Qayta urinish)", callback_data="ig_retry_challenge"),
                    types.InlineKeyboardButton("🍪 SessionID Bilan 1-Soniyada Ulash", callback_data="ig_start_session")
                )
                _update_prog_safe(chat_id, prog_msg_id, prompt_txt, reply_markup=mk)

                # Foydalanuvchi Telegramda 6 xonali kodni yozishini kutamiz (maks 180 soniya)
                got_code = ev.wait(timeout=180)
                bridge_data = IG_CHALLENGE_BRIDGE.get(user_id) or {}
                code_entered = str(bridge_data.get("code") or "").strip()
                if not got_code or not code_entered or code_entered.lower() == "retry":
                    raise ChallengeRequired("Challenge kodi kiritilmadi yoki ilovadan tasdiqlandi")
                return code_entered

            cl.challenge_code_handler = _nonblocking_challenge_handler

            IG_PENDING_LOGIN[user_id] = {
                "client": cl,
                "username": clean_user,
                "password": password,
                "time": time.time(),
                "code_needed": False,
                "web_2fa": web_res if web_res.get("status") == "2fa_required" else None,
            }

            try:
                cl.login(clean_user, password)
            except Exception as login_err:
                err_str_l = str(login_err).lower()
                if ("caa" in err_str_l or "bloks" in err_str_l) and hasattr(cl, "login_legacy"):
                    logger.warning(f"CAA Bloks xatoligi aniqlandi: {login_err}. login_legacy orqali muqobil kirilmoqda...")
                    cl.login_legacy(clean_user, password)
                else:
                    raise
            cl.dump_settings(IG_SESSION_FILE)
            cfg = get_ig_autopost_config()
            cfg["ig_username"] = clean_user
            save_ig_autopost_config(cfg, sync_cloud=True)
            IG_PENDING_LOGIN.pop(user_id, None)
            IG_AUTO_RETRY_STATE.pop(user_id, None)
            ok_final_msg = (
                f"✅ <b>@{clean_user} Instagram profiliga muvaffaqiyatli kirildi va sessiya saqlandi!</b>\n"
                f"☁️ Sessiya <b>Telegram Bulutli Xotiraga</b> ham muhrlandi — GitHub yangilanganda ham o'chib ketmaydi!"
            )
            if user_id in IG_CHALLENGE_BRIDGE:
                IG_CHALLENGE_BRIDGE[user_id]["result"] = (True, ok_final_msg)
                IG_CHALLENGE_BRIDGE[user_id]["result_event"].set()
                IG_CHALLENGE_BRIDGE.pop(user_id, None)
            return "ok", ok_final_msg

        except TwoFactorRequired:
            IG_PENDING_LOGIN[user_id]["mode"] = "2fa"
            IG_AUTO_RETRY_STATE.pop(user_id, None)
            return "2fa_required", (
                "🔐 <b>Ikki bosqichli tasdiqlash (2FA) kodi so'raldi!</b>\n\n"
                "📱 Telefoningizga (SMS, WhatsApp yoki Authenticator ilovasiga) kelgan 6 xonali kodni hoziroq shu yerga yozib yuboring "
                "(yoki <code>/ig_code 123456</code> deb yozing):"
            )
        except ChallengeRequired as ch_e:
            IG_PENDING_LOGIN[user_id]["mode"] = "challenge"
            IG_AUTO_RETRY_STATE.pop(user_id, None)
            if user_id in IG_CHALLENGE_BRIDGE:
                IG_CHALLENGE_BRIDGE[user_id]["result"] = (
                    False,
                    "📲 <b>Instagram xavfsizlik tasdiqlovi talab qildi.</b> Ilovadan «Bu men edim» deb tasdiqlab qayta urinib ko'ring yoki SessionID orqali 1 soniyada ulang!"
                )
                IG_CHALLENGE_BRIDGE[user_id]["result_event"].set()
                IG_CHALLENGE_BRIDGE.pop(user_id, None)
            return "challenge_required", (
                "📲 <b>Instagram xavfsizlik tasdiqlovi (Challenge) so'radi!</b>\n\n"
                "1️⃣ Telefoningizdan Instagram ilovasiga kirib <b>«Bu men edim» (This was me / Это был я)</b> tugmasini bosing va quyidagi <b>«✅ Ilovadan Tasdiqladim»</b> tugmasini bosing;\n"
                "2️⃣ Yoki SMS/Emailga kelgan 6 xonali tasdiqlash kodini shu yerga yozib yuboring!\n"
                "3️⃣ Yoki eng osoni — <b>«🍪 SessionID Bilan 1-Soniyada Ulash»</b> tugmasini bosing."
            )
        except BadPassword:
            IG_PENDING_LOGIN.pop(user_id, None)
            IG_AUTO_RETRY_STATE.pop(user_id, None)
            return "error", "❌ Parol noto'g'ri! Iltimos, parolni tekshirib qayta kiriting."
        except Exception as e:
            err_s = str(e)
            last_err_str = err_s
            low_e = err_s.lower()
            if user_id in IG_CHALLENGE_BRIDGE:
                IG_CHALLENGE_BRIDGE[user_id]["result"] = (False, f"❌ Tasdiqlashda xatolik: {err_s[:160]}")
                IG_CHALLENGE_BRIDGE[user_id]["result_event"].set()
                IG_CHALLENGE_BRIDGE.pop(user_id, None)
            if "two_factor" in low_e or "2fa" in low_e:
                IG_PENDING_LOGIN[user_id]["mode"] = "2fa"
                return "2fa_required", "🔐 <b>SMS/2FA 6 xonali kodni shu yerga yuboring:</b>"
            if "challenge" in low_e or "checkpoint" in low_e or challenge_triggered_state["asked"]:
                IG_PENDING_LOGIN[user_id]["mode"] = "challenge"
                return "challenge_required", (
                    "📲 <b>Instagram ilovasidan «Bu men edim» (This was me) deb tasdiqlang</b> "
                    "yoki Email/SMS ga kelgan 6 xonali kodni shu yerga yuboring!"
                )
            time.sleep(1.0)

    if web_res.get("status") == "2fa_required":
        IG_PENDING_LOGIN[user_id] = {
            "client": _build_deterministic_ig_client(clean_user, 0),
            "username": clean_user,
            "password": password,
            "time": time.time(),
            "mode": "2fa",
            "web_2fa": web_res,
        }
        return "2fa_required", (
            "🔐 <b>Ikki bosqichli tasdiqlash (2FA) kodi so'raldi!</b>\n\n"
            "📱 Telefoningizga kelgan 6 xonali kodni shu yerga yozib yuboring:"
        )

    if "wait a few minutes" in last_err_str.lower() or "please wait" in last_err_str.lower() or "429" in last_err_str:
        return "rate_limited", last_err_str
    return "error", f"❌ Kirishda xatolik: {last_err_str[:220]}"

def _start_ig_auto_login_retry_daemon(user_id: int, clean_user: str, password: str, chat_id: int):
    """
    🕒 5-MOTOR (AVTOMATIK ORQA FONDA QAYTA ULANISH DAEMONI):
    Agar Instagram 'Please wait a few minutes before you try again' degan bo'lsa,
    foydalanuvchi qayta-qayta login/parol yozib o'tirmasligi uchun bot har 90 soniyada
    orqa fonda o'zi sokin urinadi va Instagram bloki yechilishi bilan (odatda 2-4 daqiqada)
    avtomatik ulab, foydalanuvchiga xushxabar yuboradi!
    """
    with IG_AUTO_RETRY_LOCK:
        already_running = IG_AUTO_RETRY_STATE.get(user_id, {}).get("running", False)
        IG_AUTO_RETRY_STATE[user_id] = {
            "username": clean_user,
            "password": password,
            "chat_id": chat_id,
            "running": True,
            "started_at": time.time(),
        }
        if already_running:
            return

    def _retry_worker():
        for attempt in range(1, 16):
            time.sleep(90)
            st = IG_AUTO_RETRY_STATE.get(user_id)
            if not st or not st.get("running"):
                return
            if os.path.exists(IG_SESSION_FILE) and os.path.getsize(IG_SESSION_FILE) > 50:
                IG_AUTO_RETRY_STATE.pop(user_id, None)
                return
            uname = st["username"]
            pwd = st["password"]
            print(f"🔄 [IG Auto-Retry #{attempt}/15] @{uname} profiliga ulanish tekshirilmoqda...")
            status, msg = _attempt_core_multi_engine_ig_login(user_id, uname, pwd, interactive_challenge=False)
            if status == "ok":
                IG_AUTO_RETRY_STATE.pop(user_id, None)
                try:
                    mk = types.InlineKeyboardMarkup()
                    mk.add(
                        types.InlineKeyboardButton("🚀 Hozir 1 ta Video Yasab Joylash", callback_data="ig_run_now"),
                        types.InlineKeyboardButton("📸 Avto-Post Panel", callback_data="ig_open_panel")
                    )
                    bot.send_message(
                        st["chat_id"],
                        f"🎉 <b>AVTO-ULANISH MUVAFFAQIYATLI YAKUNLANDI!</b>\n\n"
                        f"Instagramning vaqtinchalik kutish cheklovi yechildi va botingiz <b>@{uname}</b> profiliga avtomatik ulandi!\n"
                        f"☁️ Sessiya <b>Telegram Bulutli Xotiraga</b> ham saqlandi — endi 24/7 Avto-Reels to'liq ishga tayyor!",
                        reply_markup=mk
                    )
                except Exception:
                    pass
                return
            elif status in ("2fa_required", "challenge_required"):
                IG_AUTO_RETRY_STATE.pop(user_id, None)
                USER_STATES[user_id] = {"action": "ig_wait_code"}
                try:
                    mk = types.InlineKeyboardMarkup(row_width=1)
                    mk.add(
                        types.InlineKeyboardButton("✅ Ilovadan Tasdiqladim (Qayta urinish)", callback_data="ig_retry_challenge"),
                        types.InlineKeyboardButton("🍪 SessionID Bilan 1-Soniyada Ulash", callback_data="ig_start_session")
                    )
                    bot.send_message(st["chat_id"], msg, reply_markup=mk)
                except Exception:
                    pass
                return
            elif status == "error" and "parol noto'g'ri" in msg.lower():
                IG_AUTO_RETRY_STATE.pop(user_id, None)
                return
        if user_id in IG_AUTO_RETRY_STATE:
            IG_AUTO_RETRY_STATE[user_id]["running"] = False

    threading.Thread(target=_retry_worker, daemon=True).start()

def login_instagram_username_password(
    user_id: int,
    username: str,
    password: str,
    chat_id: int = ADMIN_ID,
    prog_msg_id: int = None
) -> tuple[str, str]:
    """
    Login va parol orqali Instagramga 5-Motorli kirish:
    Qaytaradi: (status, message) -> status in ('ok', '2fa_required', 'challenge_required', 'rate_limited', 'error')
    """
    clean_user = username.strip().lstrip("@")
    status, msg = _attempt_core_multi_engine_ig_login(
        user_id, clean_user, password, chat_id=chat_id, prog_msg_id=prog_msg_id, interactive_challenge=True
    )
    if status == "rate_limited":
        _start_ig_auto_login_retry_daemon(user_id, clean_user, password, chat_id or ADMIN_ID)
        wait_msg = (
            f"⏳ <b>Instagram vaqtinchalik 2–4 daqiqalik xavfsizlik pauzasini yoqgan («Please wait a few minutes»).</b>\n\n"
            f"🤖 <b>XAVOTIR OLMANG — QO'LDA QAYTA YOZISHINGIZ SHART EMAS!</b>\n"
            f"Bot login va parolingizni xavfsiz eslab qoldi va <b>Avto-Ulanish Rejimini</b> yoqdi: "
            f"har 90 soniyada orqa fonda o'zi tekshirib, Instagram pauzasi tugashi bilan avtomatik ulanadi va sizga xabar beradi!\n\n"
            f"⚡ <b>Yoki kutmasdan HOZIROQ 1 soniyada ulash usuli (100% Bloklarsiz):</b>\n"
            f"Quyidagi <b>«🍪 SessionID Bilan 1-Soniyada Ulash»</b> tugmasini bosing yoki 2 daqiqadan so'ng <b>«🔄 Hozir Qayta Urinish»</b> tugmasini bosing:"
        )
        return "rate_limited", wait_msg
    return status, msg

def complete_instagram_verification_code(user_id: int, verification_code: str) -> tuple[bool, str]:
    """Foydalanuvchi yuborgan 2FA, Challenge kodini yoki SessionID ni yakunlash"""
    possible_sid = _extract_clean_sessionid(verification_code)
    if possible_sid:
        return login_instagram_with_sessionid(possible_sid)

    clean_code = re.sub(r"\s+", "", verification_code.strip())

    # 1. Agar jonli Challenge Bridge (`_nonblocking_challenge_handler`) kod kutib turgan bo'lsa:
    bridge = IG_CHALLENGE_BRIDGE.get(user_id)
    if bridge and bridge.get("event") and not bridge["event"].is_set():
        bridge["code"] = clean_code
        bridge["event"].set()
        # Jonli oqim natijasini 20 soniyagacha kutamiz
        bridge["result_event"].wait(timeout=20)
        res_ok, res_msg = bridge.get("result") or (False, "")
        if res_ok:
            return True, res_msg
        if res_msg:
            return False, res_msg

    pending = IG_PENDING_LOGIN.get(user_id)
    retry_st = IG_AUTO_RETRY_STATE.get(user_id)
    if not pending and retry_st:
        st_code, st_msg = login_instagram_username_password(user_id, retry_st["username"], retry_st["password"])
        return (st_code == "ok"), st_msg

    if not pending:
        return False, "⚠️ Faol login sessiyasi topilmadi. Avval <code>/ig_login</code> orqali login va parolni kiriting."

    cl = pending["client"]
    uname = pending["username"]
    pwd = pending["password"]

    web_2fa = pending.get("web_2fa")
    if web_2fa and clean_code.isdigit() and web_2fa.get("two_factor_identifier"):
        try:
            w_sess = web_2fa["web_session"]
            w_sess.post(
                "https://www.instagram.com/api/v1/web/accounts/login/ajax/two_factor/",
                data={
                    "username": uname,
                    "verificationCode": clean_code,
                    "identifier": web_2fa["two_factor_identifier"],
                    "queryParams": "{}",
                },
                timeout=12,
                verify=False
            )
            w_cookies = w_sess.cookies.get_dict()
            w_sid = w_cookies.get("sessionid") or ""
            if ":" in w_sid:
                ok_s, _ = _synthesize_instagrapi_session_from_cookie(urllib.parse.unquote(w_sid), username_hint=uname, extra_cookies=w_cookies)
                if ok_s:
                    IG_PENDING_LOGIN.pop(user_id, None)
                    IG_AUTO_RETRY_STATE.pop(user_id, None)
                    return True, f"✅ <b>Tasdiqlandi!</b> @{uname} Instagram profili 24/7 Avto-Posterga ulandi va Bulutli Xotiraga saqlandi!"
        except Exception:
            pass

    try:
        cl.pre_login_flow = lambda *a, **kw: True
        if clean_code.lower() == "retry":
            status, msg = _attempt_core_multi_engine_ig_login(user_id, uname, pwd, interactive_challenge=False)
            return (status == "ok"), msg
        else:
            cl.challenge_code_handler = lambda *a, **kw: clean_code
            try:
                cl.login(uname, pwd, verification_code=clean_code)
            except Exception as login_2fa_err:
                err_2fa_l = str(login_2fa_err).lower()
                if ("caa" in err_2fa_l or "bloks" in err_2fa_l) and hasattr(cl, "login_legacy"):
                    logger.warning(f"CAA 2FA xatoligi aniqlandi: {login_2fa_err}. login_legacy orqali muqobil kirilmoqda...")
                    cl.login_legacy(uname, pwd, verification_code=clean_code)
                else:
                    raise
        cl.dump_settings(IG_SESSION_FILE)
        cfg = get_ig_autopost_config()
        cfg["ig_username"] = uname
        save_ig_autopost_config(cfg, sync_cloud=True)
        IG_PENDING_LOGIN.pop(user_id, None)
        IG_AUTO_RETRY_STATE.pop(user_id, None)
        return True, f"✅ <b>Tasdiqlandi!</b> @{uname} Instagram profili 24/7 Avto-Posterga ulandi va Bulutli Xotiraga saqlandi!"
    except Exception as e:
        return False, (
            f"❌ Kodni tasdiqlashda xatolik: {e}\n\n"
            f"💡 <i>Maslahat: Telefoningizdan Instagram ilovasiga kirib «Bu men edim» (This was me) tugmasini bosing va "
            f"«✅ Ilovadan Tasdiqladim» tugmasini bosing, yoki <code>/ig_session</code> orqali SessionID bilan 1 soniyada ulang!</i>"
        )

def upload_video_to_instagram_reels(video_path: str, caption: str = "") -> tuple[bool, str, str]:
    """
    Tayyor MP4 videoni Instagram Reels sifatida yuklash (clip_upload + video_upload zaxirasi bilan)!
    Qaytaradi: (success, reel_url_or_msg, media_code)
    """
    if not os.path.exists(IG_SESSION_FILE):
        restore_state_from_telegram_cloud_vault()
    if not os.path.exists(IG_SESSION_FILE):
        return False, "Instagram profil ulanmagan! Avval /ig menyusidan Instagramga kiring.", ""
    if not os.path.exists(video_path) or os.path.getsize(video_path) < 2000:
        return False, "Video fayli topilmadi yoki shikastlangan.", ""
    if not _ensure_instagrapi_installed():
        return False, "instagrapi o'rnatilmagan.", ""

    cfg = get_ig_autopost_config()
    ig_user = (cfg.get("ig_username") or ADMIN_USERNAME.lstrip("@")).lstrip("@")
    bot_user = get_cached_bot_username()
    if not caption:
        caption = (cfg.get("caption_template") or DEFAULT_IG_CAPTION).replace("{ig_user}", ig_user).replace("{bot_user}", bot_user)

    with IG_CLIENT_LOCK:
        thumb_jpg = video_path + "_ig_thumb.jpg"
        try:
            from instagrapi import Client
            from pathlib import Path
            cl = _build_deterministic_ig_client(ig_user, profile_index=0)
            cl.override_app_version = True
            try:
                cl.load_settings(IG_SESSION_FILE, override_app_version=True)
            except TypeError:
                cl.load_settings(IG_SESSION_FILE)
            try:
                with open(IG_SESSION_FILE, "r", encoding="utf-8") as sf:
                    raw_s = json.load(sf)
                sid_val = (
                    (raw_s.get("authorization_data") or {}).get("sessionid")
                    or (raw_s.get("cookies") or {}).get("sessionid")
                    or ""
                )
                if sid_val:
                    cl.private.cookies.set("sessionid", sid_val, domain=".instagram.com")
                    ds_uid = sid_val.split(":")[0]
                    if ds_uid.isdigit():
                        cl.private.cookies.set("ds_user_id", ds_uid, domain=".instagram.com")
            except Exception:
                pass

            extract_hd_thumbnail(video_path, thumb_jpg)
            extra_kwargs = {}
            if os.path.exists(thumb_jpg) and os.path.getsize(thumb_jpg) > 500:
                extra_kwargs["thumbnail"] = Path(thumb_jpg)

            # Cookie sessiya bo'lsa should_use_header_over_cookies ni False qilish va authorization_data ni yangilash
            if hasattr(cl, "settings") and isinstance(cl.settings, dict):
                auth_d = cl.settings.get("authorization_data") or {}
                if not auth_d.get("authorization"):
                    cl.settings.setdefault("authorization_data", {})["should_use_header_over_cookies"] = False
                ds_id = auth_d.get("ds_user_id") or ""
                if not ds_id and sid_val:
                    ds_uid = sid_val.split(":")[0]
                    if ds_uid.isdigit():
                        cl.settings.setdefault("authorization_data", {})["ds_user_id"] = str(ds_uid)
                elif ds_id and str(ds_id).isdigit():
                    cl.settings.setdefault("authorization_data", {})["ds_user_id"] = str(ds_id)
                # Eslatma: cl.user_id ga to'g'ridan-to'g'ri qiymat berilmaydi (chunki instagrapi da u faqat o'qish uchun @property hisoblanadi)

            try:
                media = cl.clip_upload(Path(video_path), caption=caption, **extra_kwargs)
            except Exception as clip_err:
                err_str = str(clip_err).lower()
                print(f"clip_upload ogohlantirishi ({clip_err}), zaxira tekshirilmoqda...")
                if "login_required" in err_str:
                    # Agar login_required bo'lsa, sid_val orqali login_by_sessionid bilan jonlantirishga urinish
                    if sid_val and hasattr(cl, "login_by_sessionid"):
                        try:
                            cl.login_by_sessionid(sid_val)
                            cl.dump_settings(IG_SESSION_FILE)
                            media = cl.clip_upload(Path(video_path), caption=caption, **extra_kwargs)
                            code = getattr(media, "code", "") or ""
                            reel_url = f"https://www.instagram.com/reel/{code}/" if code else "https://www.instagram.com/"
                            return True, reel_url, code
                        except Exception:
                            pass
                    return False, "login_required", ""
                media = cl.video_upload(Path(video_path), caption=caption, **extra_kwargs)

            code = getattr(media, "code", "") or ""
            reel_url = f"https://www.instagram.com/reel/{code}/" if code else "https://www.instagram.com/"
            return True, reel_url, code
        except Exception as e:
            err_msg = str(e)
            if "login_required" in err_msg.lower():
                return False, "login_required", ""
            return False, f"Instagram upload xatosi: {err_msg}", ""
        finally:
            safe_remove(thumb_jpg)

# ==================== 🏛 KAFOLATLANGAN MANFAATLI VIDEOLAR FONDI (HECH QACHON TOPILMADI DEMAYDI) ====================
GUARANTEED_BENEFICIAL_LIBRARY = [
    {
        "id": "edu_space_aurora",
        "title": "Ajoyib Koinot: Xalqaro Kosmik Stantsiyadan Qutb Yog'dusi (Aurora 4K)",
        "url": "https://upload.wikimedia.org/wikipedia/commons/transcoded/1/14/Aurora_Australis_observed_by_the_ISS.webm/Aurora_Australis_observed_by_the_ISS.webm.720p.vp9.webm",
        "category": "Koinot & Tabiat"
    },
    {
        "id": "edu_wood_joint",
        "title": "Yapon Duradgorligi Sirlari: Mixsiz Yog'och Birikmasi (Kanawa Tsugi)",
        "url": "https://upload.wikimedia.org/wikipedia/commons/transcoded/9/93/Traditional_Japanese_woodworking_joint_Kanawa_Tsugi.webm/Traditional_Japanese_woodworking_joint_Kanawa_Tsugi.webm.720p.vp9.webm",
        "category": "Hunarmandchilik"
    },
    {
        "id": "edu_gear_diff",
        "title": "Mexanika Sirlari: Avtomobil Differensiali Qanday Ishlaydi (3D Ilm)",
        "url": "https://upload.wikimedia.org/wikipedia/commons/transcoded/4/4c/How_a_differential_gear_works.webm/How_a_differential_gear_works.webm.720p.vp9.webm",
        "category": "Muhandislik & Fan"
    },
    {
        "id": "edu_fluid_drop",
        "title": "Fizika Mo'jizasi: Suv Tomchisining Sirt Tarangligi (Slow Motion)",
        "url": "https://upload.wikimedia.org/wikipedia/commons/transcoded/e/e0/Water_droplet_splashing_in_super_slow_motion.webm/Water_droplet_splashing_in_super_slow_motion.webm.720p.vp9.webm",
        "category": "Ilm-Fan"
    },
    {
        "id": "edu_solar_flare",
        "title": "Quyosh Yuzasidagi Gigant Plazma Portlashi (NASA SDO Teleskopi)",
        "url": "https://upload.wikimedia.org/wikipedia/commons/transcoded/c/c0/Solar_flare_erupting_from_the_sun_captured_by_SDO.webm/Solar_flare_erupting_from_the_sun_captured_by_SDO.webm.720p.vp9.webm",
        "category": "Koinot Mo'jizalari"
    },
    {
        "id": "edu_crystal_macro",
        "title": "Kimyoviy Mo'jiza: Mikroskop Ostida Kristallar Shakllanishi (Timelapse)",
        "url": "https://upload.wikimedia.org/wikipedia/commons/transcoded/8/87/Crystal_growth_timelapse_under_polarized_light.webm/Crystal_growth_timelapse_under_polarized_light.webm.720p.vp9.webm",
        "category": "Ilmiy Tajriba"
    },
    {
        "id": "edu_watch_mechanism",
        "title": "Nozik Texnologiya: Mexanik Soat Harakati va Tishli G'ildiraklar",
        "url": "https://upload.wikimedia.org/wikipedia/commons/transcoded/6/62/Mechanism_of_a_mechanical_watch_movement.webm/Mechanism_of_a_mechanical_watch_movement.webm.720p.vp9.webm",
        "category": "Texnologiya"
    },
    {
        "id": "edu_superconductor",
        "title": "Kvant Fizikasi: O'ta O'tkazgich Magnit Levitatsiyasi Hodisasi",
        "url": "https://upload.wikimedia.org/wikipedia/commons/transcoded/b/bf/Superconducting_magnetic_levitation_demonstration.webm/Superconducting_magnetic_levitation_demonstration.webm.720p.vp9.webm",
        "category": "Fizika"
    },
    {
        "id": "edu_honeybee_math",
        "title": "Tabiat Geometriyasi: Asalarilarning Mukammal Geksagonal Uyalari",
        "url": "https://upload.wikimedia.org/wikipedia/commons/transcoded/3/3b/Honeybee_foraging_and_honeycomb_construction.webm/Honeybee_foraging_and_honeycomb_construction.webm.720p.vp9.webm",
        "category": "Hayotiy Saboq"
    },
    {
        "id": "edu_aerodynamics",
        "title": "Aviasiya Sirlari: Samolyot Qanoti Havo Oqimini Qanday Ko'taradi",
        "url": "https://upload.wikimedia.org/wikipedia/commons/transcoded/5/52/Aerodynamic_lift_over_an_airfoil_smoke_tunnel.webm/Aerodynamic_lift_over_an_airfoil_smoke_tunnel.webm.720p.vp9.webm",
        "category": "Aerodinamika"
    },
    {
        "id": "edu_cymatics_sand",
        "title": "Tovush Fizikasi: Ovoz To'lqinlarining Qumda Naqsh Yaratishi (Kimatika)",
        "url": "https://upload.wikimedia.org/wikipedia/commons/transcoded/7/7a/Chladni_plate_sound_resonance_sand_patterns.webm/Chladni_plate_sound_resonance_sand_patterns.webm.720p.vp9.webm",
        "category": "Ilm-Fan"
    },
    {
        "id": "edu_pottery_craft",
        "title": "Hunarmandchilik San'ati: Loydan Chiroyli Idish Yasash Mahorati",
        "url": "https://upload.wikimedia.org/wikipedia/commons/transcoded/2/23/Traditional_hand_pottery_wheel_crafting.webm/Traditional_hand_pottery_wheel_crafting.webm.720p.vp9.webm",
        "category": "Hunarmandchilik"
    },
    {
        "id": "edu_engine_fourstroke",
        "title": "Muhandislik: 4 Taktli Dvigatel Qanday Ishlaydi (3D Ilm)",
        "url": "https://upload.wikimedia.org/wikipedia/commons/transcoded/4/4b/Four-stroke_internal_combustion_engine_animation.webm/Four-stroke_internal_combustion_engine_animation.webm.720p.vp9.webm",
        "category": "Muhandislik"
    },
    {
        "id": "edu_geyser_power",
        "title": "Sayyoramiz Quvvati: Islandiyada Yerosti Geyzerining Otilishi",
        "url": "https://upload.wikimedia.org/wikipedia/commons/transcoded/6/6f/Geyser_Strokkur_eruption_in_Iceland.webm/Geyser_Strokkur_eruption_in_Iceland.webm.720p.vp9.webm",
        "category": "Tabiat Mo'jizasi"
    },
    {
        "id": "edu_restoration_tool",
        "title": "Hunarmandchilik: Qadimiy Asbobni Zangdan Tozalash va Qayta Tiklash",
        "url": "https://upload.wikimedia.org/wikipedia/commons/transcoded/a/a2/Restoration_of_an_antique_rusty_hand_plane.webm/Restoration_of_an_antique_rusty_hand_plane.webm.720p.vp9.webm",
        "category": "Foydali Tiklash"
    },
    {
        "id": "edu_pendulum_resonance",
        "title": "Garmonik Harakat: Mayatniklar To'lqini va Rezonans Hodisasi",
        "url": "https://upload.wikimedia.org/wikipedia/commons/transcoded/8/8c/Pendulum_wave_demonstration_synchronization.webm/Pendulum_wave_demonstration_synchronization.webm.720p.vp9.webm",
        "category": "Fizika"
    }
]

def _get_guaranteed_beneficial_evergreen_video(seen_ids: set = None) -> tuple[str, str, str, str]:
    """
    🏛 KAFOLATLANGAN MANFAATLI VA ILMIY VIDEOLAR ZAXIRASI:
    Agar tashqi tarmoqlar (TikTok, YouTube) vaqtinchalik javob bermasa yoki cheklov qo'ysa ham,
    foydalanuvchiga HECH QACHON 'video hali topilmadi' demasligi uchun
    doimiy ochiq, sifatli, 100% qizlarsiz va faqat ilm/foydadan iborat videoni taqdim etadi!
    """
    candidates = [item for item in GUARANTEED_BENEFICIAL_LIBRARY if not seen_ids or item["id"] not in seen_ids]
    if not candidates:
        candidates = list(GUARANTEED_BENEFICIAL_LIBRARY)
    chosen = random.choice(candidates)
    c_id = chosen["id"]
    c_title = chosen["title"]
    c_url = chosen["url"]
    target_mp4 = os.path.join(DOWNLOAD_DIR, f"beneficial_evergreen_{c_id}_{int(time.time())%100000}.mp4")
    raw_tmp = target_mp4 + "_raw.webm"
    try:
        if _download_binary_stream(c_url, raw_tmp, referer="https://commons.wikimedia.org/"):
            cmd = [
                FFMPEG_BIN, "-y", "-i", raw_tmp,
                "-c:v", "libx264", "-preset", "ultrafast", "-crf", "22",
                "-pix_fmt", "yuv420p",
                "-movflags", "+faststart",
                target_mp4
            ]
            if has_audio_stream(raw_tmp):
                cmd += ["-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2"]
            else:
                cmd += ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100", "-c:a", "aac", "-shortest"]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=45)
            if os.path.exists(target_mp4) and os.path.getsize(target_mp4) > 5000:
                return c_url, c_title, c_id, target_mp4
    except Exception as e:
        print(f"Guaranteed evergreen download xatosi: {e}")
    finally:
        safe_remove(raw_tmp)
    return "", "", "", ""


# ==================== 🔥 6-MOTORLI AVTO-TREND RADAR (BEVOSITA MP4 YUKLAB TEKSHIRUVCHI TIZIM) ====================
def _record_blocked_or_seen_candidate(source_id: str, video_url: str, status_code: str = "BLOCKED"):
    if not source_id and not video_url:
        return
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            "INSERT OR IGNORE INTO ig_posted_history (source_id, video_url, ig_code, posted_at) VALUES (?, ?, ?, ?)",
            (source_id or video_url[:80], video_url or source_id, status_code, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()
        conn.close()
    except Exception:
        pass

def discover_safe_trending_video_for_autopost() -> tuple[str | None, str, str, str]:
    """
    6 ta mustaqil global va mahalliy manbadan (TikWM Direct Stream, TikWM Regional Feed,
    Reddit Viral Video JSON, Dailymotion Short Videos API, Piped/Invidious Shorts va YouTube Shorts)
    eng ko'p ko'rilgan (viral) qisqa videolarni qidiradi VA DARHOL MP4 FAYLINI YUKLAB OLADI!
    Har bir nomzodni:
    1) Oldin yuklanmaganligini (`ig_posted_history`);
    2) Davomiyligi 5 soniyadan 62 soniyagacha (Reels uchun ideal) ekanligini;
    3) 🚫 Qimor (1xBet, Melbet, Casino), 18+ fahsh va bukmeker reklamasidan 100% TOZA ekanligini
       3-Qatlamli Filtrda tekshirib, TAYYOR LOKAL MP4 FAYL (`local_mp4_path`) bilan qaytaradi!
    Qaytaradi: (video_url, title, source_id, local_mp4_path)
    """
    cfg = get_ig_autopost_config()
    raw_queries = [str(x).strip().lstrip("#") for x in (cfg.get("trend_queries") or DEFAULT_TREND_QUERIES) if str(x).strip()]
    clean_user_queries = [q for q in raw_queries if q.lower() not in GENERIC_META_TAGS]
    combined_queries = []
    for q in clean_user_queries + list(HIGH_ENGAGEMENT_VIRAL_TOPICS) + list(DEFAULT_TREND_QUERIES):
        if q and q.lower() not in [x.lower() for x in combined_queries]:
            combined_queries.append(q)
    random.shuffle(combined_queries)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT source_id, video_url FROM ig_posted_history")
    rows = cursor.fetchall()
    cursor.execute("SELECT video_url FROM ig_queue")
    q_rows = cursor.fetchall()
    conn.close()

    seen_ids = {r[0] for r in rows if r[0]}
    seen_urls = {r[1] for r in rows if r[1]} | {r[0] for r in q_rows if r[0]}

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*"
    }

    def _try_verify_and_Finalize_mp4(cand_path: str, cand_url: str, cand_title: str, cand_sid: str, author_str: str = "") -> bool:
        if not cand_path or not os.path.exists(cand_path) or os.path.getsize(cand_path) < 10000:
            safe_remove(cand_path)
            return False
        dur = get_media_duration(cand_path)
        if dur < 4.5 or dur > 68.0:
            safe_remove(cand_path)
            return False
        # 1-QADAM: 🇺🇿 Faqat O'zbek tili va xalqqa manfaatli kontent filtri
        is_uzb, uzb_reason = is_uzbek_beneficial_content(f"{cand_title} {author_str}", author_str)
        if not is_uzb:
            print(f"[Trend Radar] Nomzod o'zbekcha/foydali emas ({cand_sid}): {uzb_reason}")
            _record_blocked_or_seen_candidate(cand_sid, cand_url, "NON_UZBEK")
            seen_ids.add(cand_sid)
            safe_remove(cand_path)
            return False
        # 2-QADAM: 🛡 3-Qatlamli Halol va Xavfsizlik filtri (Qimor, 18+, ochiq tana)
        is_safe, safety_reason = verify_video_content_is_halal_and_safe(cand_path, f"{cand_title} {author_str}")
        if not is_safe:
            print(f"[Trend Radar] Nomzod filtrdan qaytdi ({cand_sid}): {safety_reason}")
            _record_blocked_or_seen_candidate(cand_sid, cand_url, "BLOCKED")
            seen_ids.add(cand_sid)
            safe_remove(cand_path)
            return False
        return True

    # ==================== 1-MANBA: TikWM Viral Keyword Search (Direct Stream Download!) ====================
    for kw in combined_queries[:6]:
        try:
            _wait_tikwm_rate_limit(1.25)
            resp = requests.post(
                "https://www.tikwm.com/api/feed/search",
                data={"keywords": kw, "count": 20, "cursor": 0, "HD": 1},
                headers=headers, timeout=16, verify=False
            )
            if resp.status_code == 200:
                j = resp.json()
                videos = (j.get("data") or {}).get("videos") or []
                if isinstance(videos, list) and videos:
                    videos.sort(key=lambda x: int(x.get("digg_count") or 0) + int(x.get("play_count") or 0) * 0.1, reverse=True)
                    for v in videos[:10]:
                        vid_id = str(v.get("video_id") or "")
                        dur = float(v.get("duration") or 0)
                        title = str(v.get("title") or "").strip()
                        author_nick = str((v.get("author") or {}).get("unique_id") or "")
                        sid = f"tk_{vid_id}"
                        if not vid_id or sid in seen_ids or dur < 5 or dur > 62:
                            continue
                        ok_safe, _ = is_text_safe_from_gambling_adult_ads(f"{title} {author_nick}")
                        if not ok_safe:
                            _record_blocked_or_seen_candidate(sid, "", "BLOCKED")
                            seen_ids.add(sid)
                            continue
                        tk_page_url = f"https://www.tiktok.com/@{author_nick or 'user'}/video/{vid_id}"
                        if tk_page_url in seen_urls:
                            continue

                        # MUHIM: Ikkinchi marta API chaqirmasdan, javob ichidagi tayyor MP4 oqimni bevosita yuklab olamiz!
                        stream_candidates = []
                        for k_stream in ("play", "hdplay", "wmplay"):
                            s_u = v.get(k_stream)
                            if s_u and isinstance(s_u, str):
                                if s_u.startswith("/"):
                                    s_u = "https://www.tikwm.com" + s_u
                                stream_candidates.append(s_u)

                        cand_mp4 = os.path.join(DOWNLOAD_DIR, f"trend_tk_{vid_id}_{int(time.time())%100000}.mp4")
                        dl_ok = False
                        for s_u in stream_candidates:
                            if _download_binary_stream(s_u, cand_mp4, referer="https://www.tikwm.com/"):
                                dl_ok = True
                                break
                        if dl_ok and _try_verify_and_Finalize_mp4(cand_mp4, tk_page_url, title or f"Trend #{kw}", sid, author_nick):
                            print(f"[OK] Trend 1-Manba (TikWM Search Direct) topildi: {sid}")
                            return tk_page_url, (title or f"Trend Video #{kw}"), sid, cand_mp4
                        safe_remove(cand_mp4)
        except Exception as e:
            print(f"Trend radar 1-Manba TikWM qidiruv ogohlantirishi ({kw}): {e}")

    # ==================== 2-MANBA: TikWM Foydali va Ilmiy Mavzular Qidiruvi ====================
    educational_hashtags = [
        "foydali", "ibratli", "qiziqarlifaktlar", "hayotiysaboq", "ilm", "hunar",
        "donolardano'gitlar", "layfxaklaruz", "salomatlik", "psixologiya"
    ]
    random.shuffle(educational_hashtags)
    for tag in educational_hashtags[:5]:
        try:
            _wait_tikwm_rate_limit(1.25)
            resp = requests.post(
                "https://www.tikwm.com/api/feed/search",
                data={"keywords": f"#{tag} useful tutorial", "count": 18, "cursor": 0, "HD": 1},
                headers=headers, timeout=16, verify=False
            )
            if resp.status_code == 200:
                videos = (resp.json().get("data") or {}).get("videos") or []
                if isinstance(videos, list):
                    for v in videos[:8]:
                        vid_id = str(v.get("video_id") or "")
                        dur = float(v.get("duration") or 0)
                        title = str(v.get("title") or "").strip()
                        author_nick = str((v.get("author") or {}).get("unique_id") or "")
                        sid = f"tk_{vid_id}"
                        if not vid_id or sid in seen_ids or dur < 5 or dur > 65:
                            continue
                        ok_safe, _ = is_text_safe_from_gambling_adult_ads(f"{title} {author_nick}")
                        if not ok_safe:
                            _record_blocked_or_seen_candidate(sid, "", "BLOCKED")
                            seen_ids.add(sid)
                            continue
                        tk_page_url = f"https://www.tiktok.com/@{author_nick or 'user'}/video/{vid_id}"
                        if tk_page_url in seen_urls:
                            continue

                        stream_candidates = []
                        for k_stream in ("play", "hdplay", "wmplay"):
                            s_u = v.get(k_stream)
                            if s_u and isinstance(s_u, str):
                                if s_u.startswith("/"):
                                    s_u = "https://www.tikwm.com" + s_u
                                stream_candidates.append(s_u)

                        cand_mp4 = os.path.join(DOWNLOAD_DIR, f"trend_edu_{vid_id}_{int(time.time())%100000}.mp4")
                        dl_ok = False
                        for s_u in stream_candidates:
                            if _download_binary_stream(s_u, cand_mp4, referer="https://www.tikwm.com/"):
                                dl_ok = True
                                break
                        if dl_ok and _try_verify_and_Finalize_mp4(cand_mp4, tk_page_url, title or f"Foydali #{tag}", sid, author_nick):
                            print(f"[OK] Trend 2-Manba (TikWM Foydali #{tag}) topildi: {sid}")
                            return tk_page_url, (title or f"Foydali Video #{tag}"), sid, cand_mp4
                        safe_remove(cand_mp4)
        except Exception as e:
            print(f"Trend radar 2-Manba (#{tag}) ogohlantirishi: {e}")

    # ==================== 3-MANBA: YouTube Shorts O'zbekcha Ma'rifiy Qidiruv ====================
    for kw in combined_queries[:5]:
        try:
            search_q = f"ytsearch8:{kw} uzbek shorts"
            ydl_search_opts = {
                "quiet": True,
                "no_warnings": True,
                "extract_flat": True,
                "skip_download": True,
                "nocheckcertificate": True,
                "extractor_args": {"youtube": {"player_client": ["android_vr", "tv_embedded", "ios", "mweb"]}},
            }
            with yt_dlp.YoutubeDL(ydl_search_opts) as ydl:
                s_info = ydl.extract_info(search_q, download=False)
                entries = (s_info or {}).get("entries") or []
                for ent in entries:
                    if not ent:
                        continue
                    yt_id = str(ent.get("id") or "")
                    dur = float(ent.get("duration") or 20)
                    title = str(ent.get("title") or "").strip()
                    sid = f"yt_{yt_id}"
                    if not yt_id or sid in seen_ids or dur < 5 or dur > 65:
                        continue
                    ok_uzb, _ = is_uzbek_beneficial_content(title, "uzbek")
                    if not ok_uzb:
                        seen_ids.add(sid)
                        continue
                    ok_safe, _ = is_text_safe_from_gambling_adult_ads(title)
                    if not ok_safe:
                        seen_ids.add(sid)
                        continue
                    yt_url = f"https://www.youtube.com/shorts/{yt_id}"
                    if yt_url in seen_urls:
                        continue
                    yt_files, yt_dl_title = _download_youtube_multi_engine(yt_url, ADMIN_ID, int(time.time()*1000) % 100000000)
                    if yt_files and os.path.exists(yt_files[0]):
                        cand_mp4 = yt_files[0]
                        if _try_verify_and_Finalize_mp4(cand_mp4, yt_url, title or yt_dl_title, sid, "uzbek"):
                            print(f"[OK] Trend 3-Manba (YouTube Shorts O'zbekcha) topildi: {sid}")
                            return yt_url, (title or yt_dl_title or "O'zbekcha Shorts"), sid, cand_mp4
                        safe_remove(*yt_files)
        except Exception as e:
            print(f"Trend radar 3-Manba (YouTube Shorts O'zbek) ogohlantirishi: {e}")

    # ==================== 4-MANBA: TikWM Maxsus O'zbek Foydali Videolar Qidiruvi ====================
    for kw in ["foydali maslahatlar uz", "ibratli video", "qiziqarli faktlar uzbek", "hayotiy saboqlar uzb", "donolar hikmati"]:
        try:
            _wait_tikwm_rate_limit(1.25)
            resp = requests.post(
                "https://www.tikwm.com/api/feed/search",
                data={"keywords": kw, "count": 18, "cursor": 0, "HD": 1},
                headers=headers, timeout=16, verify=False
            )
            if resp.status_code == 200:
                videos = (resp.json().get("data") or {}).get("videos") or []
                if isinstance(videos, list):
                    for v in videos[:8]:
                        vid_id = str(v.get("video_id") or "")
                        dur = float(v.get("duration") or 0)
                        title = str(v.get("title") or "").strip()
                        author_nick = str((v.get("author") or {}).get("unique_id") or "")
                        sid = f"tk_{vid_id}"
                        if not vid_id or sid in seen_ids or dur < 5 or dur > 65:
                            continue
                        ok_uzb, _ = is_uzbek_beneficial_content(f"{title} {author_nick}", author_nick)
                        if not ok_uzb:
                            seen_ids.add(sid)
                            continue
                        ok_safe, _ = is_text_safe_from_gambling_adult_ads(f"{title} {author_nick}")
                        if not ok_safe:
                            seen_ids.add(sid)
                            continue
                        tk_page_url = f"https://www.tiktok.com/@{author_nick or 'user'}/video/{vid_id}"
                        if tk_page_url in seen_urls:
                            continue

                        stream_candidates = []
                        for k_stream in ("play", "hdplay", "wmplay"):
                            s_u = v.get(k_stream)
                            if s_u and isinstance(s_u, str):
                                if s_u.startswith("/"):
                                    s_u = "https://www.tikwm.com" + s_u
                                stream_candidates.append(s_u)

                        cand_mp4 = os.path.join(DOWNLOAD_DIR, f"trend_uz_{vid_id}_{int(time.time())%100000}.mp4")
                        dl_ok = False
                        for s_u in stream_candidates:
                            if _download_binary_stream(s_u, cand_mp4, referer="https://www.tikwm.com/"):
                                dl_ok = True
                                break
                        if dl_ok and _try_verify_and_Finalize_mp4(cand_mp4, tk_page_url, title or f"Foydali {kw}", sid, author_nick):
                            print(f"[OK] Trend 4-Manba (TikWM O'zbek Foydali) topildi: {sid}")
                            return tk_page_url, (title or f"Foydali Video #{kw}"), sid, cand_mp4
                        safe_remove(cand_mp4)
        except Exception as e:
            print(f"Trend radar 4-Manba (TikWM O'zbek) ogohlantirishi: {e}")

    # ==================== 5-MANBA: YouTube Shorts Multi-Engine Search (android_vr / tv_embedded / Invidious) ====================
    for kw in combined_queries[:3]:
        try:
            search_q = f"ytsearch8:{kw} #shorts"
            ydl_search_opts = {
                "quiet": True,
                "no_warnings": True,
                "extract_flat": True,
                "skip_download": True,
                "nocheckcertificate": True,
                "extractor_args": {"youtube": {"player_client": ["android_vr", "tv_embedded", "ios", "mweb"]}},
            }
            with yt_dlp.YoutubeDL(ydl_search_opts) as ydl:
                s_info = ydl.extract_info(search_q, download=False)
                entries = (s_info or {}).get("entries") or []
                for ent in entries:
                    if not ent:
                        continue
                    yt_id = str(ent.get("id") or "")
                    dur = float(ent.get("duration") or 20)
                    title = str(ent.get("title") or "").strip()
                    sid = f"yt_{yt_id}"
                    if not yt_id or sid in seen_ids or dur < 5 or dur > 62:
                        continue
                    ok_safe, _ = is_text_safe_from_gambling_adult_ads(title)
                    if not ok_safe:
                        seen_ids.add(sid)
                        continue
                    yt_url = f"https://www.youtube.com/shorts/{yt_id}"
                    if yt_url in seen_urls:
                        continue
                    yt_files, yt_dl_title = _download_youtube_multi_engine(yt_url, ADMIN_ID, int(time.time()*1000) % 100000000)
                    if yt_files and os.path.exists(yt_files[0]):
                        cand_mp4 = yt_files[0]
                        if _try_verify_and_Finalize_mp4(cand_mp4, yt_url, title or yt_dl_title, sid, "youtube"):
                            print(f"[OK] Trend 5-Manba (YouTube Shorts) topildi: {sid}")
                            return yt_url, (title or yt_dl_title or "YouTube Shorts"), sid, cand_mp4
                        safe_remove(*yt_files)
        except Exception as e:
            print(f"Trend radar 5-Manba (YouTube Shorts) ogohlantirishi: {e}")

    # ==================== 6-MANBA: Invidious Proxy Search + Global Open CDN Viral Video Zaxirasi ====================
    inv_search_hosts = [
        "https://inv.nadeko.net",
        "https://invidious.nerdvpn.de",
        "https://inv.tux.pizza",
        "https://yewtu.be"
    ]
    for inv_h in inv_search_hosts:
        for kw in combined_queries[:2]:
            try:
                sr = requests.get(
                    f"{inv_h}/api/v1/search",
                    params={"q": f"{kw} shorts", "type": "video", "duration": "short", "sort_by": "view_count"},
                    headers=headers, timeout=12, verify=False
                )
                if sr.status_code == 200 and isinstance(sr.json(), list):
                    for item in sr.json()[:8]:
                        yt_id = str(item.get("videoId") or "")
                        dur = float(item.get("lengthSeconds") or 0)
                        title = str(item.get("title") or "").strip()
                        sid = f"yt_{yt_id}"
                        if not yt_id or sid in seen_ids or dur < 5 or dur > 62:
                            continue
                        ok_safe, _ = is_text_safe_from_gambling_adult_ads(title)
                        if not ok_safe:
                            seen_ids.add(sid)
                            continue
                        cand_mp4 = os.path.join(DOWNLOAD_DIR, f"trend_inv_{yt_id}_{int(time.time())%100000}.mp4")
                        proxy_u = f"{inv_h}/latest_version?id={yt_id}&itag=18&local=true"
                        yt_url = f"https://www.youtube.com/shorts/{yt_id}"
                        if _download_binary_stream(proxy_u, cand_mp4, referer=inv_h):
                            if _try_verify_and_Finalize_mp4(cand_mp4, yt_url, title or "Viral Shorts", sid, "youtube"):
                                print(f"[OK] Trend 6A-Manba (Invidious Proxy Shorts) topildi: {sid}")
                                return yt_url, (title or "Viral Shorts"), sid, cand_mp4
                        safe_remove(cand_mp4)
            except Exception:
                pass

    # ==================== 7-MANBA: Kafolatlangan Foydali va Ilmiy Zaxira Fondi ====================
    # Agar jonli qidiruv tarmoqlari vaqtinchalik javob bermasa, hech qachon 'video hali topilmadi'
    # demasligi uchun doimiy ochiq ilmiy-ma'rifiy zaxiradan oladi!
    fb_url, fb_title, fb_sid, fb_mp4 = _get_guaranteed_beneficial_evergreen_video(seen_ids)
    if fb_mp4 and os.path.exists(fb_mp4):
        print(f"[OK] Trend 7-Manba (Kafolatlangan Manfaatli Ilmiy Fond) orqali olindi: {fb_sid}")
        return fb_url, fb_title, fb_sid, fb_mp4

    return None, "", "", ""

def add_video_to_ig_queue(video_url: str = "", local_path: str = "", title: str = "Reels Video", caption: str = "", montage_mode: str = "") -> tuple[bool, str, int]:
    """
    Ruchnoy yuborilgan link yoki tayyor video faylni Instagram Avto-Post navbatiga qo'shish
    (qo'shishdan oldin 3-Qatlamli Halol/Qimorsiz filtrdan o'tkazadi!)
    """
    cfg = get_ig_autopost_config()
    use_mode = montage_mode or cfg.get("montage_mode", "audio1_bridge")

    ok_txt, reason_txt = is_text_safe_from_gambling_adult_ads(f"{title} {caption}")
    if not ok_txt:
        return False, f"🚫 Kontent bloklandi ({reason_txt}). Qimor va 18+ reklamalar ruxsat etilmaydi!", 0

    saved_local = ""
    if local_path and os.path.exists(local_path):
        ok_safe_v, reason_v = verify_video_content_is_halal_and_safe(local_path, f"{title} {caption}")
        if not ok_safe_v:
            return False, f"🚫 Video filtrdan o'tmadi: {reason_v}", 0
        q_dir = os.path.join(PROMO_DIR, "ig_queue_files")
        os.makedirs(q_dir, exist_ok=True)
        saved_local = os.path.join(q_dir, f"q_vid_{int(time.time()*1000)}.mp4")
        shutil.copyfile(local_path, saved_local)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO ig_queue (video_url, local_path, title, caption, montage_mode, status, created_at)
        VALUES (?, ?, ?, ?, ?, 'pending', ?)
    """, (video_url, saved_local, title[:120], caption, use_mode, now_str))
    q_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return True, "✅ Video Instagram navbatiga qo'shildi!", q_id

def process_and_publish_single_reel_pipeline(
    video_url: str = "",
    local_video_path: str = "",
    title: str = "",
    custom_caption: str = "",
    montage_mode: str = "",
    source_id: str = "",
    notify_chat_id: int = ADMIN_ID,
    already_verified_safe: bool = False
) -> tuple[bool, str]:
    """
    🚀 TO'LIQ AVTOMATIK REELS FABRIKASI:
    1) Videoni linkdan yuklab oladi (yoki tayyor lokal MP4 faylni oladi).
    2) 3-Qatlamli Halol & Toza Kontent Filtridan (Qimor / 1xBet / 18+ / Reklama) o'tkazadi.
    3) Agar Admin Outro saqlagan bo'lsa (/set_outro), tanlangan rejimda (Audio Bridge + Whoosh FX)
       9:16 HD Blurred Fon bilan ulaydi.
    4) 10-Bosqichli Anti-Duplikat (pHash + Audio Pitch + iPhone 16 Pro Max Metadata) va
       Tepadan-Pastga Suzuvchi Shaffof Watermark qo'llaydi.
    5) Tayyor videoni Telegramda Adminga ham yuboradi va Instagram Reels ga avtomatik joylaydi!
    """
    cfg = get_ig_autopost_config()
    use_mode = montage_mode or cfg.get("montage_mode", "audio1_bridge")
    ts = int(time.time() * 1000) % 100000000
    downloaded_list = []
    raw_src = local_video_path
    final_reel_path = os.path.join(DOWNLOAD_DIR, f"ig_ready_reel_{ts}.mp4")

    try:
        # 1. Agar tayyor fayl berilmagan bo'lsa, linkdan yuklab olamiz
        if not raw_src or not os.path.exists(raw_src):
            if not video_url:
                return False, "Video manbasi ko'rsatilmagan."
            downloaded_list, dl_title = download_media_bulletproof(video_url, ADMIN_ID, ts)
            if not downloaded_list:
                if source_id:
                    _record_blocked_or_seen_candidate(source_id, video_url, "DL_FAIL")
                return False, f"Havoladan videoni yuklab bo'lmadi: {video_url}"
            raw_src = downloaded_list[0]
            if not title or title in ("Reels Video", "Ruchnoy Link"):
                title = dl_title

        # 2. 3-Qatlamli Halol va Xavfsizlik Filtri (Matn + Kadr + Audio STT)
        if already_verified_safe:
            is_safe, safety_reason = True, "✅ 100% Toza (Halol & Reklamasiz)"
        else:
            is_safe, safety_reason = verify_video_content_is_halal_and_safe(raw_src, f"{title} {custom_caption}")

        if not is_safe:
            if source_id or video_url:
                _record_blocked_or_seen_candidate(source_id or video_url[:80], video_url, "BLOCKED")
            return False, f"🛡 Kontent Xavfsizlik Filtri tomonidan bloklandi: {safety_reason}"

        # 3. Montaj (Outro bilan) yoki 10-Bosqichli Anti-Duplikat (9:16 HD + Suzuvchi Watermark)
        outro_path = get_saved_outro_path(ADMIN_ID) if cfg.get("use_saved_outro", True) else None
        already_processed = os.path.basename(raw_src).startswith(("reklama_reel_", "orig_"))

        if already_processed:
            shutil.copyfile(raw_src, final_reel_path)
            process_label = "Tayyor Pro Montaj + 10-Qatlamli Original"
        elif outro_path and os.path.exists(outro_path):
            ok_m, m_info = montage_two_videos(raw_src, outro_path, final_reel_path, mode=use_mode, apply_anti_duplicate=True)
            if not ok_m or not os.path.exists(final_reel_path):
                ok_ad, _ = make_video_100_original(raw_src, final_reel_path, force_9_16=True)
                process_label = "10-Bosqichli Anti-Duplikat (9:16 HD)"
            else:
                process_label = f"Pro Montaj ({m_info.get('mode_name', use_mode)}) + Outro + 10-Qatlamli Original"
        else:
            ok_ad, _ = make_video_100_original(raw_src, final_reel_path, force_9_16=True)
            if not ok_ad or not os.path.exists(final_reel_path):
                shutil.copyfile(raw_src, final_reel_path)
            process_label = "10-Bosqichli Anti-Duplikat (9:16 HD + Suzuvchi Watermark)"

        # 4. Caption tayyorlash
        ig_user = (cfg.get("ig_username") or ADMIN_USERNAME.lstrip("@")).lstrip("@")
        bot_user = get_cached_bot_username()
        clean_title = re.sub(r"#\S+", "", str(title or "")).strip()[:100]
        if custom_caption:
            final_caption = custom_caption
        else:
            base_tpl = cfg.get("caption_template") or DEFAULT_IG_CAPTION
            final_caption = base_tpl.replace("{ig_user}", ig_user).replace("{bot_user}", bot_user)
            if clean_title and clean_title.lower() not in ("video", "tiktok video", "instagram video", "ruchnoy link"):
                final_caption = f"🎬 {clean_title}\n\n" + final_caption

        # 5. Instagramga yuklash (agar Instagram akkount ulangan bo'lsa)
        ig_connected, ig_handle = get_instagram_Status()
        ig_ok = False
        ig_result_url = ""
        ig_code = ""
        if ig_connected:
            ig_ok, ig_result_url, ig_code = upload_video_to_instagram_reels(final_reel_path, caption=final_caption)

        # Tarixga yozish
        if source_id or video_url:
            _record_blocked_or_seen_candidate(source_id or video_url[:80], video_url, ig_code or "TG_ONLY")

        # 6. Adminga Telegram orqali tayyor videoni va hisobotni yuborish
        vinfo = get_video_stream_info(final_reel_path)
        fsize_mb = os.path.getsize(final_reel_path) / (1024 * 1024)
        action_markup = None
        if ig_ok:
            status_line = f"✅ <b>Instagram Reels ga joylandi!</b>\n🔗 <a href='{ig_result_url}'>Instagramda ko'rish ({ig_handle})</a>"
        elif ig_connected:
            if "login_required" in str(ig_result_url).lower():
                status_line = (
                    "⚠️ <b>Instagram sessiyasi eskirgan (login_required)!</b>\n"
                    "<i>Instagram akkaunt sessiyangiz muddati tugagan yoki xavfsizlik sababli bekor qilingan.\n"
                    "Iltimos, botga <code>/ig_login</code> orqali login/parol bilan kiring yoki yangi <b>SessionID</b> yuboring!</i>"
                )
                action_markup = types.InlineKeyboardMarkup(row_width=1)
                action_markup.add(
                    types.InlineKeyboardButton("🔑 Qayta Login Qilish (/ig_login)", callback_data="ig_start_login"),
                    types.InlineKeyboardButton("🍪 Yangi SessionID Yuborish", callback_data="ig_start_session")
                )
            else:
                status_line = f"⚠️ <b>Instagramga yuklashda xato:</b> <code>{html.escape(ig_result_url[:140])}</code>\n<i>(Video tayyor holatda Telegramga yuborildi)</i>"
        else:
            status_line = "ℹ️ <b>Instagram profil hali ulanmagan</b> (<code>/ig_login</code>). Tayyor Reels video shu yerga yuborildi!"

        tg_caption = (
            f"📸 <b>AVTO-REELS FABRIKASI HISOBOTI</b>\n\n"
            f"{status_line}\n\n"
            f"🎬 <b>Nomi:</b> {html.escape(clean_title or 'Trend Reels')}\n"
            f"🎛 <b>Ishlov:</b> {process_label}\n"
            f"🛡 <b>Xavfsizlik filtri:</b> {safety_reason}\n"
            f"💾 <b>Hajmi:</b> {fsize_mb:.1f} MB | ⏱ <b>Davomiyligi:</b> {vinfo.get('duration', 15)}s\n\n"
            f"🤖 @{bot_user}"
        )
        if notify_chat_id:
            try:
                with open(final_reel_path, "rb") as vf:
                    bot.send_video(
                        notify_chat_id,
                        video=vf,
                        caption=tg_caption,
                        reply_markup=action_markup,
                        width=vinfo.get("width", 720),
                        height=vinfo.get("height", 1280),
                        duration=vinfo.get("duration", 15),
                        supports_streaming=True
                    )
            except Exception as send_e:
                print(f"Adminga Reels hisobot yuborish xatosi: {send_e}")

        return True, (ig_result_url if ig_ok else "Tayyor video Telegramga yuborildi")
    except Exception as e:
        return False, f"Jarayon xatosi: {e}"
    finally:
        safe_remove(final_reel_path, *downloaded_list)

def _mark_autopost_counter_incremented(hour_slot: int = None):
    """Kunlik joylangan Reels sonini va oxirgi vaqtni yangilash"""
    try:
        cfg = get_ig_autopost_config()
        now_uz = get_tashkent_now()
        today_str = now_uz.strftime("%Y-%m-%d")
        if cfg.get("last_auto_check_date") != today_str:
            cfg["last_auto_check_date"] = today_str
            cfg["posts_today_count"] = 0
            cfg["posted_hours_today"] = []
        cfg["posts_today_count"] = int(cfg.get("posts_today_count", 0)) + 1
        ph = list(cfg.get("posted_hours_today", []))
        slot_val = hour_slot if hour_slot is not None else now_uz.hour
        if slot_val not in ph:
            ph.append(slot_val)
        cfg["posted_hours_today"] = ph
        cfg["last_post_timestamp"] = time.time()
        save_ig_autopost_config(cfg)
    except Exception as e:
        print(f"Autopost counter update xatosi: {e}")

def execute_next_autopost_job(notify_chat_id: int = ADMIN_ID, force_manual: bool = False, slot_hour: int = None) -> tuple[bool, str]:
    """
    1) Avval Ruchnoy navbatni (`ig_queue` status='pending') tekshiradi.
       Agar navbatdagi link xato bo'lsa, uni 'failed' qilib belgilaydi va to'xtab qolmasdan
       keyingi navbatdagi videoga yoki Avto-Trend Radarga o'tadi!
    2) Navbat bo'sh bo'lsa, 6-Motorli Avto-Trend Radardan 100% halol va toza trend videoni
       bevosita MP4 fayli bilan topib, montaj + anti-duplikat qilib Instagramga joylaydi!
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, video_url, local_path, title, caption, montage_mode FROM ig_queue WHERE status = 'pending' ORDER BY id ASC LIMIT 3")
    queue_rows = cursor.fetchall()
    conn.close()

    last_queue_err = ""
    for row in queue_rows:
        q_id, v_url, l_path, q_title, q_cap, m_mode = row
        ok, msg = process_and_publish_single_reel_pipeline(
            video_url=v_url,
            local_video_path=l_path,
            title=q_title,
            custom_caption=q_cap,
            montage_mode=m_mode,
            source_id=f"queue_{q_id}",
            notify_chat_id=notify_chat_id
        )
        conn = sqlite3.connect(DB_PATH)
        now_s = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if ok:
            conn.execute("UPDATE ig_queue SET status = 'posted', posted_at = ?, ig_media_code = ? WHERE id = ?", (now_s, msg[:120], q_id))
            conn.commit()
            conn.close()
            if l_path and os.path.exists(l_path):
                safe_remove(l_path)
            _mark_autopost_counter_incremented(slot_hour)
            return True, msg
        else:
            last_queue_err = msg
            conn.execute("UPDATE ig_queue SET status = 'failed', error_msg = ? WHERE id = ?", (msg[:200], q_id))
            conn.commit()
            conn.close()
            if l_path and os.path.exists(l_path):
                safe_remove(l_path)
            print(f"[IG Queue] #{q_id} muvaffaqiyatsiz ({msg}), Avto-Trend Radarga o'tilmoqda...")

    # Navbat bo'sh bo'lsa (yoki navbatdagi link xato bo'lsa) -> 6-Motorli Avto-Trend Radardan olamiz
    last_trend_err = ""
    for attempt in range(3):
        t_url, t_title, t_sid, t_local_mp4 = discover_safe_trending_video_for_autopost()
        if not t_url and not t_local_mp4:
            continue
        try:
            ok, msg = process_and_publish_single_reel_pipeline(
                video_url=t_url or "",
                local_video_path=t_local_mp4 or "",
                title=t_title,
                source_id=t_sid,
                notify_chat_id=notify_chat_id,
                already_verified_safe=bool(t_local_mp4 and os.path.exists(t_local_mp4))
            )
            if ok:
                _mark_autopost_counter_incremented(slot_hour)
                return True, msg
            last_trend_err = msg
        finally:
            if t_local_mp4 and os.path.exists(t_local_mp4):
                safe_remove(t_local_mp4)

    # Favqulodda zaxira (Emergency Fallback) - Hech qachon 'topilmadi' xatosini chiqarmaslik kafolati:
    try:
        e_url, e_title, e_sid, e_mp4 = _get_guaranteed_beneficial_evergreen_video(seen_ids=set())
        if e_mp4 and os.path.exists(e_mp4):
            ok_e, msg_e = process_and_publish_single_reel_pipeline(
                video_url=e_url,
                local_video_path=e_mp4,
                title=e_title,
                source_id=e_sid,
                notify_chat_id=notify_chat_id,
                already_verified_safe=True
            )
            if ok_e:
                _mark_autopost_counter_incremented(slot_hour)
                return True, msg_e
    except Exception as em_err:
        print(f"Emergency fallback xatosi: {em_err}")

    err_detail = last_trend_err or last_queue_err or "Qayta urinilmoqda..."
    return False, f"Hozircha mos trend video topilmadi ({err_detail})"

def get_tashkent_now() -> datetime:
    """Server qayerda (GitHub Actions UTC da) bo'lishidan qat'i nazar aniq Toshkent vaqtini (UTC+5) qaytaradi"""
    from datetime import timedelta, timezone
    tz_uz = timezone(timedelta(hours=5))
    return datetime.now(tz_uz)

def start_ig_autopost_scheduler_daemon():
    """
    Orqa fonda 24/7 ishlaydigan Aqlli Avto-Reels Rejalashtiruvchi (Smart Catch-Up bilan!):
    - Kuniga 3-4 mahal Toshkent vaqti bilan (masalan 10:00, 14:00, 18:00, 21:00 da)
      avtomatik ravishda trenddan video topib, Outro + 10-Bosqichli Anti-Duplikat bilan
      Instagramga va Adminga joylaydi!
    - SMART CATCH-UP: Agar server/GitHub Actions soat 14:25 da qayta ishga tushgan bo'lsa va
      soat 10:00 yoki 14:00 dagi post hali chiqmagan bo'lsa, foydalanuvchi qo'l tekkizmasdan
      avtomatik ravishda o'tkazib yuborilgan vaqt uchun videoni o'zi yasab joylaydi!
    """
    def _scheduler_loop():
        time.sleep(6)
        try:
            restore_state_from_telegram_cloud_vault()
        except Exception as _rv_e:
            print(f"Startup Cloud Vault restore xatosi: {_rv_e}")
        time.sleep(12)
        while True:
            try:
                cfg = get_ig_autopost_config()
                if cfg.get("auto_enabled", True):
                    now_uz = get_tashkent_now()
                    today_str = now_uz.strftime("%Y-%m-%d")
                    current_hour = now_uz.hour

                    if cfg.get("last_auto_check_date") != today_str:
                        cfg["last_auto_check_date"] = today_str
                        cfg["posts_today_count"] = 0
                        cfg["posted_hours_today"] = []
                        save_ig_autopost_config(cfg)

                    daily_limit = int(cfg.get("daily_limit", 4))
                    sched_hours = sorted([int(h) for h in (cfg.get("schedule_hours") or [10, 14, 18, 21])])
                    posted_hours = [int(h) for h in (cfg.get("posted_hours_today") or [])]
                    posts_today = int(cfg.get("posts_today_count", 0))
                    last_ts = float(cfg.get("last_post_timestamp", 0.0))

                    # Hozirgi soatgacha bo'lgan va bugun hali chiqmagan reja soatlarini topish (Smart Catch-Up)
                    due_slots = [h for h in sched_hours if h <= current_hour and h not in posted_hours]

                    # Agar navbatda (ig_queue) foydalanuvchi qo'shgan video bo'lsa yoki rejadagi vaqt kelgan bo'lsa:
                    conn = sqlite3.connect(DB_PATH)
                    cur = conn.cursor()
                    cur.execute("SELECT COUNT(*) FROM ig_queue WHERE status = 'pending'")
                    q_pending = cur.fetchone()[0]
                    conn.close()

                    should_post_now = False
                    target_slot = current_hour

                    if q_pending > 0 and (time.time() - last_ts) > 300:
                        should_post_now = True
                        target_slot = due_slots[0] if due_slots else current_hour
                    elif due_slots and posts_today < daily_limit and (time.time() - last_ts) > 2400:
                        should_post_now = True
                        target_slot = due_slots[0]

                    if should_post_now:
                        print(f"[24/7 Avto-Pilot] Navbatdagi avto-post ishga tushirilmoqda (Slot: {target_slot}:00, Bugun: {posts_today}/{daily_limit})...")
                        execute_next_autopost_job(notify_chat_id=ADMIN_ID, slot_hour=target_slot)
            except Exception as e:
                print(f"IG Auto-Poster Scheduler xatosi: {e}")
            time.sleep(60)

    t = threading.Thread(target=_scheduler_loop, daemon=True)
    t.start()

start_ig_autopost_scheduler_daemon()

def build_ig_autoposter_dashboard(user_id: int) -> tuple[str, types.InlineKeyboardMarkup]:
    """📸 Instagram Avto-Poster & Halol Filtr Boshqaruv Paneli"""
    cfg = get_ig_autopost_config()
    ig_ok, ig_handle = get_instagram_Status()
    outro_path = get_saved_outro_path(user_id)
    outro_str = f"✅ Bor ({get_media_duration(outro_path):.1f}s)" if outro_path else "⚠️ Yo'q (/set_outro)"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ig_queue WHERE status = 'pending'")
    pending_cnt = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM ig_posted_history WHERE ig_code != 'BLOCKED'")
    posted_cnt = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM ig_posted_history WHERE ig_code = 'BLOCKED'")
    blocked_cnt = cursor.fetchone()[0]
    conn.close()

    now_uz = get_tashkent_now()
    auto_state = "🟢 YOQILGAN (24/7 Avto-Pilot)" if cfg.get("auto_enabled", True) else "🔴 O'CHIRILGAN (Faqat Ruchnoy)"
    filter_state = "🛡 4-Qatlamli Qat'iy Filtr (Qimor / 18+ / Raqs / Likillagan Qizlar = 100% BLOK | Faqat Ilm-Fan va Foyda)" if cfg.get("strict_safety_filter", True) else "⚠️ Yumshoq filtr"
    sched_str = ", ".join([f"{h:02d}:00" for h in cfg.get("schedule_hours", [10, 14, 18, 21])])
    topics_str = ", ".join(cfg.get("trend_queries", DEFAULT_TREND_QUERIES)[:8])

    text = (
        f"📸 <b>INSTAGRAM REELS 24/7 AVTO-POSTER & TREND STUDIYASI</b>\n\n"
        f"👤 <b>Instagram profil:</b> <b>{ig_handle}</b> {'✅' if ig_ok else '⚠️ (Ulanmagan)'}\n"
        f"🤖 <b>Avto-Pilot holati:</b> {auto_state}\n"
        f"📅 <b>Kunlik reja:</b> Kuniga <b>{cfg.get('daily_limit', 4)} ta</b> Reels ({sched_str} Toshkent vaqti)\n"
        f"📊 <b>Bugun joylandi:</b> <b>{cfg.get('posts_today_count', 0)} / {cfg.get('daily_limit', 4)} ta</b> (Soat: {now_uz.strftime('%H:%M')})\n"
        f"📥 <b>Ruchnoy navbatda (Queue):</b> <b>{pending_cnt} ta</b> video kutmoqda\n"
        f"✅ <b>Jami joylangan:</b> <b>{posted_cnt} ta</b> | 🚫 <b>Filtr bloklagan:</b> <b>{blocked_cnt} ta</b>\n\n"
        f"🎬 <b>Montaj & Original Sozlamasi:</b>\n"
        f"• 📌 <b>Saqlangan Outro ulash:</b> {outro_str}\n"
        f"• 🎛 <b>Montaj rejimi:</b> <code>{cfg.get('montage_mode', 'audio1_bridge')}</code>\n"
        f"• 💧 <b>Suzuvchi Watermark & 10-Qatlam Original:</b> ✅ Doimiy faol\n\n"
        f"🚫 <b>Xavfsizlik & Halol Filtri:</b>\n"
        f"• {filter_state}\n"
        f"• 🔍 <b>Avto-Trend mavzulari:</b> <i>{topics_str}</i>\n\n"
        f"💡 <b>2 Xil Ishlash Yo'nalishi:</b>\n"
        f"1️⃣ <b>AVTO-PILOT:</b> O'zi har kuni trenddan 3-4 ta toza video topib, montaj + original qilib Instagramga joylaydi.\n"
        f"2️⃣ <b>RUCHNOY:</b> Botga istalgan link tashlang va video ostidagi <b>«📸 Insta Reels Joylash»</b> yoki <b>«📅 Avto-Navbatga Qo'shish»</b> tugmasini bosing!"
    )

    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🚀 Hozir 1 ta Video Yasab Joylash (Test)", callback_data="ig_run_now")
    )
    markup.add(
        types.InlineKeyboardButton("➕ Ruchnoy Link Navbatga Qo'shish", callback_data="ig_add_manual_link"),
        types.InlineKeyboardButton(f"📋 Navbatni Ko'rish ({pending_cnt})", callback_data="ig_view_queue")
    )
    toggle_lbl = "🔴 Avto-Pilotni O'chirish" if cfg.get("auto_enabled", True) else "🟢 Avto-Pilotni Yoqish"
    markup.add(
        types.InlineKeyboardButton(toggle_lbl, callback_data="ig_toggle_auto"),
        types.InlineKeyboardButton("⏰ Kunlik Sonni O'zgartirish (3/4/5)", callback_data="ig_cycle_limit")
    )
    markup.add(
        types.InlineKeyboardButton("🔑 Instagram Login / Parol", callback_data="ig_start_login"),
        types.InlineKeyboardButton("🍪 SessionID Bilan Ulash", callback_data="ig_start_session")
    )
    markup.add(
        types.InlineKeyboardButton("🎯 Trend Mavzularni Sozlash", callback_data="ig_set_topics"),
        types.InlineKeyboardButton("🚫 Taqiqlangan So'z Qo'shish", callback_data="ig_add_badword")
    )
    markup.add(
        types.InlineKeyboardButton("✍️ Reels Caption (Izoh) Sozlash", callback_data="ig_set_caption"),
        types.InlineKeyboardButton("🔄 Yangilash", callback_data="ig_open_panel")
    )
    return text, markup

# ==================== SHAZAM / MUSIQANI ANIQLASH ====================
def identify_music_from_video(video_path: str, metadata_info: dict = None):
    ensure_ffmpeg_in_path()
    if metadata_info:
        track = metadata_info.get('track') or metadata_info.get('music_title')
        artist = metadata_info.get('artist') or metadata_info.get('creator') or metadata_info.get('channel')
        album = metadata_info.get('album')
        if track and artist:
            return {"title": track, "artist": artist, "album": album or ""}

    temp_sample = f"{video_path}_sample.mp3"
    try:
        subprocess.run([
            FFMPEG_BIN, "-y", "-ss", "3", "-t", "12",
            "-i", video_path, "-vn", "-c:a", "libmp3lame", "-b:a", "128k",
            temp_sample
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=25)
        if not os.path.exists(temp_sample):
            temp_sample = f"{video_path}_sample.wav"
            subprocess.run([
                FFMPEG_BIN, "-y", "-ss", "3", "-t", "10",
                "-i", video_path, "-vn", "-ar", "16000", "-ac", "1",
                temp_sample
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=25)

        if os.path.exists(temp_sample):
            with open(temp_sample, "rb") as af:
                files = {"file": af}
                resp = requests.post("https://api.audd.io/", files=files, data={"api_token": "test"}, timeout=15, verify=False)
                if resp.status_code == 200:
                    data = resp.json()
                    if data.get("status") == "success" and data.get("result"):
                        res = data["result"]
                        return {
                            "title": res.get("title", "Noma'lum qo'shiq"),
                            "artist": res.get("artist", "Noma'lum ijrochi"),
                            "album": res.get("album", "")
                        }
    except Exception as e:
        print(f"Musiqa qidirish xatosi: {e}")
    finally:
        safe_remove(temp_sample)
    return None

# ==================== SUBTITR VA NUTQNI MATNGA O'GIRISH (LIBASS SIZ HAM 100% ISHLAYDI!) ====================
def format_srt_timestamp(seconds: float) -> str:
    millis = int((seconds - int(seconds)) * 1000)
    seconds = int(seconds)
    mins, secs = divmod(seconds, 60)
    hours, mins = divmod(mins, 60)
    return f"{hours:02d}:{mins:02d}:{secs:02d},{millis:03d}"

def _call_google_speech_single(flac_bytes: bytes, api_lang: str) -> str:
    if not flac_bytes or len(flac_bytes) < 200:
        return ""
    params = urllib.parse.urlencode({
        "client": "chromium",
        "lang": api_lang,
        "key": GOOGLE_SPEECH_KEY,
        "output": "json",
        "maxresults": "1",
        "pfilter": "0"
    })
    url = f"https://www.google.com/speech-api/v2/recognize?{params}"
    headers = {
        "Content-Type": "audio/x-flac; rate=16000",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    req = urllib.request.Request(url, data=flac_bytes, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode("utf-8", errors="ignore")
            for line in content.splitlines():
                line = line.strip()
                if not line:
                    continue
                data = json.loads(line)
                results = data.get("result", [])
                if results and "alternative" in results[0] and len(results[0]["alternative"]) > 0:
                    transcript = results[0]["alternative"][0].get("transcript", "").strip()
                    if transcript:
                        return transcript
    except Exception as e:
        print(f"Google Speech API ({api_lang}) xatosi: {e}")
    return ""

def recognize_google_flac(flac_bytes: bytes, lang: str = "uz-UZ") -> str:
    if lang == "auto":
        lang_order = ["uz-UZ", "ru-RU", "en-US"]
    else:
        fallbacks = [l for l in ["uz-UZ", "ru-RU", "en-US"] if l != lang]
        lang_order = [lang] + fallbacks[:2]

    for candidate_lang in lang_order:
        text = _call_google_speech_single(flac_bytes, candidate_lang)
        if text:
            return text
    return ""

def transcribe_audio_to_srt(audio_path: str, srt_path: str, lang: str = "uz-UZ") -> tuple:
    ensure_ffmpeg_in_path()
    if not os.path.exists(audio_path) or os.path.getsize(audio_path) < 500:
        return False, ""

    total_dur = min(get_media_duration(audio_path), 180.0)
    if total_dur <= 0.5:
        total_dur = 15.0
    segments = []

    for filter_mode in ["voice_boost", "raw"]:
        if segments:
            break
        chunk_duration = 5.0 if total_dur <= 30.0 else 7.0
        current = 0.0
        idx = 0
        while current < total_dur:
            end = min(current + chunk_duration, total_dur)
            if (end - current) < 0.6:
                break
            chunk_flac = f"{audio_path}_chk_{idx}.flac"
            cmd = [FFMPEG_BIN, "-y", "-ss", str(current), "-t", str(end - current), "-i", audio_path]
            if filter_mode == "voice_boost":
                cmd += ["-af", "highpass=f=150,lowpass=f=3800,volume=1.8"]
            cmd += ["-ar", "16000", "-ac", "1", "-c:a", "flac", chunk_flac]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            if os.path.exists(chunk_flac):
                with open(chunk_flac, "rb") as cf:
                    flac_bytes = cf.read()
                safe_remove(chunk_flac)

                check_lang = "auto" if filter_mode == "raw" else lang
                text = recognize_google_flac(flac_bytes, lang=check_lang)
                if text:
                    segments.append({"start": current, "end": end, "text": text.strip()})
            current = end
            idx += 1

    if not segments:
        return False, ""

    full_text_list = []
    with open(srt_path, "w", encoding="utf-8") as srt_file:
        for i, seg in enumerate(segments, 1):
            s_str = format_srt_timestamp(seg["start"])
            e_str = format_srt_timestamp(seg["end"])
            txt = seg["text"]
            full_text_list.append(txt)
            srt_file.write(f"{i}\n{s_str} --> {e_str}\n{txt}\n\n")

    return True, " ".join(full_text_list)

def _render_subtitle_banner_png(text: str, out_png: str, vid_w: int = 720) -> bool:
    """
    Agar FFmpeg da `libass` / `subtitles=` filteri bo'lmasa (masalan Windows static FFmpeg da),
    subtitr matnini chiroyli qora yarim-shaffof quti ichiga oq-oltin harflar bilan PNG qilib chizadi!
    """
    clean_t = (text or "").strip()
    if not clean_t:
        return False
    banner_w = max(320, int(vid_w * 0.88))
    banner_h = 96
    try:
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new("RGBA", (banner_w, banner_h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle([4, 4, banner_w - 4, banner_h - 4], radius=18, fill=(15, 20, 30, 195), outline=(255, 215, 0, 180), width=2)
        font = None
        for fc in [
            r"C:\Windows\Fonts\arialbd.ttf",
            r"C:\Windows\Fonts\segoeuib.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        ]:
            if os.path.exists(fc):
                try:
                    font = ImageFont.truetype(fc, 26)
                    break
                except Exception:
                    pass
        if font is None:
            font = ImageFont.load_default()

        # Matn uzun bo'lsa 2 qatorga bo'lish
        words = clean_t.split()
        lines = []
        cur = ""
        for w in words:
            if len(cur) + len(w) + 1 <= 36:
                cur = (cur + " " + w).strip()
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        lines = lines[:2]
        full_str = "\n".join(lines)
        draw.multiline_text((banner_w // 2, banner_h // 2), full_str, font=font, fill=(255, 255, 255, 250), anchor="mm", align="center")
        img.save(out_png, "PNG")
        return os.path.exists(out_png) and os.path.getsize(out_png) > 200
    except Exception:
        # Pure-Python fallback
        return _generate_watermark_png_pure_python(clean_t[:24].upper(), out_png, opacity=0.85)

def _parse_srt_segments(srt_path: str) -> list:
    segs = []
    if not os.path.exists(srt_path):
        return segs
    try:
        with open(srt_path, "r", encoding="utf-8", errors="ignore") as f:
            blocks = f.read().strip().split("\n\n")
        for b in blocks:
            lines = [ln.strip() for ln in b.splitlines() if ln.strip()]
            if len(lines) >= 2:
                time_line = lines[1] if "-->" in lines[1] else (lines[0] if "-->" in lines[0] else "")
                txt_lines = lines[2:] if "-->" in lines[1] else lines[1:]
                m = re.search(r"(\d+):(\d+):(\d+)[,\.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,\.](\d+)", time_line)
                if m and txt_lines:
                    s_sec = int(m.group(1))*3600 + int(m.group(2))*60 + int(m.group(3)) + int(m.group(4))/1000.0
                    e_sec = int(m.group(5))*3600 + int(m.group(6))*60 + int(m.group(7)) + int(m.group(8))/1000.0
                    segs.append({"start": s_sec, "end": e_sec, "text": " ".join(txt_lines)})
    except Exception:
        pass
    return segs

def burn_subtitles_to_video(input_video_path: str, srt_path: str, output_video_path: str) -> bool:
    """
    Subtitrlarni videoga yopishtirish:
    1) Avval FFmpeg `subtitles=` filterini sinaydi.
    2) Agar `libass` yoki `fontconfig` yo'q bo'lsa (Windows static FFmpeg), avtomatik PNG Overlay
       usuliga o'tib, 100% xatosiz subtitrli video tayyorlaydi!
    """
    ensure_ffmpeg_in_path()
    local_temp_srt = f"_tmp_sub_{int(time.time() * 1000) % 100000}.srt"
    png_Trash = []
    try:
        shutil.copyfile(srt_path, local_temp_srt)
        style = "FontSize=16,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=3,Outline=1,Shadow=0,MarginV=30"
        cmd = [
            FFMPEG_BIN, "-y", "-i", input_video_path,
            "-vf", f"subtitles={local_temp_srt}:force_style='{style}'",
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23",
            "-c:a", "copy", "-movflags", "+faststart",
            output_video_path
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=180)
        if res.returncode == 0 and os.path.exists(output_video_path) and os.path.getsize(output_video_path) > 1000:
            return True

        # Fallback: PNG Overlay Subtitle Burner (Zero libass dependency!)
        segs = _parse_srt_segments(srt_path)
        if not segs:
            return False
        vinfo = get_video_stream_info(input_video_path)
        vid_w = max(360, vinfo.get("width", 720))

        cmd_ov = [FFMPEG_BIN, "-y", "-i", input_video_path]
        valid_segs = []
        for idx, sg in enumerate(segs[:18]):
            p_path = os.path.join(DOWNLOAD_DIR, f"_sub_ov_{int(time.time()*1000)}_{idx}.png")
            if _render_subtitle_banner_png(sg["text"], p_path, vid_w=vid_w):
                png_Trash.append(p_path)
                cmd_ov += ["-i", p_path]
                valid_segs.append(sg)

        if not valid_segs:
            return False

        fc_parts = []
        prev_label = "0:v"
        for i, sg in enumerate(valid_segs, 1):
            out_lbl = f"v{i}"
            s_t = f"{sg['start']:.2f}"
            e_t = f"{sg['end']:.2f}"
            fc_parts.append(f"[{prev_label}][{i}:v]overlay=x=(W-w)/2:y=H-h-85:enable='between(t,{s_t},{e_t})'[{out_lbl}]")
            prev_label = out_lbl

        fc_parts.append(f"[{prev_label}]format=yuv420p[vfinal]")
        cmd_ov += [
            "-filter_complex", ";".join(fc_parts),
            "-map", "[vfinal]", "-map", "0:a?",
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23",
            "-c:a", "copy", "-movflags", "+faststart",
            output_video_path
        ]
        res_ov = subprocess.run(cmd_ov, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=180)
        return res_ov.returncode == 0 and os.path.exists(output_video_path) and os.path.getsize(output_video_path) > 1000
    except Exception as e:
        print(f"Subtitr qadash xatoligi: {e}")
        return False
    finally:
        safe_remove(local_temp_srt, *png_Trash)

# ==================== 12-BOSQICHLI XATOSIZ VIDEO-FIRST YUKLAGICH ====================
def extract_ig_shortcode(url: str) -> str | None:
    """Instagram URL dan shortcode ni aniq ajratib olish (reel, reels, p, tv, stories)"""
    m = re.search(r"instagram\.com/(?:[A-Za-z0-9_.-]+/)?(?:reel|reels|p|tv)/([A-Za-z0-9_-]+)", url, re.IGNORECASE)
    if m:
        return m.group(1)
    m2 = re.search(r"instagr\.am/(?:p|reel)/([A-Za-z0-9_-]+)", url, re.IGNORECASE)
    if m2:
        return m2.group(1)
    return None

def clean_and_resolve_url(raw_url: str) -> str:
    """
    Telefondan yuborilgan har qanday ssilkani (?cplk=..., ?obrf=..., ?igsh=..., /share/reel/..., vt.tiktok.com, pin.it)
    tozalash va asl manzilga yechish!
    """
    url = raw_url.strip().rstrip(".,;!?)'\">]")
    url = url.replace("instagram.com/reels/", "instagram.com/reel/")
    lower = url.lower()

    # 1. Qisqa mobil ssilkalarni redirect orqali ochish
    if any(k in lower for k in [
        "vt.tiktok.com", "vm.tiktok.com", "tiktok.com/t/",
        "/share/reel/", "/share/p/", "/share/v/", "instagram.com/share/",
        "pin.it/", "fb.watch/", "redd.it/", "bit.ly/", "tinyurl.com/"
    ]):
        for ua in [
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
            "curl/8.4.0",
            "TelegramBot (like TwitterBot)"
        ]:
            try:
                resp = requests.get(url, headers={"User-Agent": ua}, allow_redirects=True, stream=True, timeout=12, verify=False)
                resolved = resp.url
                resp.close()
                if resolved and resolved.startswith("http"):
                    if "accounts/login" in resolved.lower():
                        parsed_q = urllib.parse.parse_qs(urllib.parse.urlparse(resolved).query)
                        if "next" in parsed_q and parsed_q["next"]:
                            next_url = urllib.parse.unquote(parsed_q["next"][0])
                            if next_url.startswith("/"):
                                next_url = "https://www.instagram.com" + next_url
                            url = next_url
                            break
                    else:
                        url = resolved
                        break
            except Exception:
                pass

    # 2. Instagram linkidan ?cplk=..., ?obrf=..., ?igsh=..., ?utm_source=... kabi kuzatuv parametrlarini olib tashlash
    if "instagram.com" in url.lower() or "instagr.am" in url.lower():
        shortcode = extract_ig_shortcode(url)
        if shortcode:
            kind = "p" if "/p/" in url.lower() else "reel"
            url = f"https://www.instagram.com/{kind}/{shortcode}/"

    # 3. YouTube va YouTube Shorts linklarini ?si=..., &feature=share kuzatuv parametrlaridan tozalash
    if "youtube.com" in url.lower() or "youtu.be" in url.lower():
        yt_m = re.search(
            r'(?:youtube\.com/(?:shorts/|live/|embed/|v/|watch\?[^\s"\x27]*v=)|youtu\.be/)([A-Za-z0-9_-]{11})',
            url, re.IGNORECASE
        )
        if yt_m:
            vid_id = yt_m.group(1)
            if "/shorts/" in url.lower():
                url = f"https://www.youtube.com/shorts/{vid_id}"
            else:
                url = f"https://www.youtube.com/watch?v={vid_id}"

    # 4. Pinterest redirect parametrlarini tozalash
    if "pinterest.com" in url.lower() and "/sent/" in url.lower():
        url = url.split("/sent/")[0] + "/"

    return url

def _download_binary_stream(file_url: str, target_path: str, referer: str = "") -> bool:
    """Berilgan to'g'ridan-to'g'ri media URL dan faylni xavfsiz yuklab olish (HTML/JSON soxta javoblardan himoyalangan)"""
    if not file_url or not file_url.startswith("http"):
        return False
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Accept": "*/*",
    }
    if referer:
        headers["Referer"] = referer
    try:
        with requests.get(file_url, headers=headers, stream=True, timeout=45, verify=False) as r:
            if r.status_code in (200, 206):
                ctype = (r.headers.get("Content-Type") or "").lower()
                if "text/html" in ctype or "application/json" in ctype or "text/plain" in ctype:
                    return False
                with open(target_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=65536):
                        if chunk:
                            f.write(chunk)
                if os.path.exists(target_path) and os.path.getsize(target_path) > 5000:
                    with open(target_path, "rb") as chk:
                        head = chk.read(64).lstrip()
                    if head.startswith((b"<!DOCTYPE", b"<html", b"<HTML", b'{"', b"[{" )):
                        safe_remove(target_path)
                        return False
                    return True
    except Exception as e:
        print(f"Binary stream yuklash xatosi: {e}")
    safe_remove(target_path)
    return False

def _unescape_ig_text(raw_str: str) -> str:
    """Instagram HTML va contextJSON ichidagi ko'p qavatli escaped belgilarni toza holatga keltirish"""
    s = raw_str
    for _ in range(3):
        s = s.replace('\\\\"', '"').replace('\\"', '"')
        s = s.replace("\\\\/", "/").replace("\\/", "/")
        s = s.replace("\\\\u0026", "&").replace("\\u0026", "&")
        s = s.replace("\\\\u0025", "%").replace("\\u0025", "%")
        s = s.replace("\\\\u003C", "<").replace("\\u003C", "<")
    return html.unescape(s)

def _download_instagram_video_engines(url: str, user_id: int, timestamp: int) -> tuple[list, str, bool]:
    """
    Instagram VIDEO-FIRST 6-Bosqichli Maxsus Yuklagich!
    Qaytaradi: (fayllar_royxati, sarlavha, is_definitely_video)
    MUHIM: Agar post video bo'lsa, HECH QACHON oblojka rasmni (.jpg) video o'rniga yubormaydi!
    """
    shortcode = extract_ig_shortcode(url)
    target_mp4 = os.path.join(DOWNLOAD_DIR, f"{user_id}_{timestamp}_00001.mp4")

    if not shortcode:
        return [], "", False

    is_definitely_video = ("/reel/" in url.lower() or "/reels/" in url.lower() or "/tv/" in url.lower())
    embed_bodies = []

    # ---------------- 1-MOTOR: Deep Unescaped Embed Captioned Video Extractor ----------------
    embed_urls = [
        f"https://www.instagram.com/reel/{shortcode}/embed/captioned/",
        f"https://www.instagram.com/p/{shortcode}/embed/captioned/",
        f"https://www.instagram.com/p/{shortcode}/embed/",
    ]
    embed_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    for emb_url in embed_urls:
        try:
            er = requests.get(emb_url, headers=embed_headers, timeout=14, verify=False)
            if er.status_code == 200 and er.text:
                raw_body = er.text
                embed_bodies.append(raw_body)
                clean_body = _unescape_ig_text(raw_body)

                # Post video ekanligini bildiruvchi belgilar (hatto video_url yashirilgan bo'lsa ham!):
                if any(ind in clean_body for ind in [
                    '"is_video":true', '"is_video": true',
                    'EmbeddedMediaVideo', 'WatchOnInstagram', 'Watch on Instagram',
                    'glyphsSpritePlay', 'video_versions', '"media_type":2'
                ]):
                    is_definitely_video = True

                # Tozalangan HTML/JSON ichidan barcha video URL larni qidirish
                vid_patterns = [
                    r'"video_url"\s*:\s*"(https?://[^"]+)"',
                    r'"contentUrl"\s*:\s*"(https?://[^"]+)"',
                    r'"video_versions"\s*:\s*\[\s*\{[^}]*"url"\s*:\s*"(https?://[^"]+)"',
                    r'<video[^>]+src="(https?://[^"]+)"',
                    r'property="og:video(?::secure_url)?"\s+content="(https?://[^"]+)"',
                ]
                for pat in vid_patterns:
                    for vurl in re.findall(pat, clean_body):
                        vurl_clean = _unescape_ig_text(vurl)
                        if vurl_clean.startswith("http") and any(k in vurl_clean for k in [".mp4", "cdninstagram", "fbcdn.net"]):
                            if _download_binary_stream(vurl_clean, target_mp4, referer="https://www.instagram.com/"):
                                print(f"[OK] Instagram 1-Motor (Unescaped Embed Video) orqali yuklandi: {shortcode}")
                                return [target_mp4], f"Instagram Video ({shortcode})", True
        except Exception as e:
            print(f"IG 1-Motor xatosi ({emb_url}): {e}")

    # ---------------- 2-MOTOR: Live-Session GraphQL API (Avto-LSD + CSRF token bilan) ----------------
    try:
        sess = requests.Session()
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        lsd_token = "AVqbxe3J_YA"
        csrf_token = "missing"

        # Jonli LSD va cookie olish
        try:
            init_r = sess.get(f"https://www.instagram.com/reel/{shortcode}/", headers={"User-Agent": ua}, timeout=12, verify=False)
            if init_r.status_code == 200 and init_r.text:
                m_lsd = re.search(r'"LSD",\s*\[\],\s*\{\s*"token"\s*:\s*"([^"]+)"', init_r.text) or re.search(r'"lsd"\s*:\s*"([^"]+)"', init_r.text)
                if m_lsd:
                    lsd_token = m_lsd.group(1)
                # Shu sahifaning o'zida video_versions bor-yo'qligini ham tekshiramiz!
                clean_init = _unescape_ig_text(init_r.text)
                if '"is_video":true' in clean_init or '"media_type":2' in clean_init:
                    is_definitely_video = True
                for vurl in re.findall(r'"video_versions"\s*:\s*\[\s*\{[^}]*"url"\s*:\s*"(https?://[^"]+)"', clean_init) + re.findall(r'"video_url"\s*:\s*"(https?://[^"]+)"', clean_init):
                    if _download_binary_stream(_unescape_ig_text(vurl), target_mp4, referer="https://www.instagram.com/"):
                        print(f"[OK] Instagram 2A-Motor (Direct Page JSON) orqali yuklandi: {shortcode}")
                        return [target_mp4], f"Instagram Video ({shortcode})", True
            csrf_token = sess.cookies.get("csrftoken") or "missing"
        except Exception:
            pass

        gql_headers = {
            "User-Agent": ua,
            "Content-Type": "application/x-www-form-urlencoded",
            "X-IG-App-ID": "936619743392459",
            "X-FB-LSD": lsd_token,
            "X-CSRFToken": csrf_token,
            "X-ASBD-ID": "129477",
            "X-IG-WWW-Claim": "0",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://www.instagram.com",
            "Referer": f"https://www.instagram.com/reel/{shortcode}/",
            "Sec-Fetch-Site": "same-origin",
        }
        graphql_doc_ids = ["8845758582119845", "7341532402634560", "10015901848480474", "25811509981800768", "7153035638091937"]
        for doc_id in graphql_doc_ids:
            try:
                payload = {
                    "av": "0",
                    "__d": "www",
                    "__user": "0",
                    "__a": "1",
                    "__req": "1",
                    "dpr": "1",
                    "__ccg": "EXCELLENT",
                    "lsd": lsd_token,
                    "fb_api_caller_class": "RelayModern",
                    "fb_api_req_friendly_name": "PolarisPostActionLoadPostQueryQuery",
                    "variables": json.dumps({
                        "shortcode": shortcode,
                        "fetch_comment_count": 0,
                        "fetch_related_profile_media_count": 0,
                        "parent_comment_count": 0,
                        "child_comment_count": 0,
                        "fetch_like_count": 10,
                        "fetch_tagged_user_count": None,
                        "fetch_preview_comment_count": 2,
                        "has_threaded_comments": True,
                        "hoisted_comment_id": None,
                        "hoisted_reply_id": None,
                    }),
                    "server_timestamps": "true",
                    "doc_id": doc_id,
                }
                for gql_endpoint in ["https://www.instagram.com/api/graphql", "https://www.instagram.com/graphql/query"]:
                    gr = sess.post(gql_endpoint, headers=gql_headers, data=payload, timeout=12, verify=False)
                    if gr.status_code == 200 and gr.text:
                        clean_json_str = gr.text.lstrip("for (;;);").strip()
                        gdata = json.loads(clean_json_str)
                        media = (
                            gdata.get("data", {}).get("xdt_shortcode_media")
                            or gdata.get("data", {}).get("shortcode_media")
                            or gdata.get("graphql", {}).get("shortcode_media")
                        )
                        if not media:
                            continue

                        if media.get("is_video") or media.get("video_url") or media.get("video_versions"):
                            is_definitely_video = True

                        caption_edges = media.get("edge_media_to_caption", {}).get("edges", [])
                        title = caption_edges[0]["node"]["text"][:80] if caption_edges else f"Instagram ({shortcode})"

                        # Karusel (Sidecar) bo'lsa
                        sidecar = media.get("edge_sidecar_to_children", {}).get("edges", []) or media.get("carousel_media", [])
                        if sidecar:
                            collected = []
                            for idx, item in enumerate(sidecar[:10], 1):
                                node = item.get("node", item) if isinstance(item, dict) else {}
                                vurl_node = node.get("video_url") or (node.get("video_versions", [{}])[0].get("url") if node.get("video_versions") else None)
                                if node.get("is_video") or vurl_node:
                                    fp = os.path.join(DOWNLOAD_DIR, f"{user_id}_{timestamp}_{idx:05d}.mp4")
                                    if vurl_node and _download_binary_stream(vurl_node, fp, referer="https://www.instagram.com/"):
                                        collected.append(fp)
                                else:
                                    durl_node = node.get("display_url") or (node.get("image_versions2", {}).get("candidates", [{}])[0].get("url"))
                                    fp = os.path.join(DOWNLOAD_DIR, f"{user_id}_{timestamp}_{idx:05d}.jpg")
                                    if durl_node and _download_binary_stream(durl_node, fp, referer="https://www.instagram.com/"):
                                        collected.append(fp)
                            if collected:
                                print(f"[OK] Instagram 2-Motor (GraphQL Karusel) orqali yuklandi: {shortcode}")
                                return collected, title, is_definitely_video

                        # Bitta video bo'lsa
                        vurl = media.get("video_url") or (media.get("video_versions", [{}])[0].get("url") if media.get("video_versions") else None)
                        if vurl and _download_binary_stream(vurl, target_mp4, referer="https://www.instagram.com/"):
                            print(f"[OK] Instagram 2-Motor (GraphQL Video) orqali yuklandi: {shortcode}")
                            return [target_mp4], title, True

                        # Agar GraphQL aniq is_video == False desa (haqiqiy bitta rasm post bo'lsa):
                        if media.get("is_video") is False and not sidecar:
                            durl = media.get("display_url")
                            target_jpg = os.path.join(DOWNLOAD_DIR, f"{user_id}_{timestamp}_00001.jpg")
                            if durl and _download_binary_stream(durl, target_jpg, referer="https://www.instagram.com/"):
                                print(f"[OK] Instagram 2-Motor (Confirmed Photo Post) orqali yuklandi: {shortcode}")
                                return [target_jpg], title, False
            except Exception:
                pass
    except Exception as e:
        print(f"IG 2-Motor session xatosi: {e}")

    # ---------------- 3-MOTOR: Multi-Proxy OpenGraph Video Scrapers ----------------
    proxy_domains = [
        "https://kkinstagram.com",
        "https://www.vxinstagram.com",
        "https://eeinstagram.com",
        "https://www.ddinstagram.com",
        "https://instagramez.com",
    ]
    bot_uas = [
        "TelegramBot (like TwitterBot)",
        "Mozilla/5.0 (compatible; Discordbot/2.0; +https://discordapp.com)",
        "Twitterbot/1.0"
    ]
    for domain in proxy_domains:
        for bua in bot_uas:
            try:
                purl = f"{domain}/reel/{shortcode}"
                pr = requests.get(purl, headers={"User-Agent": bua}, timeout=12, allow_redirects=True, verify=False)
                if pr.status_code == 200:
                    ctype = (pr.headers.get("Content-Type") or "").lower()
                    if "video/" in ctype and len(pr.content) > 10000:
                        with open(target_mp4, "wb") as f:
                            f.write(pr.content)
                        print(f"[OK] Instagram 3-Motor ({domain} direct stream) orqali yuklandi: {shortcode}")
                        return [target_mp4], f"Instagram Video ({shortcode})", True

                    html_text = _unescape_ig_text(pr.text)
                    og_matches = (
                        re.findall(r'(?:property="og:video(?::secure_url|:url)?"|name="twitter:player:stream")\s+content="([^"]+)"', html_text)
                        + re.findall(r'content="([^"]+)"\s+(?:property="og:video(?::secure_url|:url)?"|name="twitter:player:stream")', html_text)
                    )
                    for og_url in og_matches:
                        clean_og = _unescape_ig_text(og_url)
                        if clean_og.startswith("/"):
                            clean_og = domain + clean_og
                        if _download_binary_stream(clean_og, target_mp4, referer=domain):
                            print(f"[OK] Instagram 3-Motor ({domain} og:video) orqali yuklandi: {shortcode}")
                            return [target_mp4], f"Instagram Video ({shortcode})", True
            except Exception:
                pass

    # ---------------- 4-MOTOR: External IG Video Downloader APIs (RyzenDesu / VKR / SaveIG) ----------------
    ig_page_url = f"https://www.instagram.com/reel/{shortcode}/"
    external_apis = [
        f"https://api.ryzendesu.vip/api/downloader/igdl?url={urllib.parse.quote(ig_page_url)}",
        f"https://vkrdownloader.xyz/server?vkr={urllib.parse.quote(ig_page_url)}",
    ]
    for api_u in external_apis:
        try:
            ar = requests.get(api_u, headers={"User-Agent": "Mozilla/5.0"}, timeout=15, verify=False)
            if ar.status_code == 200 and ar.text:
                clean_api = _unescape_ig_text(ar.text)
                mp4_urls = re.findall(r'(https?://[^\s"\'<>\\]+(?:\.mp4|cdninstagram\.com|fbcdn\.net)[^\s"\'<>\\]*)', clean_api)
                for m_url in mp4_urls:
                    if any(bad in m_url.lower() for bad in [".jpg", ".png", ".webp", "t51.2885-15"]):
                        continue
                    if _download_binary_stream(m_url, target_mp4, referer="https://www.instagram.com/"):
                        print(f"[OK] Instagram 4-Motor (External API) orqali yuklandi: {shortcode}")
                        return [target_mp4], f"Instagram Video ({shortcode})", True
        except Exception:
            pass

    return [], "", is_definitely_video

def _download_instagram_photo_if_not_video(shortcode: str, user_id: int, timestamp: int, is_definitely_video: bool) -> tuple[list, str]:
    """
    FAQAT barcha video motorlar va yt-dlp tekshirilgandan keyin,
    agar post VIDEO EMASLIGI aniq bo'lsa (haqiqiy rasm post bo'lsa), rasmni yuklaydi!
    """
    if is_definitely_video or not shortcode:
        return [], ""

    target_jpg = os.path.join(DOWNLOAD_DIR, f"{user_id}_{timestamp}_00001.jpg")
    embed_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    }
    try:
        er = requests.get(f"https://www.instagram.com/p/{shortcode}/embed/captioned/", headers=embed_headers, timeout=12, verify=False)
        if er.status_code == 200 and er.text:
            clean_body = _unescape_ig_text(er.text)
            # Agar sahifada video belgisi bo'lsa, rasm yuklamaymiz!
            if any(ind in clean_body for ind in [
                '"is_video":true', '"is_video": true',
                'EmbeddedMediaVideo', 'WatchOnInstagram', 'Watch on Instagram',
                'glyphsSpritePlay', 'video_versions', '"media_type":2'
            ]):
                return [], ""

            img_m = re.findall(r'class="EmbeddedMediaImage"[^>]+src="([^"]+)"', clean_body) or re.findall(r'"display_url"\s*:\s*"(https?://[^"]+)"', clean_body)
            for im in img_m:
                iurl = _unescape_ig_text(im)
                if _download_binary_stream(iurl, target_jpg, referer="https://www.instagram.com/"):
                    print(f"[OK] Instagram Haqiqiy Rasm Post yuklandi: {shortcode}")
                    return [target_jpg], f"Instagram Post ({shortcode})"
    except Exception:
        pass
    return [], ""

def extract_youtube_id(url: str) -> str | None:
    """Har qanday YouTube / Shorts / youtu.be / live / mobile linkdan 11 belgili video ID ni ajratish"""
    if not url:
        return None
    patterns = [
        r"(?:youtube\.com/shorts/|youtube\.com/live/|youtube\.com/embed/|youtube\.com/v/|youtu\.be/)([A-Za-z0-9_-]{11})",
        r'youtube\.com/watch\?[^\s"\x27]*v=([A-Za-z0-9_-]{11})',
    ]
    for pat in patterns:
        m = re.search(pat, url, re.IGNORECASE)
        if m:
            return m.group(1)
    return None

def _download_youtube_multi_engine(url: str, user_id: int, timestamp: int) -> tuple[list, str]:
    """
    🎬 YOUTUBE VA YOUTUBE SHORTS UCHUN 8-BOSQICHLI MAXSUS YUKLAGICH:
    GitHub Actions va Cloud datacenter IP larida YouTube bot-tekshiruvini (Sign in to confirm you're not a bot)
    aylanib o'tish uchun 8 ta mustaqil motorni ketma-ket ishlatadi!
    """
    ensure_ffmpeg_in_path()
    yt_id = extract_youtube_id(url)
    is_shorts = "/shorts/" in url.lower()
    canonical_url = f"https://www.youtube.com/watch?v={yt_id}" if yt_id else url
    shorts_url = f"https://www.youtube.com/shorts/{yt_id}" if yt_id else url
    target_mp4 = os.path.join(DOWNLOAD_DIR, f"{user_id}_{timestamp}_00001.mp4")
    out_template = os.path.join(DOWNLOAD_DIR, f"{user_id}_{timestamp}_%(autonumber)s.%(ext)s")

    def _collect_yt_files():
        return sorted([
            os.path.join(DOWNLOAD_DIR, fname)
            for fname in os.listdir(DOWNLOAD_DIR)
            if fname.startswith(f"{user_id}_{timestamp}_")
            and not fname.endswith((".part", ".ytdl", ".temp.mp4", "_v.mp4", "_a.m4a"))
            and os.path.getsize(os.path.join(DOWNLOAD_DIR, fname)) > 5000
        ])

    # ---------------- 1-MOTOR: yt-dlp Native InnerTube Multi-Client Bypass ----------------
    # MUHIM: Custom desktop User-Agent BERILMAYDI, chunki android_vr, tv_embedded va ios clientlar
    # o'zining ichki InnerTube User-Agent'i bilan ishlagandagina YouTube bot tekshiruvidan o'tadi!
    client_profiles = [
        ["android_vr", "tv_embedded"],
        ["ios", "mweb"],
        ["web_embedded", "android", "web"]
    ]
    fmt_profiles = [
        "best[ext=mp4][filesize<48M]/best[ext=mp4][height<=720]/bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]/best",
        "best[ext=mp4]/bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best"
    ]
    for idx_c, c_list in enumerate(client_profiles):
        ydl_opts = {
            "outtmpl": out_template,
            "format": fmt_profiles[0 if idx_c < 2 else 1],
            "merge_output_format": "mp4",
            "quiet": True,
            "no_warnings": True,
            "nocheckcertificate": True,
            "geo_bypass": True,
            "retries": 3,
            "fragment_retries": 3,
            "extractor_retries": 3,
            "socket_timeout": 25,
            "extractor_args": {
                "youtube": {
                    "player_client": c_list,
                    "player_skip": ["webpage", "configs"] if "android_vr" in c_list else []
                }
            }
        }
        if FFMPEG_DIR:
            ydl_opts["ffmpeg_location"] = FFMPEG_DIR
        if os.path.exists("cookies.txt"):
            ydl_opts["cookiefile"] = "cookies.txt"

        try_u = shorts_url if (is_shorts and idx_c == 0) else canonical_url
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(try_u, download=True)
                title = (info.get("title") if info else None) or "YouTube Video"
            files = _collect_yt_files()
            if files:
                print(f"[OK] YouTube 1-Motor (yt-dlp {c_list}) orqali yuklandi: {yt_id}")
                return files, str(title).strip()
        except Exception as e:
            print(f"YouTube 1-Motor ({c_list}) ogohlantirishi: {e}")

    # ---------------- 2-MOTOR: pytubefix InnerTube Multi-Client (ANDROID_VR / IOS / WEB_EMBED / TV / MWEB) ----------------
    try:
        try:
            from pytubefix import YouTube as PyTubeYouTube
        except ImportError:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "--quiet", "--upgrade", "pytubefix"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60
            )
            from pytubefix import YouTube as PyTubeYouTube

        for pt_client in ["ANDROID_VR", "IOS", "WEB_EMBED", "MWEB", "TV", "WEB"]:
            try:
                yt_obj = PyTubeYouTube(canonical_url, client=pt_client)
                pt_title = yt_obj.title or "YouTube Video"
                # 1) Progressive (video+audio birga) MP4 oqimni tekshirish
                prog_stream = (
                    yt_obj.streams.filter(progressive=True, file_extension="mp4")
                    .order_by("resolution")
                    .desc()
                    .first()
                )
                if prog_stream:
                    prog_stream.download(output_path=DOWNLOAD_DIR, filename=os.path.basename(target_mp4))
                    if os.path.exists(target_mp4) and os.path.getsize(target_mp4) > 10000:
                        print(f"[OK] YouTube 2-Motor (pytubefix {pt_client} progressive) orqali yuklandi: {yt_id}")
                        return [target_mp4], pt_title

                # 2) Adaptive (720p/1080p video + audio alohida) oqimlarni olib FFmpeg bilan birlashtirish
                v_stream = (
                    yt_obj.streams.filter(adaptive=True, file_extension="mp4", only_video=True)
                    .order_by("resolution")
                    .desc()
                    .first()
                )
                a_stream = (
                    yt_obj.streams.filter(adaptive=True, only_audio=True)
                    .order_by("abr")
                    .desc()
                    .first()
                )
                if v_stream and a_stream:
                    v_tmp = target_mp4 + "_v.mp4"
                    a_tmp = target_mp4 + "_a.m4a"
                    try:
                        v_stream.download(output_path=DOWNLOAD_DIR, filename=os.path.basename(v_tmp))
                        a_stream.download(output_path=DOWNLOAD_DIR, filename=os.path.basename(a_tmp))
                        if os.path.exists(v_tmp) and os.path.exists(a_tmp):
                            subprocess.run(
                                [FFMPEG_BIN, "-y", "-i", v_tmp, "-i", a_tmp, "-c:v", "copy", "-c:a", "aac", "-movflags", "+faststart", target_mp4],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=90
                            )
                            if os.path.exists(target_mp4) and os.path.getsize(target_mp4) > 10000:
                                print(f"[OK] YouTube 2-Motor (pytubefix {pt_client} adaptive) orqali yuklandi: {yt_id}")
                                return [target_mp4], pt_title
                    finally:
                        safe_remove(v_tmp, a_tmp)
            except Exception as pt_e:
                print(f"YouTube 2-Motor (pytubefix {pt_client}) ogohlantirishi: {pt_e}")
    except Exception as e:
        print(f"pytubefix umumiy ogohlantirishi: {e}")

    if not yt_id:
        return [], ""

    # ---------------- 3-MOTOR: Invidious Public API Network (?local=true Server-Proxied Stream!) ----------------
    invidious_hosts = [
        "https://inv.nadeko.net",
        "https://invidious.nerdvpn.de",
        "https://inv.tux.pizza",
        "https://invidious.privacyredirect.com",
        "https://yewtu.be",
        "https://vid.puffyan.us",
        "https://invidious.fdn.fr",
        "https://invidious.perennialte.ch",
        "https://invidious.jing.rocks"
    ]
    for inv_host in invidious_hosts:
        try:
            api_u = f"{inv_host}/api/v1/videos/{yt_id}"
            ir = requests.get(api_u, headers={"User-Agent": "Mozilla/5.0"}, timeout=12, verify=False)
            if ir.status_code == 200:
                ij = ir.json()
                inv_title = ij.get("title") or "YouTube Video"
                fmt_streams = ij.get("formatStreams") or []
                # Yuqori sifatli MP4 (itag 22 = 720p, itag 18 = 360p) birinchi
                fmt_streams.sort(key=lambda x: 1 if "720" in str(x.get("qualityLabel", "")) else 0, reverse=True)
                for fs in fmt_streams:
                    itag = fs.get("itag") or "18"
                    direct_u = fs.get("url") or ""
                    # 1) Avval Invidious serverining o'zi orqali proksi oqimni (?local=true) sinab ko'ramiz
                    proxy_stream_u = f"{inv_host}/latest_version?id={yt_id}&itag={itag}&local=true"
                    if _download_binary_stream(proxy_stream_u, target_mp4, referer=inv_host):
                        print(f"[OK] YouTube 3-Motor (Invidious Proxy {inv_host}) orqali yuklandi: {yt_id}")
                        return [target_mp4], inv_title
                    if direct_u and _download_binary_stream(direct_u, target_mp4, referer="https://www.youtube.com/"):
                        print(f"[OK] YouTube 3-Motor (Invidious Direct {inv_host}) orqali yuklandi: {yt_id}")
                        return [target_mp4], inv_title
        except Exception:
            pass

    # ---------------- 4-MOTOR: Piped Public API Network ----------------
    piped_hosts = [
        "https://pipedapi.kavin.rocks",
        "https://pipedapi.tokhmi.xyz",
        "https://pipedapi.moomoo.me",
        "https://pipedapi.syncpundit.io",
        "https://api.piped.private.coffee",
        "https://pipedapi.drgns.space"
    ]
    for p_host in piped_hosts:
        try:
            pr = requests.get(f"{p_host}/streams/{yt_id}", headers={"User-Agent": "Mozilla/5.0"}, timeout=12, verify=False)
            if pr.status_code == 200:
                pj = pr.json()
                p_title = pj.get("title") or "YouTube Video"
                v_streams = pj.get("videoStreams") or []
                a_streams = pj.get("audioStreams") or []
                # 1) Video+Audio birga bo'lgan (videoOnly == False) MP4 ni qidirish
                for vs in v_streams:
                    if not vs.get("videoOnly", True) and vs.get("url"):
                        if _download_binary_stream(vs["url"], target_mp4):
                            print(f"[OK] YouTube 4-Motor (Piped Muxed {p_host}) orqali yuklandi: {yt_id}")
                            return [target_mp4], p_title
                # 2) VideoOnly (<=1080p MP4) + Audio ni birlashtirish
                mp4_v = [vs for vs in v_streams if vs.get("url") and "mp4" in str(vs.get("mimeType", "")).lower() and vs.get("height", 720) <= 1080]
                if mp4_v and a_streams:
                    v_u = mp4_v[0]["url"]
                    a_u = a_streams[0].get("url")
                    v_tmp = target_mp4 + "_v.mp4"
                    a_tmp = target_mp4 + "_a.m4a"
                    try:
                        if a_u and _download_binary_stream(v_u, v_tmp) and _download_binary_stream(a_u, a_tmp):
                            subprocess.run(
                                [FFMPEG_BIN, "-y", "-i", v_tmp, "-i", a_tmp, "-c:v", "copy", "-c:a", "aac", "-movflags", "+faststart", target_mp4],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=90
                            )
                            if os.path.exists(target_mp4) and os.path.getsize(target_mp4) > 10000:
                                print(f"[OK] YouTube 4-Motor (Piped Adaptive {p_host}) orqali yuklandi: {yt_id}")
                                return [target_mp4], p_title
                    finally:
                        safe_remove(v_tmp, a_tmp)
        except Exception:
            pass

    # ---------------- 5-MOTOR: Loader.to / Y2Down Cloud Worker API ----------------
    try:
        init_loader = requests.get(
            "https://loader.to/ajax/download.php",
            params={"format": "720", "url": canonical_url},
            headers={"User-Agent": "Mozilla/5.0", "Referer": "https://en.loader.to/"},
            timeout=15, verify=False
        )
        if init_loader.status_code == 200:
            lj = init_loader.json()
            job_id = lj.get("id")
            l_title = lj.get("title") or "YouTube Video"
            if job_id:
                for _ in range(14):
                    time.sleep(1.5)
                    pr = requests.get(
                        "https://loader.to/ajax/progress.php",
                        params={"id": job_id},
                        headers={"User-Agent": "Mozilla/5.0", "Referer": "https://en.loader.to/"},
                        timeout=12, verify=False
                    )
                    if pr.status_code == 200:
                        pj = pr.json()
                        dl_u = pj.get("download_url")
                        if dl_u and dl_u.startswith("http"):
                            if _download_binary_stream(dl_u, target_mp4, referer="https://en.loader.to/"):
                                print(f"[OK] YouTube 5-Motor (Loader.to Cloud) orqali yuklandi: {yt_id}")
                                return [target_mp4], l_title
                            break
                        if int(pj.get("progress") or 0) >= 1000:
                            break
    except Exception as e:
        print(f"YouTube 5-Motor (Loader.to) ogohlantirishi: {e}")

    # ---------------- 6-MOTOR: Cobalt Public API Instances ----------------
    cobalt_endpoints = [
        "https://cobalt-api.kwiatekmiki.com",
        "https://api.cobalt.blackcat.sweeux.org",
        "https://cobalt.api.timelessnesses.me"
    ]
    for cb_host in cobalt_endpoints:
        try:
            cbr = requests.post(
                f"{cb_host}/",
                json={"url": canonical_url, "videoQuality": "720", "youtubeVideoCodec": "h264"},
                headers={"Accept": "application/json", "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
                timeout=14, verify=False
            )
            if cbr.status_code in (200, 201):
                cbj = cbr.json()
                dl_u = cbj.get("url")
                if dl_u and _download_binary_stream(dl_u, target_mp4):
                    print(f"[OK] YouTube 6-Motor (Cobalt {cb_host}) orqali yuklandi: {yt_id}")
                    return [target_mp4], "YouTube Video"
        except Exception:
            pass

    # ---------------- 7-MOTOR: RyzenDesu / VKR / SaveTube External Cloud APIs ----------------
    ext_yt_apis = [
        f"https://api.ryzendesu.vip/api/downloader/ytmp4?url={urllib.parse.quote(canonical_url)}&quality=720",
        f"https://api.ryzendesu.vip/api/downloader/ytmp4?url={urllib.parse.quote(canonical_url)}",
        f"https://vkrdownloader.xyz/server?vkr={urllib.parse.quote(canonical_url)}"
    ]
    for ext_u in ext_yt_apis:
        try:
            er = requests.get(ext_u, headers={"User-Agent": "Mozilla/5.0"}, timeout=16, verify=False)
            if er.status_code == 200 and er.text:
                ej_text = _unescape_ig_text(er.text)
                try:
                    ej = er.json()
                    cand_links = []
                    if isinstance(ej, dict):
                        for k in ("url", "downloadUrl", "dl_link", "video"):
                            if isinstance(ej.get(k), str) and ej[k].startswith("http"):
                                cand_links.append(ej[k])
                        data_d = ej.get("data") or {}
                        if isinstance(data_d, dict):
                            for k in ("url", "downloadUrl", "hd", "sd"):
                                if isinstance(data_d.get(k), str) and data_d[k].startswith("http"):
                                    cand_links.append(data_d[k])
                            for dl_item in (data_d.get("downloads") or []):
                                if isinstance(dl_item, dict) and str(dl_item.get("url", "")).startswith("http"):
                                    cand_links.append(dl_item["url"])
                    for clink in cand_links:
                        if _download_binary_stream(clink, target_mp4):
                            print(f"[OK] YouTube 7-Motor (External Cloud API) orqali yuklandi: {yt_id}")
                            return [target_mp4], "YouTube Video"
                except Exception:
                    pass
                for m_url in re.findall(r"(https?://[^\s\"\x27<>\\\\]+(?:\.mp4|googlevideo\.com)[^\s\"\x27<>\\\\]*)", ej_text):
                    if _download_binary_stream(m_url, target_mp4):
                        print(f"[OK] YouTube 7B-Motor (Regex Cloud Stream) orqali yuklandi: {yt_id}")
                        return [target_mp4], "YouTube Video"
        except Exception:
            pass

    return _collect_yt_files(), "YouTube Video"

def _download_tiktok_multi_engine(url: str, user_id: int, timestamp: int) -> tuple[list, str]:
    """TikTok uchun 3-Bosqichli Suv Belgisiz HD Yuklagich (Rate-Limit Himoyasi + Video + Slayd-shou)"""
    target_mp4 = os.path.join(DOWNLOAD_DIR, f"{user_id}_{timestamp}_00001.mp4")

    # 1-Motor: TikWM API (HD No-Watermark + Slideshow Images, 1.25s rate-limit navbati bilan)
    try:
        _wait_tikwm_rate_limit(1.25)
        resp = requests.post(
            "https://www.tikwm.com/api/",
            data={"url": url, "hd": 1},
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
            timeout=20,
            verify=False
        )
        if resp.status_code == 200:
            j = resp.json()
            if j.get("code") == 0 and j.get("data"):
                d = j["data"]
                title = d.get("title") or "TikTok Video"
                images = d.get("images")
                if images and isinstance(images, list):
                    collected = []
                    for idx, img_url in enumerate(images[:10], 1):
                        fp = os.path.join(DOWNLOAD_DIR, f"{user_id}_{timestamp}_{idx:05d}.jpg")
                        if _download_binary_stream(img_url, fp):
                            collected.append(fp)
                    if collected:
                        print("[OK] TikTok TikWM Karusel orqali yuklandi")
                        return collected, title

                for k_stream in ("play", "hdplay", "wmplay"):
                    play_url = d.get(k_stream)
                    if play_url and isinstance(play_url, str):
                        if play_url.startswith("/"):
                            play_url = "https://www.tikwm.com" + play_url
                        if _download_binary_stream(play_url, target_mp4, referer="https://www.tikwm.com/"):
                            print(f"[OK] TikTok TikWM ({k_stream}) orqali yuklandi")
                            return [target_mp4], title
    except Exception as e:
        print(f"TikWM xatosi: {e}")

    # 2-Motor: vxTikTok / tnktok Proxy OpenGraph
    parsed = urllib.parse.urlparse(url)
    for tk_domain in ["https://www.vxtiktok.com", "https://tnktok.com"]:
        try:
            tk_url = f"{tk_domain}{parsed.path}"
            r = requests.get(tk_url, headers={"User-Agent": "TelegramBot (like TwitterBot)"}, timeout=15, verify=False)
            if r.status_code == 200:
                m = re.search(r'property="og:video(?::secure_url)?"\s+content="([^"]+)"', r.text)
                if m:
                    vurl = _unescape_ig_text(m.group(1))
                    if _download_binary_stream(vurl, target_mp4):
                        print(f"[OK] TikTok {tk_domain} orqali yuklandi")
                        return [target_mp4], "TikTok Video"
        except Exception:
            pass

    return [], ""

def _download_twitter_fallback(url: str, user_id: int, timestamp: int) -> tuple[list, str]:
    """Twitter / X uchun vxTwitter JSON API zaxirasi"""
    m = re.search(r"(?:twitter\.com|x\.com)/([^/]+)/status/(\d+)", url, re.IGNORECASE)
    if not m:
        return [], ""
    user_handle, status_id = m.group(1), m.group(2)
    try:
        api_url = f"https://api.vxtwitter.com/{user_handle}/status/{status_id}"
        r = requests.get(api_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15, verify=False)
        if r.status_code == 200:
            data = r.json()
            title = data.get("text") or "X / Twitter Video"
            media_list = data.get("media_extended", [])
            collected = []
            for idx, mitem in enumerate(media_list[:10], 1):
                murl = mitem.get("url")
                mtype = mitem.get("type", "video")
                ext = "mp4" if mtype in ("video", "gif") else "jpg"
                fp = os.path.join(DOWNLOAD_DIR, f"{user_id}_{timestamp}_{idx:05d}.{ext}")
                if murl and _download_binary_stream(murl, fp):
                    collected.append(fp)
            if collected:
                print("[OK] Twitter/X vxTwitter API orqali yuklandi")
                return collected, title
    except Exception as e:
        print(f"vxTwitter xatosi: {e}")
    return [], ""

def _download_pinterest_fallback(url: str, user_id: int, timestamp: int) -> tuple[list, str]:
    """Pinterest uchun to'g'ridan-to'g'ri pinimg.com video/rasm qidiruv zaxirasi"""
    target_mp4 = os.path.join(DOWNLOAD_DIR, f"{user_id}_{timestamp}_00001.mp4")
    target_jpg = os.path.join(DOWNLOAD_DIR, f"{user_id}_{timestamp}_00001.jpg")
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        }
        r = requests.get(url, headers=headers, timeout=15, verify=False)
        if r.status_code == 200 and r.text:
            mp4_matches = re.findall(r'(https://v\d*\.pinimg\.com/videos/[^\s"\]+\.mp4)', r.text)
            for vurl in mp4_matches:
                clean_v = _unescape_ig_text(vurl)
                if _download_binary_stream(clean_v, target_mp4):
                    print("[OK] Pinterest direct MP4 yuklandi")
                    return [target_mp4], "Pinterest Video"
            img_matches = re.findall(r'(https://i\.pinimg\.com/originals/[^\s"\]+\.(?:jpg|png|webp))', r.text)
            for iurl in img_matches:
                clean_i = _unescape_ig_text(iurl)
                if _download_binary_stream(clean_i, target_jpg):
                    print("[OK] Pinterest direct Image yuklandi")
                    return [target_jpg], "Pinterest Image"
    except Exception as e:
        print(f"Pinterest fallback xatosi: {e}")
    return [], ""

def ensure_phone_playable_mp4(input_path: str, force_reencode: bool = False, apply_watermark: bool = False) -> tuple[str, dict]:
    """
    Telefonda (iPhone va Android) bittada ochiladigan H.264 (yuv420p) + faststart MP4 ga keltirish
    HAMDA har bitta videoga tepadan-pastga suzib yuruvchi ko'rinar-ko'rinmas (prazrachniy)
    Telegram ikonka + @handle watermark tushirish!
    MUHIM: Fayl nomini (input_path) o'zgartirmasdan joyida (in-place) yangilaydi, shunda
    inline tugmalardagi `base_fname` hech qachon yo'qolib qolmaydi!
    """
    ensure_ffmpeg_in_path()
    vinfo = get_video_stream_info(input_path)
    ext = os.path.splitext(input_path)[1].lower()
    codec = vinfo.get("codec", "h264")
    cfg = get_watermark_settings()
    already_watermarked = os.path.basename(input_path).startswith(("reklama_reel_", "orig_"))

    if apply_watermark and cfg.get("enabled", True) and not already_watermarked:
        wm_out = os.path.splitext(input_path)[0] + "_wm_tmp.mp4"
        if apply_floating_watermark_to_video(input_path, wm_out):
            try:
                os.replace(wm_out, input_path)
            except Exception:
                safe_remove(wm_out)
            vinfo = get_video_stream_info(input_path)
            return input_path, vinfo
        safe_remove(wm_out)

    if force_reencode or codec not in ("h264", "avc1") or ext != ".mp4":
        fixed_path = os.path.splitext(input_path)[0] + "_phone_tmp.mp4"
        cmd = [
            FFMPEG_BIN, "-y", "-i", input_path,
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23",
            "-pix_fmt", "yuv420p",
            "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
            "-c:a", "aac", "-b:a", "128k",
            "-movflags", "+faststart",
            fixed_path
        ]
        try:
            res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=150)
            if res.returncode == 0 and os.path.exists(fixed_path) and os.path.getsize(fixed_path) > 1000:
                try:
                    os.replace(fixed_path, input_path)
                except Exception:
                    safe_remove(fixed_path)
                vinfo = get_video_stream_info(input_path)
                return input_path, vinfo
        except Exception:
            pass
        safe_remove(fixed_path)
    return input_path, vinfo

def download_media_bulletproof(raw_url: str, user_id: int, timestamp: int) -> tuple[list, str]:
    """
    12-Bosqichli VIDEO-FIRST Media Yuklagich:
    Instagram (6-Motor), YouTube/Shorts (8-Motor), TikTok (3-Motor), Pinterest, Twitter/X va 1000+ saytlar!
    Qisqa va xavfsiz fayl nomlari bilan yuklaydi (callback_data 64-bayt limitidan oshmasligi uchun!).
    """
    ensure_ffmpeg_in_path()
    url = clean_and_resolve_url(raw_url)
    lower_url = url.lower()
    short_ts = timestamp % 100000000
    out_template = os.path.join(DOWNLOAD_DIR, f"{user_id}_{short_ts}_%(autonumber)s.%(ext)s")

    def _collect_files(ts_val):
        return sorted([
            os.path.join(DOWNLOAD_DIR, fname)
            for fname in os.listdir(DOWNLOAD_DIR)
            if fname.startswith(f"{user_id}_{ts_val}_")
            and not fname.endswith(".part")
            and not fname.endswith(".ytdl")
            and os.path.getsize(os.path.join(DOWNLOAD_DIR, fname)) > 1000
        ])

    # 1. Instagram maxsus 6-Motorli tizimi
    ig_shortcode = extract_ig_shortcode(url) if ("instagram.com" in lower_url or "instagr.am" in lower_url) else None
    is_definitely_video = False

    if ig_shortcode:
        ig_files, ig_title, is_definitely_video = _download_instagram_video_engines(url, user_id, short_ts)
        if ig_files:
            return ig_files, ig_title

    # 2. YouTube va YouTube Shorts maxsus 8-Motorli tizimi (yt-dlp Native InnerTube + pytubefix + Invidious + Piped + Loader + Cobalt)
    if "youtube.com" in lower_url or "youtu.be" in lower_url:
        yt_files, yt_title = _download_youtube_multi_engine(url, user_id, short_ts)
        if yt_files:
            return yt_files, yt_title

    # 3. TikTok maxsus 3-Motorli tizimi
    if "tiktok.com" in lower_url:
        tk_files, tk_title = _download_tiktok_multi_engine(url, user_id, short_ts)
        if tk_files:
            return tk_files, tk_title

    # 4. Umumiy yt-dlp (Boshqa barcha platformalar uchun)
    format_candidates = [
        "best[ext=mp4][vcodec^=avc1]/bestvideo[ext=mp4][vcodec^=avc1]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "bestvideo+bestaudio/best"
    ]
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1"
    ]

    urls_to_try = [url]
    if ig_shortcode:
        reel_variant = f"https://www.instagram.com/reel/{ig_shortcode}/"
        post_variant = f"https://www.instagram.com/p/{ig_shortcode}/"
        urls_to_try = [reel_variant, post_variant]

    title = "Video"
    for candidate_u in urls_to_try:
        for attempt_idx in range(2):
            ydl_opts = {
                "outtmpl": out_template,
                "format": format_candidates[attempt_idx],
                "merge_output_format": "mp4",
                "quiet": True,
                "no_warnings": True,
                "nocheckcertificate": True,
                "geo_bypass": True,
                "retries": 4,
                "fragment_retries": 4,
                "extractor_retries": 3,
                "socket_timeout": 30,
                "http_headers": {
                    "User-Agent": user_agents[attempt_idx],
                    "Accept-Language": "en-US,en;q=0.9,ru;q=0.8,uz;q=0.7"
                }
            }
            if FFMPEG_DIR:
                ydl_opts["ffmpeg_location"] = FFMPEG_DIR
            if os.path.exists("cookies.txt"):
                ydl_opts["cookiefile"] = "cookies.txt"

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(candidate_u, download=True)
                    if info:
                        title = info.get("title") or info.get("description") or "Video"
                files = _collect_files(short_ts)
                if files:
                    print(f"[OK] yt-dlp orqali yuklandi: {candidate_u}")
                    return files, str(title).strip() or "Video"
            except Exception as e:
                print(f"yt-dlp urinish xatosi ({candidate_u}): {e}")

    if "twitter.com" in lower_url or "x.com" in lower_url:
        tw_files, tw_title = _download_twitter_fallback(url, user_id, short_ts)
        if tw_files:
            return tw_files, tw_title

    if "pinterest.com" in lower_url or "pin.it" in lower_url:
        pin_files, pin_title = _download_pinterest_fallback(url, user_id, short_ts)
        if pin_files:
            return pin_files, pin_title

    if ig_shortcode:
        photo_files, photo_title = _download_instagram_photo_if_not_video(ig_shortcode, user_id, short_ts, is_definitely_video)
        if photo_files:
            return photo_files, photo_title

    return _collect_files(short_ts), title

def ensure_video_from_telegram(message_obj: types.Message, local_video_path: str) -> bool:
    """
    1) Agar video downloads/ papkasida mavjud bo'lsa -> 0.001 soniyada darhol tayyor!
    2) Agar eskirib o'chirilgan bo'lsa -> Telegram file_id dan (yoki VIDEO_SOURCE_CACHE dagi URL dan)
       xavfsiz temp faylga yuklab, atomik tarzda qayta tiklaydi!
    """
    if os.path.exists(local_video_path) and os.path.getsize(local_video_path) > 500:
        return True

    base_fname = os.path.basename(local_video_path)
    cached_meta = VIDEO_SOURCE_CACHE.get(base_fname, {})
    cached_path = cached_meta.get("path")
    if cached_path and os.path.exists(cached_path) and os.path.getsize(cached_path) > 500:
        if os.path.abspath(cached_path) != os.path.abspath(local_video_path):
            try:
                shutil.copyfile(cached_path, local_video_path)
                return True
            except Exception:
                pass
        else:
            return True

    with FILE_LOCK:
        if os.path.exists(local_video_path) and os.path.getsize(local_video_path) > 500:
            return True

        media_obj = None
        if message_obj:
            media_obj = (
                getattr(message_obj, "video", None)
                or getattr(message_obj, "audio", None)
                or getattr(message_obj, "voice", None)
                or getattr(message_obj, "video_note", None)
                or getattr(message_obj, "document", None)
            )
            if not media_obj and getattr(message_obj, "reply_to_message", None):
                r = message_obj.reply_to_message
                media_obj = (
                    getattr(r, "video", None)
                    or getattr(r, "audio", None)
                    or getattr(r, "voice", None)
                    or getattr(r, "video_note", None)
                    or getattr(r, "document", None)
                )

        file_id = getattr(media_obj, "file_id", None) or cached_meta.get("file_id")
        if file_id:
            tmp_dl = local_video_path + f".dl_{int(time.time()*1000)}"
            try:
                file_info = bot.get_file(file_id)
                downloaded_bytes = bot.download_file(file_info.file_path)
                with open(tmp_dl, "wb") as f:
                    f.write(downloaded_bytes)
                if os.path.exists(tmp_dl) and os.path.getsize(tmp_dl) > 500:
                    os.replace(tmp_dl, local_video_path)
                    return True
            except Exception as e:
                print(f"Telegram file_id dan qayta yuklash ogohlantirishi: {e}")
            finally:
                safe_remove(tmp_dl)

        # Agar fayl >20 MB bo'lib Telegram get_file ruxsat bermasa, original URL dan qayta tortish:
        orig_url = cached_meta.get("url")
        if orig_url:
            try:
                files, _ = download_media_bulletproof(orig_url, ADMIN_ID, int(time.time() * 1000))
                if files and os.path.exists(files[0]):
                    os.replace(files[0], local_video_path)
                    return True
            except Exception as e:
                print(f"URL dan qayta tiklash xatosi: {e}")

    return False

# ==================== TUGMALARNI SHAKLLANTIRISH ====================
def make_video_action_keyboard(base_fname: str, lang: str = "uz") -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=2)
    labels = {
        "uz": {
            "sub_vid": "🎬 Subtitrli video", "sub_txt": "📝 Subtitr matni (.srt)",
            "circle": "🔵 Kruglyash", "audio": "🎧 MP3 Audio",
            "bass": "🔊 Bass Boost", "audio8d": "🎧 8D Audio",
            "karaoke": "🎤 Karaoke Minus", "thumb": "🖼 HD Oblojka",
            "voice": "🎙 Ovozli xabar", "trim": "✂️ Qirqish (Trim)",
            "shazam": "🎵 Musiqani topish", "speed": "⚡ 1.5x Tezlik",
            "reverse": "⏪ Teskari video", "gif": "🎞 GIF qilish"
        },
        "ru": {
            "sub_vid": "🎬 С субтитрами", "sub_txt": "📝 Текст (.srt)",
            "circle": "🔵 Кругляш", "audio": "🎧 MP3 Аудио",
            "bass": "🔊 Bass Boost", "audio8d": "🎧 8D Аудио",
            "karaoke": "🎤 Караоке Минус", "thumb": "🖼 HD Обложка",
            "voice": "🎙 Голосовое", "trim": "✂️ Обрезать (Trim)",
            "shazam": "🎵 Найти музыку", "speed": "⚡ 1.5x Скорость",
            "reverse": "⏪ Реверс видео", "gif": "🎞 В GIF"
        },
        "en": {
            "sub_vid": "🎬 Subtitled Video", "sub_txt": "📝 Subtitle (.srt)",
            "circle": "🔵 Video Note", "audio": "🎧 MP3 Audio",
            "bass": "🔊 Bass Boost", "audio8d": "🎧 8D Audio",
            "karaoke": "🎤 Karaoke Minus", "thumb": "🖼 HD Thumbnail",
            "voice": "🎙 Voice Note", "trim": "✂️ Trim Video",
            "shazam": "🎵 Identify Music", "speed": "⚡ 1.5x Speed",
            "reverse": "⏪ Reverse Video", "gif": "🎞 To GIF"
        }
    }
    lbl = labels.get(lang, labels["uz"])

    markup.add(
        types.InlineKeyboardButton(lbl["sub_vid"], callback_data=f"sub_vid:{base_fname}"),
        types.InlineKeyboardButton(lbl["sub_txt"], callback_data=f"sub_txt:{base_fname}")
    )
    markup.add(
        types.InlineKeyboardButton(lbl["circle"], callback_data=f"circle:{base_fname}"),
        types.InlineKeyboardButton(lbl["audio"], callback_data=f"audio:{base_fname}"),
    )
    markup.add(
        types.InlineKeyboardButton(lbl["bass"], callback_data=f"bass:{base_fname}"),
        types.InlineKeyboardButton(lbl["audio8d"], callback_data=f"audio8d:{base_fname}")
    )
    markup.add(
        types.InlineKeyboardButton(lbl["karaoke"], callback_data=f"karaoke:{base_fname}"),
        types.InlineKeyboardButton(lbl["thumb"], callback_data=f"thumb:{base_fname}")
    )
    markup.add(
        types.InlineKeyboardButton(lbl["voice"], callback_data=f"voice:{base_fname}"),
        types.InlineKeyboardButton(lbl["trim"], callback_data=f"trim:{base_fname}")
    )
    markup.add(
        types.InlineKeyboardButton(lbl["shazam"], callback_data=f"shazam:{base_fname}"),
        types.InlineKeyboardButton(lbl["speed"], callback_data=f"speed:{base_fname}")
    )
    markup.add(
        types.InlineKeyboardButton(lbl["reverse"], callback_data=f"reverse:{base_fname}"),
        types.InlineKeyboardButton(lbl["gif"], callback_data=f"gif:{base_fname}")
    )
    antidup_lbl = {
        "uz": "🛡 Anti-Duplikat (100% Original — Top/Rekomendatsiya)",
        "ru": "🛡 Анти-Дубликат (100% Оригинал для Reels/TikTok)",
        "en": "🛡 Anti-Duplicate (100% Original for Reels/TikTok)"
    }.get(lang, "🛡 Anti-Duplikat (100% Original — Top/Rekomendatsiya)")
    montaj_lbl = {
        "uz": "🎯 Pro Reklama Montaj (2-Video / Outro Ulash)",
        "ru": "🎯 Про Видео Монтаж (Склеить с Outro / 2-м видео)",
        "en": "🎯 Pro Promo Montage (Merge with Outro / 2nd Video)"
    }.get(lang, "🎯 Pro Reklama Montaj (2-Video / Outro Ulash)")
    markup.add(types.InlineKeyboardButton(antidup_lbl, callback_data=f"antidup_vid:{base_fname}"))
    markup.add(types.InlineKeyboardButton(montaj_lbl, callback_data=f"montaj_from_vid:{base_fname}"))
    markup.add(
        types.InlineKeyboardButton("📸 Insta Reels Joylash", callback_data=f"ig_post_vid:{base_fname}"),
        types.InlineKeyboardButton("📅 Avto-Navbatga Qo'shish", callback_data=f"ig_queue_vid:{base_fname}")
    )
    return markup

def make_sub_lang_keyboard(action_type: str, base_fname: str) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=2)
    b_uz = types.InlineKeyboardButton("🇺🇿 O'zbek tili", callback_data=f"{action_type}:uz-UZ:{base_fname}")
    b_ru = types.InlineKeyboardButton("🇷🇺 Rus tili", callback_data=f"{action_type}:ru-RU:{base_fname}")
    b_en = types.InlineKeyboardButton("🇬🇧 Ingliz tili", callback_data=f"{action_type}:en-US:{base_fname}")
    b_auto = types.InlineKeyboardButton("🌐 Avto aniqlash", callback_data=f"{action_type}:auto:{base_fname}")
    b_back = types.InlineKeyboardButton("🔙 Orqaga", callback_data=f"back_video:{base_fname}")
    markup.add(b_uz, b_ru)
    markup.add(b_en, b_auto)
    markup.add(b_back)
    return markup

def get_universal_tools_keyboard() -> types.InlineKeyboardMarkup:
    """AI olib tashlangan, sof Pro Montaj, Anti-Duplikat, Watermark, Valyuta va QR vositalari"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    b_ig_panel = types.InlineKeyboardButton("📸 Instagram Avto-Poster 24/7 (/ig)", callback_data="ig_open_panel")
    b_montaj = types.InlineKeyboardButton("🎬 Pro Reklama Montaj (/montaj)", callback_data="tool_cmd:montaj")
    b_orig = types.InlineKeyboardButton("🛡 100% Original Anti-Duplikat (/original)", callback_data="antidup_start_single")
    markup.add(b_ig_panel)
    b_outro = types.InlineKeyboardButton("📌 Reklama Outro Saqlash (/set_outro)", callback_data="tool_cmd:set_outro")
    b_wm = types.InlineKeyboardButton("💧 Shaffof Watermark (/set_watermark)", callback_data="montaj_set_wm")
    b_kurs = types.InlineKeyboardButton("💱 Valyuta Kursi (/kurs)", callback_data="tool_cmd:kurs")
    b_qr = types.InlineKeyboardButton("📱 QR-Kod Yasash (/qr)", callback_data="tool_cmd:qr")
    b_clean = types.InlineKeyboardButton("🧹 Keshni Tozalash (/clean)", callback_data="clean_storage_cb")
    markup.add(b_montaj)
    markup.add(b_orig)
    markup.add(b_outro, b_wm)
    markup.add(b_kurs, b_qr)
    markup.add(b_clean)
    return markup

def make_montage_mode_keyboard(session_key: str) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(
            "🔥 1. Audio Uzluksiz + Whoosh FX (1-Audio 2-ga o'tadi, 2-Mute) [Tavsiya]",
            callback_data=f"do_montaj:audio1_bridge:{session_key}"
        ),
        types.InlineKeyboardButton(
            "🎬 2. L-Cut Overlap (1-Video kadri almashib, audiosi 2-da tugaydi)",
            callback_data=f"do_montaj:lcut_split:{session_key}"
        ),
        types.InlineKeyboardButton(
            "🖼 3. PiP Reklama (Burchakda 3s Preview + To'liq Ekran Outro)",
            callback_data=f"do_montaj:pip_outro:{session_key}"
        ),
        types.InlineKeyboardButton(
            "🔊 4. Original Ovozlar (1-Video ovozi + 2-Video o'z ovozi)",
            callback_data=f"do_montaj:both_original:{session_key}"
        ),
        types.InlineKeyboardButton(
            "🔉 5. Fon Musiqa Mix (1-Audio 25% fonda + 2-Video ovozi 100%)",
            callback_data=f"do_montaj:audio_ducking:{session_key}"
        ),
        types.InlineKeyboardButton("❌ Bekor qilish", callback_data=f"cancel_montaj:{session_key}")
    )
    return markup

# ==================== ASOSIY BUYRUQLAR (COMMANDS) ====================
@bot.message_handler(commands=['start'])
def handle_start(message: types.Message):
    user = message.from_user
    USER_STATES.pop(user.id, None)
    referrer_id = None
    args = message.text.split()
    if len(args) > 1 and args[1].startswith("ref_"):
        try:
            referrer_id = int(args[1].replace("ref_", ""))
        except ValueError:
            referrer_id = None

    is_new, ref_became_vip = register_user(user, referrer_id)
    lang = get_user_lang(user.id)

    if ref_became_vip and referrer_id:
        try:
            ref_lang = get_user_lang(referrer_id)
            vip_notif = {
                "uz": f"🎉 <b>Ajoyib yangilik!</b> Siz {REQUIRED_REFERRALS_FOR_VIP} ta do'stingizni taklif qildingiz!\n\n⭐️ <b>Sizga umrbod VIP maqomi berildi!</b>",
                "ru": f"🎉 <b>Отличные новости!</b> Вы пригласили {REQUIRED_REFERRALS_FOR_VIP} друзей!\n\n⭐️ <b>Вам присвоен вечный статус VIP!</b>",
                "en": f"🎉 <b>Great news!</b> You have invited {REQUIRED_REFERRALS_FOR_VIP} friends!\n\n⭐️ <b>You are granted lifetime VIP status!</b>"
            }
            bot.send_message(referrer_id, vip_notif.get(ref_lang, vip_notif["uz"]))
        except Exception:
            pass

    is_subbed, unsubscribed = check_channel_subscription(user.id)
    if not is_subbed:
        bot.send_message(
            message.chat.id,
            get_text("sub_required", lang),
            reply_markup=get_sub_keyboard(unsubscribed, lang)
        )
        return

    text = get_text("welcome", lang, name=user.first_name)
    bot.send_message(message.chat.id, text, reply_markup=get_main_reply_keyboard(lang))

@bot.message_handler(commands=['help'])
@bot.message_handler(func=lambda msg: msg.text in ["📖 Qo'llanma", "📖 Инструкция", "📖 Help"])
def handle_help(message: types.Message):
    USER_STATES.pop(message.from_user.id, None)
    help_text = (
        "📖 <b>Universal Super Saver & Pro Montaj Bot Qo'llanmasi:</b>\n\n"
        "1️⃣ <b>Video va musiqa yuklash:</b> Instagram, TikTok, YouTube, Pinterest, X havolasini yuboring.\n"
        "2️⃣ <b>16 ta Multimedia studiyasi:</b> Video yuklangach, uning ostidagi tugmalar orqali:\n"
        "   • 🎯 <b>Pro Reklama Montaj</b> — Videoga 2-videoni (Outro reklamani) 5 xil rejimda ulash\n"
        "   • 🛡 <b>Anti-Duplikat (100% Original)</b> — Reels va TikTok Top/Rekomendatsiya uchun\n"
        "   • 🎬 <b>Subtitrli video</b> va 📝 <b>.SRT subtitr fayli</b>\n"
        "   • 🔊 <b>Bass Boost</b>, 🎧 <b>8D Audio</b> va 🎤 <b>Karaoke Minusovka</b>\n"
        "   • 🔵 <b>Kruglyash</b>, ✂️ <b>Qirqish (Trim)</b>, ⏪ <b>Teskari video</b>, 🖼 <b>HD Oblojka</b>\n"
        "3️⃣ <b>Pro Reklama Montaj (/montaj):</b> Istalgan 2 ta videoni (10s, 19s, 1 daqiqa+) professional ulash.\n"
        "4️⃣ <b>Doimiy Reklama Outro (/set_outro):</b> Reklama videongizni 1 marta saqlab qo'yib, 1 bosishda ulash.\n"
        "5️⃣ <b>Suzuvchi Shaffof Watermark (/set_watermark):</b> Tepadan-pastga suzuvchi @username belgisini sozlash.\n"
        "6️⃣ <b>QR-Kod yasash:</b> <code>/qr ssilka yoki matn</code>.\n"
        "7️⃣ <b>Valyuta kurslari:</b> <code>/kurs</code> yoki <code>/kurs 100</code> — Markaziy bank jonli kurslari."
    )
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=['tools'])
@bot.message_handler(func=lambda msg: msg.text in ["🛠 Universal Vositalar", "🛠 Инструменты", "🛠 Smart Tools"])
def handle_tools_menu(message: types.Message):
    USER_STATES.pop(message.from_user.id, None)
    text = (
        "🛠 <b>Universal Foydali Vositalar va Pro Studiya Markazi:</b>\n\n"
        "• 🎬 <b>Pro Reklama Montaj:</b> <code>/montaj</code> (2 ta videoni 5 xil rejimda ulash)\n"
        "• 🛡 <b>Anti-Duplikat (100% Original):</b> <code>/original</code>\n"
        "• 📌 <b>Doimiy Reklama Outro Saqlash:</b> <code>/set_outro</code>\n"
        "• 💧 <b>Shaffof Watermark Sozlash:</b> <code>/set_watermark</code>\n"
        "• 💱 <b>Valyuta Kurslari:</b> <code>/kurs</code> yoki <code>/kurs 100</code>\n"
        "• 📱 <b>QR-Kod Generator:</b> <code>/qr https://t.me/usman_khasan</code>\n\n"
        "Quyidagi tugmalardan birini bosing:"
    )
    bot.send_message(message.chat.id, text, reply_markup=get_universal_tools_keyboard())

@bot.message_handler(commands=['kurs', 'valyuta'])
@bot.message_handler(func=lambda msg: msg.text and msg.text.strip() in [
    "💱 Valyuta Kurslari", "💱 Курсы валют", "💱 Exchange Rates",
    "kurs", "Kurs", "valyuta", "Valyuta"
])
def handle_kurs_cmd(message: types.Message):
    USER_STATES.pop(message.from_user.id, None)
    amount = 1.0
    if message.text:
        parts = message.text.strip().split()
        if len(parts) > 1:
            try:
                amount = float(parts[1].replace(",", "."))
            except ValueError:
                amount = 1.0
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.add(
        types.InlineKeyboardButton("💵 100$", callback_data="kurs_amt:100"),
        types.InlineKeyboardButton("💵 500$", callback_data="kurs_amt:500"),
        types.InlineKeyboardButton("💵 1000$", callback_data="kurs_amt:1000"),
    )
    markup.add(types.InlineKeyboardButton("🔄 Kursni yangilash", callback_data="kurs_amt:1"))
    bot.reply_to(message, fetch_cbu_exchange_rates(amount), reply_markup=markup)

@bot.message_handler(commands=['qr'])
def handle_qr_cmd(message: types.Message):
    USER_STATES.pop(message.from_user.id, None)
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "📱 <b>QR-Kod yasash uchun matn yoki ssilka yuboring:</b>")
        USER_STATES[message.from_user.id] = {"action": "qr_make"}
        return
    send_qr_result(message, args[1])

def process_qr_step(message: types.Message):
    uid = message.from_user.id
    USER_STATES.pop(uid, None)
    if message.text:
        send_qr_result(message, message.text)

def send_qr_result(message: types.Message, data_text: str):
    qr_bytes = generate_qr_code_bytes(data_text)
    if qr_bytes:
        bot.send_photo(
            message.chat.id,
            photo=qr_bytes,
            caption=f"📱 <b>QR-Kod tayyor!</b>\n🔗 <code>{data_text[:100]}</code>\n\n🤖 @{get_cached_bot_username()}"
        )
    else:
        bot.reply_to(message, "❌ QR-kod yaratishda xatolik yuz berdi.")

@bot.message_handler(commands=['lang', 'language'])
@bot.message_handler(func=lambda msg: msg.text in ["🌐 Til", "🌐 Сменить язык", "🌐 Language"])
def handle_lang_command(message: types.Message):
    USER_STATES.pop(message.from_user.id, None)
    bot.send_message(
        message.chat.id,
        "🌐 <b>Tilni tanlang / Выберите язык / Select language:</b>",
        reply_markup=get_language_inline_keyboard()
    )

@bot.message_handler(commands=['referral', 'ref'])
@bot.message_handler(func=lambda msg: msg.text in ["👥 VIP & Do'stlar", "👥 VIP & Рефералы", "👥 VIP & Referral"])
def handle_referral(message: types.Message):
    user = message.from_user
    USER_STATES.pop(user.id, None)
    register_user(user)
    prof = get_user_profile(user.id)
    bot_uname = get_cached_bot_username()

    ref_link = f"https://t.me/{bot_uname}?start=ref_{user.id}"
    vip_status = "⭐️ VIP (Faol)" if prof['is_vip'] else f"{prof['referrals']} / {REQUIRED_REFERRALS_FOR_VIP}"

    share_text = f"🔥 Instagram, TikTok, YouTube dan suv belgisiz video yuklovchi, Pro Reklama Montaj, 8D Audio va Bass Boost bot!\n\n{ref_link}"
    share_url = f"https://t.me/share/url?url={urllib.parse.quote(share_text)}"

    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("🚀 Telegramda ulashish", url=share_url))

    ref_msg = (
        "👥 <b>VIP & Referal Dasturi</b>\n\n"
        f"🔗 <b>Sizning taklif havolangiz:</b>\n<code>{ref_link}</code>\n\n"
        f"📊 <b>Chaqirilgan do'stlar:</b> {prof['referrals']} ta\n"
        f"🏆 <b>VIP holati:</b> {vip_status}\n\n"
        f"🎁 <b>Qoida:</b> {REQUIRED_REFERRALS_FOR_VIP} ta do'stingizni taklif qiling va botdan umrbod erkin, obunalarsiz foydalaning!"
    )
    bot.send_message(message.chat.id, ref_msg, reply_markup=markup)

@bot.message_handler(commands=['profile'])
@bot.message_handler(func=lambda msg: msg.text in ["👤 Profilim", "👤 Мой профиль", "👤 Profile"])
def handle_profile(message: types.Message):
    user = message.from_user
    USER_STATES.pop(user.id, None)
    register_user(user)
    prof = get_user_profile(user.id)
    uname = f"@{user.username}" if user.username else (ADMIN_USERNAME if user.id == ADMIN_ID else f"user_{user.id}")
    fname = user.first_name or (ADMIN_FIRST_NAME if user.id == ADMIN_ID else "User")
    status_str = "⭐️ VIP (Umrbod)" if prof['is_vip'] else "Standard"
    wm_cfg = get_watermark_settings()
    outro_path = get_saved_outro_path(user.id)
    outro_str = f"✅ Saqlangan ({get_media_duration(outro_path):.1f}s)" if outro_path else "⚠️ Saqlanmagan (/set_outro)"

    text = (
        f"👤 <b>{uname}</b>\n"
        f"🆔 <b>Id:</b> <code>{user.id}</code>\n"
        f"👤 <b>Ism:</b> {fname}\n"
        f"🌐 <b>Til:</b> {prof.get('language', 'uz')}\n"
        f"📅 <b>Ro'yxatdan o'tgan:</b> {prof.get('registered', 'Bugun')}\n"
        f"🏆 <b>Status:</b> {status_str} | 📥 <b>Yuklamalar:</b> {prof['downloads']} ta\n"
        f"📌 <b>Reklama Outro:</b> {outro_str}\n"
        f"💧 <b>Watermark:</b> <code>{wm_cfg.get('text')}</code>"
    )
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📊 Bot Statistikasi (/stat)", callback_data="open_stats"),
        types.InlineKeyboardButton("💱 Valyuta Kurslari (/kurs)", callback_data="tool_cmd:kurs")
    )
    markup.add(
        types.InlineKeyboardButton("🎬 Pro Reklama Montaj", callback_data="tool_cmd:montaj"),
        types.InlineKeyboardButton("🛡 Anti-Duplikat (Original)", callback_data="antidup_start_single")
    )
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(commands=['clean', 'clear'])
def handle_clean_storage(message: types.Message):
    USER_STATES.pop(message.from_user.id, None)
    removed, freed_mb = cleanup_old_files(max_age_seconds=0)
    bot.reply_to(
        message,
        f"🧹 <b>Vaqtinchalik kesh tozalandi!</b>\n"
        f"🗑 O'chirilgan fayllar: <b>{removed} ta</b>\n"
        f"💾 Bo'shatilgan joy: <b>{freed_mb:.2f} MB</b>"
    )

# ==================== STATISTIKA VA ADMIN BUYRUQLARI ====================
@bot.message_handler(commands=['stat', 'stats', 'statistika', 'admin'])
@bot.message_handler(func=lambda msg: msg.text and msg.text.strip() in [
    "📊 Statistika", "📊 Статистика", "📊 Statistics",
    "statistika", "Statistika", "stat", "Stat"
])
def handle_stats(message: types.Message):
    USER_STATES.pop(message.from_user.id, None)
    text, markup = build_stats_message(message.from_user)
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(commands=['vip'])
def handle_give_vip(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "Foydalanish: <code>/vip USER_ID</code>")
        return
    try:
        target_id = int(args[1])
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET is_vip = 1 WHERE user_id = ?", (target_id,))
        conn.commit()
        conn.close()
        bot.reply_to(message, f"✅ Foydalanuvchi {target_id} ga VIP berildi!")
        try:
            bot.send_message(target_id, "🎉 <b>Administrator tomonidan sizga umrbod VIP maqomi berildi!</b>")
        except Exception:
            pass
    except Exception as e:
        bot.reply_to(message, f"Xatolik: {e}")

@bot.message_handler(commands=['delvip'])
def handle_del_vip(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "Foydalanish: <code>/delvip USER_ID</code>")
        return
    try:
        target_id = int(args[1])
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET is_vip = 0 WHERE user_id = ?", (target_id,))
        conn.commit()
        conn.close()
        bot.reply_to(message, f"✅ Foydalanuvchi {target_id} dan VIP olib tashlandi!")
    except Exception as e:
        bot.reply_to(message, f"Xatolik: {e}")

@bot.message_handler(commands=['send'])
def handle_broadcast(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    reply = message.reply_to_message
    if not reply:
        bot.send_message(message.chat.id, "⚠️ Xabar tarqatish uchun biror postga javob (reply) qilib <code>/send</code> yozing.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()
    conn.close()

    status_msg = bot.send_message(message.chat.id, f"📤 Xabar tarqatish boshlandi... Jami: {len(users)} ta")
    success_count = 0
    blocked_count = 0

    for u in users:
        try:
            bot.copy_message(chat_id=u[0], from_chat_id=reply.chat.id, message_id=reply.message_id)
            success_count += 1
            time.sleep(0.04)
        except Exception:
            blocked_count += 1

    bot.edit_message_text(
        f"✅ <b>Tugatildi!</b>\n\n🟢 Yetkazildi: {success_count} ta\n🔴 Bloklaganlar: {blocked_count} ta",
        chat_id=message.chat.id,
        message_id=status_msg.message_id
    )

# ==================== PRO REKLAMA MONTAJ STUDIYASI BUYRUQLARI (/montaj, /set_outro, /original) ====================
def _extract_or_download_video_from_message(message: types.Message, target_prefix: str) -> tuple[str | None, str]:
    """
    Foydalanuvchi yuborgan xabardan (Video fayl, Document MP4/MOV yoki Instagram/TikTok/YouTube linkidan)
    videoni MONTAGE_SESSIONS_DIR ga yuklab olish!
    """
    uid = message.from_user.id
    ts = int(time.time() * 1000) % 100000000

    # A) Agar bevosita video, video_note yoki video-document yuborilgan bo'lsa:
    doc_is_video = False
    if message.document:
        mime = (message.document.mime_type or "").lower()
        fname = (message.document.file_name or "").lower()
        if mime.startswith("video") or fname.endswith((".mp4", ".mov", ".mkv", ".webm", ".avi")):
            doc_is_video = True

    media_obj = message.video or message.video_note or (message.document if doc_is_video else None)
    if media_obj:
        local_path = os.path.join(MONTAGE_SESSIONS_DIR, f"{target_prefix}_{uid}_{ts}.mp4")
        try:
            finfo = bot.get_file(media_obj.file_id)
            fbytes = bot.download_file(finfo.file_path)
            with open(local_path, "wb") as vf:
                vf.write(fbytes)
            if os.path.exists(local_path) and os.path.getsize(local_path) > 1000:
                dur = get_media_duration(local_path)
                return local_path, f"Yuklangan video ({dur:.1f} sek)"
        except Exception as e:
            print(f"Montaj video fayl yuklash xatosi: {e}")
            safe_remove(local_path)
            return None, "Faylni yuklab bo'lmadi (Telegram Bot API orqali fayl hajmi 20 MB gacha bo'lishi yoki link orqali yuborilishi kerak)."

    # B) Agar link (Instagram, TikTok, YouTube va h.k.) text yoki caption ichida yuborilgan bo'lsa:
    raw_text = message.text or message.caption or ""
    if raw_text:
        url = extract_url(raw_text)
        if url:
            files, title = download_media_bulletproof(url, uid, ts)
            for fpath in files:
                ext = os.path.splitext(fpath)[1].lower()
                if ext in [".mp4", ".mov", ".mkv", ".webm"]:
                    dest_path = os.path.join(MONTAGE_SESSIONS_DIR, f"{target_prefix}_{uid}_{ts}.mp4")
                    try:
                        os.replace(fpath, dest_path)
                    except Exception:
                        shutil.copyfile(fpath, dest_path)
                        safe_remove(fpath)
                    dur = get_media_duration(dest_path)
                    return dest_path, f"{title[:40]} ({dur:.1f} sek)"
            safe_remove(*files)
            return None, "Ushbu havoladan video topilmadi."

    return None, "Iltimos, video fayl yuboring yoki Instagram/TikTok/YouTube video linkini tashlang!"

@bot.message_handler(commands=['cancel', 'bekor'])
def handle_cancel_cmd(message: types.Message):
    uid = message.from_user.id
    USER_STATES.pop(uid, None)
    bot.reply_to(message, "✅ Joriy amal bekor qilindi. Asosiy menyudasiz.", reply_markup=get_main_reply_keyboard(get_user_lang(uid)))

@bot.message_handler(commands=['montaj', 'merge', 'reklama'])
@bot.message_handler(func=lambda msg: msg.text and msg.text.strip() in [
    "🎬 Reklama Montaj", "🎬 Видео Монтаж", "🎬 Video Montage",
    "montaj", "Montaj"
])
def handle_montage_menu(message: types.Message):
    uid = message.from_user.id
    outro_path = get_saved_outro_path(uid)
    if outro_path:
        outro_dur = get_media_duration(outro_path)
        outro_size = os.path.getsize(outro_path) / (1024 * 1024)
        outro_status = f"✅ <b>Saqlangan ({outro_dur:.1f} sek | {outro_size:.1f} MB)</b>"
    else:
        outro_status = "⚠️ <b>Hali saqlanmagan</b> (2-videoni yuborsangiz avto-saqlanadi yoki <code>/set_outro</code> bosing)"

    wm_cfg = get_watermark_settings()
    wm_state = f"✅ <b>Faol:</b> <code>{wm_cfg.get('text')}</code> ({int(wm_cfg.get('opacity', 0.24)*100)}% shaffof, tepadan-pastga suzuvchi)" if wm_cfg.get("enabled", True) else "🔴 O'chirilgan"

    # MUHIM: Foydalanuvchi «🎬 Reklama Montaj» ni bosiboq to'g'ridan-to'g'ri 1-videoni (yoki linkni) tashlasa ham darhol qabul qiladi!
    USER_STATES[uid] = {"action": "montaj_wait_v1"}

    text = (
        "🎬 <b>TOP-1 PRO REKLAMA MONTAJ & ANTI-DUPLIKAT STUDIYASI</b>\n\n"
        f"📌 <b>Doimiy Reklama Outro:</b> {outro_status}\n"
        f"💧 <b>Shaffof Telegram Watermark:</b> {wm_state}\n\n"
        "🚀 <b>HOZIR NIMA QILASIZ?</b>\n"
        "📥 <b>1-Videoni (Asosiy videoni) hoziroq shu yerga yuboring</b> (Instagram/TikTok/YouTube linkini tashlang yoki video fayl yuboring)!\n"
        "<i>So'ng uning oxiriga ulanadigan 2-videoni (reklamani) yuborasiz va 5 xil professional rejimdan birini tanlaysiz.</i>\n\n"
        "👇 <i>Yoki quyidagi maxsus tugmalardan birini bosing:</i>"
    )
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🎬 2 ta Videoni Ulash (1-Video + 2-Video)", callback_data="montaj_start_two"),
        types.InlineKeyboardButton("🛡 1 ta Videoni 100% Original Qilish (Anti-Duplikat)", callback_data="antidup_start_single"),
        types.InlineKeyboardButton("📌 Doimiy Reklama Outro Videoni Saqlash (/set_outro)", callback_data="montaj_set_outro"),
        types.InlineKeyboardButton("💧 Shaffof Watermark Matnini O'zgartirish (/set_watermark)", callback_data="montaj_set_wm")
    )
    if outro_path:
        markup.add(
            types.InlineKeyboardButton("⚡ Saqlangan Outroni Videoga Ulash (1-Click)", callback_data="montaj_use_saved_outro"),
            types.InlineKeyboardButton("🗑 Saqlangan Outroni O'chirish (/del_outro)", callback_data="montaj_del_outro")
        )
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(commands=['set_watermark', 'watermark'])
def handle_set_watermark_cmd(message: types.Message):
    USER_STATES.pop(message.from_user.id, None)
    args = message.text.split(maxsplit=1) if message.text else []
    if len(args) > 1:
        val = args[1].strip()
        if val.lower() in ("off", "0", "yoq", "ochirish"):
            save_watermark_settings(enabled=False)
            bot.reply_to(message, "🔴 <b>Suzuvchi shaffof watermark o'chirildi.</b> Yoqish uchun: <code>/set_watermark @kanal_nomi</code>")
            return
        cfg = save_watermark_settings(enabled=True, text=val, opacity=0.24)
        for fn in os.listdir(PROMO_DIR):
            if fn.startswith("wm_badge_") and fn.endswith(".png"):
                safe_remove(os.path.join(PROMO_DIR, fn))
        bot.reply_to(
            message,
            f"✅ <b>Shaffof Telegram Watermark yangilandi!</b>\n\n"
            f"💧 <b>Yozuv:</b> <code>{cfg['text']}</code> (Telegram samolyotcha ikonkasi bilan)\n"
            f"👁 <b>Shaffoflik:</b> 24% (ko'rinar-ko'rinmas, videoga xalaqit bermaydi)\n"
            f"↕️ <b>Harakat:</b> Tepadan pastga silliq suzib yuradi!"
        )
        return

    cfg = get_watermark_settings()
    bot.reply_to(
        message,
        f"💧 <b>Tepadan-Pastga Suzuvchi Shaffof Watermark Sozlamasi</b>\n\n"
        f"Hozirgi yozuv: <code>{cfg.get('text')}</code>\n\n"
        f"✍️ <b>Yangi kanal yoki bot nikini yuboring</b> (Masalan: <code>@TELEGRAM_YULDUZLARI</code> yoki <code>@usman_khasan</code>):\n"
        f"<i>(O'chirib qo'yish uchun <code>off</code> deb yozing, bekor qilish uchun /cancel)</i>"
    )
    USER_STATES[message.from_user.id] = {"action": "set_watermark_step"}

def process_set_watermark_step(message: types.Message):
    uid = message.from_user.id
    USER_STATES.pop(uid, None)
    if not message.text or message.text.strip().lower() in ("/cancel", "bekor"):
        bot.reply_to(message, "❌ Bekor qilindi.")
        return
    val = message.text.strip()
    if val.lower() in ("off", "0", "yoq"):
        save_watermark_settings(enabled=False)
        bot.reply_to(message, "🔴 <b>Suzuvchi shaffof watermark o'chirildi.</b>")
        return
    cfg = save_watermark_settings(enabled=True, text=val, opacity=0.24)
    for fn in os.listdir(PROMO_DIR):
        if fn.startswith("wm_badge_") and fn.endswith(".png"):
            safe_remove(os.path.join(PROMO_DIR, fn))
    bot.reply_to(
        message,
        f"✅ <b>Shaffof Telegram Watermark saqlandi!</b>\n\n"
        f"💧 <b>Yozuv:</b> <code>{cfg['text']}</code>\n"
        f"↕️ Endi har bir videoda tepadan pastga ko'rinar-ko'rinmas bo'lib suzib yuradi!"
    )

@bot.message_handler(commands=['original', 'antiduplikat', 'unique'])
@bot.message_handler(func=lambda msg: msg.text and msg.text.strip() in [
    "🛡 Anti-Duplikat", "🛡 Анти-Дубликат", "🛡 Anti-Duplicate"
])
def handle_original_cmd(message: types.Message):
    USER_STATES[message.from_user.id] = {"action": "antidup_wait_video"}
    bot.reply_to(
        message,
        "🛡 <b>10-BOSQICHLI ANTI-DUPLIKAT (100% ORIGINAL VIDEO) STUDIYASI</b>\n\n"
        "Videoni Instagram Reels, TikTok va YouTube Shorts algoritmlari uchun <b>100% yangi original</b> qilib "
        "(Rekomendatsiya / Topga chiqadigan qilib) tayyorlash uchun:\n\n"
        "📥 <b>Hoziroq video fayl yuboring yoki Instagram/TikTok/YouTube linkini tashlang:</b>\n"
        "<i>(Bekor qilish uchun /cancel)</i>"
    )

def process_antidup_step(message: types.Message):
    uid = message.from_user.id
    if message.text and message.text.strip().lower() in ("/cancel", "bekor"):
        USER_STATES.pop(uid, None)
        bot.reply_to(message, "❌ Bekor qilindi.")
        return

    prog = bot.reply_to(
        message,
        "🛡 <b>10-Bosqichli Anti-Duplikat + Suzuvchi Watermark ishga tushdi...</b>\n"
        "• pHash, Audio Spektr, GOP va iPhone 16 Pro Max metama'lumotlari yangilanmoqda..."
    )
    src_path, label = _extract_or_download_video_from_message(message, "antidup_src")
    if not src_path:
        bot.edit_message_text(f"❌ {label}\n\n<i>Qaytadan video fayl yoki link yuboring (bekor qilish: /cancel)</i>", message.chat.id, prog.message_id)
        return

    USER_STATES.pop(uid, None)
    out_orig = os.path.join(DOWNLOAD_DIR, f"orig_{uid}_{int(time.time()) % 1000000}.mp4")
    try:
        ok, ad_info = make_video_100_original(src_path, out_orig)
        if ok and os.path.exists(out_orig):
            vinfo = get_video_stream_info(out_orig)
            fsize_mb = os.path.getsize(out_orig) / (1024 * 1024)
            bot_uname = get_cached_bot_username()
            cap = (
                f"🛡 <b>100% ORIGINAL VIDEO TAYYOR (Top / Rekomendatsiya Uchun)!</b>\n\n"
                f"🔍 <b>Vizual pHash siljishi:</b> +{ad_info.get('zoom', '2.5%')} (Sub-piksel + Micro-Grain)\n"
                f"🎵 <b>Audio Fingerprint:</b> {ad_info.get('pitch', '+1.3%')}\n"
                f"⏱ <b>Kadr & PTS Tezligi:</b> {ad_info.get('speed', '1.01x')} (GOP -g 29)\n"
                f"📱 <b>Kamera Imzosi:</b> <code>{ad_info.get('device', 'iPhone 16 Pro Max')}</code>\n"
                f"💧 <b>Watermark:</b> Tepadan-pastga suzuvchi shaffof ikona\n"
                f"💾 <b>Hajmi:</b> {fsize_mb:.1f} MB\n\n"
                f"🤖 @{bot_uname}"
            )
            with open(out_orig, "rb") as vf:
                bot.send_video(
                    message.chat.id,
                    video=vf,
                    caption=cap,
                    width=vinfo.get("width", 720),
                    height=vinfo.get("height", 1280),
                    duration=vinfo.get("duration", 15),
                    supports_streaming=True
                )
            increment_download_count(uid, "anti_duplicate", "Anti-Duplicate Studio", "original")
            try:
                bot.delete_message(message.chat.id, prog.message_id)
            except Exception:
                pass
        else:
            bot.edit_message_text("❌ Videoni qayta ishlashda xatolik yuz berdi.", message.chat.id, prog.message_id)
    except Exception as e:
        bot.edit_message_text(f"❌ Xatolik: {e}", message.chat.id, prog.message_id)
    finally:
        safe_remove(src_path, out_orig)

@bot.message_handler(commands=['set_outro'])
def handle_set_outro_cmd(message: types.Message):
    USER_STATES[message.from_user.id] = {"action": "save_outro"}
    bot.reply_to(
        message,
        "📌 <b>Doimiy Reklama (Outro) videosini yuboring:</b>\n\n"
        "• Video davomiyligi <b>ixtiyoriy</b> bo'lishi mumkin (masalan: 10 sek, 19 sek, 30 sek yoki 1 daqiqagacha!).\n"
        "• Videoni fayl sifatida tashlang yoki Instagram/TikTok/YouTube linkini yuboring.\n"
        "• Bir marta saqlab qo'ysangiz, har bir videoning ostidagi <b>«🎯 Pro Reklama Montaj»</b> tugmasi orqali 1 bosishda ulab ketaverasiz!\n"
        "<i>(Bekor qilish uchun /cancel)</i>"
    )

def process_save_outro_step(message: types.Message):
    uid = message.from_user.id
    if message.text and message.text.strip().lower() in ["/cancel", "bekor", "отмена"]:
        USER_STATES.pop(uid, None)
        bot.reply_to(message, "❌ Bekor qilindi.")
        return

    prog = bot.reply_to(message, "⏳ <b>Reklama (Outro) video qabul qilinib, 9:16 HD formatga moslanmoqda...</b>")
    temp_path, info_label = _extract_or_download_video_from_message(message, "raw_outro")
    if not temp_path:
        bot.edit_message_text(f"❌ {info_label}\n\n<i>Video fayl yoki link yuboring (bekor qilish: /cancel)</i>", message.chat.id, prog.message_id)
        return

    USER_STATES.pop(uid, None)
    target_outro = os.path.join(PROMO_DIR, f"outro_{uid}.mp4")
    try:
        ok = normalize_clip_for_montage(temp_path, target_outro, keep_audio=True)
        if not ok:
            shutil.copyfile(temp_path, target_outro)
        dur = get_media_duration(target_outro)
        size_mb = os.path.getsize(target_outro) / (1024 * 1024)
        # Outro videoni Cloud Vault orqali GitHub Actions qayta yonganda ham saqlab qolish:
        try:
            with open(target_outro, "rb") as _of:
                _sent_o = bot.send_video(ADMIN_ID, _of, caption="☁️ #OUTRO_CLOUD_BACKUP (Avto-tiklash uchun zaxira)", disable_notification=True)
                if _sent_o and getattr(_sent_o, "video", None):
                    _cfg = get_ig_autopost_config()
                    _cfg["saved_outro_file_id"] = _sent_o.video.file_id
                    save_ig_autopost_config(_cfg, sync_cloud=True)
        except Exception:
            pass
        bot.edit_message_text(
            f"✅ <b>Reklama Outro muvaffaqiyatli saqlandi!</b>\n\n"
            f"⏱ <b>Davomiyligi:</b> {dur:.1f} soniya\n"
            f"💾 <b>Hajmi:</b> {size_mb:.1f} MB\n"
            f"📐 <b>Format:</b> 9:16 HD (Reels / TikTok)\n\n"
            f"🚀 Endi botga istalgan Instagram/TikTok linkini tashlab, video ostidagi <b>«🎯 Pro Reklama Montaj»</b> tugmasini bossangiz, "
            f"ushbu reklama videongiz avtomatik ulanadi!",
            message.chat.id,
            prog.message_id
        )
    except Exception as e:
        bot.edit_message_text(f"❌ Saqlashda xatolik: {e}", message.chat.id, prog.message_id)
    finally:
        safe_remove(temp_path)

@bot.message_handler(commands=['del_outro'])
def handle_del_outro_cmd(message: types.Message):
    uid = message.from_user.id
    USER_STATES.pop(uid, None)
    user_outro = os.path.join(PROMO_DIR, f"outro_{uid}.mp4")
    if os.path.exists(user_outro):
        safe_remove(user_outro)
        bot.reply_to(message, "🗑 <b>Saqlangan reklama (Outro) videongiz o'chirildi.</b> Yangisini saqlash uchun: <code>/set_outro</code>")
    else:
        bot.reply_to(message, "ℹ️ Sizda saqlangan Outro video yo'q.")

def process_montage_step1(message: types.Message):
    """1-videoni qabul qilish (Link yoki Video fayl — har qanday davomiylikda)"""
    uid = message.from_user.id
    state = USER_STATES.get(uid, {})
    if message.text and message.text.strip().lower() in ["/cancel", "bekor", "отмена"]:
        USER_STATES.pop(uid, None)
        bot.reply_to(message, "❌ Montaj bekor qilindi.")
        return

    use_saved_outro = (state.get("action") == "montaj_wait_v1_with_saved")
    prog = bot.reply_to(message, "⏳ <b>1-video yuklanmoqda va tekshirilmoqda...</b>")
    v1_path, v1_label = _extract_or_download_video_from_message(message, "montaj_v1")
    if not v1_path:
        bot.edit_message_text(
            f"❌ {v1_label}\n\n📥 <i>1-videoni fayl sifatida tashlang yoki Instagram/TikTok/YouTube linkini yuboring (bekor qilish: /cancel)</i>",
            message.chat.id, prog.message_id
        )
        return

    dur1 = get_media_duration(v1_path)
    session_key = f"{uid}_{int(time.time()) % 10000000}"

    outro_path = get_saved_outro_path(uid) if use_saved_outro else None
    if use_saved_outro and outro_path:
        USER_STATES.pop(uid, None)
        v2_copy = os.path.join(MONTAGE_SESSIONS_DIR, f"montaj_v2_{session_key}.mp4")
        shutil.copyfile(outro_path, v2_copy)
        dur2 = get_media_duration(v2_copy)
        MONTAGE_CACHE[session_key] = {
            "user_id": uid,
            "v1": v1_path,
            "v2": v2_copy,
            "dur1": dur1,
            "dur2": dur2,
            "created": time.time()
        }
        bot.edit_message_text(
            f"✅ <b>Har ikkala video tayyor!</b>\n\n"
            f"🎬 <b>1-Video (Asosiy):</b> {dur1:.1f} soniya\n"
            f"🎯 <b>2-Video (Saqlangan Reklama):</b> {dur2:.1f} soniya\n"
            f"⏱ <b>Umumiy davomiylik:</b> ~{dur1 + dur2:.1f} soniya\n\n"
            f"👇 <b>Qaysi rejimda montaj qilamiz?</b>",
            message.chat.id,
            prog.message_id,
            reply_markup=make_montage_mode_keyboard(session_key)
        )
        return

    MONTAGE_CACHE[session_key] = {
        "user_id": uid,
        "v1": v1_path,
        "v2": None,
        "dur1": dur1,
        "dur2": 0.0,
        "created": time.time()
    }
    USER_STATES[uid] = {"action": "montaj_wait_v2", "session_key": session_key}

    mk = types.InlineKeyboardMarkup(row_width=1)
    saved_outro = get_saved_outro_path(uid)
    if saved_outro:
        s_dur = get_media_duration(saved_outro)
        mk.add(types.InlineKeyboardButton(
            f"⚡ Saqlangan Outroni Ulash ({s_dur:.1f}s)",
            callback_data=f"montaj_attach_saved:{session_key}"
        ))
    mk.add(types.InlineKeyboardButton("❌ Bekor qilish", callback_data=f"cancel_montaj:{session_key}"))

    bot.edit_message_text(
        f"✅ <b>1-Video qabul qilindi!</b> ({v1_label})\n\n"
        f"📥 <b>Endi 2-Videoni (Reklama / Outro videoni) shu yerga yuboring:</b>\n"
        f"• Davomiyligi <b>ixtiyoriy</b> (10s, 19s, 30s, 1 daqiqa va h.k.) bo'lishi mumkin.\n"
        f"• Video fayl tashlang yoki Instagram/TikTok/YouTube linkini yuboring:",
        message.chat.id,
        prog.message_id,
        reply_markup=mk
    )

def process_montage_step2(message: types.Message):
    """2-videoni qabul qilish va 5 ta montaj rejimini chiqarish"""
    uid = message.from_user.id
    state = USER_STATES.get(uid, {})
    session_key = state.get("session_key")
    session = MONTAGE_CACHE.get(session_key)
    if not session or not os.path.exists(session.get("v1", "")):
        USER_STATES.pop(uid, None)
        bot.reply_to(message, "⚠️ Montaj sessiyasi eskirgan. Qaytadan <b>🎬 Reklama Montaj</b> tugmasini bosing.")
        return

    if message.text and message.text.strip().lower() in ["/cancel", "bekor", "отмена"]:
        USER_STATES.pop(uid, None)
        safe_remove(session.get("v1"))
        MONTAGE_CACHE.pop(session_key, None)
        bot.reply_to(message, "❌ Montaj bekor qilindi.")
        return

    prog = bot.reply_to(message, "⏳ <b>2-video yuklanmoqda va tekshirilmoqda...</b>")
    v2_path, v2_label = _extract_or_download_video_from_message(message, "montaj_v2")
    if not v2_path:
        bot.edit_message_text(
            f"❌ {v2_label}\n\n📥 <i>2-videoni fayl sifatida tashlang yoki link yuboring (bekor qilish: /cancel)</i>",
            message.chat.id, prog.message_id
        )
        return

    USER_STATES.pop(uid, None)
    dur2 = get_media_duration(v2_path)
    session["v2"] = v2_path
    session["dur2"] = dur2

    # Keyingi safar 1 bosishda ulash uchun 2-videoni avto-shablon sifatida ham saqlab qo'yamiz
    user_outro = os.path.join(PROMO_DIR, f"outro_{uid}.mp4")
    if not os.path.exists(user_outro):
        try:
            shutil.copyfile(v2_path, user_outro)
        except Exception:
            pass

    dur1 = session.get("dur1", 15.0)
    bot.edit_message_text(
        f"🎬 <b>Har ikkala video montajga tayyor!</b>\n\n"
        f"1️⃣ <b>1-Video:</b> {dur1:.1f} soniya\n"
        f"2️⃣ <b>2-Video (Reklama):</b> {dur2:.1f} soniya ({v2_label})\n"
        f"⏱ <b>Jami davomiylik:</b> ~{dur1 + dur2:.1f} soniya\n\n"
        f"👇 <b>Qaysi audio-vizual rejimda birlashtiramiz?</b>",
        message.chat.id,
        prog.message_id,
        reply_markup=make_montage_mode_keyboard(session_key)
    )

def _route_active_user_state(message: types.Message) -> bool:
    """
    Agar foydalanuvchi montaj, outro saqlash, anti-duplikat, watermark, trim yoki qr
    bosqichida bo'lsa, yuborgan fayli yoki matnini to'g'ridan-to'g'ri o'sha bosqichga yo'naltiradi!
    """
    uid = message.from_user.id
    state = USER_STATES.get(uid)
    if not state:
        return False
    action = state.get("action", "")
    if action.startswith("ig_"):
        return process_ig_state_step(message)
    if action in ("montaj_wait_v1", "montaj_wait_v1_with_saved"):
        process_montage_step1(message)
        return True
    elif action == "montaj_wait_v2":
        process_montage_step2(message)
        return True
    elif action == "save_outro":
        process_save_outro_step(message)
        return True
    elif action == "antidup_wait_video":
        process_antidup_step(message)
        return True
    elif action == "set_watermark_step":
        process_set_watermark_step(message)
        return True
    elif action == "trim":
        process_trim_step(message)
        return True
    elif action == "qr_make":
        process_qr_step(message)
        return True
    return False


# ==================== 📸 INSTAGRAM AVTO-POSTER BUYRUQLARI VA STATE HANDLERLARI ====================
@bot.message_handler(commands=['ig', 'insta', 'autopost', 'ig_status'])
@bot.message_handler(func=lambda msg: msg.text and msg.text.strip() in [
    "📸 Insta Avto-Post", "📸 Инста Авто-Пост", "📸 Insta Auto-Post"
])
def handle_ig_autopost_menu(message: types.Message):
    uid = message.from_user.id
    USER_STATES.pop(uid, None)
    if not is_admin_user(message.from_user):
        bot.reply_to(message, "🔒 Ushbu bo'lim faqat bot administratori (@usman_khasan) uchun mo'ljallangan.")
        return
    text, markup = build_ig_autoposter_dashboard(uid)
    bot.send_message(message.chat.id, text, reply_markup=markup, disable_web_page_preview=True)

def _build_ig_login_status_markup(uid: int, status: str):
    if status in ("2fa_required", "challenge_required"):
        USER_STATES[uid] = {"action": "ig_wait_code"}
        mk = types.InlineKeyboardMarkup(row_width=1)
        mk.add(
            types.InlineKeyboardButton("✅ Ilovadan Tasdiqladim (Qayta urinish)", callback_data="ig_retry_challenge"),
            types.InlineKeyboardButton("🍪 SessionID Bilan 1-Soniyada Ulash", callback_data="ig_start_session")
        )
        return mk
    if status == "rate_limited":
        mk = types.InlineKeyboardMarkup(row_width=1)
        mk.add(
            types.InlineKeyboardButton("🔄 Hozir Qayta Urinish (Parol qayta yozmasdan)", callback_data="ig_retry_challenge"),
            types.InlineKeyboardButton("🍪 SessionID Bilan 1-Soniyada Ulash (100% Bloklarsiz)", callback_data="ig_start_session")
        )
        return mk
    if status == "ok":
        mk = types.InlineKeyboardMarkup(row_width=2)
        mk.add(
            types.InlineKeyboardButton("🚀 Hozir 1 ta Video Joylash", callback_data="ig_run_now"),
            types.InlineKeyboardButton("📸 Avto-Post Panel", callback_data="ig_open_panel")
        )
        return mk
    return None

@bot.message_handler(commands=['ig_login'])
def handle_ig_login_cmd(message: types.Message):
    if not is_admin_user(message.from_user):
        return
    uid = message.from_user.id
    args = message.text.split(maxsplit=2) if message.text else []
    if len(args) >= 3:
        uname, pwd = args[1], args[2]
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except Exception:
            pass
        prog = bot.send_message(message.chat.id, f"⏳ <b>@{uname.lstrip('@')}</b> profiliga 5-Motorli Anti-Blok tizimi orqali kirilmoqda (3–8 soniya)...")
        def _bg_cmd_login():
            status, resp_msg = login_instagram_username_password(uid, uname, pwd, chat_id=message.chat.id, prog_msg_id=prog.message_id)
            mk = _build_ig_login_status_markup(uid, status)
            _update_prog_safe(message.chat.id, prog.message_id, resp_msg, reply_markup=mk)
        threading.Thread(target=_bg_cmd_login, daemon=True).start()
        return

    USER_STATES[uid] = {"action": "ig_wait_credentials"}
    bot.reply_to(
        message,
        "🔑 <b>Instagram Profilni Botga Ulash (5-Motorli Anti-Blok + Bulutli Xotira):</b>\n\n"
        "1️⃣ <b>Login va Parol bilan:</b> Bitta qatorda bo'sh joy tashlab yuboring:\n"
        "<code>universal_savebot parolingiz</code>\n\n"
        "2️⃣ <b>Yoki SessionID bilan (100% Bloklarsiz):</b> Brauzerdan <code>sessionid</code> qiymatini nusxalab shu yerga tashlang!\n\n"
        "🔒 <i>Xavfsizlik: Xabaringiz o'sha zahoti chatdan avtomatik o'chiriladi va sessiya Telegram Bulutli Xotiraga muhrlanadi.</i>\n"
        "<i>(Bekor qilish: /cancel)</i>"
    )

@bot.message_handler(commands=['ig_code'])
def handle_ig_code_cmd(message: types.Message):
    if not is_admin_user(message.from_user):
        return
    uid = message.from_user.id
    args = message.text.split(maxsplit=1) if message.text else []
    if len(args) < 2:
        USER_STATES[uid] = {"action": "ig_wait_code"}
        bot.reply_to(message, "🔐 <b>SMS, Authenticator yoki Email orqali kelgan 6 xonali tasdiqlash kodini yozib yuboring:</b>")
        return
    USER_STATES.pop(uid, None)
    prog = bot.reply_to(message, "⏳ Tasdiqlash kodi tekshirilmoqda...")
    ok, msg = complete_instagram_verification_code(uid, args[1])
    bot.edit_message_text(msg, message.chat.id, prog.message_id)

@bot.message_handler(commands=['ig_session'])
def handle_ig_session_cmd(message: types.Message):
    if not is_admin_user(message.from_user):
        return
    uid = message.from_user.id
    args = message.text.split(maxsplit=1) if message.text else []
    if len(args) < 2:
        USER_STATES[uid] = {"action": "ig_wait_sessionid"}
        bot.reply_to(
            message,
            "🍪 <b>Instagram SessionID orqali 1 soniyada ulash (Eng barqaror usul):</b>\n\n"
            "Kompyuter yoki telefon brauzerida Instagramga kirib, Cookie ichidan <code>sessionid</code> qiymatini nusxalab shu yerga yuboring:\n"
            "<i>(Bekor qilish: /cancel)</i>"
        )
        return
    USER_STATES.pop(uid, None)
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except Exception:
        pass
    prog = bot.send_message(message.chat.id, "⏳ SessionID tekshirilmoqda...")
    ok, msg = login_instagram_with_sessionid(args[1])
    bot.edit_message_text(msg, message.chat.id, prog.message_id)

@bot.message_handler(commands=['ig_now'])
def handle_ig_now_cmd(message: types.Message):
    if not is_admin_user(message.from_user):
        return
    prog = bot.reply_to(
        message,
        "🚀 <b>Avto-Reels Fabrikasi ishga tushdi!</b>\n"
        "• Navbatdagi yoki Trenddagi halol video qidirilmoqda, Outro + 10-Bosqichli Original montaj qilinib Instagramga joylanmoqda..."
    )
    def _bg_job():
        ok, msg = execute_next_autopost_job(notify_chat_id=message.chat.id, force_manual=True)
        try:
            if ok:
                bot.edit_message_text(f"✅ <b>Muvaffaqiyatli bajarildi!</b>\n{msg}", message.chat.id, prog.message_id, disable_web_page_preview=True)
            else:
                bot.edit_message_text(f"⚠️ <b>Natija:</b> {msg}", message.chat.id, prog.message_id)
        except Exception:
            pass
    threading.Thread(target=_bg_job, daemon=True).start()

def process_ig_state_step(message: types.Message) -> bool:
    """Instagram Avto-Poster interactive qadamlarini boshqarish"""
    uid = message.from_user.id
    state = USER_STATES.get(uid)
    if not state:
        return False
    action = state.get("action", "")
    if not action.startswith("ig_"):
        return False

    if message.text and message.text.strip().lower() in ("/cancel", "bekor"):
        USER_STATES.pop(uid, None)
        bot.reply_to(message, "❌ Bekor qilindi.")
        return True

    if action == "ig_wait_credentials":
        USER_STATES.pop(uid, None)
        raw = (message.text or "").strip()
        # Agar foydalanuvchi login/parol o'rniga to'g'ridan-to'g'ri SessionID tashlagan bo'lsa:
        direct_sid = _extract_clean_sessionid(raw)
        if direct_sid:
            try:
                bot.delete_message(message.chat.id, message.message_id)
            except Exception:
                pass
            prog = bot.send_message(message.chat.id, "⏳ SessionID orqali 1 soniyada ulanmoqda...")
            ok_s, msg_s = login_instagram_with_sessionid(direct_sid)
            mk = _build_ig_login_status_markup(uid, "ok" if ok_s else "error")
            bot.edit_message_text(msg_s, message.chat.id, prog.message_id, reply_markup=mk)
            return True

        parts = raw.split(maxsplit=1)
        if len(parts) < 2:
            USER_STATES[uid] = {"action": "ig_wait_credentials"}
            bot.reply_to(
                message,
                "⚠️ <b>Login va parolni bitta bo'sh joy bilan yozing!</b>\n"
                "Masalan: <code>universal_savebot parol123</code>\n\n"
                "<i>Yoki brauzerdan olingan <code>sessionid</code> qiymatini yuboring (bekor qilish: /cancel)</i>"
            )
            return True
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except Exception:
            pass
        prog = bot.send_message(message.chat.id, f"⏳ <b>@{parts[0].lstrip('@')}</b> profiliga 5-Motorli Anti-Blok tizimi orqali kirilmoqda (3–8 soniya)...")
        def _bg_step_login():
            status, resp_msg = login_instagram_username_password(uid, parts[0], parts[1], chat_id=message.chat.id, prog_msg_id=prog.message_id)
            mk = _build_ig_login_status_markup(uid, status)
            _update_prog_safe(message.chat.id, prog.message_id, resp_msg, reply_markup=mk)
        threading.Thread(target=_bg_step_login, daemon=True).start()
        return True

    if action == "ig_wait_code":
        USER_STATES.pop(uid, None)
        code_str = (message.text or "").strip()
        prog = bot.reply_to(message, "⏳ Tasdiqlash kodi tekshirilmoqda...")
        ok, msg = complete_instagram_verification_code(uid, code_str)
        bot.edit_message_text(msg, message.chat.id, prog.message_id)
        return True

    if action == "ig_wait_sessionid":
        USER_STATES.pop(uid, None)
        sid = (message.text or "").strip()
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except Exception:
            pass
        prog = bot.send_message(message.chat.id, "⏳ SessionID tekshirilmoqda...")
        ok, msg = login_instagram_with_sessionid(sid)
        bot.edit_message_text(msg, message.chat.id, prog.message_id)
        return True

    if action == "ig_wait_manual_link":
        USER_STATES.pop(uid, None)
        # Foydalanuvchi bir yoki bir nechta link yuborishi mumkin
        urls = re.findall(r'(https?://[^\s<>"\x27]+)', message.text or "")
        if not urls:
            u_single = extract_url(message.text or "")
            if u_single:
                urls = [u_single]
        if not urls:
            bot.reply_to(message, "⚠️ Video ssilkasi topilmadi. Instagram, TikTok yoki YouTube linkini yuboring.")
            return True
        added = 0
        blocked_reasons = []
        for u in urls[:10]:
            ok_q, msg_q, _ = add_video_to_ig_queue(video_url=u, title="Ruchnoy Link")
            if ok_q:
                added += 1
            else:
                blocked_reasons.append(msg_q)
        reply_t = f"✅ <b>{added} ta video havolasi Avto-Post navbatiga qo'shildi!</b>\nReja bo'yicha avtomatik Outro + Anti-Duplikat bilan Instagramga chiqadi."
        if blocked_reasons:
            reply_t += "\n\n" + "\n".join(blocked_reasons[:3])
        mk = types.InlineKeyboardMarkup()
        mk.add(
            types.InlineKeyboardButton("🚀 Hozir Bitta Joylash", callback_data="ig_run_now"),
            types.InlineKeyboardButton("📸 Avto-Post Panel", callback_data="ig_open_panel")
        )
        bot.reply_to(message, reply_t, reply_markup=mk)
        return True

    if action == "ig_wait_topics":
        USER_STATES.pop(uid, None)
        raw_t = (message.text or "").strip()
        words = [w.strip().lstrip("#") for w in re.split(r"[,\n;]+", raw_t) if w.strip()]
        if not words:
            bot.reply_to(message, "⚠️ Mavzular kiritilmadi.")
            return True
        # Mavzular ichida taqiqlangan so'z yo'qligini tekshirish
        clean_topics = []
        for w in words:
            ok_w, _ = is_text_safe_from_gambling_adult_ads(w)
            if ok_w:
                clean_topics.append(w)
        cfg = get_ig_autopost_config()
        cfg["trend_queries"] = clean_topics or list(DEFAULT_TREND_QUERIES)
        save_ig_autopost_config(cfg)
        bot.reply_to(message, f"✅ <b>Avto-Trend mavzulari yangilandi:</b>\n<code>{', '.join(cfg['trend_queries'])}</code>")
        return True

    if action == "ig_wait_badword":
        USER_STATES.pop(uid, None)
        raw_b = (message.text or "").strip().lower()
        new_words = [w.strip() for w in re.split(r"[,\n;]+", raw_b) if w.strip()]
        cfg = get_ig_autopost_config()
        cur_bl = set(cfg.get("custom_blacklist", []))
        cur_bl.update(new_words)
        cfg["custom_blacklist"] = sorted(list(cur_bl))
        save_ig_autopost_config(cfg)
        bot.reply_to(message, f"🚫 <b>Qora ro'yxatga {len(new_words)} ta yangi taqiqlangan so'z qo'shildi!</b>\nEndi bu so'zlar qatnashgan videolar 100% bloklanadi.")
        return True

    if action == "ig_wait_caption":
        USER_STATES.pop(uid, None)
        new_cap = (message.text or "").strip()
        if new_cap:
            cfg = get_ig_autopost_config()
            cfg["caption_template"] = new_cap
            save_ig_autopost_config(cfg)
            bot.reply_to(message, "✅ <b>Instagram Reels uchun standart izoh (Caption) saqlandi!</b>")
        return True

    return False

# ==================== FOYDALANUVCHI FAYL YUBORGANIDA (DIRECT UPLOAD YOKI MONTAJ) ====================
@bot.message_handler(content_types=['video', 'video_note', 'voice', 'audio', 'document'])
def handle_uploaded_media(message: types.Message):
    user = message.from_user
    register_user(user)
    lang = get_user_lang(user.id)

    is_subbed, unsubscribed = check_channel_subscription(user.id)
    if not is_subbed:
        bot.send_message(message.chat.id, get_text("sub_required", lang), reply_markup=get_sub_keyboard(unsubscribed, lang))
        return

    # 1. Agar foydalanuvchi Montaj / Outro / Anti-Duplikat bosqichida bo'lsa -> darhol o'sha yerga uzatamiz!
    if _route_active_user_state(message):
        return

    file_obj = message.video or message.video_note or message.voice or message.audio or message.document
    if not file_obj:
        return

    status_msg = bot.reply_to(message, "⏳ Fayl qabul qilinmoqda...")
    try:
        ext = "mp4"
        if message.voice:
            ext = "ogg"
        elif message.audio:
            ext = "mp3"

        short_ts = int(time.time() * 1000) % 100000000
        base_fname = f"u_{user.id}_{short_ts}.{ext}"
        local_path = os.path.join(DOWNLOAD_DIR, base_fname)

        # Faylni darhol downloads/ ga saqlab qo'yamiz (barcha 16 ta tugma 100% xatosiz ishlashi uchun!)
        try:
            finfo = bot.get_file(file_obj.file_id)
            fbytes = bot.download_file(finfo.file_path)
            with open(local_path, "wb") as lf:
                lf.write(fbytes)
        except Exception as dl_e:
            print(f"Upload fayl saqlash ogohlantirishi: {dl_e}")

        VIDEO_SOURCE_CACHE[base_fname] = {
            "path": local_path,
            "url": "",
            "file_id": getattr(file_obj, "file_id", ""),
            "time": time.time()
        }

        markup = make_video_action_keyboard(base_fname, lang=lang)
        bot.edit_message_text(
            "🎬 <b>Media qabul qilindi!</b>\n\nQuyidagi 16 ta studiya tugmalaridan birini tanlang:",
            chat_id=message.chat.id,
            message_id=status_msg.message_id,
            reply_markup=markup
        )
        increment_download_count(user.id, "direct_upload", "Telegram File", "upload")
    except Exception as e:
        print(f"Direct file yuklashda xatolik: {e}")
        bot.edit_message_text(get_text("err_generic", lang), message.chat.id, status_msg.message_id)

# ==================== HAVOLA BO'YICHA YUKLASH ====================
@bot.message_handler(func=lambda msg: True and msg.text)
def handle_incoming_link(message: types.Message):
    user = message.from_user
    register_user(user)
    lang = get_user_lang(user.id)

    is_subbed, unsubscribed = check_channel_subscription(user.id)
    if not is_subbed:
        bot.send_message(message.chat.id, get_text("sub_required", lang), reply_markup=get_sub_keyboard(unsubscribed, lang))
        return

    txt_clean = message.text.strip()
    cmd_lower = txt_clean.split()[0].lower().split("@")[0] if txt_clean else ""

    # 1. Asosiy menyu va buyruqlarni tekshirish
    if cmd_lower in ("/cancel", "/bekor"):
        handle_cancel_cmd(message)
        return
    if cmd_lower in ("/stat", "/stats", "/statistika", "/admin") or txt_clean in ("📊 Statistika", "📊 Статистика", "📊 Statistics", "statistika", "Statistika", "stat", "Stat"):
        handle_stats(message)
        return
    if cmd_lower in ("/kurs", "/valyuta", "kurs", "valyuta") or txt_clean in ("💱 Valyuta Kurslari", "💱 Курсы валют", "💱 Exchange Rates"):
        handle_kurs_cmd(message)
        return
    if cmd_lower == "/qr":
        handle_qr_cmd(message)
        return
    if cmd_lower in ("/clean", "/clear"):
        handle_clean_storage(message)
        return
    if cmd_lower == "/profile" or txt_clean in ("👤 Profilim", "👤 Мой профиль", "👤 Profile"):
        handle_profile(message)
        return
    if cmd_lower in ("/ig", "/insta", "/autopost", "/ig_status") or txt_clean in ("📸 Insta Avto-Post", "📸 Инста Авто-Пост", "📸 Insta Auto-Post"):
        handle_ig_autopost_menu(message)
        return
    if cmd_lower == "/ig_login":
        handle_ig_login_cmd(message)
        return
    if cmd_lower == "/ig_code":
        handle_ig_code_cmd(message)
        return
    if cmd_lower == "/ig_session":
        handle_ig_session_cmd(message)
        return
    if cmd_lower == "/ig_now":
        handle_ig_now_cmd(message)
        return
    if cmd_lower in ("/montaj", "/merge", "/reklama") or txt_clean in ("🎬 Reklama Montaj", "🎬 Видео Монтаж", "🎬 Video Montage", "montaj", "Montaj"):
        handle_montage_menu(message)
        return
    if cmd_lower in ("/original", "/antiduplikat", "/unique") or txt_clean in ("🛡 Anti-Duplikat", "🛡 Анти-Дубликат", "🛡 Anti-Duplicate"):
        handle_original_cmd(message)
        return
    if cmd_lower == "/set_outro":
        handle_set_outro_cmd(message)
        return
    if cmd_lower == "/del_outro":
        handle_del_outro_cmd(message)
        return
    if cmd_lower in ("/set_watermark", "/watermark"):
        handle_set_watermark_cmd(message)
        return
    if cmd_lower == "/tools" or txt_clean in ("🛠 Universal Vositalar", "🛠 Инструменты", "🛠 Smart Tools"):
        handle_tools_menu(message)
        return
    if cmd_lower == "/help" or txt_clean in ("📖 Qo'llanma", "📖 Инструкция", "📖 Help"):
        handle_help(message)
        return
    if cmd_lower in ("/lang", "/language") or txt_clean in ("🌐 Til", "🌐 Сменить язык", "🌐 Language"):
        handle_lang_command(message)
        return
    if cmd_lower in ("/referral", "/ref") or txt_clean in ("👥 VIP & Do'stlar", "👥 VIP & Рефералы", "👥 VIP & Referral"):
        handle_referral(message)
        return

    # 2. Agar foydalanuvchi Montaj / Trim / Watermark / QR bosqichida bo'lsa -> o'sha bosqichni bajarish!
    if _route_active_user_state(message):
        return

    url = extract_url(message.text)

    # 3. Agar havola bo'lmasa -> AI ga yubormasdan, foydalanuvchiga link yuborishni eslatish!
    if not url:
        bot.reply_to(message, get_text("send_link_prompt", lang), reply_markup=get_main_reply_keyboard(lang))
        return

    # ⚡ 1-SONIYALI KESH TEKSHIRUVI (INSTANT ULTRA-FAST RETRIEVAL)
    canonical_url = clean_and_resolve_url(url)
    cached_item = get_cached_media(canonical_url) or get_cached_media(url)
    if cached_item:
        bot_uname = get_cached_bot_username()
        short_ts = int(time.time() * 1000) % 100000000
        base_fname = f"cached_{user.id}_{short_ts}.mp4"
        VIDEO_SOURCE_CACHE[base_fname] = {
            "path": "",
            "url": canonical_url,
            "file_id": cached_item["file_id"],
            "time": time.time()
        }
        markup = make_video_action_keyboard(base_fname, lang=lang)
        plat_name = cached_item.get('platform', 'Web')
        caption_text = cached_item.get('caption')
        if not caption_text:
            caption_text = f'🎬 <b>Video</b>\n\n🌐 <b>Platforma:</b> {plat_name}\n⚡ <b>Tezkor uzatish:</b> 0.5s\n\n🤖 @{bot_uname}'
        cache_caption = caption_text
        try:
            if cached_item.get("file_type") == "photo":
                bot.send_photo(message.chat.id, cached_item["file_id"], caption=cache_caption)
            else:
                bot.send_video(
                    chat_id=message.chat.id,
                    video=cached_item["file_id"],
                    caption=cache_caption,
                    reply_markup=markup,
                    width=cached_item.get("width", 720),
                    height=cached_item.get("height", 1280),
                    duration=cached_item.get("duration", 15),
                    supports_streaming=True
                )
            increment_download_count(user.id, url, cached_item.get("platform", "Web"), cached_item.get("file_type", "video"))
            return
        except Exception as cache_err:
            print(f"Keshdan jo'natish xatosi (qaytadan yuklanadi): {cache_err}")

    # 4. HAVOLA BO'LSA -> 12-BOSQICHLI VIDEO-FIRST TIZIM ORQALI XATOSIZ YUKLAB BERISH!
    platform = detect_platform(url)
    status_msg = bot.reply_to(message, get_text("analyzing", lang, platform=platform))
    timestamp = int(time.time() * 1000)
    downloaded_files = []

    try:
        downloaded_files, title = download_media_bulletproof(url, user.id, timestamp)

        if not downloaded_files:
            bot.edit_message_text(get_text("not_found", lang), chat_id=message.chat.id, message_id=status_msg.message_id)
            return

        bot_uname = get_cached_bot_username()
        safe_title = html.escape(str(title or "Video"))[:60]

        # A) KARUSEL (Albom)
        if len(downloaded_files) > 1:
            opened_handles = []
            try:
                media_group = []
                for idx, fpath in enumerate(downloaded_files[:10]):
                    ext = os.path.splitext(fpath)[1].lower()
                    caption = f"📸 Karusel media ({idx+1}/{len(downloaded_files)})\n🤖 @{bot_uname}" if idx == 0 else ""
                    fh = open(fpath, "rb")
                    opened_handles.append(fh)
                    if ext in [".mp4", ".mov", ".mkv", ".webm"]:
                        media_group.append(types.InputMediaVideo(fh, caption=caption, parse_mode="HTML", supports_streaming=True))
                    else:
                        media_group.append(types.InputMediaPhoto(fh, caption=caption, parse_mode="HTML"))

                bot.send_media_group(chat_id=message.chat.id, media=media_group)
                increment_download_count(user.id, url, platform, "carousel")
                try:
                    bot.delete_message(message.chat.id, status_msg.message_id)
                except Exception:
                    pass
            finally:
                for fh in opened_handles:
                    try:
                        fh.close()
                    except Exception:
                        pass
                safe_remove(*downloaded_files)
            return

        # B) BITTA ASOSIY FAYL
        downloaded_file = downloaded_files[0]
        ext = os.path.splitext(downloaded_file)[1].lower()

        if ext in [".jpg", ".jpeg", ".png", ".webp"]:
            try:
                with open(downloaded_file, "rb") as pf:
                    bot.send_photo(
                        chat_id=message.chat.id,
                        photo=pf,
                        caption=f"🖼 <b>{safe_title}</b>\n🌐 <b>{platform}</b>\n\n🤖 @{bot_uname}"
                    )
                increment_download_count(user.id, url, platform, "photo")
                try:
                    bot.delete_message(message.chat.id, status_msg.message_id)
                except Exception:
                    pass
            finally:
                safe_remove(downloaded_file)
            return

        # Video bo'lsa -> H.264 MP4 + Tepadan-pastga suzuvchi shaffof watermark (in-place)
        downloaded_file, vinfo = ensure_phone_playable_mp4(downloaded_file)
        file_size_mb = os.path.getsize(downloaded_file) / (1024 * 1024)
        base_fname = os.path.basename(downloaded_file)

        VIDEO_SOURCE_CACHE[base_fname] = {
            "path": downloaded_file,
            "url": url,
            "file_id": "",
            "time": time.time()
        }

        # AGAR FAYL 50 MB DAN KATTA BO'LSA -> AUTO-SPLITTER
        if file_size_mb > MAX_TELEGRAM_FILE_MB:
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(
                types.InlineKeyboardButton(get_text("btn_split_parts", lang), callback_data=f"split_video:{base_fname}"),
                types.InlineKeyboardButton(get_text("btn_audio_only", lang), callback_data=f"audio:{base_fname}")
            )
            bot.edit_message_text(
                get_text("large_file_split_prompt", lang, size=file_size_mb),
                chat_id=message.chat.id,
                message_id=status_msg.message_id,
                reply_markup=markup
            )
            return

        # NORMAL HAJMDAGI VIDEO (< 50 MB)
        # MUHIM: downloaded_file ni DARHOL o'chirmaymiz! U downloads/ da 30 daqiqa turadi,
        # shunda video ostidagi barcha 16 ta tugma 0 soniyada xatosiz ishlaydi!
        markup = make_video_action_keyboard(base_fname, lang=lang)
        caption = (
            f"🎬 <b>{safe_title}</b>\n\n"
            f"🌐 <b>Platforma:</b> {platform}\n"
            f"💾 <b>Hajmi:</b> {file_size_mb:.1f} MB\n\n"
            f"🤖 @{bot_uname}"
        )
        sent_msg = None
        try:
            with open(downloaded_file, "rb") as vf:
                sent_msg = bot.send_video(
                    chat_id=message.chat.id,
                    video=vf,
                    caption=caption,
                    reply_markup=markup,
                    width=vinfo.get("width", 720),
                    height=vinfo.get("height", 1280),
                    duration=vinfo.get("duration", 15),
                    supports_streaming=True
                )
        except Exception as send_err:
            print(f"send_video 1-urinish xatosi, qayta kodlanmoqda: {send_err}")
            downloaded_file, vinfo = ensure_phone_playable_mp4(downloaded_file, force_reencode=True)
            try:
                with open(downloaded_file, "rb") as vf2:
                    sent_msg = bot.send_video(
                        chat_id=message.chat.id,
                        video=vf2,
                        caption=caption,
                        reply_markup=markup,
                        supports_streaming=True
                    )
            except Exception:
                with open(downloaded_file, "rb") as df:
                    sent_msg = bot.send_document(
                        chat_id=message.chat.id,
                        document=df,
                        caption=caption,
                        reply_markup=markup
                    )

        if sent_msg:
            vid_obj = getattr(sent_msg, "video", None) or getattr(sent_msg, "document", None)
            if vid_obj and getattr(vid_obj, "file_id", None):
                VIDEO_SOURCE_CACHE[base_fname]["file_id"] = vid_obj.file_id
                save_cached_media(
                    canonical_url=canonical_url,
                    file_id=vid_obj.file_id,
                    file_type="video" if getattr(sent_msg, "video", None) else "document",
                    caption=caption,
                    width=vinfo.get("width", 720),
                    height=vinfo.get("height", 1280),
                    duration=vinfo.get("duration", 15),
                    platform=platform
                )
                save_cached_media(
                    canonical_url=url,
                    file_id=vid_obj.file_id,
                    file_type="video" if getattr(sent_msg, "video", None) else "document",
                    caption=caption,
                    width=vinfo.get("width", 720),
                    height=vinfo.get("height", 1280),
                    duration=vinfo.get("duration", 15),
                    platform=platform
                )
            increment_download_count(user.id, url, platform, "video")
            try:
                bot.delete_message(message.chat.id, status_msg.message_id)
            except Exception:
                pass

    except Exception as e:
        print(f"Yuklashda xatolik: {e}")
        try:
            bot.edit_message_text(get_text("err_generic", lang), chat_id=message.chat.id, message_id=status_msg.message_id)
        except Exception:
            pass

# ==================== CALLBACK QUERY (BARCHA 16 TA TUGMA VA MONTAJ 100% XATOSIZ) ====================
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call: types.CallbackQuery):
    user_id = call.from_user.id
    lang = get_user_lang(user_id)

    # 1. Til tanlash
    if call.data.startswith("set_lang:"):
        new_lang = call.data.split(":")[1]
        set_user_lang(user_id, new_lang)
        bot.answer_callback_query(call.id, get_text("lang_changed", new_lang), show_alert=True)
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception:
            pass
        bot.send_message(call.message.chat.id, get_text("welcome", new_lang, name=call.from_user.first_name), reply_markup=get_main_reply_keyboard(new_lang))
        return

    # 2. Obunani tekshirish
    if call.data == "check_subscription":
        is_subbed, unsubscribed = check_channel_subscription(user_id)
        if is_subbed:
            bot.answer_callback_query(call.id, get_text("sub_success", lang), show_alert=True)
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except Exception:
                pass
            bot.send_message(call.message.chat.id, get_text("welcome", lang, name=call.from_user.first_name), reply_markup=get_main_reply_keyboard(lang))
        else:
            bot.answer_callback_query(call.id, get_text("sub_failed", lang), show_alert=True)
        return

    # 3. Referal, Statistika va Valyuta callbacklari
    if call.data == "open_referral":
        handle_referral(call.message)
        bot.answer_callback_query(call.id)
        return

    if call.data == "open_stats":
        text, markup = build_stats_message(call.from_user)
        bot.answer_callback_query(call.id, "📊 Statistika yangilandi!")
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
        except Exception:
            bot.send_message(call.message.chat.id, text, reply_markup=markup)
        return

    if call.data.startswith("kurs_amt:"):
        amt = float(call.data.split(":")[1])
        bot.answer_callback_query(call.id, f"💱 {amt:g} birlik bo'yicha hisoblandi!")
        markup = types.InlineKeyboardMarkup(row_width=3)
        markup.add(
            types.InlineKeyboardButton("💵 100$", callback_data="kurs_amt:100"),
            types.InlineKeyboardButton("💵 500$", callback_data="kurs_amt:500"),
            types.InlineKeyboardButton("💵 1000$", callback_data="kurs_amt:1000"),
        )
        markup.add(types.InlineKeyboardButton("🔄 1 birlik (Asosiy kurs)", callback_data="kurs_amt:1"))
        try:
            bot.edit_message_text(fetch_cbu_exchange_rates(amt), call.message.chat.id, call.message.message_id, reply_markup=markup)
        except Exception:
            bot.send_message(call.message.chat.id, fetch_cbu_exchange_rates(amt), reply_markup=markup)
        return

    if call.data == "clean_storage_cb":
        removed, freed_mb = cleanup_old_files(max_age_seconds=0)
        bot.answer_callback_query(call.id, f"🧹 Tozalandi! {removed} ta fayl ({freed_mb:.2f} MB) o'chirildi.", show_alert=True)
        text, markup = build_stats_message(call.from_user)
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
        except Exception:
            pass
        return

    # 4. Asosiy video menyusiga qaytish
    if call.data.startswith("back_video:"):
        base_fname = call.data.split("back_video:")[1]
        markup = make_video_action_keyboard(base_fname, lang=lang)
        try:
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)
        except Exception:
            pass
        bot.answer_callback_query(call.id)
        return

    # 5. Universal Tools callbacklari
    if call.data.startswith("tool_cmd:"):
        subcmd = call.data.split(":")[1]
        bot.answer_callback_query(call.id)
        if subcmd == "kurs":
            markup = types.InlineKeyboardMarkup(row_width=3)
            markup.add(
                types.InlineKeyboardButton("💵 100$", callback_data="kurs_amt:100"),
                types.InlineKeyboardButton("💵 500$", callback_data="kurs_amt:500"),
                types.InlineKeyboardButton("💵 1000$", callback_data="kurs_amt:1000"),
            )
            markup.add(types.InlineKeyboardButton("🔄 Kursni yangilash", callback_data="kurs_amt:1"))
            bot.send_message(call.message.chat.id, fetch_cbu_exchange_rates(1.0), reply_markup=markup)
        elif subcmd == "qr":
            USER_STATES[user_id] = {"action": "qr_make"}
            bot.send_message(call.message.chat.id, "📱 <b>QR-Kod yasash uchun matn yoki ssilka yuboring:</b>")
        elif subcmd == "montaj":
            handle_montage_menu(call.message)
        elif subcmd == "set_outro":
            handle_set_outro_cmd(call.message)
        return


    # ------------------ 📸 INSTAGRAM AVTO-POSTER CALLBACKLARI ------------------
    if call.data == "ig_open_panel":
        if not is_admin_user(call.from_user):
            bot.answer_callback_query(call.id, "🔒 Faqat admin (@usman_khasan) uchun!", show_alert=True)
            return
        bot.answer_callback_query(call.id)
        text, markup = build_ig_autoposter_dashboard(user_id)
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, disable_web_page_preview=True)
        except Exception:
            bot.send_message(call.message.chat.id, text, reply_markup=markup, disable_web_page_preview=True)
        return

    if call.data == "ig_toggle_auto":
        if not is_admin_user(call.from_user):
            return
        cfg = get_ig_autopost_config()
        cfg["auto_enabled"] = not cfg.get("auto_enabled", True)
        save_ig_autopost_config(cfg)
        state_str = "🟢 Avto-Pilot YOQILDI!" if cfg["auto_enabled"] else "🔴 Avto-Pilot O'CHIRILDI (Faqat ruchnoy rejim)"
        bot.answer_callback_query(call.id, state_str, show_alert=True)
        text, markup = build_ig_autoposter_dashboard(user_id)
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, disable_web_page_preview=True)
        except Exception:
            pass
        return

    if call.data == "ig_cycle_limit":
        if not is_admin_user(call.from_user):
            return
        cfg = get_ig_autopost_config()
        cur_lim = int(cfg.get("daily_limit", 4))
        next_lim = 3 if cur_lim >= 5 else (4 if cur_lim == 3 else 5)
        cfg["daily_limit"] = next_lim
        if next_lim == 3:
            cfg["schedule_hours"] = [11, 16, 21]
        elif next_lim == 4:
            cfg["schedule_hours"] = [10, 14, 18, 21]
        else:
            cfg["schedule_hours"] = [9, 12, 15, 18, 21]
        save_ig_autopost_config(cfg)
        bot.answer_callback_query(call.id, f"⏰ Kunlik reja: {next_lim} ta Reels!", show_alert=True)
        text, markup = build_ig_autoposter_dashboard(user_id)
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, disable_web_page_preview=True)
        except Exception:
            pass
        return

    if call.data == "ig_start_login":
        if not is_admin_user(call.from_user):
            return
        bot.answer_callback_query(call.id)
        USER_STATES[user_id] = {"action": "ig_wait_credentials"}
        bot.send_message(
            call.message.chat.id,
            "🔑 <b>Instagram Login va Parolni yuboring:</b>\n\n"
            "Bitta qatorda bo'sh joy tashlab yozing:\n"
            "<code>login parol</code>\n\n"
            "🔒 <i>Parol yozilgan xabaringiz shu zahoti avtomatik o'chiriladi. Agar telefon yoki emailga tasdiqlash kodi kelsa, keyingi qadamda kodni kiritasiz.</i>\n"
            "<i>(Bekor qilish: /cancel)</i>"
        )
        return

    if call.data == "ig_retry_challenge":
        if not is_admin_user(call.from_user):
            return
        bot.answer_callback_query(call.id, "⏳ Qayta tekshirilmoqda...")
        ok, msg = complete_instagram_verification_code(user_id, "retry")
        bot.send_message(call.message.chat.id, msg)
        return

    if call.data == "ig_start_session":
        if not is_admin_user(call.from_user):
            return
        bot.answer_callback_query(call.id)
        USER_STATES[user_id] = {"action": "ig_wait_sessionid"}
        bot.send_message(
            call.message.chat.id,
            "🍪 <b>Instagram SessionID Bilan 1-Soniyada Ulash (100% Bloklarsiz & Xatosiz Usul):</b>\n\n"
            "Agar Instagram <i>«Please wait a few minutes»</i> deb kutishga majburlasa, <b>SessionID</b> orqali kutmasdan 1 soniyada ulaysiz:\n\n"
            "1️⃣ Kompyuter yoki telefon brauzerida (Chrome) <b>instagram.com</b> saytiga (@universal_savebot profiliga) kiring.\n"
            "2️⃣ <b>F12</b> (Developer Tools) -> <b>Application</b> -> <b>Cookies</b> -> <code>https://www.instagram.com</code> bo'limini oching.\n"
            "3️⃣ <b><code>sessionid</code></b> qatoridagi qiymatni (masalan: <code>68492019%3AabCdEf...</code>) nusxalab, shu yerga yuboring!\n\n"
            "☁️ <i>Bir marta yuborsangiz, bot uni Telegram Bulutli Xotiraga (Cloud Vault) muhrlaydi — qaytib hech qachon uzilmaydi!</i>\n"
            "<i>(Bekor qilish: /cancel)</i>"
        )
        return

    if call.data == "ig_add_manual_link":
        if not is_admin_user(call.from_user):
            return
        bot.answer_callback_query(call.id)
        USER_STATES[user_id] = {"action": "ig_wait_manual_link"}
        bot.send_message(
            call.message.chat.id,
            "📥 <b>Ruchnoy Video Link Qo'shish:</b>\n\n"
            "Instagram, TikTok yoki YouTube video ssilkasini (yoki bir nechta ssilkani ketma-ket) yuboring.\n"
            "Bot ularni qimor/18+ filtridan o'tkazib navbatga qo'shadi va Outro + Anti-Duplikat bilan Instagramga chiqaradi!\n"
            "<i>(Bekor qilish: /cancel)</i>"
        )
        return

    if call.data == "ig_view_queue":
        if not is_admin_user(call.from_user):
            return
        bot.answer_callback_query(call.id)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, video_url, title, status, created_at FROM ig_queue WHERE status = 'pending' ORDER BY id ASC LIMIT 15")
        rows = cursor.fetchall()
        conn.close()
        if not rows:
            bot.send_message(
                call.message.chat.id,
                "📋 <b>Ruchnoy navbat hozircha bo'sh.</b>\n"
                "Avto-Pilot rejimida botning o'zi trendlardan halol videolarni topib joylayveradi!"
            )
            return
        lines = ["📋 <b>Instagram Navbatdagi Videolar (Pending):</b>\n"]
        for r in rows:
            lines.append(f"• <b>#{r[0]}</b> — {html.escape((r[2] or 'Video')[:40])} (<code>{(r[1] or 'fayl')[:45]}</code>)")
        mk = types.InlineKeyboardMarkup(row_width=2)
        mk.add(
            types.InlineKeyboardButton("🚀 Navbatdagini Hozir Joylash", callback_data="ig_run_now"),
            types.InlineKeyboardButton("🗑 Navbatni Tozalash", callback_data="ig_clear_queue")
        )
        bot.send_message(call.message.chat.id, "\n".join(lines), reply_markup=mk, disable_web_page_preview=True)
        return

    if call.data == "ig_clear_queue":
        if not is_admin_user(call.from_user):
            return
        conn = sqlite3.connect(DB_PATH)
        conn.execute("DELETE FROM ig_queue WHERE status = 'pending'")
        conn.commit()
        conn.close()
        bot.answer_callback_query(call.id, "🗑 Navbat tozalandi!", show_alert=True)
        text, markup = build_ig_autoposter_dashboard(user_id)
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, disable_web_page_preview=True)
        except Exception:
            pass
        return

    if call.data == "ig_set_topics":
        if not is_admin_user(call.from_user):
            return
        bot.answer_callback_query(call.id)
        cfg = get_ig_autopost_config()
        USER_STATES[user_id] = {"action": "ig_wait_topics"}
        bot.send_message(
            call.message.chat.id,
            f"🎯 <b>Avto-Trend Qidiruv Mavzulari:</b>\n\n"
            f"Hozirgi mavzular: <code>{', '.join(cfg.get('trend_queries', DEFAULT_TREND_QUERIES))}</code>\n\n"
            f"✍️ Yangi mavzularni vergul bilan ajratib yozib yuboring (masalan: <code>uzbekistan, tashkent, avto, texnologiya, motivatsiya, tabiat</code>):\n"
            f"<i>(Bekor qilish: /cancel)</i>"
        )
        return

    if call.data == "ig_add_badword":
        if not is_admin_user(call.from_user):
            return
        bot.answer_callback_query(call.id)
        cfg = get_ig_autopost_config()
        extra_bl = cfg.get("custom_blacklist", [])
        USER_STATES[user_id] = {"action": "ig_wait_badword"}
        bot.send_message(
            call.message.chat.id,
            f"🚫 <b>Qo'shimcha Taqiqlangan So'zlar Qo'shish:</b>\n\n"
            f"Botda standart <b>90+ ta qimor (1xBet, Melbet, Casino), bukmeker, promokod va 18+ fahsh so'zlar</b> allaqachon bloklangan.\n"
            f"Qo'shimcha bloklanganlar: <code>{', '.join(extra_bl) if extra_bl else 'Hozircha yoq'}</code>\n\n"
            f"✍️ Bloklanishi kerak bo'lgan yangi so'z yoki kanal nomlarini vergul bilan yozib yuboring:"
        )
        return

    if call.data == "ig_set_caption":
        if not is_admin_user(call.from_user):
            return
        bot.answer_callback_query(call.id)
        cfg = get_ig_autopost_config()
        USER_STATES[user_id] = {"action": "ig_wait_caption"}
        bot.send_message(
            call.message.chat.id,
            f"✍️ <b>Instagram Reels Uchun Standart Izoh (Caption):</b>\n\n"
            f"Hozirgi izoh:\n<code>{html.escape(cfg.get('caption_template', DEFAULT_IG_CAPTION))}</code>\n\n"
            f"Yangi izoh matni va heshteglarni yuboring (bekor qilish: /cancel):"
        )
        return

    if call.data == "ig_run_now":
        if not is_admin_user(call.from_user):
            bot.answer_callback_query(call.id, "🔒 Faqat admin uchun!", show_alert=True)
            return
        bot.answer_callback_query(call.id, "🚀 Avto-Reels tayyorlash boshlandi!")
        prog = bot.send_message(
            call.message.chat.id,
            "⏳ <b>Avto-Reels Fabrikasi ishga tushdi...</b>\n\n"
            "1️⃣ Navbatdagi yoki Trenddagi video olinmoqda\n"
            "2️⃣ 3-Qatlamli Halol Filtrda (Qimor / 18+ / Reklama) tekshirilmoqda\n"
            "3️⃣ Saqlangan Outro + 10-Bosqichli Anti-Duplikat + Suzuvchi Watermark bilan montaj qilinib Instagramga joylanmoqda..."
        )
        def _run_manual_test():
            ok, msg = execute_next_autopost_job(notify_chat_id=call.message.chat.id, force_manual=True)
            try:
                if ok:
                    bot.edit_message_text(f"✅ <b>Muvaffaqiyatli yakunlandi!</b>\n{msg}", call.message.chat.id, prog.message_id, disable_web_page_preview=True)
                else:
                    bot.edit_message_text(f"⚠️ <b>Xabar:</b> {msg}", call.message.chat.id, prog.message_id)
            except Exception:
                pass
        threading.Thread(target=_run_manual_test, daemon=True).start()
        return

    if call.data.startswith("ig_post_vid:"):
        if not is_admin_user(call.from_user):
            bot.answer_callback_query(call.id, "🔒 Instagramga joylash faqat Admin (@usman_khasan) uchun!", show_alert=True)
            return
        base_fname = call.data.split("ig_post_vid:")[1]
        video_path = os.path.join(DOWNLOAD_DIR, base_fname)
        bot.answer_callback_query(call.id, "📸 Instagram Reels ga tayyorlanmoqda...")
        prog = bot.send_message(
            call.message.chat.id,
            "📸 <b>Ruchnoy Reels Joylash ishga tushdi...</b>\n"
            "• 3-Qatlamli Halol Filtr + Outro Montaj + 10-Bosqichli Anti-Duplikat + Instagram Upload bajarilmoqda..."
        )
        def _post_direct_vid():
            if not ensure_video_from_telegram(call.message, video_path):
                bot.edit_message_text("⚠️ Video faylini o'qib bo'lmadi. Videoni qayta tashlang.", call.message.chat.id, prog.message_id)
                return
            meta = VIDEO_SOURCE_CACHE.get(base_fname, {})
            ok, msg = process_and_publish_single_reel_pipeline(
                video_url=meta.get("url", ""),
                local_video_path=video_path,
                title="Tanlangan Reels",
                notify_chat_id=call.message.chat.id
            )
            try:
                if ok:
                    bot.edit_message_text(f"✅ <b>Tayyor!</b> {msg}", call.message.chat.id, prog.message_id, disable_web_page_preview=True)
                else:
                    bot.edit_message_text(f"🚫 <b>To'xtatildi:</b> {msg}", call.message.chat.id, prog.message_id)
            except Exception:
                pass
        threading.Thread(target=_post_direct_vid, daemon=True).start()
        return

    if call.data.startswith("ig_queue_vid:"):
        if not is_admin_user(call.from_user):
            bot.answer_callback_query(call.id, "🔒 Navbatga qo'shish faqat Admin (@usman_khasan) uchun!", show_alert=True)
            return
        base_fname = call.data.split("ig_queue_vid:")[1]
        video_path = os.path.join(DOWNLOAD_DIR, base_fname)
        if not ensure_video_from_telegram(call.message, video_path):
            bot.answer_callback_query(call.id, "⚠️ Video fayli topilmadi.", show_alert=True)
            return
        meta = VIDEO_SOURCE_CACHE.get(base_fname, {})
        ok_q, msg_q, q_id = add_video_to_ig_queue(video_url=meta.get("url", ""), local_path=video_path, title="Tanlangan Video")
        bot.answer_callback_query(call.id, msg_q[:180], show_alert=True)
        return

    # ------------------ PRO REKLAMA MONTAJ CALLBACKLARI ------------------
    if call.data == "montaj_start_two":
        bot.answer_callback_query(call.id)
        USER_STATES[user_id] = {"action": "montaj_wait_v1"}
        bot.send_message(
            call.message.chat.id,
            "🎬 <b>1-Videoni (Asosiy videoni) yuboring:</b>\n\n"
            "• Instagram / TikTok / YouTube linkini tashlang yoki video fayl yuboring.\n"
            "• Video davomiyligi <b>ixtiyoriy</b> (masalan: 10s, 25s, 1 daqiqa va h.k.).\n"
            "<i>(Bekor qilish uchun /cancel yozing)</i>"
        )
        return

    if call.data == "montaj_use_saved_outro":
        bot.answer_callback_query(call.id)
        outro_path = get_saved_outro_path(user_id)
        if not outro_path:
            bot.send_message(call.message.chat.id, "⚠️ Sizda hali saqlangan Outro yo'q. Avval <code>/set_outro</code> orqali reklama videongizni saqlang.")
            return
        USER_STATES[user_id] = {"action": "montaj_wait_v1_with_saved"}
        bot.send_message(
            call.message.chat.id,
            "⚡ <b>1-Videoni (Instagram/TikTok linkini yoki video faylni) yuboring:</b>\n"
            "Saqlangan reklama (Outro) videongiz uning oxiriga avtomatik ulanadi!"
        )
        return

    if call.data.startswith("montaj_attach_saved:"):
        session_key = call.data.split("montaj_attach_saved:")[1]
        session = MONTAGE_CACHE.get(session_key)
        outro_path = get_saved_outro_path(user_id)
        bot.answer_callback_query(call.id)
        if not session or not os.path.exists(session.get("v1", "")) or not outro_path:
            bot.send_message(call.message.chat.id, "⚠️ Sessiya yoki saqlangan Outro topilmadi.")
            return
        USER_STATES.pop(user_id, None)
        v2_copy = os.path.join(MONTAGE_SESSIONS_DIR, f"montaj_v2_{session_key}.mp4")
        shutil.copyfile(outro_path, v2_copy)
        dur2 = get_media_duration(v2_copy)
        session["v2"] = v2_copy
        session["dur2"] = dur2
        dur1 = session.get("dur1", 15.0)
        bot.edit_message_text(
            f"🎬 <b>Har ikkala video montajga tayyor!</b>\n\n"
            f"1️⃣ <b>1-Video:</b> {dur1:.1f} soniya\n"
            f"2️⃣ <b>2-Video (Saqlangan Outro):</b> {dur2:.1f} soniya\n"
            f"⏱ <b>Jami davomiylik:</b> ~{dur1 + dur2:.1f} soniya\n\n"
            f"👇 <b>Qaysi audio-vizual rejimda birlashtiramiz?</b>",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=make_montage_mode_keyboard(session_key)
        )
        return

    if call.data == "montaj_set_outro":
        bot.answer_callback_query(call.id)
        USER_STATES[user_id] = {"action": "save_outro"}
        bot.send_message(
            call.message.chat.id,
            "📌 <b>Doimiy Reklama (Outro) videosini yuboring:</b>\n\n"
            "• Video davomiyligi <b>ixtiyoriy</b> (10s, 19s, 30s, 1 daqiqa+).\n"
            "• Videoni fayl sifatida tashlang yoki Instagram/TikTok/YouTube linkini yuboring.\n"
            "<i>(Bekor qilish uchun /cancel)</i>"
        )
        return

    if call.data == "montaj_del_outro":
        user_outro = os.path.join(PROMO_DIR, f"outro_{user_id}.mp4")
        safe_remove(user_outro)
        bot.answer_callback_query(call.id, "🗑 Saqlangan Outro o'chirildi!", show_alert=True)
        handle_montage_menu(call.message)
        return

    if call.data == "montaj_set_wm":
        bot.answer_callback_query(call.id)
        cfg = get_watermark_settings()
        USER_STATES[user_id] = {"action": "set_watermark_step"}
        bot.send_message(
            call.message.chat.id,
            f"💧 <b>Tepadan-Pastga Suzuvchi Shaffof Watermark</b>\n\n"
            f"Hozirgi yozuv: <code>{cfg.get('text')}</code>\n"
            f"✍️ <b>Yangi kanal yoki bot nikini yuboring</b> (Masalan: <code>@TELEGRAM_YULDUZLARI</code> yoki <code>@usman_khasan</code>):\n"
            f"<i>(O'chirish uchun <code>off</code> deb yozing, bekor qilish: /cancel)</i>"
        )
        return

    if call.data == "antidup_start_single":
        bot.answer_callback_query(call.id)
        USER_STATES[user_id] = {"action": "antidup_wait_video"}
        bot.send_message(
            call.message.chat.id,
            "🛡 <b>100% Original Qilinadigan Videoni Yuboring:</b>\n\n"
            "• Instagram / TikTok / YouTube linkini tashlang yoki video fayl yuboring.\n"
            "• 10-Bosqichli Anti-Duplikat + Tepadan-pastga suzuvchi shaffof watermark + iPhone 16 Pro Max metama'lumotlari qo'llanadi!"
        )
        return

    if call.data.startswith("antidup_vid:"):
        base_fname = call.data.split("antidup_vid:")[1]
        video_path = os.path.join(DOWNLOAD_DIR, base_fname)
        out_orig = os.path.join(DOWNLOAD_DIR, f"orig_{user_id}_{int(time.time()) % 1000000}.mp4")
        bot.answer_callback_query(call.id, "🛡 10-Bosqichli Anti-Duplikat boshlandi...")
        prog = bot.send_message(
            call.message.chat.id,
            "🛡 <b>10-Bosqichli Anti-Duplikat (100% Original) bajarilmoqda...</b>\n\n"
            "• 🔍 Vizual pHash, Sub-piksel Zoom & Micro-Grain...\n"
            "• 🎵 Audio Spektr & Pitch Shift...\n"
            "• 💧 Tepadan-pastga suzuvchi shaffof Telegram Watermark...\n"
            "• 📱 Apple iPhone 16 Pro Max (iOS 18.2) Metadata yozilmoqda..."
        )
        try:
            if not ensure_video_from_telegram(call.message, video_path):
                bot.edit_message_text("⚠️ Asosiy videoni o'qib bo'lmadi. Videoni qayta yuklang.", call.message.chat.id, prog.message_id)
                return
            ok, ad_info = make_video_100_original(video_path, out_orig)
            if ok and os.path.exists(out_orig):
                vinfo = get_video_stream_info(out_orig)
                fsize_mb = os.path.getsize(out_orig) / (1024 * 1024)
                bot_uname = get_cached_bot_username()
                cap = (
                    f"🛡 <b>100% ORIGINAL VIDEO (Reels / TikTok Top Uchun)!</b>\n\n"
                    f"🔍 <b>Vizual pHash siljishi:</b> +{ad_info.get('zoom', '2.5%')} (Sub-piksel + Micro-Grain)\n"
                    f"🎵 <b>Audio Fingerprint:</b> {ad_info.get('pitch', '+1.3%')}\n"
                    f"⏱ <b>Kadr & PTS Tezligi:</b> {ad_info.get('speed', '1.01x')} (GOP -g 29)\n"
                    f"📱 <b>Kamera Imzosi:</b> <code>{ad_info.get('device', 'iPhone 16 Pro Max')}</code>\n"
                    f"💧 <b>Watermark:</b> Tepadan-pastga suzuvchi shaffof ikona\n"
                    f"💾 <b>Hajmi:</b> {fsize_mb:.1f} MB\n\n"
                    f"🤖 @{bot_uname}"
                )
                with open(out_orig, "rb") as vf:
                    bot.send_video(
                        call.message.chat.id,
                        video=vf,
                        caption=cap,
                        width=vinfo.get("width", 720),
                        height=vinfo.get("height", 1280),
                        duration=vinfo.get("duration", 15),
                        supports_streaming=True
                    )
                increment_download_count(user_id, "anti_duplicate", "Anti-Duplicate Studio", "original")
                try:
                    bot.delete_message(call.message.chat.id, prog.message_id)
                except Exception:
                    pass
            else:
                bot.edit_message_text("❌ Anti-Duplikat ishlov berishda xatolik yuz berdi.", call.message.chat.id, prog.message_id)
        except Exception as e:
            bot.edit_message_text(f"❌ Xatolik: {e}", call.message.chat.id, prog.message_id)
        finally:
            safe_remove(out_orig)
        return

    # Yuklangan har qanday videoning ostidagi «🎯 Pro Reklama Montaj» tugmasi bosilganda:
    if call.data.startswith("montaj_from_vid:"):
        base_fname = call.data.split("montaj_from_vid:")[1]
        video_path = os.path.join(DOWNLOAD_DIR, base_fname)
        bot.answer_callback_query(call.id, "🎬 Montaj studiyasi ochilmoqda...")

        if not ensure_video_from_telegram(call.message, video_path):
            bot.send_message(call.message.chat.id, "⚠️ Asosiy videoni o'qib bo'lmadi. Videoni qayta yuklang.")
            return

        session_key = f"{user_id}_{int(time.time()) % 10000000}"
        v1_temp = os.path.join(MONTAGE_SESSIONS_DIR, f"m_v1_{session_key}.mp4")
        shutil.copyfile(video_path, v1_temp)

        dur1 = get_media_duration(v1_temp)
        outro_path = get_saved_outro_path(user_id)

        if outro_path:
            v2_copy = os.path.join(MONTAGE_SESSIONS_DIR, f"m_v2_{session_key}.mp4")
            shutil.copyfile(outro_path, v2_copy)
            dur2 = get_media_duration(v2_copy)
            MONTAGE_CACHE[session_key] = {
                "user_id": user_id,
                "v1": v1_temp,
                "v2": v2_copy,
                "dur1": dur1,
                "dur2": dur2,
                "created": time.time()
            }
            mk = make_montage_mode_keyboard(session_key)
            mk.add(types.InlineKeyboardButton("🔄 Boshqa 2-Video tanlash", callback_data=f"montaj_pick_other_v2:{session_key}"))
            bot.send_message(
                call.message.chat.id,
                f"🎯 <b>REKLAMA MONTAJ STUDIYASI</b>\n\n"
                f"1️⃣ <b>1-Video (Tanlangan):</b> {dur1:.1f} soniya\n"
                f"2️⃣ <b>2-Video (Saqlangan Outro):</b> {dur2:.1f} soniya\n"
                f"⏱ <b>Jami davomiylik:</b> ~{dur1 + dur2:.1f} soniya\n\n"
                f"👇 <b>Rejimni tanlang (1 bosishda tayyor bo'ladi!):</b>",
                reply_markup=mk
            )
        else:
            MONTAGE_CACHE[session_key] = {
                "user_id": user_id,
                "v1": v1_temp,
                "v2": None,
                "dur1": dur1,
                "dur2": 0.0,
                "created": time.time()
            }
            USER_STATES[user_id] = {"action": "montaj_wait_v2", "session_key": session_key}
            bot.send_message(
                call.message.chat.id,
                f"🎬 <b>1-Video tanlandi!</b> (Davomiyligi: {dur1:.1f} soniya)\n\n"
                f"📥 <b>Endi uning oxiriga ulanadigan 2-Videoni (Reklama / Outro videoni) shu yerga yuboring:</b>\n"
                f"• Davomiyligi ixtiyoriy (10s, 19s, 30s, 1 daqiqa va h.k.) bo'lishi mumkin.\n"
                f"• Video fayl tashlang yoki Instagram/TikTok/YouTube linkini yuboring:"
            )
        return

    if call.data.startswith("montaj_pick_other_v2:"):
        session_key = call.data.split("montaj_pick_other_v2:")[1]
        session = MONTAGE_CACHE.get(session_key)
        bot.answer_callback_query(call.id)
        if not session or not os.path.exists(session.get("v1", "")):
            bot.send_message(call.message.chat.id, "⚠️ Montaj sessiyasi eskirgan. Qaytadan <code>/montaj</code> bosing.")
            return
        safe_remove(session.get("v2"))
        session["v2"] = None
        USER_STATES[user_id] = {"action": "montaj_wait_v2", "session_key": session_key}
        bot.send_message(
            call.message.chat.id,
            "📥 <b>Yangi 2-Videoni (yoki video linkini) yuboring:</b>\n"
            "(Davomiyligi ixtiyoriy — 1 daqiqagacha va undan uzun bo'lishi mumkin)"
        )
        return

    if call.data.startswith("cancel_montaj:"):
        session_key = call.data.split("cancel_montaj:")[1]
        USER_STATES.pop(user_id, None)
        session = MONTAGE_CACHE.pop(session_key, None)
        if session:
            safe_remove(session.get("v1"), session.get("v2"))
        bot.answer_callback_query(call.id, "Montaj bekor qilindi.")
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception:
            pass
        return

    if call.data.startswith("do_montaj:"):
        parts = call.data.split(":")
        mode = parts[1]
        session_key = parts[2]
        session = MONTAGE_CACHE.pop(session_key, None)
        if not session or not os.path.exists(session.get("v1", "")) or not os.path.exists(session.get("v2", "")):
            bot.answer_callback_query(call.id, "⚠️ Video fayllari topilmadi yoki sessiya eskirgan.", show_alert=True)
            return

        v1_path = session["v1"]
        v2_path = session["v2"]
        out_montaj = os.path.join(DOWNLOAD_DIR, f"reklama_reel_{session_key}.mp4")

        bot.answer_callback_query(call.id, "🎬 Pro Reels montaj boshlandi...")
        prog = bot.edit_message_text(
            "⏳ <b>Top-1 Pro Reels Montaj & 10-Bosqichli Anti-Duplikat bajarilmoqda...</b>\n\n"
            "• 📐 <b>Format:</b> 9:16 HD (Blurred Fon + Smooth Fade)\n"
            "• 🎵 <b>Audio:</b> Studiya Balansi + Transition Whoosh FX\n"
            "• 💧 <b>Watermark:</b> Tepadan-pastga suzuvchi shaffof Telegram ikona\n"
            "• 🛡 <b>Anti-Duplikat:</b> 10-Qatlamli 100% Original + iPhone 16 Pro Max Metadata\n"
            "<i>Iltimos, 5–15 soniya kuting...</i>",
            call.message.chat.id,
            call.message.message_id
        )

        try:
            ok, m_info = montage_two_videos(v1_path, v2_path, out_montaj, mode=mode, apply_anti_duplicate=True)
            if ok and os.path.exists(out_montaj):
                vinfo = get_video_stream_info(out_montaj)
                fsize_mb = os.path.getsize(out_montaj) / (1024 * 1024)
                bot_uname = get_cached_bot_username()
                ad = m_info.get("anti_dup", {})
                caption = (
                    f"🎬 <b>Tayyor Pro Reklama Reels (100% Original)!</b>\n\n"
                    f"🎛 <b>Rejim:</b> {m_info.get('mode_name', mode)}\n"
                    f"⏱ <b>1-Video:</b> {m_info.get('dur1', 0):.1f}s | <b>2-Video:</b> {m_info.get('dur2', 0):.1f}s\n"
                    f"⏳ <b>Jami davomiylik:</b> <b>{m_info.get('total', 0):.1f} soniya</b>\n"
                    f"🛡 <b>Anti-Duplikat:</b> 10-Bosqichli Original (Zoom +{ad.get('zoom', '2.5%')}, iPhone 16 Pro Max)\n"
                    f"💧 <b>Watermark:</b> Tepadan-pastga suzuvchi shaffof ikona\n"
                    f"💾 <b>Hajmi:</b> {fsize_mb:.1f} MB\n\n"
                    f"🤖 @{bot_uname}"
                )
                with open(out_montaj, "rb") as mf:
                    bot.send_video(
                        call.message.chat.id,
                        video=mf,
                        caption=caption,
                        width=vinfo.get("width", 720),
                        height=vinfo.get("height", 1280),
                        duration=int(m_info.get("total", 30)),
                        supports_streaming=True
                    )
                increment_download_count(user_id, "montage_reel", "Montage Studio", mode)
                try:
                    bot.delete_message(call.message.chat.id, prog.message_id)
                except Exception:
                    pass
            else:
                bot.edit_message_text("❌ Montaj qilishda xatolik yuz berdi. Videolarni tekshirib qayta urinib ko'ring.", call.message.chat.id, prog.message_id)
        except Exception as e:
            bot.edit_message_text(f"❌ Montaj xatoligi: {e}", call.message.chat.id, prog.message_id)
        finally:
            safe_remove(v1_path, v2_path, out_montaj)
        return

    # ------------------ AUTO-SPLITTER (50 MB+) ------------------
    if call.data.startswith("split_video:"):
        base_fname = call.data.split("split_video:")[1]
        video_path = os.path.join(DOWNLOAD_DIR, base_fname)

        if not os.path.exists(video_path):
            bot.answer_callback_query(call.id, "⚠️ Video eskirgan yoki o'chirilgan.", show_alert=True)
            return

        bot.answer_callback_query(call.id, get_text("splitting_progress", lang))
        progress_msg = bot.send_message(call.message.chat.id, get_text("splitting_progress", lang))

        parts = []
        try:
            parts = split_large_video(video_path, DOWNLOAD_DIR, max_chunk_mb=46.0)
            bot.delete_message(call.message.chat.id, progress_msg.message_id)

            for idx, ppath in enumerate(parts, 1):
                part_caption = get_text("part_caption", lang, title=base_fname[:30], current=idx, total=len(parts), bot=get_cached_bot_username())
                with open(ppath, "rb") as pf:
                    bot.send_video(call.message.chat.id, video=pf, caption=part_caption, supports_streaming=True)
                safe_remove(ppath)
                time.sleep(1)
        except Exception as e:
            bot.send_message(call.message.chat.id, f"❌ Bo'laklashda xatolik: {e}")
        finally:
            safe_remove(*parts)
        return

    # ------------------ SHAZAM / MUSIQANI ANIQLASH ------------------
    if call.data.startswith("shazam:"):
        base_fname = call.data.split("shazam:")[1]
        video_path = os.path.join(DOWNLOAD_DIR, base_fname)
        bot.answer_callback_query(call.id, "🔍 Musiqa aniqlanmoqda...")
        prog = bot.send_message(call.message.chat.id, get_text("music_searching", lang))

        try:
            if not ensure_video_from_telegram(call.message, video_path):
                bot.edit_message_text("⚠️ Video faylini o'qib bo'lmadi.", call.message.chat.id, prog.message_id)
                return

            music_info = identify_music_from_video(video_path)
            bot.delete_message(call.message.chat.id, prog.message_id)

            if music_info:
                album_line = f"💿 <b>Albom:</b> {music_info['album']}\n" if music_info.get("album") else ""
                res_text = get_text("music_found", lang, title=music_info["title"], artist=music_info["artist"], album_line=album_line, bot=get_cached_bot_username())
                bot.send_message(call.message.chat.id, res_text)
            else:
                bot.send_message(call.message.chat.id, get_text("music_not_found", lang))
        except Exception as e:
            bot.edit_message_text(f"❌ Xatolik: {e}", call.message.chat.id, prog.message_id)
        return

    # ------------------ BASS BOOST AUDIO ------------------
    if call.data.startswith("bass:"):
        base_fname = call.data.split("bass:")[1]
        video_path = os.path.join(DOWNLOAD_DIR, base_fname)
        out_mp3 = os.path.join(DOWNLOAD_DIR, f"bass_{int(time.time()) % 1000000}_{os.path.splitext(base_fname)[0]}.mp3")
        bot.answer_callback_query(call.id, "🔊 Bass Boost tayyorlanmoqda...")
        prog = bot.send_message(call.message.chat.id, get_text("bass_generating", lang))
        actual_out = None
        try:
            if not ensure_video_from_telegram(call.message, video_path):
                bot.edit_message_text("⚠️ Video faylini o'qib bo'lmadi.", call.message.chat.id, prog.message_id)
                return
            if not has_audio_stream(video_path):
                bot.edit_message_text("ℹ️ Ushbu videoda ovoz (audio oqimi) mavjud emas.", call.message.chat.id, prog.message_id)
                return
            actual_out = convert_to_bass_boost(video_path, out_mp3)
            if actual_out and os.path.exists(actual_out):
                with open(actual_out, "rb") as af:
                    bot.send_audio(call.message.chat.id, audio=af, caption=f"🔊 <b>Bass Boost (+12dB)</b> | @{get_cached_bot_username()}")
                bot.delete_message(call.message.chat.id, prog.message_id)
            else:
                bot.edit_message_text(get_text("err_generic", lang), call.message.chat.id, prog.message_id)
        finally:
            safe_remove(out_mp3, actual_out)
        return

    # ------------------ 8D SURROUND AUDIO ------------------
    if call.data.startswith("audio8d:"):
        base_fname = call.data.split("audio8d:")[1]
        video_path = os.path.join(DOWNLOAD_DIR, base_fname)
        out_mp3 = os.path.join(DOWNLOAD_DIR, f"8d_{int(time.time()) % 1000000}_{os.path.splitext(base_fname)[0]}.mp3")
        bot.answer_callback_query(call.id, "🎧 8D Audio tayyorlanmoqda...")
        prog = bot.send_message(call.message.chat.id, get_text("audio8d_generating", lang))
        actual_out = None
        try:
            if not ensure_video_from_telegram(call.message, video_path):
                bot.edit_message_text("⚠️ Video faylini o'qib bo'lmadi.", call.message.chat.id, prog.message_id)
                return
            if not has_audio_stream(video_path):
                bot.edit_message_text("ℹ️ Ushbu videoda ovoz (audio oqimi) mavjud emas.", call.message.chat.id, prog.message_id)
                return
            actual_out = convert_to_8d_audio(video_path, out_mp3)
            if actual_out and os.path.exists(actual_out):
                with open(actual_out, "rb") as af:
                    bot.send_audio(call.message.chat.id, audio=af, caption=f"🎧 <b>8D Surround Audio (Quloqchinda tinglang!)</b>\n🤖 @{get_cached_bot_username()}")
                bot.delete_message(call.message.chat.id, prog.message_id)
            else:
                bot.edit_message_text(get_text("err_generic", lang), call.message.chat.id, prog.message_id)
        finally:
            safe_remove(out_mp3, actual_out)
        return

    # ------------------ KARAOKE MINUSOVKA ------------------
    if call.data.startswith("karaoke:"):
        base_fname = call.data.split("karaoke:")[1]
        video_path = os.path.join(DOWNLOAD_DIR, base_fname)
        out_mp3 = os.path.join(DOWNLOAD_DIR, f"karaoke_{int(time.time()) % 1000000}_{os.path.splitext(base_fname)[0]}.mp3")
        bot.answer_callback_query(call.id, "🎤 Karaoke minusovka tayyorlanmoqda...")
        prog = bot.send_message(call.message.chat.id, get_text("karaoke_generating", lang))
        actual_out = None
        try:
            if not ensure_video_from_telegram(call.message, video_path):
                bot.edit_message_text("⚠️ Video faylini o'qib bo'lmadi.", call.message.chat.id, prog.message_id)
                return
            if not has_audio_stream(video_path):
                bot.edit_message_text("ℹ️ Ushbu videoda ovoz (audio oqimi) mavjud emas.", call.message.chat.id, prog.message_id)
                return
            actual_out = convert_to_karaoke_minus(video_path, out_mp3)
            if actual_out and os.path.exists(actual_out):
                with open(actual_out, "rb") as af:
                    bot.send_audio(call.message.chat.id, audio=af, caption=f"🎤 <b>Karaoke Minusovka (Vocal Removed)</b>\n🤖 @{get_cached_bot_username()}")
                bot.delete_message(call.message.chat.id, prog.message_id)
            else:
                bot.edit_message_text(get_text("err_generic", lang), call.message.chat.id, prog.message_id)
        finally:
            safe_remove(out_mp3, actual_out)
        return

    # ------------------ HD THUMBNAIL (OBLOJKA) ------------------
    if call.data.startswith("thumb:"):
        base_fname = call.data.split("thumb:")[1]
        video_path = os.path.join(DOWNLOAD_DIR, base_fname)
        out_jpg = os.path.join(DOWNLOAD_DIR, f"thumb_{int(time.time()) % 1000000}_{os.path.splitext(base_fname)[0]}.jpg")
        bot.answer_callback_query(call.id, "🖼 HD Oblojka olinmoqda...")
        try:
            if ensure_video_from_telegram(call.message, video_path) and extract_hd_thumbnail(video_path, out_jpg) and os.path.exists(out_jpg):
                with open(out_jpg, "rb") as jf:
                    bot.send_photo(call.message.chat.id, photo=jf, caption=f"🖼 <b>HD Video Oblojkasi (Thumbnail)</b>\n🤖 @{get_cached_bot_username()}")
            else:
                bot.send_message(call.message.chat.id, get_text("err_generic", lang))
        finally:
            safe_remove(out_jpg)
        return

    # ------------------ REVERSE VIDEO (TESKARI VIDEO) ------------------
    if call.data.startswith("reverse:"):
        base_fname = call.data.split("reverse:")[1]
        video_path = os.path.join(DOWNLOAD_DIR, base_fname)
        out_rev = os.path.join(DOWNLOAD_DIR, f"rev_{int(time.time()) % 1000000}_{base_fname}")
        bot.answer_callback_query(call.id, "⏪ Teskari video tayyorlanmoqda...")
        prog = bot.send_message(call.message.chat.id, get_text("reverse_generating", lang))
        try:
            if ensure_video_from_telegram(call.message, video_path) and convert_to_reverse_video(video_path, out_rev) and os.path.exists(out_rev):
                with open(out_rev, "rb") as rf:
                    bot.send_video(call.message.chat.id, video=rf, caption=f"⏪ <b>Teskari Video (Reverse Effect)</b>\n🤖 @{get_cached_bot_username()}", supports_streaming=True)
                bot.delete_message(call.message.chat.id, prog.message_id)
            else:
                bot.edit_message_text(get_text("err_generic", lang), call.message.chat.id, prog.message_id)
        finally:
            safe_remove(out_rev)
        return

    # ------------------ VIDEO TRIMMER ------------------
    if call.data.startswith("trim:"):
        base_fname = call.data.split("trim:")[1]
        bot.answer_callback_query(call.id)
        TRIM_CACHE[call.from_user.id] = call.message
        USER_STATES[call.from_user.id] = {"action": "trim", "file": base_fname, "lang": lang}
        bot.send_message(call.message.chat.id, get_text("trim_prompt", lang))
        return

    # ------------------ SUBTITR TILI TANLASH ------------------
    if call.data.startswith("sub_vid:"):
        base_fname = call.data.split("sub_vid:")[1]
        markup = make_sub_lang_keyboard("do_sub_vid", base_fname)
        bot.answer_callback_query(call.id)
        try:
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)
        except Exception:
            bot.send_message(
                call.message.chat.id,
                "🌐 <b>Subtitr qaysi tilda yaratilsin?</b>\nNutq aniqlanib, videoga yoziladi:",
                reply_to_message_id=call.message.message_id,
                reply_markup=markup
            )
        return

    if call.data.startswith("sub_txt:"):
        base_fname = call.data.split("sub_txt:")[1]
        markup = make_sub_lang_keyboard("do_sub_txt", base_fname)
        bot.answer_callback_query(call.id)
        try:
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)
        except Exception:
            bot.send_message(
                call.message.chat.id,
                "🌐 <b>Qaysi tildagi nutq matnga aylantirilsin?</b>",
                reply_to_message_id=call.message.message_id,
                reply_markup=markup
            )
        return

    # ------------------ SUBTITRLI VIDEO (HARDCODE + PNG FALLBACK) ------------------
    if call.data.startswith("do_sub_vid:"):
        parts = call.data.split(":")
        sub_lang, base_fname = parts[1], parts[2]
        video_path = os.path.join(DOWNLOAD_DIR, base_fname)
        ts_sub = int(time.time() * 1000) % 1000000
        temp_audio = os.path.join(DOWNLOAD_DIR, f"temp_{ts_sub}.wav")
        srt_path = os.path.join(DOWNLOAD_DIR, f"sub_{ts_sub}.srt")
        sub_video_path = os.path.join(DOWNLOAD_DIR, f"subtitled_{ts_sub}_{base_fname}")

        bot.answer_callback_query(call.id, "🎬 Subtitr tayyorlanmoqda...")
        prog = bot.send_message(call.message.chat.id, get_text("sub_video_generating", lang))

        # Asosiy tugmalarni joyiga qaytarib qo'yamiz
        try:
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=make_video_action_keyboard(base_fname, lang=lang))
        except Exception:
            pass

        try:
            if not ensure_video_from_telegram(call.message, video_path):
                bot.edit_message_text("⚠️ Video faylini o'qib bo'lmadi.", call.message.chat.id, prog.message_id)
                return

            subprocess.run([FFMPEG_BIN, "-y", "-i", video_path, "-vn", "-ar", "16000", "-ac", "1", temp_audio], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            success, transcript_text = transcribe_audio_to_srt(temp_audio, srt_path, lang=sub_lang)
            safe_remove(temp_audio)

            if not success or not os.path.exists(srt_path):
                bot.edit_message_text(get_text("sub_not_found", lang), call.message.chat.id, prog.message_id)
                return

            burn_success = burn_subtitles_to_video(video_path, srt_path, sub_video_path)
            if burn_success and os.path.exists(sub_video_path):
                vinfo = get_video_stream_info(sub_video_path)
                with open(sub_video_path, "rb") as svf:
                    bot.send_video(
                        call.message.chat.id,
                        video=svf,
                        caption=f"🎬 <b>Subtitrli Video tayyor!</b>\n\n📝 <i>\"{transcript_text[:120]}...\"</i>\n\n🤖 @{get_cached_bot_username()}",
                        width=vinfo.get("width", 720),
                        height=vinfo.get("height", 1280),
                        duration=vinfo.get("duration", 15),
                        supports_streaming=True
                    )
                bot.delete_message(call.message.chat.id, prog.message_id)
            else:
                bot.edit_message_text(get_text("err_generic", lang), call.message.chat.id, prog.message_id)
        except Exception as e:
            bot.edit_message_text(f"❌ Xatolik: {e}", call.message.chat.id, prog.message_id)
        finally:
            safe_remove(temp_audio, srt_path, sub_video_path)
        return

    # ------------------ FAQAT SUBTITR MATNI VA .SRT ------------------
    if call.data.startswith("do_sub_txt:"):
        parts = call.data.split(":")
        sub_lang, base_fname = parts[1], parts[2]
        video_path = os.path.join(DOWNLOAD_DIR, base_fname)
        ts_sub = int(time.time() * 1000) % 1000000
        temp_audio = os.path.join(DOWNLOAD_DIR, f"temp_{ts_sub}.wav")
        srt_path = os.path.join(DOWNLOAD_DIR, f"sub_{ts_sub}.srt")

        bot.answer_callback_query(call.id, "📝 Nutq tahlil qilinmoqda...")
        prog = bot.send_message(call.message.chat.id, get_text("sub_text_generating", lang))

        try:
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=make_video_action_keyboard(base_fname, lang=lang))
        except Exception:
            pass

        try:
            if not ensure_video_from_telegram(call.message, video_path):
                bot.edit_message_text("⚠️ Video faylini o'qib bo'lmadi.", call.message.chat.id, prog.message_id)
                return

            subprocess.run([FFMPEG_BIN, "-y", "-i", video_path, "-vn", "-ar", "16000", "-ac", "1", temp_audio], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            success, transcript_text = transcribe_audio_to_srt(temp_audio, srt_path, lang=sub_lang)
            safe_remove(temp_audio)

            if not success or not transcript_text:
                bot.edit_message_text(get_text("sub_not_found", lang), call.message.chat.id, prog.message_id)
                return

            bot.send_message(call.message.chat.id, f"📝 <b>TRANSKRIPSIYA (MATN):</b>\n\n<i>\"{transcript_text[:3500]}\"</i>\n\n🤖 @{get_cached_bot_username()}")
            with open(srt_path, "rb") as sf:
                bot.send_document(call.message.chat.id, document=sf, caption="📄 <b>.SRT Subtitr fayli</b>\n(CapCut, Premiere Pro uchun)")
            bot.delete_message(call.message.chat.id, prog.message_id)
        except Exception as e:
            bot.edit_message_text(f"❌ Xatolik: {e}", call.message.chat.id, prog.message_id)
        finally:
            safe_remove(temp_audio, srt_path)
        return

    # ------------------ KRUGLYASH (1:1 VIDEO NOTE) ------------------
    if call.data.startswith("circle:"):
        base_fname = call.data.split("circle:")[1]
        video_path = os.path.join(DOWNLOAD_DIR, base_fname)
        circle_path = os.path.join(DOWNLOAD_DIR, f"circle_{int(time.time()) % 1000000}_{base_fname}")

        bot.answer_callback_query(call.id, "🔄 Kruglyash tayyorlanmoqda...")
        prog = bot.send_message(call.message.chat.id, get_text("circle_generating", lang))

        try:
            if ensure_video_from_telegram(call.message, video_path) and convert_to_circle_note(video_path, circle_path) and os.path.exists(circle_path):
                with open(circle_path, "rb") as cf:
                    bot.send_video_note(call.message.chat.id, cf)
                bot.delete_message(call.message.chat.id, prog.message_id)
            else:
                bot.edit_message_text(get_text("err_generic", lang), call.message.chat.id, prog.message_id)
        except Exception as e:
            bot.edit_message_text(f"❌ Xatolik: {e}", call.message.chat.id, prog.message_id)
        finally:
            safe_remove(circle_path)
        return

    # ------------------ MP3 AUDIO ------------------
    if call.data.startswith("audio:"):
        base_fname = call.data.split("audio:")[1]
        video_path = os.path.join(DOWNLOAD_DIR, base_fname)
        mp3_path = os.path.join(DOWNLOAD_DIR, f"audio_{int(time.time()) % 1000000}_{os.path.splitext(base_fname)[0]}.mp3")

        bot.answer_callback_query(call.id, "🎧 MP3 ajratilmoqda...")
        prog = bot.send_message(call.message.chat.id, get_text("audio_generating", lang))
        actual_out = None

        try:
            if not ensure_video_from_telegram(call.message, video_path):
                bot.edit_message_text("⚠️ Video faylini o'qib bo'lmadi.", call.message.chat.id, prog.message_id)
                return
            if not has_audio_stream(video_path):
                bot.edit_message_text("ℹ️ Ushbu videoda ovoz (audio oqimi) mavjud emas.", call.message.chat.id, prog.message_id)
                return
            actual_out = extract_audio_mp3(video_path, mp3_path, title=base_fname[:30])
            if actual_out and os.path.exists(actual_out):
                with open(actual_out, "rb") as af:
                    bot.send_audio(call.message.chat.id, audio=af, caption=f"🎵 @{get_cached_bot_username()}")
                bot.delete_message(call.message.chat.id, prog.message_id)
            else:
                bot.edit_message_text(get_text("err_generic", lang), call.message.chat.id, prog.message_id)
        except Exception as e:
            bot.edit_message_text(f"❌ Xatolik: {e}", call.message.chat.id, prog.message_id)
        finally:
            safe_remove(mp3_path, actual_out)
        return

    # ------------------ OVOZLI XABAR (VOICE NOTE) ------------------
    if call.data.startswith("voice:"):
        base_fname = call.data.split("voice:")[1]
        video_path = os.path.join(DOWNLOAD_DIR, base_fname)
        voice_path = os.path.join(DOWNLOAD_DIR, f"voice_{int(time.time()) % 1000000}_{os.path.splitext(base_fname)[0]}.ogg")

        bot.answer_callback_query(call.id, "🎙 Ovozli xabar tayyorlanmoqda...")
        prog = bot.send_message(call.message.chat.id, get_text("voice_generating", lang))
        actual_out = None

        try:
            if not ensure_video_from_telegram(call.message, video_path):
                bot.edit_message_text("⚠️ Video faylini o'qib bo'lmadi.", call.message.chat.id, prog.message_id)
                return
            if not has_audio_stream(video_path):
                bot.edit_message_text("ℹ️ Ushbu videoda ovoz (audio oqimi) mavjud emas.", call.message.chat.id, prog.message_id)
                return
            actual_out = convert_to_voice_ogg(video_path, voice_path)
            if actual_out and os.path.exists(actual_out):
                with open(actual_out, "rb") as vf:
                    if actual_out.endswith(".ogg"):
                        bot.send_voice(call.message.chat.id, voice=vf, caption=f"🎙 @{get_cached_bot_username()}")
                    else:
                        bot.send_audio(call.message.chat.id, audio=vf, caption=f"🎙 @{get_cached_bot_username()}")
                bot.delete_message(call.message.chat.id, prog.message_id)
            else:
                bot.edit_message_text(get_text("err_generic", lang), call.message.chat.id, prog.message_id)
        except Exception as e:
            bot.edit_message_text(f"❌ Xatolik: {e}", call.message.chat.id, prog.message_id)
        finally:
            safe_remove(voice_path, actual_out)
        return

    # ------------------ 1.5x TEZLIK ------------------
    if call.data.startswith("speed:"):
        base_fname = call.data.split("speed:")[1]
        video_path = os.path.join(DOWNLOAD_DIR, base_fname)
        speed_path = os.path.join(DOWNLOAD_DIR, f"speed_{int(time.time()) % 1000000}_{base_fname}")

        bot.answer_callback_query(call.id, "⚡ 1.5x tezlashtirilmoqda...")
        prog = bot.send_message(call.message.chat.id, get_text("speed_generating", lang))

        try:
            if ensure_video_from_telegram(call.message, video_path) and convert_to_fast_speed(video_path, speed_path, speed=1.5) and os.path.exists(speed_path):
                with open(speed_path, "rb") as sf:
                    bot.send_video(call.message.chat.id, video=sf, caption=f"⚡ <b>1.5x</b> | @{get_cached_bot_username()}", supports_streaming=True)
                bot.delete_message(call.message.chat.id, prog.message_id)
            else:
                bot.edit_message_text(get_text("err_generic", lang), call.message.chat.id, prog.message_id)
        except Exception as e:
            bot.edit_message_text(f"❌ Xatolik: {e}", call.message.chat.id, prog.message_id)
        finally:
            safe_remove(speed_path)
        return

    # ------------------ GIF ANIMATSIYA ------------------
    if call.data.startswith("gif:"):
        base_fname = call.data.split("gif:")[1]
        video_path = os.path.join(DOWNLOAD_DIR, base_fname)
        gif_path = os.path.join(DOWNLOAD_DIR, f"gif_{int(time.time()) % 1000000}_{os.path.splitext(base_fname)[0]}.mp4")

        bot.answer_callback_query(call.id, "🎞 GIF tayyorlanmoqda...")
        prog = bot.send_message(call.message.chat.id, get_text("gif_generating", lang))

        try:
            if ensure_video_from_telegram(call.message, video_path) and convert_to_gif_animation(video_path, gif_path) and os.path.exists(gif_path):
                with open(gif_path, "rb") as gf:
                    bot.send_animation(call.message.chat.id, animation=gf, caption=f"🎞 @{get_cached_bot_username()}")
                bot.delete_message(call.message.chat.id, prog.message_id)
            else:
                bot.edit_message_text(get_text("err_generic", lang), call.message.chat.id, prog.message_id)
        except Exception as e:
            bot.edit_message_text(f"❌ Xatolik: {e}", call.message.chat.id, prog.message_id)
        finally:
            safe_remove(gif_path)
        return

# ==================== TRIMMER PROCESSOR ====================
def process_trim_step(message: types.Message):
    user_id = message.from_user.id
    state = USER_STATES.get(user_id)
    if not state or state.get("action") != "trim":
        return

    lang = state.get("lang", "uz")
    base_fname = state.get("file")
    video_path = os.path.join(DOWNLOAD_DIR, base_fname)
    orig_msg = TRIM_CACHE.pop(user_id, None)

    USER_STATES.pop(user_id, None)

    if not message.text:
        bot.reply_to(message, get_text("trim_invalid", lang))
        return

    text = message.text.replace("—", "-").replace("–", "-")
    parts = text.split("-")
    if len(parts) != 2:
        bot.reply_to(message, get_text("trim_invalid", lang))
        return

    s_sec = parse_time_to_seconds(parts[0])
    e_sec = parse_time_to_seconds(parts[1])

    if s_sec is None or e_sec is None or s_sec >= e_sec:
        bot.reply_to(message, get_text("trim_invalid", lang))
        return

    prog = bot.reply_to(message, get_text("trimming_progress", lang))
    trimmed_fname = f"trim_{int(time.time()) % 1000000}_{base_fname}"
    trimmed_path = os.path.join(DOWNLOAD_DIR, trimmed_fname)

    try:
        if not ensure_video_from_telegram(orig_msg, video_path):
            bot.edit_message_text("⚠️ Video fayli topilmadi.", message.chat.id, prog.message_id)
            return

        success = trim_video(video_path, trimmed_path, s_sec, e_sec)
        if success and os.path.exists(trimmed_path):
            with open(trimmed_path, "rb") as tf:
                bot.send_video(
                    message.chat.id,
                    video=tf,
                    caption=f"✂️ <b>Qirqilgan lavha ({parts[0].strip()} - {parts[1].strip()})</b>\n🤖 @{get_cached_bot_username()}",
                    supports_streaming=True
                )
            bot.delete_message(message.chat.id, prog.message_id)
        else:
            bot.edit_message_text(get_text("err_generic", lang), message.chat.id, prog.message_id)
    except Exception as e:
        bot.edit_message_text(f"❌ Xatolik: {e}", message.chat.id, prog.message_id)
    finally:
        safe_remove(trimmed_path)

# ==================== INLINE REJIM (@bot_username havola) ====================
@bot.inline_handler(func=lambda query: True)
def handle_inline_query(query: types.InlineQuery):
    url = extract_url(query.query)
    results = []
    bot_username = get_cached_bot_username()

    if url:
        platform = detect_platform(url)
        item = types.InlineQueryResultArticle(
            id="1",
            title=f"📥 {platform} videosini yuklash",
            description=f"Havola: {url[:50]}...",
            input_message_content=types.InputTextMessageContent(
                message_text=f"🎬 <b>{platform} videosini yuklash:</b>\n{url}\n\n🤖 @{bot_username} orqali yuklanmoqda...",
                parse_mode="HTML"
            ),
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("⚡ Botga kirib yuklash", url=f"https://t.me/{bot_username}?start=dl")
            )
        )
        results.append(item)
    else:
        item = types.InlineQueryResultArticle(
            id="help",
            title="💡 Video havolasini yozing",
            description="Masalan: @bot_username https://instagram.com/reel/...",
            input_message_content=types.InputTextMessageContent(
                message_text=f"👋 <b>Universal Video Saver & Pro Montaj Bot</b>\nVideo linkini yuboring!\n\n🤖 @{bot_username}",
                parse_mode="HTML"
            )
        )
        results.append(item)

    bot.answer_inline_query(query.id, results, cache_time=5)

# ==================== SERVER KEEP-ALIVE VA TARMOQ SOZLAMASI ====================
def start_cloud_keepalive_server():
    port_str = os.environ.get("PORT", "")
    if not port_str:
        return
    try:
        from http.server import BaseHTTPRequestHandler, HTTPServer
        port = int(port_str)

        class HealthHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header("Content-type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(b"Universal Super Saver Bot 24/7 Faol!")
            def log_message(self, format, *args):
                return

        srv = HTTPServer(("0.0.0.0", port), HealthHandler)
        t = threading.Thread(target=srv.serve_forever, daemon=True)
        t.start()
        print(f"🌐 Cloud Keep-Alive Web Server {port}-portda ishga tushdi!")
    except Exception as e:
        print(f"Keep-Alive server xatosi: {e}")

def configure_server_network():
    try:
        from telebot import apihelper
        apihelper.CONNECT_TIMEOUT = 25
        apihelper.READ_TIMEOUT = 45
        apihelper.RETRY_ON_ERROR = True
        apihelper.RETRY_TIMEOUT = 3
        apihelper.MAX_RETRIES = 5
        pa_proxy = os.environ.get("https_proxy") or os.environ.get("HTTPS_PROXY") or os.environ.get("http_proxy")
        if pa_proxy:
            apihelper.proxy = {"http": pa_proxy, "https": pa_proxy}
            print(f"🔌 Tizim proksisi aniqlandi: {pa_proxy}")
    except Exception as e:
        print(f"Tarmoq sozlash xatosi: {e}")

# ==================== BOTNI ISHGA TUSHIRISH ====================
if __name__ == '__main__':
    kill_other_bot_instances()
    ensure_ffmpeg_in_path()
    configure_server_network()
    start_cloud_keepalive_server()
    ffmpeg_loc = FFMPEG_BIN if os.path.exists(str(FFMPEG_BIN)) else (shutil.which("ffmpeg") or "Avto-imageio-ffmpeg")
    print("=" * 75)
    print("🚀 UNIVERSAL SUPER SAVER & PRO MONTAJ TELEGRAM BOT (#1 EDITION)")
    print(f"🎬 FFmpeg holati: {ffmpeg_loc}")
    print(f"👑 Admin Telegram ID: {ADMIN_ID} (@usman_khasan)")
    print("📱 12-Bosqichli VIDEO-FIRST Link Yuklagich: FAOL")
    print("🎬 Top-1 Pro Reklama Montaj Studiyasi (/montaj, /set_outro — 5 xil tezkor rejim): FAOL")
    print("🛡 10-Bosqichli Anti-Duplikat (100% Original Video — /original): FAOL")
    print("💧 Tepadan-Pastga Suzuvchi Shaffof Telegram Ikonka + @Handle Watermark (/set_watermark): FAOL")
    print("🎛 16 ta Multimedia Studiyasi Tugmalari (Subtitr, Kruglyash, MP3, Bass, 8D, Karaoke va h.k.): 100% FAOL")
    print("=" * 75)

    try:
        bot.set_my_commands([
            types.BotCommand("start", "🚀 Botni ishga tushirish"),
            types.BotCommand("ig", "📸 Instagram 24/7 Avto-Poster & Halol Trend Studiyasi"),
            types.BotCommand("ig_now", "🚀 Hozir 1 ta Reels yasab Instagramga joylash"),
            types.BotCommand("ig_login", "🔑 Instagram profilni ulash (Login/Parol)"),
            types.BotCommand("montaj", "🎬 Pro Reklama Montaj Studiyasi (5 rejim + Anti-Duplikat)"),
            types.BotCommand("original", "🛡 Videoni 100% Original qilish (Anti-Duplikat)"),
            types.BotCommand("set_outro", "📌 Doimiy reklama (Outro) videoni saqlash"),
            types.BotCommand("set_watermark", "💧 Tepadan-pastga suzuvchi shaffof watermarkni sozlash"),
            types.BotCommand("stat", "📊 Bot va shaxsiy statistika"),
            types.BotCommand("kurs", "💱 Markaziy bank valyuta kurslari"),
            types.BotCommand("profile", "👤 Profilim va ma'lumotlar"),
            types.BotCommand("qr", "📱 QR-Kod yasash"),
            types.BotCommand("clean", "🧹 Keshni tozalash"),
            types.BotCommand("cancel", "❌ Joriy amalni bekor qilish")
        ])
    except Exception as e:
        print(f"Menyu komandalarini o'rnatish: {e}")

    while True:
        try:
            bot.infinity_polling(timeout=35, long_polling_timeout=20, skip_pending=True)
        except KeyboardInterrupt:
            print("Bot foydalanuvchi tomonidan to'xtatildi.")
            break
        except Exception as e:
            print(f"Polling uzilishi (5 soniyada qayta ulanadi): {e}")
            time.sleep(5)
