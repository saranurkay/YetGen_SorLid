import os
from pyairtable import Api, Base
import json

base_key = 'apptBVFZNgcUrWQiQ'
personal_access_token = 'patCa2Sww54dPls9U.62203ef13aa26e2ef65d55f7a1533ce692d9e991b9164a03a080acc9895ec4ec'
table_name = 'tbl9e6AyqSb6ghDtt' # Tablo adını liderlerin tablolarına göre değiştireceğimiz şekilde bir değişken atıyoruz.
file_path = "/Users/saranurkay/YetGen/rec1Pifgbt9PHqKSr.txt" # txt dosyasını değiştirebileceğimiz şekilde atıyoruz.

def read_txt_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    data = []
    record = {} # Boş kayıt sözlüğü oluşturuyoruz.
    for line in lines:
        line = line.strip()
        if line == "********************": # Yıldızları her gördüğünde yeni bir kayıt sözlüğü oluşturuyoruz.
            if record:
                data.append(record) # Tamamlanan kaydı atıyoruz.
                record = {} # Kayıt sözlüğünü sıfırladık.
        elif line:
            key, value = line.split(': ', 1) # Her bir satırları ayırdık.
            if key == "ID":
                key = "id"
            elif key == "Ad":
                key = "first_name"
            elif key == "Soyad":
                key = "last_name"
            elif key == "Cinsiyet":
                key = "gender"
            elif key == "Okul":
                key = "university_name"
            elif key == "Şehir":
                key = "city_of_residence"
            elif key == "Bolum":
                key = "field_of_study"
            elif key == "Ilgi Alanı Kategorisi":
                key = "category_interest"
            elif key == "Ilgi Alanı":
                key = "interest"
            record[key] = value # Alanlara ekleme işlemini yapıyoruz.

    if record:
        data.append(record) # Eğer mevcut bir kayıt varsa veriler arasına ekliyoruz.

    return data

def upload_data_to_airtable(base_key, personal_access_token, table_name, file_path):
    api = Api(personal_access_token)
    base = Base(api, base_key)
    table = base.table(table_name)
    data = read_txt_file(file_path) # txt dosyasındaki verileri okutuyoruz.
    
    # Her bir veriyi tabloya sırasıyla eklemek için döngü kuruyoruz.
    for i, record in enumerate(data):
        if 'ID' in record:
            record.pop('ID')  # ID'yi kaldırıyoruz ki birincil anahtar olarak öğrenci ID'sini algılamasın.
        try:
            response = table.create(fields=record) # Airtable'da yeni kayıt oluşturuyoruz.
            print(f"Kayıt {i+1} eklendi: {json.dumps(response, indent=2)}") # Eklenen kayıdımız hakkında bilgi verdiriyoruz. 
        except Exception as e:
            print(f"Hata: Kayıt {i+1} eklenirken bir hata oluştu: {str(e)}") # Kayıt oluştururken hata olduysa hangi kayıtta nasıl bir sorun yaşadığımızın çıktısını isitiyoruz.

upload_data_to_airtable(base_key, personal_access_token, table_name, file_path) # Verileri sıryla yüklüyoruz.
