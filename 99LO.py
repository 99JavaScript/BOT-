import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

BOT_TOKEN = '7066732329:AAGFKVdXxtGGQ7Ok8TxBinJGLhFYmk9T-rQ'  # Token ที่ได้จาก BotFather

# ใส่ chat_id ของกลุ่มที่ต้องการส่งต่อไป
GROUP_CHAT_ID = '-1002489574080,'  # chat_id ของกลุ่ม (แก้ไขจาก tuple)

# ฟังก์ชันเพื่อส่งรูปต่อไปที่กลุ่ม
async def forward_image(update: Update, context: CallbackContext):
    if update.message.photo:
        # เลือกรูปภาพที่มีขนาดใหญ่ที่สุด
        photo = update.message.photo[-1]
        # ส่งรูปภาพไปยังกลุ่ม
        await context.bot.send_photo(chat_id=GROUP_CHAT_ID, photo=photo.file_id)

# ฟังก์ชันเพื่อส่งข้อความไปยังกลุ่ม
async def forward_text(update: Update, context: CallbackContext):
    user_message = update.message.text.strip()

    # ตรวจสอบว่าข้อความมีรูปแบบที่ต้องการหรือไม่
    if is_valid_message(user_message):
        # แบ่งข้อความออกเป็นบรรทัด
        lines = user_message.split("\n")
        updated_message = ""

        # สำหรับแต่ละบรรทัด ตรวจสอบและเพิ่มหัวข้อ
        for line in lines:
            line = line.strip()
            if line:
                updated_message += auto_add_topic(line) + "\n"

        # ส่งข้อความที่ปรับแล้วไปยังกลุ่ม
        await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=updated_message.strip())
    else:
        # ถ้าข้อความไม่ตรงตามรูปแบบที่ต้องการ ไม่ทำอะไร
        pass

# ฟังก์ชันในการตรวจจับเบอร์โทรศัพท์
def extract_phone_number(text: str):
    phone_pattern = r'\d{10}|\d{3}[-.\s]?\d{3}[-.\s]?\d{4}'  # รองรับรูปแบบเบอร์โทร
    match = re.search(phone_pattern, text)
    if match:
        return match.group(0)
    return None

# ฟังก์ชันตรวจสอบว่าข้อความเป็นไปตามรูปแบบที่ต้องการหรือไม่
def is_valid_message(text: str):
    # ตรวจสอบว่าในข้อความมีข้อมูลครบทั้ง 6 หัวข้อหรือไม่
    id_pattern = r'\b\d{6,}\b'  # ID ที่เป็นตัวเลข
    phone_pattern = r'\d{10}'  # เบอร์โทรศัพท์ 10 หลัก
    bank_pattern = r'\b\d{10,}\b'  # เลขบัญชี
    name_pattern = r'[A-Za-zก-ฮ]+\s+[A-Za-zก-ฮ]+'  # ชื่อ-นามสกุล
    deposit_pattern = r'ฝาก\s*\d+'  # ฝาก ตามด้วยตัวเลข
    withdraw_pattern = r'ถอน\s*\d+'  # ถอน ตามด้วยตัวเลข

    # ตรวจสอบว่ามีทั้งหมด 6 หัวข้อหรือไม่
    has_id = re.search(id_pattern, text)
    has_phone = re.search(phone_pattern, text)
    has_bank = re.search(bank_pattern, text)
    has_name = re.search(name_pattern, text)
    has_deposit = re.search(deposit_pattern, text)
    has_withdraw = re.search(withdraw_pattern, text)

    # ถ้าทุกหัวข้อที่เราต้องการมีอยู่ในข้อความ ให้ส่งไป
    return bool(has_id and has_phone and has_bank and has_name and has_deposit and has_withdraw)

# ฟังก์ชันเพื่อแทรกหัวข้อที่เหมาะสมให้กับข้อความที่ไม่มีหัวข้อ
def auto_add_topic(text: str):
    topics = {
        "ID": r"(\d{6,})",  # ถ้าพบเลข 6 หลักเป็น ID
        "Tle": r"\b\d{10}\b",  # ถ้าพบเบอร์โทรศัพท์ 10 หลัก
        "Name": r"\b[A-Za-zก-ฮ]+\s+[A-Za-zก-ฮ]+\b",  # ถ้าพบชื่อคน (ชื่อ-นามสกุล)
        "ธนาคาร": r"\b\d{10,}\b",  # ถ้าพบเลขบัญชี
        "ถอน": r"\bถอน\s*(\d+)",  # ถ้าพบคำว่า ถอน ตามด้วยจำนวนเงิน
        "ฝาก": r"\bฝาก\s*(\d+)"  # ถ้าพบคำว่า ฝาก ตามด้วยจำนวนเงิน
    }

    message = ""

    # ตรวจสอบทุกหัวข้อแล้วเพิ่มข้อความที่พบ
    for topic, pattern in topics.items():
        match = re.search(pattern, text)
        if match:
            message += f"{topic}: {match.group(0)}\n"

    if message:
        return message.strip()  # ส่งข้อความที่มีหัวข้อ
    else:
        return f"ข้อมูลไม่สมบูรณ์: {text}"  # หากไม่พบหัวข้อ ให้ส่งข้อความว่า "ข้อมูลไม่สมบูรณ์" พร้อมข้อมูลที่มี

# ฟังก์ชันเริ่มต้นเมื่อ Bot พร้อมใช้งาน
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("ขอบคุณที่อยู่ด้วยกันนะคะคุณพี่ลุยให้เต็มที่เลยงับ")

def main():
    # สร้าง Application และรับ Token ของ Bot
    application = Application.builder().token(BOT_TOKEN).build()

    # เพิ่ม handler สำหรับคำสั่ง /start
    application.add_handler(CommandHandler("start", start))

    # เพิ่ม handler สำหรับการส่งรูปภาพ
    application.add_handler(MessageHandler(filters.PHOTO, forward_image))

    # เพิ่ม handler สำหรับการส่งข้อความ
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_text))

    # เริ่มรับข้อความจากผู้ใช้
    application.run_polling()

if __name__ == '__main__':
    main()
