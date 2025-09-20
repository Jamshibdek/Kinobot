# import telebot
# import os
# import json
# import random
# import string
# import time  # Rate limiting uchun

# bot = telebot.TeleBot("7454505092:AAE4SOvZ5nG-RlY8DfN3xXZBnNSyvazxgck")
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
import json
import random
import string
import time

bot = telebot.TeleBot("7960038374:AAE8oIdCkpqOdU3EDAq1GGC1-f46PjBevPo")
SUPER_ADMIN = 6215236648  # Super admin ID

# Load data from JSON
try:
    movies = json.load(open("movies.json"))
except:
    movies = {}  # Format: {"code": {"file_id": "telegram_file_id", "description": "desc"}}

try:
    admins = json.load(open("admins.json"))
except:
    admins = [SUPER_ADMIN]  # Adminlar ro'yxati

try:
    channels = json.load(open("channels.json"))
except:
    channels = []  # Kanallar ro'yxati (e.g., "@channel")

try:
    users = set(json.load(open("users.json")))
except:
    users = set()  # Foydalanuvchilar ro'yxati

# Pending actions
pending = {}  # {user_id: {"action": "add_movie", "step": 1, "data": {}}}

def save_data():
    json.dump(movies, open("movies.json", "w"))
    json.dump(admins, open("admins.json", "w"))
    json.dump(channels, open("channels.json", "w"))
    json.dump(list(users), open("users.json", "w"))

def generate_unique_code(length=3):
    if len(movies) >= 1000:  # 000-999 gacha 1000 ta imkoniyat
        raise ValueError("Kino kodlari tugadi! 3 xonali raqamlar chegarasiga yetdi.")
    attempts = 0
    max_attempts = 100
    while attempts < max_attempts:
        code = ''.join(random.choices(string.digits, k=length))  # Faqat raqamlar
        if code not in movies:
            return code
        attempts += 1
    raise ValueError("Yangi 3 xonali kod topilmadi. Iltimos, boshqa uzunlik sinab ko'ring.")

def is_admin(user_id):
    return user_id in admins

def check_subscription(user_id):
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

