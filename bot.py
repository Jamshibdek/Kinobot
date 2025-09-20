# import telebot
# import os
# import json
# import random
# import string
# import time  # Rate limiting uchun

# bot = telebot.TeleBot("7960038374:AAE8oIdCkpqOdU3EDAq1GGC1-f46PjBevPo")
# SUPER_ADMIN = 6215236648  # Super admin ID




# # Load data from JSON
# try:
#     movies = json.load(open("movies.json"))
# except:
#     movies = {}  # Format: {"code": {"file_id": "telegram_file_id", "description": "desc"}}

# try:
#     admins = json.load(open("admins.json"))
# except:
#     admins = [SUPER_ADMIN]  # Adminlar ro'yxati

# try:
#     channels = json.load(open("channels.json"))
# except:
#     channels = []  # Kanallar ro'yxati (e.g., "@channel")

# try:
#     users = set(json.load(open("users.json")))
# except:
#     users = set()  # Foydalanuvchilar ro'yxati

# # Pending actions
# pending = {}  # {user_id: {"action": "add_movie", "step": 1, "data": {}}}

# def save_data():
#     json.dump(movies, open("movies.json", "w"))
#     json.dump(admins, open("admins.json", "w"))
#     json.dump(channels, open("channels.json", "w"))
#     json.dump(list(users), open("users.json", "w"))

# def generate_unique_code(length=3):
#     if len(movies) >= 1000:  # 000-999 gacha 1000 ta imkoniyat
#         raise ValueError("Kino kodlari tugadi! 3 xonali raqamlar chegarasiga yetdi.")
#     attempts = 0
#     max_attempts = 100  # Cheksiz tsiklni oldini olish
#     while attempts < max_attempts:
#         code = ''.join(random.choices(string.digits, k=length))  # Faqat raqamlar
#         if code not in movies:
#             return code
#         attempts += 1
#     raise ValueError("Yangi 3 xonali kod topilmadi. Iltimos, boshqa uzunlik sinab ko'ring.")

# def is_admin(user_id):
#     return user_id in admins

# def check_subscription(user_id):
#     if not channels:
#         return True
#     for channel in channels:
#         try:
#             member = bot.get_chat_member(channel, user_id)
#             if member.status in ['left', 'kicked', 'restricted']:
#                 return False
#         except:
#             return False
#     return True

# @bot.message_handler(commands=['start'])
# def start(m):
#     user_id = m.from_user.id
#     users.add(user_id)
#     save_data()
    
#     if check_subscription(user_id):
#         bot.reply_to(m, "Xush kelibsiz! Kino kodini yozing.")
#     else:
#         markup = telebot.types.InlineKeyboardMarkup()
#         for channel in channels:
#             markup.add(telebot.types.InlineKeyboardButton(f"Obuna bo'ling: {channel}", url=f"https://t.me/{channel.lstrip('@')}"))
#         markup.add(telebot.types.InlineKeyboardButton("Tekshirish", callback_data="check_sub"))
#         bot.reply_to(m, "Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:", reply_markup=markup)

# @bot.callback_query_handler(func=lambda call: call.data == "check_sub")
# def check_sub_callback(call):
#     user_id = call.from_user.id
#     if check_subscription(user_id):
#         bot.answer_callback_query(call.id, "Obuna tasdiqlandi! Kino kodini yozing.")
#         bot.edit_message_text("Xush kelibsiz! Kino kodini yozing.", call.message.chat.id, call.message.message_id)
#     else:
#         bot.answer_callback_query(call.id, "Hali obuna bo'lmagansiz. Iltimos, obuna bo'ling.", show_alert=True)

# # Super admin: Admin qo'shish/o'chirish
# @bot.message_handler(commands=['add_admin'])
# def add_admin(m):
#     if m.from_user.id != SUPER_ADMIN:
#         return
#     try:
#         admin_id = int(m.text.split()[1])
#         if admin_id not in admins:
#             admins.append(admin_id)
#             save_data()
#             bot.reply_to(m, f"Admin qo'shildi: {admin_id}")
#         else:
#             bot.reply_to(m, "Bu foydalanuvchi allaqachon admin.")
#     except:
#         bot.reply_to(m, "Foydalanuvchi ID'sini kiriting: /add_admin <ID>")

