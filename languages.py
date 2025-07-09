"""
Language configuration for iBaza bot
Supports Uzbek (uz), Russian (ru), and English (eng)
"""

# Language codes
LANGUAGES = {
    'uz': '🇺🇿 O\'zbekcha',
    'ru': '🇷🇺 Русский', 
    'eng': '🇺🇸 English'
}

# Translations for all static content
TRANSLATIONS = {
    'uz': {
        # Welcome messages
        'welcome_title': '🏪 **iBaza** telefon va gadgetlar olamiga xush kelibsiz',
        'welcome_description': 'Biz sizga eng yaxshi texnologik mahsulotlarni xarid qilishda quyidagi xizmatlarni taklif qilamiz:',
        'welcome_services': [
            'Qayerdan va qanday qilib eng yaxshi narxlarda xarid qilish',
            'Nasiya (muddatli to\'lov) asosida xarid qilish imkoniyati',
            'Telefon va boshqa qurilmalar narxini aniqlab berish'
        ],
        'welcome_footer': 'Sifatli, qulay va ishonchli xizmatlar biz bilan!',
        
        # Main menu buttons
        'menu_map': '🗺️ Do\'konlar xaritasi',
        'menu_price_calculator': '💰 Telefonimni narxla',
        'menu_call_center': '📞 Call center',
        'menu_admin_contact': '👨‍💼 Admin bilan bog\'lanish',
        'menu_admin_panel': '⚙️ Admin panel',
        
        # Map section
        'map_title': '🗺️ **Do\'konlar xaritasi**',
        'map_description': 'Eng yaqin do\'konimizni topish yoki barcha joylashuvlarni ko\'rish uchun tanlang:',
        'nearest_location': '📍 Eng yaqin joylashuvni topish',
        'all_locations': '📋 Barcha do\'konlar',
        'share_location_prompt': '📍 **Eng yaqin joylashuvni topish**\n\nIltimos, o\'z joylashuvingizni yuboring:',
        'nearest_store_title': '📍 **Eng yaqin do\'konimiz:**',
        'store_name': '🏪 **{name}**',
        'store_address': '📍 **Manzil:** {address}',
        'store_distance': '📏 **Masofa:** {distance}',
        'store_image_available': '🖼️ **Rasm:** Mavjud',
        'store_image_not_available': '🖼️ **Rasm:** Mavjud emas',
        'view_on_map': 'Joylashuvni xaritada ko\'rish uchun tugmani bosing:',
        'all_stores_title': '📋 **Barcha do\'konlarimiz:**',
        'select_store': 'Kerakli do\'konni tanlang:',
        'no_stores_found': '❌ Kechirasiz, hozirda hech qanday do\'kon topilmadi.',
        'store_not_found': '❌ Do\'kon topilmadi!',
        'location_sent': '📍 Joylashuv yuborildi!',
        'error_occurred': '❌ Xatolik yuz berdi!',
        'return_to_menu': '🏪 Asosiy menyuga qaytish uchun tugmani bosing:',
        
        # Price calculator
        'price_calculator_title': '💰 **Telefonimni narxla**',
        'select_model': 'Qurilma modelini tanlang:',
        'model_selected': '📱 **{name}** tanlandi',
        'select_memory': 'Xotira hajmini tanlang:',
        'memory_selected': '💾 **{memory}** tanlandi',
        'condition_info_title': '📱 **Telefon holati haqida ma\'lumot:**',
        'condition_new': '🆕 **Ideal** - Telefon 95% da baland batareya sig\'imiga ega bo\'lishi va hech qanday shilingan va cho\'qilgan joylari bo\'lmasligi shart',
        'condition_good': '✅ **Yaxshi** - Batareya sig\'imi 85-95% bo\'lishi mumkin, ekran toza bo\'lishi kerak, telefonda shilingan joylari bo\'lish mumkin',
        'condition_fair': '🔄 **O\'rtacha** - Batareya sig\'imi 85% dan past bo\'lishi mumkin, ekranda va telefonda shilingan joylari bo\'lish mumkin',
        'got_it': '✅ Tanishib chiqdim',
        'back': '🔙 Orqaga',
        'select_condition': 'Qurilma holatini tanlang:',
        'price_result_title': '💰 **Narx hisoblagich natijasi**',
        'price_model': '📱 **Model:** {model}',
        'price_memory': '💾 **Xotira:** {memory}',
        'price_condition': '📊 **Holat:** {condition}',
        'price_amount': '💵 **Narx:** {price}',
        'additional_info_title': '📋 **Qo\'shimcha ma\'lumot:**',
        'additional_info': [
            'Bu bozorning o\'rtacha narxidir',
            'Telefon qutisi borligini hisobga olgan holda',
            'Qutisi yo\'q bo\'lsa narx biroz past bo\'lishi mumkin',
            'Rang va mintaqa ham narxga ta\'sir qilishi mumkin'
        ],
        'contact_for_details': '📞 Batafsil ma\'lumot uchun biz bilan bog\'laning!',
        'no_models_available': '❌ Kechirasiz, hozirda hech qanday model mavjud emas.',
        'model_not_found': '❌ Model topilmadi!',
        'memory_not_found': '❌ Xotira hajmi topilmadi!',
        'condition_not_found': '❌ Bu holat uchun narx topilmadi!',
        'error_restart': '❌ Xatolik yuz berdi! Qaytadan boshlang.',
        
        # Call center
        'call_center_title': '📞 **O\'zbekistonda yagona call center**',
        'call_center_description': 'Biz sizga quyidagi xizmatlarni taklif qilamiz:',
        'call_center_services': [
            'Qayirdan telefon kere bosa topib berish',
            'Vodiy bo\'ylab eng arzonlarni topib berish',
            'Har qanday gadget aksessuarlarini topib berish'
        ],
        'call_center_phone': '📱 **Telefon:** +998330170555',
        'call_center_hours': '⏰ **Ish vaqti:** 09:00 - 18:00',
        'call_center_days': '🌍 **Dushanba - Shanba**',
        'call_center_footer': 'Sizga yordam berishdan xursand bo\'lamiz!',
        'phone_copied': '📞 Call center raqami nusxalandi!',
        
        # Admin contact
        'admin_contact_title': '👨‍💼 **Admin bilan bog\'lanish**',
        'admin_contact_description': 'Savollaringiz yoki takliflaringiz bo\'lsa:',
        'admin_telegram': '📱 **Telegram:** @ibazacallcenter',
        'admin_phone': '📞 **Telefon:** +998330170555',
        'admin_footer': 'Admin sizga tez orada javob beradi!',
        'admin_info_shown': '👨‍💼 Admin ma\'lumotlari ko\'rsatildi!',
        
        # Admin panel
        'admin_panel_title': '⚙️ **Admin panel**',
        'admin_panel_description': 'Do\'konlar va narxlarni boshqarish uchun tanlang:',
        'admin_map_management': '🗺️ Xarita boshqaruvi',
        'admin_price_management': '💰 Narx boshqaruvi',
        'admin_map_title': '🗺️ **Xarita boshqaruvi**',
        'admin_map_description': 'Do\'kon joylashuvlarini boshqarish:',
        'add_location': '➕ Joylashuv qo\'shish',
        'add_location_title': '➕ **Yangi joylashuv qo\'shish**',
        'enter_store_name': 'Do\'kon nomini kiriting:',
        'name_entered': '✅ **Nom:** {name}',
        'enter_store_address': 'Endi do\'kon manzilini kiriting:',
        'address_entered': '✅ **Manzil:** {address}',
        'share_store_location': 'Endi do\'kon joylashuvini yuboring:',
        'coordinates_received': '✅ **Koordinatalar:** {lat}, {lon}',
        'upload_store_image': 'Endi do\'kon rasmini yuboring (ixtiyoriy):',
        'location_saved_title': '✅ **Joylashuv muvaffaqiyatli qo\'shildi!**',
        'location_name': '🏪 **Nomi:** {name}',
        'location_coordinates': '📍 **Koordinatalar:** {lat}, {lon}',
        'image_added': '🖼️ **Rasm:** Qo\'shildi',
        'image_not_added': '🖼️ **Rasm:** Qo\'shilmagan',
        'location_save_error': '❌ Xatolik yuz berdi! Joylashuv saqlanmadi.',
        'no_permission': '❌ Ruxsat yo\'q!',
        'please_enter_name': '❌ Iltimos, do\'kon nomini kiriting!',
        'please_enter_address': '❌ Iltimos, do\'kon manzilini kiriting!',
        'please_share_location': '❌ Iltimos, joylashuvni yuboring!',
        'error_restart_admin': '❌ Xatolik yuz berdi! Qaytadan boshlang.',
        
        # Price management
        'price_management_title': '💰 **Narx boshqaruvi**',
        'price_management_description': '📊 **Google Sheets orqali boshqarish:**',
        'price_management_features': [
            'Modellar va narxlarni qo\'shish',
            'Mavjud narxlarni tahrirlash',
            'Narxlarni o\'chirish'
        ],
        'refresh_prices_description': '🔄 **Narxlarni yangilash** tugmasini bosib, Google Sheets dagi o\'zgarishlarni botga yuklang.',
        'manage_prices_sheets': '📊 Google Sheets da narxlarni boshqarish',
        'refresh_prices': '🔄 Narxlarni yangilash',
        'prices_refreshing': '🔄 Narxlar yangilanmoqda...',
        'prices_refreshed': '✅ **Narxlar muvaffaqiyatli yangilandi!**',
        'total_models': '📱 **Jami modellar:** {count} ta',
        'prices_refresh_description': 'Google Sheets dagi barcha o\'zgarishlar botga yuklandi.',
        'sheets_error': '❌ Google Sheets dan ma\'lumotlarni olishda xatolik yuz berdi!',
        'refresh_error': '❌ Narxlarni yangilashda xatolik yuz berdi!',
        
        # Common buttons
        'cancel': '❌ Bekor qilish',
        'back_to_admin': '⬅️ Orqaga',
        'menu': 'Menu',
        'menu_emoji': '🏪 Menu',
        
        # Language selection
        'select_language': '🌍 **Tilni tanlang**\n\nIltimos, o\'zingizga qulay tilni tanlang:',
        'language_selected': '✅ Til tanlandi: {language}',
        'welcome_with_language': '🏪 **iBaza** telefon va gadgetlar olamiga xush kelibsiz\n\nTil: {language}',
        
        # Error messages
        'image_load_error': '⚠️ Rasm yuklanishida xatolik yuz berdi!',
        'general_error': '❌ Xatolik yuz berdi!',
    },
    
    'ru': {
        # Welcome messages
        'welcome_title': '🏪 **iBaza** - добро пожаловать в мир телефонов и гаджетов',
        'welcome_description': 'Мы предлагаем вам следующие услуги для покупки лучших технологических продуктов:',
        'welcome_services': [
            'Где и как купить по лучшим ценам',
            'Возможность покупки в рассрочку',
            'Определение цены телефонов и других устройств'
        ],
        'welcome_footer': 'Качественные, удобные и надежные услуги с нами!',
        
        # Main menu buttons
        'menu_map': '🗺️ Карта магазинов',
        'menu_price_calculator': '💰 Оценить мой телефон',
        'menu_call_center': '📞 Call center',
        'menu_admin_contact': '👨‍💼 Связаться с админом',
        'menu_admin_panel': '⚙️ Панель администратора',
        
        # Map section
        'map_title': '🗺️ **Карта магазинов**',
        'map_description': 'Выберите для поиска ближайшего магазина или просмотра всех местоположений:',
        'nearest_location': '📍 Найти ближайшее место',
        'all_locations': '📋 Все магазины',
        'share_location_prompt': '📍 **Поиск ближайшего места**\n\nПожалуйста, отправьте ваше местоположение:',
        'nearest_store_title': '📍 **Ближайший магазин:**',
        'store_name': '🏪 **{name}**',
        'store_address': '📍 **Адрес:** {address}',
        'store_distance': '📏 **Расстояние:** {distance}',
        'store_image_available': '🖼️ **Фото:** Доступно',
        'store_image_not_available': '🖼️ **Фото:** Недоступно',
        'view_on_map': 'Нажмите кнопку, чтобы посмотреть на карте:',
        'all_stores_title': '📋 **Все наши магазины:**',
        'select_store': 'Выберите нужный магазин:',
        'no_stores_found': '❌ Извините, в данный момент магазины не найдены.',
        'store_not_found': '❌ Магазин не найден!',
        'location_sent': '📍 Местоположение отправлено!',
        'error_occurred': '❌ Произошла ошибка!',
        'return_to_menu': '🏪 Нажмите кнопку, чтобы вернуться в главное меню:',
        
        # Price calculator
        'price_calculator_title': '💰 **Оценить мой телефон**',
        'select_model': 'Выберите модель устройства:',
        'model_selected': '📱 **{name}** выбрано',
        'select_memory': 'Выберите объем памяти:',
        'memory_selected': '💾 **{memory}** выбрано',
        'condition_info_title': '📱 **Информация о состоянии телефона:**',
        'condition_new': '🆕 **Идеальное** - Телефон должен иметь емкость батареи 95%+ и не иметь никаких царапин и вмятин',
        'condition_good': '✅ **Хорошее** - Емкость батареи может быть 85-95%, экран должен быть чистым, на телефоне могут быть царапины',
        'condition_fair': '🔄 **Среднее** - Емкость батареи может быть менее 85%, на экране и телефоне могут быть царапины',
        'got_it': '✅ Понятно',
        'back': '🔙 Назад',
        'select_condition': 'Выберите состояние устройства:',
        'price_result_title': '💰 **Результат оценки**',
        'price_model': '📱 **Модель:** {model}',
        'price_memory': '💾 **Память:** {memory}',
        'price_condition': '📊 **Состояние:** {condition}',
        'price_amount': '💵 **Цена:** {price}',
        'additional_info_title': '📋 **Дополнительная информация:**',
        'additional_info': [
            'Это средняя рыночная цена',
            'Учитывается наличие коробки телефона',
            'Цена может быть немного ниже, если коробки нет',
            'Цвет и регион также влияют на цену'
        ],
        'contact_for_details': '📞 Для подробной информации свяжитесь с нами!',
        'no_models_available': '❌ Извините, в данный момент модели недоступны.',
        'model_not_found': '❌ Модель не найдена!',
        'memory_not_found': '❌ Объем памяти не найден!',
        'condition_not_found': '❌ Цена для этого состояния не найдена!',
        'error_restart': '❌ Произошла ошибка! Начните заново.',
        
        # Call center
        'call_center_title': '📞 **Единственный call center в Узбекистане**',
        'call_center_description': 'Мы предлагаем вам следующие услуги:',
        'call_center_services': [
            'Найти телефон где угодно',
            'Найти самые дешевые по всей долине',
            'Найти любые аксессуары для гаджетов'
        ],
        'call_center_phone': '📱 **Телефон:** +998330170555',
        'call_center_hours': '⏰ **Время работы:** 09:00 - 18:00',
        'call_center_days': '🌍 **Понедельник - Суббота**',
        'call_center_footer': 'Мы рады помочь вам!',
        'phone_copied': '📞 Номер call center скопирован!',
        
        # Admin contact
        'admin_contact_title': '👨‍💼 **Связаться с администратором**',
        'admin_contact_description': 'Если у вас есть вопросы или предложения:',
        'admin_telegram': '📱 **Telegram:** @ibazacallcenter',
        'admin_phone': '📞 **Телефон:** +998330170555',
        'admin_footer': 'Администратор ответит вам в ближайшее время!',
        'admin_info_shown': '👨‍💼 Информация об администраторе показана!',
        
        # Admin panel
        'admin_panel_title': '⚙️ **Панель администратора**',
        'admin_panel_description': 'Выберите для управления магазинами и ценами:',
        'admin_map_management': '🗺️ Управление картой',
        'admin_price_management': '💰 Управление ценами',
        'admin_map_title': '🗺️ **Управление картой**',
        'admin_map_description': 'Управление местоположениями магазинов:',
        'add_location': '➕ Добавить местоположение',
        'add_location_title': '➕ **Добавить новое местоположение**',
        'enter_store_name': 'Введите название магазина:',
        'name_entered': '✅ **Название:** {name}',
        'enter_store_address': 'Теперь введите адрес магазина:',
        'address_entered': '✅ **Адрес:** {address}',
        'share_store_location': 'Теперь отправьте местоположение магазина:',
        'coordinates_received': '✅ **Координаты:** {lat}, {lon}',
        'upload_store_image': 'Теперь отправьте фото магазина (необязательно):',
        'location_saved_title': '✅ **Местоположение успешно добавлено!**',
        'location_name': '🏪 **Название:** {name}',
        'location_coordinates': '📍 **Координаты:** {lat}, {lon}',
        'image_added': '🖼️ **Фото:** Добавлено',
        'image_not_added': '🖼️ **Фото:** Не добавлено',
        'location_save_error': '❌ Произошла ошибка! Местоположение не сохранено.',
        'no_permission': '❌ Нет разрешения!',
        'please_enter_name': '❌ Пожалуйста, введите название магазина!',
        'please_enter_address': '❌ Пожалуйста, введите адрес магазина!',
        'please_share_location': '❌ Пожалуйста, отправьте местоположение!',
        'error_restart_admin': '❌ Произошла ошибка! Начните заново.',
        
        # Price management
        'price_management_title': '💰 **Управление ценами**',
        'price_management_description': '📊 **Управление через Google Sheets:**',
        'price_management_features': [
            'Добавление моделей и цен',
            'Редактирование существующих цен',
            'Удаление цен'
        ],
        'refresh_prices_description': '🔄 Нажмите кнопку **Обновить цены**, чтобы загрузить изменения из Google Sheets в бота.',
        'manage_prices_sheets': '📊 Управление ценами в Google Sheets',
        'refresh_prices': '🔄 Обновить цены',
        'prices_refreshing': '🔄 Обновление цен...',
        'prices_refreshed': '✅ **Цены успешно обновлены!**',
        'total_models': '📱 **Всего моделей:** {count} шт.',
        'prices_refresh_description': 'Все изменения из Google Sheets загружены в бота.',
        'sheets_error': '❌ Ошибка при получении данных из Google Sheets!',
        'refresh_error': '❌ Ошибка при обновлении цен!',
        
        # Common buttons
        'cancel': '❌ Отмена',
        'back_to_admin': '⬅️ Назад',
        'menu': 'Menu',
        'menu_emoji': '🏪 Menu',
        
        # Language selection
        'select_language': '🌍 **Выберите язык**\n\nПожалуйста, выберите удобный для вас язык:',
        'language_selected': '✅ Язык выбран: {language}',
        'welcome_with_language': '🏪 **iBaza** - добро пожаловать в мир телефонов и гаджетов\n\nЯзык: {language}',
        
        # Error messages
        'image_load_error': '⚠️ Ошибка при загрузке изображения!',
        'general_error': '❌ Произошла ошибка!',
    },
    
    'eng': {
        # Welcome messages
        'welcome_title': '🏪 **iBaza** - welcome to the world of phones and gadgets',
        'welcome_description': 'We offer you the following services for buying the best technological products:',
        'welcome_services': [
            'Where and how to buy at the best prices',
            'Installment payment option',
            'Phone and other device price estimation'
        ],
        'welcome_footer': 'Quality, convenient and reliable services with us!',
        
        # Main menu buttons
        'menu_map': '🗺️ Store Map',
        'menu_price_calculator': '💰 Price My Phone',
        'menu_call_center': '📞 Call Center',
        'menu_admin_contact': '👨‍💼 Contact Admin',
        'menu_admin_panel': '⚙️ Admin Panel',
        
        # Map section
        'map_title': '🗺️ **Store Map**',
        'map_description': 'Choose to find the nearest store or view all locations:',
        'nearest_location': '📍 Find Nearest Location',
        'all_locations': '📋 All Stores',
        'share_location_prompt': '📍 **Find Nearest Location**\n\nPlease share your location:',
        'nearest_store_title': '📍 **Nearest Store:**',
        'store_name': '🏪 **{name}**',
        'store_address': '📍 **Address:** {address}',
        'store_distance': '📏 **Distance:** {distance}',
        'store_image_available': '🖼️ **Image:** Available',
        'store_image_not_available': '🖼️ **Image:** Not available',
        'view_on_map': 'Click the button to view on map:',
        'all_stores_title': '📋 **All Our Stores:**',
        'select_store': 'Select the desired store:',
        'no_stores_found': '❌ Sorry, no stores found at the moment.',
        'store_not_found': '❌ Store not found!',
        'location_sent': '📍 Location sent!',
        'error_occurred': '❌ An error occurred!',
        'return_to_menu': '🏪 Click the button to return to main menu:',
        
        # Price calculator
        'price_calculator_title': '💰 **Price My Phone**',
        'select_model': 'Select device model:',
        'model_selected': '📱 **{name}** selected',
        'select_memory': 'Select memory capacity:',
        'memory_selected': '💾 **{memory}** selected',
        'condition_info_title': '📱 **Phone Condition Information:**',
        'condition_new': '🆕 **Excellent** - Phone must have 95%+ battery capacity and no scratches or dents',
        'condition_good': '✅ **Good** - Battery capacity can be 85-95%, screen should be clean, phone may have scratches',
        'condition_fair': '🔄 **Fair** - Battery capacity can be less than 85%, screen and phone may have scratches',
        'got_it': '✅ Got it',
        'back': '🔙 Back',
        'select_condition': 'Select device condition:',
        'price_result_title': '💰 **Price Estimation Result**',
        'price_model': '📱 **Model:** {model}',
        'price_memory': '💾 **Memory:** {memory}',
        'price_condition': '📊 **Condition:** {condition}',
        'price_amount': '💵 **Price:** {price}',
        'additional_info_title': '📋 **Additional Information:**',
        'additional_info': [
            'This is the average market price',
            'Phone box availability is considered',
            'Price may be slightly lower if box is missing',
            'Color and region also affect the price'
        ],
        'contact_for_details': '📞 Contact us for detailed information!',
        'no_models_available': '❌ Sorry, no models available at the moment.',
        'model_not_found': '❌ Model not found!',
        'memory_not_found': '❌ Memory capacity not found!',
        'condition_not_found': '❌ Price for this condition not found!',
        'error_restart': '❌ An error occurred! Start over.',
        
        # Call center
        'call_center_title': '📞 **Uzbekistan\'s Only Call Center**',
        'call_center_description': 'We offer you the following services:',
        'call_center_services': [
            'Find phones anywhere',
            'Find the cheapest across the valley',
            'Find any gadget accessories'
        ],
        'call_center_phone': '📱 **Phone:** +998330170555',
        'call_center_hours': '⏰ **Working Hours:** 09:00 - 18:00',
        'call_center_days': '🌍 **Monday - Saturday**',
        'call_center_footer': 'We are happy to help you!',
        'phone_copied': '📞 Call center number copied!',
        
        # Admin contact
        'admin_contact_title': '👨‍💼 **Contact Administrator**',
        'admin_contact_description': 'If you have questions or suggestions:',
        'admin_telegram': '📱 **Telegram:** @ibazacallcenter',
        'admin_phone': '📞 **Phone:** +998330170555',
        'admin_footer': 'Administrator will respond to you soon!',
        'admin_info_shown': '👨‍💼 Administrator information shown!',
        
        # Admin panel
        'admin_panel_title': '⚙️ **Admin Panel**',
        'admin_panel_description': 'Choose for managing stores and prices:',
        'admin_map_management': '🗺️ Map Management',
        'admin_price_management': '💰 Price Management',
        'admin_map_title': '🗺️ **Map Management**',
        'admin_map_description': 'Managing store locations:',
        'add_location': '➕ Add Location',
        'add_location_title': '➕ **Add New Location**',
        'enter_store_name': 'Enter store name:',
        'name_entered': '✅ **Name:** {name}',
        'enter_store_address': 'Now enter store address:',
        'address_entered': '✅ **Address:** {address}',
        'share_store_location': 'Now share store location:',
        'coordinates_received': '✅ **Coordinates:** {lat}, {lon}',
        'upload_store_image': 'Now upload store image (optional):',
        'location_saved_title': '✅ **Location Successfully Added!**',
        'location_name': '🏪 **Name:** {name}',
        'location_coordinates': '📍 **Coordinates:** {lat}, {lon}',
        'image_added': '🖼️ **Image:** Added',
        'image_not_added': '🖼️ **Image:** Not added',
        'location_save_error': '❌ An error occurred! Location not saved.',
        'no_permission': '❌ No permission!',
        'please_enter_name': '❌ Please enter store name!',
        'please_enter_address': '❌ Please enter store address!',
        'please_share_location': '❌ Please share location!',
        'error_restart_admin': '❌ An error occurred! Start over.',
        
        # Price management
        'price_management_title': '💰 **Price Management**',
        'price_management_description': '📊 **Management via Google Sheets:**',
        'price_management_features': [
            'Adding models and prices',
            'Editing existing prices',
            'Deleting prices'
        ],
        'refresh_prices_description': '🔄 Click **Refresh Prices** button to load changes from Google Sheets to the bot.',
        'manage_prices_sheets': '📊 Manage Prices in Google Sheets',
        'refresh_prices': '🔄 Refresh Prices',
        'prices_refreshing': '🔄 Refreshing prices...',
        'prices_refreshed': '✅ **Prices Successfully Updated!**',
        'total_models': '📱 **Total Models:** {count}',
        'prices_refresh_description': 'All changes from Google Sheets loaded to the bot.',
        'sheets_error': '❌ Error getting data from Google Sheets!',
        'refresh_error': '❌ Error refreshing prices!',
        
        # Common buttons
        'cancel': '❌ Cancel',
        'back_to_admin': '⬅️ Back',
        'menu': 'Menu',
        'menu_emoji': '🏪 Menu',
        
        # Language selection
        'select_language': '🌍 **Select Language**\n\nPlease select your preferred language:',
        'language_selected': '✅ Language selected: {language}',
        'welcome_with_language': '🏪 **iBaza** - welcome to the world of phones and gadgets\n\nLanguage: {language}',
        
        # Error messages
        'image_load_error': '⚠️ Error loading image!',
        'general_error': '❌ An error occurred!',
    }
}

def get_text(key: str, lang: str = 'uz', **kwargs) -> str:
    """
    Get translated text for given key and language
    
    Args:
        key: Translation key
        lang: Language code ('uz', 'ru', 'eng')
        **kwargs: Format parameters
    
    Returns:
        Translated text with formatted parameters
    """
    if lang not in TRANSLATIONS:
        lang = 'uz'  # Default to Uzbek
    
    text = TRANSLATIONS[lang].get(key, key)
    
    if kwargs:
        try:
            return text.format(**kwargs)
        except KeyError:
            return text
    
    return text

def get_language_name(lang: str) -> str:
    """Get language display name"""
    return LANGUAGES.get(lang, LANGUAGES['uz'])

def get_available_languages() -> dict:
    """Get all available languages"""
    return LANGUAGES 