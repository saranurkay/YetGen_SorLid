import csv
import random # Eğer öğrenciler hiçbir eşleştirme kriterine uygun değilse 20 kişilik sınırı aşmayacak şekilde rasgele gruplara yerleştirmek için çağırıldı.

# Liderler ile öğrenciler ve öğrenciler ile diğer öğrenciler arasındaki benzerlikleri bulmak ve benzer ilgi alanlarına sahip kişilerin eşleşmesini sağlamak için bu fonksiyon kullanıldı.
def calculate_interest_similarity(interest1, interest2): #İki ilgi aynı ise true dönecek ve aynı gruplarda eşleştirilecek.
    return interest1 == interest2

# İki öğrenci arasındaki kriterlerin benzerliğini hesaplamak için bu fonksiyon kullanıldı. Eğer ilgi alanları spesifik aynı ise öğrenci gruplandırılacak. Eğer ilgi alanı spesifik olarak aynı değilse aynı katagoridemi bakılacak ve buna göre gruplandırılacak.
def calculate_student_similarity(student1, student2):
    similarity_score = 0
    
    similarity_score += calculate_interest_similarity(student1['interest'], student2['interest'])
    similarity_score += calculate_interest_similarity(student1['category_interest'], student2['category_interest'])
    similarity_score += calculate_interest_similarity(student1['field_of_study'], student2['field_of_study'])
    
    if student1['university_name'] == student2['university_name']:
        similarity_score += 1  # Üniversite adı eşleşiyorsa benzerlik puanına 1 ekle
    
    return similarity_score

# Bu fonksiyon iki şehrin aynı bölgede olup olmadığını kontrolünü yapar. Öğrencilerin aynı şehirde ya da birbirine yakın şehirlerde olması için kullanıldı.
def is_same_region(city1, city2):
    regions = {
        "Marmara": ["İstanbul", "Kocaeli", "Bursa", "Sakarya", "Balıkesir", "Çanakkale", "Yalova", "Tekirdağ", "Edirne"],
        "Ege": ["İzmir", "Manisa", "Aydın", "Muğla", "Denizli", "Uşak"],
        "Akdeniz": ["Antalya", "Mersin", "Adana", "Hatay", "Isparta", "Burdur", "Osmaniye", "Kahramanmaraş"],
        "Karadeniz": ["Trabzon", "Samsun", "Ordu", "Giresun", "Rize", "Tokat", "Artvin", "Sinop", "Amasya", "Kastamonu", "Çorum", "Bartın", "Karabük", "Zonguldak"],
        "İç Anadolu": ["Ankara", "Konya", "Eskişehir", "Kayseri", "Kırıkkale", "Aksaray", "Karaman", "Nevşehir", "Niğde", "Kırşehir"],
        "Doğu Anadolu": ["Erzurum", "Van", "Diyarbakır", "Malatya", "Ağrı", "Elazığ", "Batman", "Muş", "Bingöl", "Şanlıurfa", "Bitlis", "Hakkari", "Şırnak", "Tunceli", "Siirt", "Kars", "Ardahan", "Iğdır"],
        "Güneydoğu Anadolu": ["Gaziantep", "Şanlıurfa", "Adıyaman", "Mardin", "Kilis"]
    }

    for region_cities in regions.values():
        if city1 in region_cities and city2 in region_cities:
            return True
    return False

# CSV dosyasını okuyup verileri yüklemek için bu fonksiyon kullanıldı.
def load_data(filename):
    with open(filename, mode='r', encoding='utf-8') as file:
        return list(csv.DictReader(file))