# @bot.message_handler(commands=['remove_admin'])
# def remove_admin(m):
#     if m.from_user.id != SUPER_ADMIN:
#         return
#     try:
#         admin_id = int(m.text.split()[1])
#         if admin_id in admins and admin_id != SUPER_ADMIN:
#             admins.remove(admin_id)
#             save_data()
#             bot.reply_to(m, f"Admin o'chirildi: {admin_id}")
#         else:
#             bot.reply_to(m, "Bu foydalanuvchi admin emas yoki super admin.")
#     except:
#         bot.reply_to(m, "Foydalanuvchi ID'sini kiriting: /remove_admin <ID>")

# # Kanallarni boshqarish
# @bot.message_handler(commands=['add_channel'])
# def add_channel(m):
#     if not is_admin(m.from_user.id):
#         return
#     try:
#         channel = m.text.split()[1]
#         if channel not in channels:
#             channels.append(channel)
#             save_data()
#             bot.reply_to(m, f"Kanal qo'shildi: {channel}")
#         else:
#             bot.reply_to(m, "Bu kanal allaqachon mavjud.")
#     except:
#         bot.reply_to(m, "Kanal usernamesini kiriting: /add_channel @channel")

# @bot.message_handler(commands=['remove_channel'])
# def remove_channel(m):
#     if not is_admin(m.from_user.id):
#         return
#     try:
#         channel = m.text.split()[1]
#         if channel in channels:
#             channels.remove(channel)
#             save_data()
#             bot.reply_to(m, f"Kanal o'chirildi: {channel}")
#         else:
#             bot.reply_to(m, "Bu kanal mavjud emas.")
#     except:
#         bot.reply_to(m, "Kanal usernamesini kiriting: /remove_channel @channel")

# # Kino qo'shish
# @bot.message_handler(commands=['add_movie'])
# def add_movie_start(m):
#     if not is_admin(m.from_user.id):
#         return
#     pending[m.from_user.id] = {"action": "add_movie", "step": 1, "data": {}}
#     bot.reply_to(m, "Kino videosini yuboring (video yoki document sifatida).")

# @bot.message_handler(content_types=['video', 'document'])
# def handle_movie_video(m):
#     user_id = m.from_user.id
#     if user_id not in pending or pending[user_id]["action"] != "add_movie" or pending[user_id]["step"] != 1:
#         return
#     if m.video:
#         f = m.video
#     elif m.document:
#         f = m.document
#     else:
#         return
#     pending[user_id]["data"]["file_id"] = f.file_id
#     pending[user_id]["step"] = 2
#     bot.reply_to(m, "Endi kino tavsifini yuboring.")

# @bot.message_handler(func=lambda m: m.from_user.id in pending and pending[m.from_user.id]["action"] == "add_movie" and pending[m.from_user.id]["step"] == 2)
# def handle_movie_desc(m):
#     user_id = m.from_user.id
#     desc = m.text.strip()
#     try:
#         code = generate_unique_code()
#         movies[code] = {"file_id": pending[user_id]["data"]["file_id"], "description": desc}
#         save_data()
#         del pending[user_id]
#         bot.reply_to(m, f"✅ Kino qo'shildi: Kod - {code}\nTavsif: {desc}")
#     except ValueError as e:
#         bot.reply_to(m, f"❌ Xato: {str(e)}")
#         del pending[user_id]

# # Kino o'chirish
# @bot.message_handler(commands=['delete_movie'])
# def delete_movie(m):
#     if not is_admin(m.from_user.id):
#         return
#     try:
#         code = m.text.split()[1]
#         if code in movies:
#             del movies[code]
#             save_data()
#             bot.reply_to(m, f"✅ Kino o'chirildi: {code}")
#         else:
#             bot.reply_to(m, "Kod topilmadi.")
#     except:
#         bot.reply_to(m, "Kodni kiriting: /delete_movie <code>")

