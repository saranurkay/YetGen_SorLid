from pyairtable import Api # Pyairtable kütüphanesindeki gerekli api sınıfını kullanmak için içe aktarma işlemi. 

# Airtable API anahtarı ve tablo adı tanımlıyoruz.
base_key = 'app4lrDCIFFMz0GPq'
table_name = 'tbl1kXwPmBDKFrJYT'
personal_access_token = 'patfUyx5Ufqaq8IjW.6a414e44eca39e842e4ddd9691e60544ef1da66b7ed65fdc7c427fcc4edfd016'

try:
    api = Api(personal_access_token) # Kişisel erişim jetonu kullanarak Api'ye bağlanma işlemi yapılıyor.
    table = api.table(base_key, table_name) # Tablo üzerinde işlem yapıyorum.
    records = table.all() # Tablodan tüm kayıtları çekiyorum.
    import csv # Verileri bilgisayara kaydediyorum. CSV dosyası şeklinde yazdırıyorum.

    with open('liderVerileri.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'first_name', 'last_name', 'gender', 'university_name', 'city_of_residence', 'field_of_study','category_interest', 'interest'])
        for record in records:
            writer.writerow([record['id'], record['fields']['first_name'], record['fields']['last_name'], record['fields']['gender'], record['fields']['university_name'], record['fields']['city_of_residence'], record['fields']['field_of_study'], record['fields']['category_interest'], record['fields']['interest']])

    print("Lider verleri şu dosyaya kaydedildi: liderVerileri.csv")

except Exception as e:
    print(f"Hata: {e}")