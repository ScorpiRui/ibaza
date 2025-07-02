# iBaza Tech Resale Market Telegram Bot

Uzbekistondagi texnologiya qayta sotish bozorlari uchun Telegram bot. Bu bot mijozlarga do'kon joylashuvlarini topish, narxlarni hisoblash va nasiya to'lovlarini hisoblash imkonini beradi.

## 🚀 Xususiyatlar

### 👥 Foydalanuvchilar uchun:
- **🗺️ Xarita xizmatlari**
  - Eng yaqin do'konni topish
  - Barcha do'konlar ro'yxati
  - Joylashuvni xaritada ko'rsatish
- **💰 Narx hisoblagich**
  - Qurilma modelini tanlash
  - Xotira hajmini tanlash
  - Holatni tanlash (yangi, yaxshi, o'rtacha)
  - Narxni ko'rsatish
- **📅 Nasiya hisoblagich**
  - 40% dastlabki to'lov bilan hisoblash
  - 1-8 oylik nasiya rejalari

### ⚙️ Adminlar uchun:
- **🗺️ Xarita boshqaruvi**
  - Yangi do'kon joylashuvini qo'shish
- **💰 Narx boshqaruvi**
  - Yangi qurilma modellarini qo'shish
  - Xotira hajmlari va narxlarni boshqarish

## 📦 O'rnatish

1. **Dasturni yuklab oling:**
```bash
git clone <repository-url>
cd ibaza_bot
```

2. **Kerakli kutubxonalarni o'rnating:**
```bash
pip install -r requirements.txt
```

3. **Konfiguratsiyani sozlang:**
   - `config.py` faylini oching
   - `BOT_TOKEN` ni o'z bot tokeni bilan almashtiring
   - `ADMIN_IDS` ro'yxatiga admin Telegram ID larini qo'shing

```python
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
ADMIN_IDS = [123456789, 987654321]  # Admin Telegram ID lari
```

4. **Botni ishga tushiring:**
```bash
python bot.py
```

## 🔧 Konfiguratsiya

### Bot Token olish:
1. Telegram da @BotFather ga murojaat qiling
2. `/newbot` buyrug'ini yuboring
3. Bot nomi va username ni kiriting
4. Olingan token ni `config.py` ga joylashtiring

### Admin ID ni topish:
1. Telegram da @userinfobot ga murojaat qiling
2. O'z ID ngingizni oling
3. `config.py` dagi `ADMIN_IDS` ro'yxatiga qo'shing

## 📁 Fayl tuzilishi

```
ibaza_bot/
├── bot.py                 # Asosiy bot fayli
├── config.py              # Konfiguratsiya
├── keyboards.py           # Klaviatura modullari
├── utils.py               # Yordamchi funksiyalar
├── requirements.txt       # Kerakli kutubxonalar
├── README.md             # Hujjatlar
├── installment.py        # Nasiya hisoblagich (eski versiya)
└── handlers/
    ├── __init__.py
    ├── user.py           # Foydalanuvchi handerlari
    ├── admin.py          # Admin handerlari
    └── installment.py    # Nasiya handerlari
└── storage/
    ├── locations.json    # Do'kon joylashuvlari
    └── models.json       # Qurilma modellari va narxlari
```

## 🎯 Foydalanish

### Foydalanuvchilar uchun:
1. `/start` buyrug'ini yuboring
2. Kerakli xizmatni tanlang:
   - 🗺️ Xarita - do'kon joylashuvlarini topish
   - 💰 Narx hisoblagich - qurilma narxini hisoblash
   - 📅 Nasiya hisoblagich - nasiya to'lovlarini hisoblash

### Adminlar uchun:
1. `/start` buyrug'ini yuboring
2. "⚙️ Admin panel" tugmasini bosing
3. Kerakli boshqaruv bo'limini tanlang:
   - 🗺️ Xarita boshqaruvi - do'konlar qo'shish
   - 💰 Narx boshqaruvi - modellar va narxlar qo'shish

## 💾 Ma'lumotlar saqlash

Bot ma'lumotlarni JSON formatida saqlaydi:
- `storage/locations.json` - do'kon joylashuvlari
- `storage/models.json` - qurilma modellari va narxlari

## 🔒 Xavfsizlik

- Faqat `ADMIN_IDS` ro'yxatidagi foydalanuvchilar admin funksiyalaridan foydalanishi mumkin
- Barcha ma'lumotlar mahalliy JSON fayllarda saqlanadi
- Bot tokeni xavfsiz saqlanishi kerak

## 🐛 Muammolarni hal qilish

### Bot ishlamayapti:
1. Token to'g'ri kiritilganini tekshiring
2. Internet aloqasini tekshiring
3. `requirements.txt` dagi kutubxonalar o'rnatilganini tekshiring

### Admin funksiyalari ishlamayapti:
1. `config.py` dagi `ADMIN_IDS` ro'yxatini tekshiring
2. Telegram ID to'g'ri kiritilganini tekshiring

### Ma'lumotlar saqlanmayapti:
1. `storage/` papkasi mavjudligini tekshiring
2. Fayl yozish huquqlarini tekshiring

## 📞 Qo'llab-quvvatlash

Muammolar yoki savollar bo'lsa, iltimos bog'laning.
tel:+998934766109

## 📄 Litsenziya

Bu loyiha ochiq manba kodidir. 