@bot.message_handler(commands=['start'])
def start(m):
    user_id = m.from_user.id
    users.add(user_id)
    save_data()
    
    if check_subscription(user_id):
        bot.reply_to(m, "Xush kelibsiz! Kino kodini yozing.")
    else:
        markup = telebot.types.InlineKeyboardMarkup()
        for channel in channels:
            markup.add(telebot.types.InlineKeyboardButton(f"Obuna bo'ling: {channel}", url=f"https://t.me/{channel.lstrip('@')}"))
        markup.add(telebot.types.InlineKeyboardButton("Tekshirish", callback_data="check_sub"))
        bot.reply_to(m, "Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_sub_callback(call):
    user_id = call.from_user.id
    if check_subscription(user_id):bot.answer_callback_query(call.id, "Obuna tasdiqlandi! Kino kodini yozing.")
        bot.edit_message_text("Xush 
        kelibsiz! Kino kodini yozing.", call.message.chat.id, call.message.message_id)
    else:
        bot.answer_callback_query(call.id, "Hali obuna bo'lmagansiz. Iltimos, obuna bo'ling.", show_alert=True)

# Super admin: Admin qo'shish/o'chirish
@bot.message_handler(commands=['add_admin'])
def add_admin(m):
    if m.from_user.id != SUPER_ADMIN:
        return
    try:
        admin_id = int(m.text.split()[1])
        if admin_id not in admins:
            admins.append(admin_id)
            save_data()
            bot.reply_to(m, f"Admin qo'shildi: {admin_id}")
        else:
            bot.reply_to(m, "Bu foydalanuvchi allaqachon admin.")
    except:
        bot.reply_to(m, "Foydalanuvchi ID'sini kiriting: /add_admin <ID>")

@bot.message_handler(commands=['remove_admin'])
def remove_admin(m):
    if m.from_user.id != SUPER_ADMIN:
        return
    try:
        admin_id = int(m.text.split()[1])
        if admin_id in admins and admin_id != SUPER_ADMIN:
            admins.remove(admin_id)
            save_data()
            bot.reply_to(m, f"Admin o'chirildi: {admin_id}")
        else:
            bot.reply_to(m, "Bu foydalanuvchi admin emas yoki super admin.")
    except:
        bot.reply_to(m, "Foydalanuvchi ID'sini kiriting: /remove_admin <ID>")

# Kanallarni boshqarish
@bot.message_handler(commands=['add_channel'])
def add_channel(m):
    if not is_admin(m.from_user.id):
        return
    try:
        channel = m.text.split()[1]
        if channel not in channels:
            channels.append(channel)
            save_data()
            bot.reply_to(m, f"Kanal qo'shildi: {channel}")
        else:
            bot.reply_to(m, "Bu kanal allaqachon mavjud.")
    except:
        bot.reply_to(m, "Kanal usernamesini kiriting: /add_channel @channel")

@bot.message_handler(commands=['remove_channel'])
def remove_channel(m):
    if not is_admin(m.from_user.id):
        return
    try:
        channel = m.text.split()[1]
        if channel in channels:
            channels.remove(channel)
            save_data()
            bot.reply_to(m, f"Kanal o'chirildi: {channel}")
        else:
            bot.reply_to(m, "Bu kanal mavjud emas.")
    except:
        bot.reply_to(m, "Kanal usernamesini kiriting: /remove_channel @channel")

# Kino qo'shish
@bot.message_handler(commands=['add_movie'])
def add_movie_start(m):
    if not is_admin(m.from_user.id):
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
        movies[code] = {"file_id": pending[user_id]["data"]["file_id"], "description": desc}
        save_data()
        del pending[user_id]
        bot.reply_to(m, f"✅ Kino qo'shildi: Kod - {code}\nTavsif: {desc}")
    except ValueError as e:
        bot.reply_to(m, f"❌ Xato: {str(e)}")
        del pending[user_id]

# Kino o'chirish
@bot.message_handler(commands=['delete_movie'])
def delete_movie(m):
    if not is_admin(m.from_user.id):
        return
    try:
        code = m.text.split()[1]
        if code in movies:
            del movies[code]
            save_data()
            bot.reply_to(m, f"✅ Kino o'chirildi: {code}")
        else:
            bot.reply_to(m, "Kod topilmadi.")
    except:
        bot.reply_to(m, "Kodni kiriting: /delete_movie <code>")

# Kino tahrirlash
@bot.message_handler(commands=['edit_movie'])
def edit_movie_start(m):
    if not is_admin(m.from_user.id):
        return
    try:
        parts = m.text.split(maxsplit=3)
        if len(parts) < 3:
            bot.reply_to(m, "Foydalanish: /edit_movie <old_code> code <new_code> yoki /edit_movie <old_code> desc <new_desc>")
            return
        old_code = parts[1]
        if old_code not in movies:
            bot.reply_to(m, "Kod topilmadi.")
            return
        if parts[2] == "code":
            new_code = parts[3]
            if new_code in movies:
                bot.reply_to(m, "Yangi kod allaqachon mavjud.")
                return
            try:
                if len(new_code) != 3 or not new_code.isdigit():
                    bot.reply_to(m, "Yangi kod 3 xonali raqam bo'lishi kerak (masalan, 123).")
                    return
                movies[new_code] = movies.pop(old_code)
                save_data()
                bot.reply_to(m, f"✅ Kod o'zgartirildi: {old_code} -> {new_code}")
            except ValueError as e:
                bot.reply_to(m, f"❌ Xato: {str(e)}")
        elif parts[2] == "desc":
            new_desc = parts[3]
            movies[old_code]["description"] = new_desc
            save_data()
            bot.reply_to(m, f"✅ Tavsif o'zgartirildi: {old_code}")
        else:
            bot.reply_to(m, "Noto'g'ri parametr: code yoki desc")
    except:
        bot.reply_to(m, "Xato. Foydalanish: /edit_movie <old_code> code <new_code> yoki /edit_movie <old_code> desc <new_desc>")

# Broadcast
@bot.message_handler(commands=['broadcast'])
def broadcast_start(m):
    if not is_admin(m.from_user.id):
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
    if len(users) == 0:
        bot.reply_to(m, "❌ Foydalanuvchilar ro'yxati bo'sh! Avval foydalanuvchilar /start bosing.")
        del pending[user_id]
        return
    
    sent = 0
    failed = 0
    for u in list(users):
        try:
            bot.copy_message(u, m.chat.id, m.message_id)
            sent += 1
            time.sleep(0.5)  # Rate limit: 30/sec
        except Exception as e:
            failed += 1
            if "chat not found" in str(e).lower() or "blocked" in str(e).lower():
                users.discard(u)
            print(f"Xato {u}: {e}")  # Log uchun
    
    save_data()
    del pending[user_id]
    bot.reply_to(m, f"✅ Xabar yuborildi: {sent} muvaffaqiyatli, {failed} xato. (Jami: {len(users)})")

# Statistika
@bot.message_handler(commands=['stats'])
def stats(m):
    if not is_admin(m.from_user.id):
        return
    reg_users = len(users)
    movie_count = len(movies)
    active_users = reg_users
    bot.reply_to(m, f"Statistika:\nRo'yxatdan o'tganlar: {reg_users}\nFoydalanayotganlar: {active_users}\nKinolar soni: {movie_count}")

# JSON fayllarni yuklab berish
@bot.message_handler(commands=['download_json'])
def download_json(m):
    if not is_admin(m.from_user.id):
        bot.reply_to(m, "❌ Faqat adminlar JSON fayllarni yuklab olishi mumkin.")
        return
    
    json_files = ["movies.json", "admins.json", "channels.json", "users.json"]
    sent = 0
    failed = 0
    
    for file_name in json_files:
        try:
            if os.path.exists(file_name):
                with open(file_name, 'rb') as f:
                    bot.send_document(m.chat.id, f, caption=f"{file_name} fayli")
                sent += 1
            else:
                failed += 1
                bot.reply_to(m, f"❌ {file_name} fayli topilmadi.")
        except Exception as e:
            failed += 1
            bot.reply_to(m, f"❌ {file_name} yuborishda xato: {str(e)}")
    
    bot.reply_to(m, f"✅ JSON fayllar yuborildi: {sent} muvaffaqiyatli, {failed} xato.")

# Kino olish
@bot.message_handler(func=lambda m: not m.text.startswith('/') and check_subscription(m.from_user.id))
def get_movie(m):
    code = m.text.strip()
    if code in movies:
        bot.send_video(m.chat.id, movies[code]["file_id"], caption=movies[code]["description"])
    else:
        bot.reply_to(m, "❌ Kod topilmadi")

# Obuna bo'lmaganlar
@bot.message_handler(func=lambda m: not m.text.startswith('/') and not check_subscription(m.from_user.id))
def unsubscribed(m):
    start(m)

bot.infinity_polling()