# # Kino tahrirlash
# @bot.message_handler(commands=['edit_movie'])
# def edit_movie_start(m):
#     if not is_admin(m.from_user.id):
#         return
#     try:
#         parts = m.text.split(maxsplit=3)
#         if len(parts) < 3:
#             bot.reply_to(m, "Foydalanish: /edit_movie <old_code> code <new_code> yoki /edit_movie <old_code> desc <new_desc>")
#             return
#         old_code = parts[1]
#         if old_code not in movies:
#             bot.reply_to(m, "Kod topilmadi.")
#             return
#         if parts[2] == "code":
#             new_code = parts[3]
#             if new_code in movies:
#                 bot.reply_to(m, "Yangi kod allaqachon mavjud.")
#                 return
#             try:
#                 if len(new_code) != 3 or not new_code.isdigit():
#                     bot.reply_to(m, "Yangi kod 3 xonali raqam bo'lishi kerak (masalan, 123).")
#                     return
#                 movies[new_code] = movies.pop(old_code)
#                 save_data()
#                 bot.reply_to(m, f"✅ Kod o'zgartirildi: {old_code} -> {new_code}")
#             except ValueError as e:
#                 bot.reply_to(m, f"❌ Xato: {str(e)}")
#         elif parts[2] == "desc":
#             new_desc = parts[3]
#             movies[old_code]["description"] = new_desc
#             save_data()
#             bot.reply_to(m, f"✅ Tavsif o'zgartirildi: {old_code}")
#         else:
#             bot.reply_to(m, "Noto'g'ri parametr: code yoki desc")
#     except:
#         bot.reply_to(m, "Xato. Foydalanish: /edit_movie <old_code> code <new_code> yoki /edit_movie <old_code> desc <new_desc>")

# # Broadcast
# @bot.message_handler(commands=['broadcast'])
# def broadcast_start(m):
#     if not is_admin(m.from_user.id):
#         return
#     if m.from_user.id in pending:
#         bot.reply_to(m, "Avval boshqa actionni tugating!")
#         return
#     pending[m.from_user.id] = {"action": "broadcast", "step": 1}
#     bot.reply_to(m, "Barcha foydalanuvchilarga yuboriladigan xabarni yuboring (matn, rasm, video va h.k.).")

# # Matn uchun broadcast
# @bot.message_handler(func=lambda m: m.from_user.id in pending and pending[m.from_user.id]["action"] == "broadcast" and pending[m.from_user.id]["step"] == 1 and m.text)
# def handle_broadcast_text(m):
#     _handle_broadcast(m)

# # Media uchun broadcast
# @bot.message_handler(content_types=['photo', 'video', 'document', 'audio'], func=lambda m: m.from_user.id in pending and pending[m.from_user.id]["action"] == "broadcast" and pending[m.from_user.id]["step"] == 1)
# def handle_broadcast_media(m):
#     _handle_broadcast(m)

# def _handle_broadcast(m):
#     user_id = m.from_user.id
#     if len(users) == 0:
#         bot.reply_to(m, "❌ Foydalanuvchilar ro'yxati bo'sh! Avval foydalanuvchilar /start bosing.")
#         del pending[user_id]
#         return
    
#     sent = 0
#     failed = 0
#     for u in list(users):
#         try:
#             bot.copy_message(u, m.chat.id, m.message_id)
#             sent += 1
#             time.sleep(0.5)  # Rate limit: 30/sec
#         except Exception as e:
#             failed += 1
#             if "chat not found" in str(e).lower() or "blocked" in str(e).lower():
#                 users.discard(u)
#             print(f"Xato {u}: {e}")  # Log uchun
    
#     save_data()  # Users yangilangan bo'lsa
#     del pending[user_id]
#     bot.reply_to(m, f"✅ Xabar yuborildi: {sent} muvaffaqiyatli, {failed} xato. (Jami: {len(users)})")

# # Statistika
# @bot.message_handler(commands=['stats'])
# def stats(m):
#     if not is_admin(m.from_user.id):
#         return
#     reg_users = len(users)
#     movie_count = len(movies)
#     active_users = reg_users  # Faol foydalanuvchilar sifatida ro'yxatdan o'tganlar
#     bot.reply_to(m, f"Statistika:\nRo'yxatdan o'tganlar: {reg_users}\nFoydalanayotganlar: {active_users}\nKinolar soni: {movie_count}")

