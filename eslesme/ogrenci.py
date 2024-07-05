from pyairtable import Api # Pyairtable kütüphanesindeki gerekli api sınıfını kullanmak için içe aktarma işlemi. 

# Airtable API anahtarı ve tablo adı tanımlıyoruz.
base_key = 'appqHL0eUNihvu2Wz'
table_name = 'tblVC9h0JnRcA1FMv'
personal_access_token = 'patTc4Xi5PLA3NucF.9f7b900def494f7d613e58ce1de120528b31d1409917d68089a7cbc7e14a915d'

try:
    api = Api(personal_access_token) # Kişisel erişim jetonu kullanarak Api'ye bağlanma işlemi yapılıyor.
    table = api.table(base_key, table_name) # Tablo üzerinde işlem yapıyorum.
    records = table.all() # Tablodan tüm kayıtları çekiyorum.
    import csv # Verileri bilgisayara kaydediyorum. CSV dosyası şeklinde yazdırıyorum.

    with open('ogrenciVerileri.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'first_name', 'last_name', 'gender', 'university_name', 'city_of_residence', 'field_of_study','category_interest', 'interest'])
        for record in records:
            writer.writerow([record['id'], record['fields']['first_name'], record['fields']['last_name'], record['fields']['gender'], record['fields']['university_name'], record['fields']['city_of_residence'], record['fields']['field_of_study'], record['fields']['category_interest'], record['fields']['interest']])

    print("Öğrenci verileri şu dosyaya kaydedildi: ogrenciVerileri.csv")

except Exception as e:
    print(f"Hata: {e}")