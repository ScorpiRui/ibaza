# Google Sheets Integration Setup Guide

Bu hujjat Google Sheets integratsiyasini sozlash va foydalanish bo'yicha ko'rsatmalarni o'z ichiga oladi.

## 📋 Tarkib

1. [Google Sheets API sozlash](#google-sheets-api-sozlash)
2. [Google Sheets shablonini yaratish](#google-sheets-shablonini-yaratish)
3. [Admin panel orqali boshqarish](#admin-panel-orqali-boshqarish)
4. [Narxlarni yangilash](#narxlarni-yangilash)
5. [Xatoliklarni hal qilish](#xatoliklarni-hal-qilish)

## 🔧 Google Sheets API sozlash

### 1. Google Cloud Console da loyiha yarating

1. [Google Cloud Console](https://console.cloud.google.com/) ga kiring
2. Yangi loyiha yarating yoki mavjud loyihani tanlang
3. Google Sheets API ni yoqing

### 2. Service Account yarating

1. "IAM & Admin" > "Service Accounts" ga o'ting
2. "Create Service Account" tugmasini bosing
3. Service account nomini kiriting (masalan: "ibaza-sheet-api")
4. "Create and Continue" tugmasini bosing
5. "Role" ni "Editor" ga o'rnating
6. "Done" tugmasini bosing

### 3. API kalitini yuklab oling

1. Yaratilgan service account ni tanlang
2. "Keys" bo'limiga o'ting
3. "Add Key" > "Create new key" ni tanlang
4. JSON formatini tanlang va yuklab oling
5. Faylni `ibaza-sheet-api-0455687921f7.json` nomi bilan saqlang

### 4. Google Sheets da ruxsat bering

1. [Google Sheets](https://docs.google.com/spreadsheets/d/1Rw3MW613RW6_4zKgtBWWkPg9bEoyvG68OLTCFbkgTAg/edit?gid=0#gid=0) ga o'ting
2. "Share" tugmasini bosing
3. Service account email manzilini qo'shing (JSON fayldan olish mumkin)
4. "Editor" huquqini bering

## 📊 Google Sheets shablonini yaratish

### Shablon strukturasi

Google Sheets da quyidagi ustunlar bo'lishi kerak:

| A | B | C | D | E | F |
|---|---|---|---|---|---|
| Model | Memory (GB) | Ideal($) | Yaxshi($) | Ortacha($) | Notes |
| iPhone 15 Pro | 128 | 1200 | 1000 | 800 | |
| iPhone 15 Pro | 256 | 1350 | 1150 | 950 | |

### Xotira hajmlari

- **64 GB** - `64`
- **128 GB** - `128`
- **256 GB** - `256`
- **512 GB** - `512`
- **1 TB** - `1TB` yoki `1024`

### Narxlar

- **Ideal($)** - Yangi qurilma narxi (USD)
- **Yaxshi($)** - Yaxshi holatdagi qurilma narxi (USD)
- **Ortacha($)** - O'rtacha holatdagi qurilma narxi (USD)

## ⚙️ Admin panel orqali boshqarish

### 1. Admin panelga kirish

1. Bot da `/start` buyrug'ini yuboring
2. "⚙️ Admin panel" tugmasini bosing
3. "💰 Narx boshqaruvi" ni tanlang

### 2. Google Sheets ga o'tish

1. "📊 Google Sheets da narxlarni boshqarish" tugmasini bosing
2. Google Sheets ochiladi
3. Modellar va narxlarni tahrirlang

### 3. Narxlarni yangilash

1. Google Sheets da o'zgarishlar kiritganingizdan so'ng
2. Bot ga qaytib keling
3. "🔄 Narxlarni yangilash" tugmasini bosing
4. O'zgarishlar botga yuklanadi

## 🔄 Narxlarni yangilash

### Avtomatik yangilash

Bot har safar narx hisoblagich ishlatilganda Google Sheets dan yangi ma'lumotlarni oladi.

### Qo'lda yangilash

Admin panel orqali "🔄 Narxlarni yangilash" tugmasini bosib narxlarni yangilashingiz mumkin.

## 🐛 Xatoliklarni hal qilish

### Xatolik: "Failed to initialize Google Sheets service"

**Sababi:** API kaliti noto'g'ri yoki Google Sheets API yoqilmagan

**Yechim:**
1. JSON fayl to'g'ri joyda ekanligini tekshiring
2. Google Cloud Console da Google Sheets API yoqilganini tekshiring
3. Service account huquqlarini tekshiring

### Xatolik: "No models found in Google Sheets"

**Sababi:** Google Sheets bo'sh yoki noto'g'ri formatda

**Yechim:**
1. Google Sheets da ma'lumotlar borligini tekshiring
2. Shablon strukturasi to'g'ri ekanligini tekshiring
3. Service account ga ruxsat berilganini tekshiring

### Xatolik: "Failed to refresh prices"

**Sababi:** Internet aloqasi yoki API muammosi

**Yechim:**
1. Internet aloqasini tekshiring
2. Google Sheets ga kirish imkoniyatini tekshiring
3. API kalitini yangilang

## 📝 Foydalanish bo'yicha maslahatlar

### 1. Narxlarni kiritish

- Narxlarni USD da kiriting (masalan: 1200)
- Vergul yoki nuqta ishlatmang
- Faqat raqamlar ishlating
- Dollar belgisi ($) avtomatik qo'shiladi

### 2. Model nomlari

- Model nomlarini aniq kiriting
- Katta-kichik harflarga e'tibor bering
- Bir xil model nomlarini takrorlamang

### 3. Xotira hajmlari

- 1 TB uchun `1TB` yoki `1024` ishlating
- Boshqa hajmlar uchun raqam ishlating (64, 128, 256, 512)

### 4. Tekshirish

- Narxlarni kiritganingizdan so'ng bot da sinab ko'ring
- Xatoliklar bo'lsa Google Sheets ni tekshiring
- Format to'g'ri ekanligini tekshiring

## 🔒 Xavfsizlik

### API kalitini himoyalash

- JSON faylni hech kimga bermang
- Git repository ga qo'shmang
- Xavfsiz joyda saqlang

### Ruxsatlar

- Service account ga faqat kerakli huquqlarni bering
- Google Sheets ni public qilmang
- Muntazam ravishda ruxsatlarni tekshiring

## 📞 Yordam

Muammolar bo'lsa:

1. Log fayllarini tekshiring
2. Google Cloud Console da xatoliklarni ko'ring
3. Google Sheets da ma'lumotlarni tekshiring
4. Bot administratoriga murojaat qiling 