# # Kino olish
# @bot.message_handler(func=lambda m: not m.text.startswith('/') and check_subscription(m.from_user.id))
# def get_movie(m):
#     code = m.text.strip()
#     if code in movies:
#         bot.send_video(m.chat.id, movies[code]["file_id"], caption=movies[code]["description"])
#     else:
#         bot.reply_to(m, "❌ Kod topilmadi")

# # Obuna bo'lmaganlar
# @bot.message_handler(func=lambda m: not m.text.startswith('/') and not check_subscription(m.from_user.id))
# def unsubscribed(m):
#     start(m)

# bot.infinity_polling()





























import telebot
import os
import psycopg2
from psycopg2.extras import RealDictCursor
import random
import string
import time
import json
import tempfile
import io
import logging

# Logging sozlamalari
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

bot = telebot.TeleBot("7960038374:AAE8oIdCkpqOdU3EDAq1GGC1-f46PjBevPo")
SUPER_ADMIN = 6215236648  # Super admin ID

# PostgreSQL connection
DATABASE_URL = "postgresql://postgres:XXpcjBwTRLctqMyJybrFXNcvnzwgxaRu@postgres.railway.internal:5432/railway")

def get_db_connection():
    if not DATABASE_URL:
        logging.error("DATABASE_URL environment variable not set")
        raise ValueError("DATABASE_URL environment variable not set")
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        logging.error(f"Failed to connect to database: {e}")
        raise

def create_tables():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Jadvallar mavjudligini tekshirish
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'movies'
            );
        """)
        movies_exists = cur.fetchone()[0]
        
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'admins'
            );
        """)
        admins_exists = cur.fetchone()[0]
        
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'channels'
            );
        """)
        channels_exists = cur.fetchone()[0]
        
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'users'
            );
        """)
        users_exists = cur.fetchone()[0]
        
        # Movies table
        if not movies_exists:
            cur.execute("""
                CREATE TABLE movies (
                    id SERIAL PRIMARY KEY,
                    code VARCHAR(3) UNIQUE NOT NULL,
                    file_id TEXT NOT NULL,
                    description TEXT NOT NULL
                );
            """)
            logging.info("Movies table created")
        
        # Admins table
        if not admins_exists:
            cur.execute("""
                CREATE TABLE admins (
                    id SERIAL PRIMARY KEY,
                    user_id BIGINT UNIQUE NOT NULL
                );
            """)
            # Insert super admin
            cur.execute("INSERT INTO admins (user_id) VALUES (%s) ON CONFLICT (user_id) DO NOTHING;", (SUPER_ADMIN,))
            logging.info("Admins table created and super admin inserted")
        
        # Channels table
        if not channels_exists:
            cur.execute("""
                CREATE TABLE channels (
                    id SERIAL PRIMARY KEY,
                    channel_name VARCHAR(255) UNIQUE NOT NULL
                );
            """)
            logging.info("Channels table created")
        
        # Users table
        if not users_exists:
            cur.execute("""
                CREATE TABLE users (
                    id SERIAL PRIMARY KEY,
                    user_id BIGINT UNIQUE NOT NULL
                );
            """)
            logging.info("Users table created")
        
        conn.commit()
        cur.close()
        conn.close()
        logging.info("Tables checked/created successfully")
    except Exception as e:
        logging.error(f"Error creating tables: {e}")
        raise

# Load initial data
try:
    create_tables()
except Exception as e:
    logging.error(f"Failed to initialize database: {e}")
    raise

def save_movie(code, file_id, description):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO movies (code, file_id, description) VALUES (%s, %s, %s) ON CONFLICT (code) DO NOTHING;", (code, file_id, description))
        conn.commit()
        return True
    except Exception as e:
        logging.error(f"Error saving movie: {e}")
        return False
    finally:
        cur.close()
        conn.close()

def get_movie_from_db(code):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("SELECT * FROM movies WHERE code = %s;", (code,))
        result = cur.fetchone()
        return result
    finally:
        cur.close()
        conn.close()