# Lider ve öğrenci eşleştirme işlemini gerçekleştiren fonksiyon.
def match_leaders_with_students(leaders, students):
    matched_data = []

    for leader in leaders:
        matched_students = []
        gender_counts = {'Male': 0, 'Female': 0}
        interest_counts = {}

        for student in students:
            if len(matched_students) >= 20: # Lider başına düşen öğrenci sayısı en fazla 20 olacak şekilde ayarlandı.
                break

            if gender_counts.get(student['gender'], 0) >= 10: # Öğrenci cinsiyet benzerliği gruplarda en fazla 10 şeklinde ayarlandı çünkü bir cinsiyetin grubun yarısından fazla olmaması istendi.
                continue

            # İlgi alanlarını gruplandırırken 20 kişilik grupta en fazla aynı ilgi alanına sahip 5 kişi olmasını istedim.
            # Böylelikle hem takımlarda aynı ilgi alanlarına ya da ilgi alanı kriterlerine sahip arkadaş bulabilirken hem de farklı...
            # ...ilgi alanlarında arkadaş edinebilecekler. Böylelikle aynı ilgi alanına sahip farklı takımlardan da arkadaş edinebilirler.
            if calculate_interest_similarity(leader['interest'], student['interest']):
                if interest_counts.get(student['interest'], 0) >= 5:
                    continue
                interest_counts[student['interest']] = interest_counts.get(student['interest'], 0) + 1

            # Lider ile öğrenci arasındaki benzerliğe bakılır. Lider ile öğrenci arasındaki benzerliklere göre takım yapmak amaçlandı.
            # Aynı zamanda eşleşmiş öğrencilerle bir diğer öğrencinin benzerliğine de bakılıyor. Takımların dinamiklerini tutturmak adına bu yöntem izlendi.
            if calculate_student_similarity(leader, student):
                if any(calculate_student_similarity(student, s) for s in matched_students):
                    continue

                # Burada liderin yaşadığı şehirde veya aynı bölgede olan öğrencileri liderin grubuna eklemeyi amaçladım.
                # Amacım öğrencilerin ya da liderlerin buluşmalarında olabildiğince yakın şehirllerdekilerle ya da bölgedekilerle tanışabilmesi.
                if leader['city_of_residence'] == student['city_of_residence'] or is_same_region(leader['city_of_residence'], student['city_of_residence']):
                    matched_students.append(student)
                    gender_counts[student['gender']] = gender_counts.get(student['gender'], 0) + 1 # Liderin takımındaki cinsiyet dengesini sağlamak için her eklenen öğrencinin cinsiyet sayısını güncelliyoruz.

        # Bütün eşleşmeler sonucu takımlarda 20 kişiden az bir mevcut varsa hiçbir takımla eşleşemeyen öğrencileri bu takımlara atamak için kullanıldı.
        while len(matched_students) < 20:
            random_student = random.choice([s for s in students if s not in matched_students])
            matched_students.append(random_student)

        # Lider ile eşleşen öğrencileri veri yapısına ekliyoruz ve eşleşen öğrencileri dosyaya kaydediyoruz.
        matched_data.append((leader, matched_students))
        save_matched_students_to_file(leader, matched_students)

    return matched_data

# Liderlerin eşleşen öğrencilerinin verilerini metin dosyasına kaydediyoruz.
# Liderin bilgilerine göre dosya adı oluşturuyoruz (sırası ile id, ad, soyad) ve eşleşen öğrencilerin verilerini bu dosyaya yazdırıyoruz.
def save_matched_students_to_file(leader, matched_students):
    filename = f"{leader['id']}.txt"
    with open(filename, mode='w', encoding='utf-8') as file:
        for student in matched_students:
            file.write(f"ID: {student['id']}\n")
            file.write(f"Ad: {student['first_name']}\n")
            file.write(f"Soyad: {student['last_name']}\n")
            file.write(f"Okul: {student['university_name']}\n")
            file.write(f"Şehir: {student['city_of_residence']}\n")
            file.write(f"Bolum: {student['field_of_study']}\n")
            file.write(f"Cinsiyet: {student['gender']}\n")
            file.write(f"Ilgi Alanı: {student['interest']}\n")
            file.write(f"Ilgi Alanı Kategorisi: {student['category_interest']}\n")
            file.write("********************\n")

# Liderlerin ve öğrencilerin verilerini yükleyip, belirlediğimiz kriterlere göre eşleşmelerini sağlayarak her lider için kaç öğrencinin eşleştiğini gösteren ana işlem akışı.
if __name__ == "__main__":
    leaders = load_data('liderVerileri.csv')
    students = load_data('ogrenciVerileri.csv')
    matched_data = match_leaders_with_students(leaders, students)

    for leader, matched_students in matched_data:
        print(f"Lider {leader['id']} {leader['first_name']} {leader['last_name']} için eşleşen öğrenci sayısı: {len(matched_students)}")