def delete_movie(code):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM movies WHERE code = %s;", (code,))
        conn.commit()
        return cur.rowcount > 0
    finally:
        cur.close()
        conn.close()

def update_movie_code(old_code, new_code):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE movies SET code = %s WHERE code = %s;", (new_code, old_code))
        conn.commit()
        return cur.rowcount > 0
    finally:
        cur.close()
        conn.close()

def update_movie_desc(code, new_desc):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE movies SET description = %s WHERE code = %s;", (new_desc, code))
        conn.commit()
        return cur.rowcount > 0
    finally:
        cur.close()
        conn.close()

def get_all_movies_count():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM movies;")
        count = cur.fetchone()[0]
        return count
    finally:
        cur.close()
        conn.close()

def add_admin(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO admins (user_id) VALUES (%s) ON CONFLICT (user_id) DO NOTHING;", (user_id,))
        conn.commit()
        return True
    except Exception as e:
        logging.error(f"Error adding admin: {e}")
        return False
    finally:
        cur.close()
        conn.close()

def remove_admin(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM admins WHERE user_id = %s;", (user_id,))
        conn.commit()
        return cur.rowcount > 0
    finally:
        cur.close()
        conn.close()

def is_admin(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT 1 FROM admins WHERE user_id = %s;", (user_id,))
        result = cur.fetchone()
        return result is not None
    finally:
        cur.close()
        conn.close()

def add_channel(channel_name):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO channels (channel_name) VALUES (%s) ON CONFLICT (channel_name) DO NOTHING;", (channel_name,))
        conn.commit()
        return True
    except Exception as e:
        logging.error(f"Error adding channel: {e}")
        return False
    finally:
        cur.close()
        conn.close()

def remove_channel(channel_name):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM channels WHERE channel_name = %s;", (channel_name,))
        conn.commit()
        return cur.rowcount > 0
    finally:
        cur.close()
        conn.close()

def get_all_channels():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT channel_name FROM channels;")
        channels = [row[0] for row in cur.fetchall()]
        return channels
    finally:
        cur.close()
        conn.close()

def add_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (user_id) VALUES (%s) ON CONFLICT (user_id) DO NOTHING;", (user_id,))
        conn.commit()
    finally:
        cur.close()
        conn.close()

def get_all_users():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT user_id FROM users;")
        users = set(row[0] for row in cur.fetchall())
        return users
    finally:
        cur.close()
        conn.close()

def remove_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM users WHERE user_id = %s;", (user_id,))
        conn.commit()
    finally:
        cur.close()
        conn.close()

def generate_unique_code(length=3):
    if get_all_movies_count() >= 1000:
        raise ValueError("Kino kodlari tugadi! 3 xonali raqamlar chegarasiga yetdi.")
    attempts = 0
    max_attempts = 100
    while attempts < max_attempts:
        code = ''.join(random.choices(string.digits, k=length))
        if get_movie_from_db(code) is None:
            return code
        attempts += 1
    raise ValueError("Yangi 3 xonali kod topilmadi.")

def check_subscription(user_id):
    channels = get_all_channels()
    if not channels:
        return True
    for channel in channels:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status in ['left', 'kicked', 'restricted']:
                return False
        except:
            return False
    return True

# Download JSON files from PostgreSQL
@bot.message_handler(commands=['download_json'])
def download_json(m):
    if not is_admin(m.from_user.id):
        bot.reply_to(m, "❌ Faqat adminlar JSON fayllarni yuklab olishi mumkin.")
        return
    
    sent = 0
    failed = 0
    
    # Movies
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT code, file_id, description FROM movies;")
        movies_data = {row['code']: {"file_id": row['file_id'], "description": row['description']} for row in cur.fetchall()}
        cur.close()
        conn.close()
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
            json.dump(movies_data, temp_file, indent=2)
            temp_file_path = temp_file.name
        with open(temp_file_path, 'rb') as f:
            bot.send_document(m.chat.id, f, caption="movies.json")
        os.remove(temp_file_path)
        sent += 1
    except Exception as e:
        bot.reply_to(m, f"❌ movies.json yuborishda xato: {str(e)}")
        failed += 1
    
    # Admins
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT user_id FROM admins;")
        admins_data = [row[0] for row in cur.fetchall()]
        cur.close()
        conn.close()
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
            json.dump(admins_data, temp_file, indent=2)
            temp_file_path = temp_file.name
        with open(temp_file_path, 'rb') as f:
            bot.send_document(m.chat.id, f, caption="admins.json")
        os.remove(temp_file_path)
        sent += 1
    except Exception as e:
        bot.reply_to(m, f"❌ admins.json yuborishda xato: {str(e)}")
        failed += 1
    
    # Channels
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT channel_name FROM channels;")
        channels_data = [row[0] for row in cur.fetchall()]
        cur.close()
        conn.close()
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
            json.dump(channels_data, temp_file, indent=2)
            temp_file_path = temp_file.name
        with open(temp_file_path, 'rb') as f:
            bot.send_document(m.chat.id, f, caption="channels.json")
        os.remove(temp_file_path)
        sent += 1
    except Exception as e:
        bot.reply_to(m, f"❌ channels.json yuborishda xato: {str(e)}")
        failed += 1
    
    # Users
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT user_id FROM users;")
        users_data = [row[0] for row in cur.fetchall()]
        cur.close()
        conn.close()
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
            json.dump(users_data, temp_file, indent=2)
            temp_file_path = temp_file.name
        with open(temp_file_path, 'rb') as f:
            bot.send_document(m.chat.id, f, caption="users.json")
        os.remove(temp_file_path)
        sent += 1
    except Exception as e:
        bot.reply_to(m, f"❌ users.json yuborishda xato: {str(e)}")
        failed += 1
    
    bot.reply_to(m, f"✅ JSON fayllar yuborildi: {sent} muvaffaqiyatli, {failed} xato.")

@bot.message_handler(commands=['start'])
def start(m):
    user_id = m.from_user.id
    add_user(user_id)
    
    if check_subscription(user_id):
        bot.reply_to(m, "Xush kelibsiz! 3 xonali kino kodini yozing (masalan, 123).")
    else:
        channels_list = get_all_channels()
        markup = telebot.types.InlineKeyboardMarkup()
        for channel in channels_list:
            markup.add(telebot.types.InlineKeyboardButton(f"Obuna bo'ling: {channel}", url=f"https://t.me/{channel.lstrip('@')}"))
        markup.add(telebot.types.InlineKeyboardButton("Tekshirish", callback_data="check_sub"))
        bot.reply_to(m, "Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_sub_callback(call):
    user_id = call.from_user.id
    if check_subscription(user_id):
        bot.answer_callback_query(call.id, "Obuna tasdiqlandi! 3 xonali kino kodini yozing.")
        bot.edit_message_text("Xush kelibsiz! 3 xonali kino kodini yozing (masalan, 123).", call.message.chat.id, call.message.message_id)
    else:
        bot.answer_callback_query(call.id, "Hali obuna bo'lmagansiz. Iltimos, obuna bo'ling.", show_alert=True)

# Super admin: Admin qo'shish/o'chirish
@bot.message_handler(commands=['add_admin'])
def add_admin_cmd(m):
    if m.from_user.id != SUPER_ADMIN:
        return
    try:
        admin_id = int(m.text.split()[1])
        if add_admin(admin_id):
            bot.reply_to(m, f"Admin qo'shildi: {admin_id}")
        else:
            bot.reply_to(m, "Bu foydalanuvchi allaqachon admin.")
    except:
        bot.reply_to(m, "Foydalanuvchi ID'sini kiriting: /add_admin <ID>")

@bot.message_handler(commands=['remove_admin'])
def remove_admin_cmd(m):
    if m.from_user.id != SUPER_ADMIN:
        return
    try:
        admin_id = int(m.text.split()[1])
        if remove_admin(admin_id):
            bot.reply_to(m, f"Admin o'chirildi: {admin_id}")
        else:
            bot.reply_to(m, "Bu foydalanuvchi admin emas yoki super admin.")
    except:
        bot.reply_to(m, "Foydalanuvchi ID'sini kiriting: /remove_admin <ID>")

# Kanallarni boshqarish
@bot.message_handler(commands=['add_channel'])
def add_channel_cmd(m):
    if not is_admin(m.from_user.id):
        return
    try:
        channel = m.text.split()[1]
        if add_channel(channel):
            bot.reply_to(m, f"Kanal qo'shildi: {channel}")
        else:
            bot.reply_to(m, "Bu kanal allaqachon mavjud.")
    except:
        bot.reply_to(m, "Kanal usernamesini kiriting: /add_channel @channel")

@bot.message_handler(commands=['remove_channel'])
def remove_channel_cmd(m):
    if not is_admin(m.from_user.id):
        return
    try:
        channel = m.text.split()[1]
        if remove_channel(channel):
            bot.reply_to(m, f"Kanal o'chirildi: {channel}")
        else:
            bot.reply_to(m, "Bu kanal mavjud emas.")
    except:
        bot.reply_to(m, "Kanal usernamesini kiriting: /remove_channel @channel")

# Kino qo'shish
@bot.message_handler(commands=['add_movie'])
def add_movie_start(m):
    if not is_admin(m.from_user.id):
        bot.reply_to(m, "❌ Faqat adminlar kino qo'shishi mumkin.")
        return
    pending[m.from_user.id] = {"action": "add_movie", "step": 1, "data": {}}
    bot.reply_to(m, "Kino videosini yuboring (video yoki document sifatida).")

@bot.message_handler(content_types=['video', 'document'])
def handle_movie_video(m):
    user_id = m.from_user.id
    if user_id not in pending or pending[user_id]["action"] != "add_movie" or pending[user_id]["step"] != 1:
        return
    if m.video:
        f = m.video
    elif m.document:
        f = m.document
    else:
        return
    pending[user_id]["data"]["file_id"] = f.file_id
    pending[user_id]["step"] = 2
    bot.reply_to(m, "Endi kino tavsifini yuboring.")

@bot.message_handler(func=lambda m: m.from_user.id in pending and pending[m.from_user.id]["action"] == "add_movie" and pending[m.from_user.id]["step"] == 2)
def handle_movie_desc(m):
    user_id = m.from_user.id
    desc = m.text.strip()
    try:
        code = generate_unique_code()
        if save_movie(code, pending[user_id]["data"]["file_id"], desc):
            del pending[user_id]
            bot.reply_to(m, f"✅ Kino qo'shildi: Kod - {code}\nTavsif: {desc}")
        else:
            bot.reply_to(m, "❌ Kino qo'shishda xato.")
    except ValueError as e:
        bot.reply_to(m, f"❌ Xato: {str(e)}")
    finally:
        if user_id in pending:
            del pending[user_id]

# Kino o'chirish
@bot.message_handler(commands=['delete_movie'])
def delete_movie_cmd(m):
    if not is_admin(m.from_user.id):
        bot.reply_to(m, "❌ Faqat adminlar kino o'chirishi mumkin.")
        return
    try:
        code = m.text.split()[1]
        if delete_movie(code):
            bot.reply_to(m, f"✅ Kino o'chirildi: {code}")
        else:
            bot.reply_to(m, "Kod topilmadi.")
    except:
        bot.reply_to(m, "Kodni kiriting: /delete_movie <code>")

# Kino tahrirlash
@bot.message_handler(commands=['edit_movie'])
def edit_movie_start(m):
    if not is_admin(m.from_user.id):
        bot.reply_to(m, "❌ Faqat adminlar kino tahrirlashi mumkin.")
        return
    try:
        parts = m.text.split(maxsplit=3)
        if len(parts) < 3:
            bot.reply_to(m, "Foydalanish: /edit_movie <old_code> code <new_code> yoki /edit_movie <old_code> desc <new_desc>")
            return
        old_code = parts[1]
        if get_movie_from_db(old_code) is None:
            bot.reply_to(m, "Kod topilmadi.")
            return
        if parts[2] == "code":
            new_code = parts[3]
            if len(new_code) != 3 or not new_code.isdigit():
                bot.reply_to(m, "Yangi kod 3 xonali raqam bo'lishi kerak (masalan, 123).")
                return
            if get_movie_from_db(new_code) is not None:
                bot.reply_to(m, "Yangi kod allaqachon mavjud.")
                return
            if update_movie_code(old_code, new_code):
                bot.reply_to(m, f"✅ Kod o'zgartirildi: {old_code} -> {new_code}")
            else:
                bot.reply_to(m, "❌ Kod o'zgartirishda xato.")
        elif parts[2] == "desc":
            new_desc = parts[3]
            if update_movie_desc(old_code, new_desc):
                bot.reply_to(m, f"✅ Tavsif o'zgartirildi: {old_code}")
            else:
                bot.reply_to(m, "❌ Tavsif o'zgartirishda xato.")
        else:
            bot.reply_to(m, "Noto'g'ri parametr: code yoki desc")
    except:
        bot.reply_to(m, "Xato. Foydalanish: /edit_movie <old_code> code <new_code> yoki /edit_movie <old_code> desc <new_desc>")

# Broadcast
@bot.message_handler(commands=['broadcast'])
def broadcast_start(m):
    if not is_admin(m.from_user.id):
        bot.reply_to(m, "❌ Faqat adminlar broadcast yuborishi mumkin.")
        return
    if m.from_user.id in pending:
        bot.reply_to(m, "Avval boshqa actionni tugating!")
        return
    pending[m.from_user.id] = {"action": "broadcast", "step": 1}
    bot.reply_to(m, "Barcha foydalanuvchilarga yuboriladigan xabarni yuboring (matn, rasm, video va h.k.).")

@bot.message_handler(func=lambda m: m.from_user.id in pending and pending[m.from_user.id]["action"] == "broadcast" and pending[m.from_user.id]["step"] == 1 and m.text)
def handle_broadcast_text(m):
    _handle_broadcast(m)

@bot.message_handler(content_types=['photo', 'video', 'document', 'audio'], func=lambda m: m.from_user.id in pending and pending[m.from_user.id]["action"] == "broadcast" and pending[m.from_user.id]["step"] == 1)
def handle_broadcast_media(m):
    _handle_broadcast(m)

def _handle_broadcast(m):
    user_id = m.from_user.id
    users_set = get_all_users()
    if len(users_set) == 0:
        bot.reply_to(m, "❌ Foydalanuvchilar ro'yxati bo'sh! Avval foydalanuvchilar /start bosing.")
        del pending[user_id]
        return
    
    sent = 0
    failed = 0
    for u in list(users_set):
        try:
            bot.copy_message(u, m.chat.id, m.message_id)
            sent += 1
            time.sleep(0.5)  # Rate limit
        except Exception as e:
            failed += 1
            if "chat not found" in str(e).lower() or "blocked" in str(e).lower():
                remove_user(u)
            logging.error(f"Broadcast error for user {u}: {e}")
    
    del pending[user_id]
    bot.reply_to(m, f"✅ Xabar yuborildi: {sent} muvaffaqiyatli, {failed} xato. (Jami: {len(users_set)})")

# Statistika
@bot.message_handler(commands=['stats'])
def stats(m):
    if not is_admin(m.from_user.id):
        bot.reply_to(m, "❌ Faqat adminlar statistikani ko'rishi mumkin.")
        return
    reg_users = len(get_all_users())
    movie_count = get_all_movies_count()
    active_users = reg_users
    bot.reply_to(m, f"Statistika:\nRo'yxatdan o'tganlar: {reg_users}\nFoydalanayotganlar: {active_users}\nKinolar soni: {movie_count}")

# Kino so'rovlarni qayta ishlash
@bot.message_handler(func=lambda m: not m.text.startswith('/') and check_subscription(m.from_user.id))
def handle_movie_request(m):
    code = m.text.strip()
    movie = get_movie_from_db(code)
    if movie:
        bot.send_video(m.chat.id, movie['file_id'], caption=movie['description'])
    else:
        bot.reply_to(m, "❌ Kod topilmadi")

# Obuna bo'lmaganlar
@bot.message_handler(func=lambda m: not m.text.startswith('/') and not check_subscription(m.from_user.id))
def unsubscribed(m):
    start(m)

# Pending dictni tozalash uchun
pending = {}

bot.infinity_polling()