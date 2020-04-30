# Yazlab 2 Ödev 1
uyduruk görüntü işlemeli sözde kütüphane otomasyonu

### araçlar 
- python
- flask
- opencv
- postgresql
- pyzbar
- pigar (requirements.txt)
- sqlalchemy (sadece raw sql, ORM kullanılmadı)

### TODO
#### improc

### snippets 
postgres cli tool
```bash
$ psql -d yazlab3 -h localhost -U mrk0
```
sqlalchemy raw SQL query, bindig
```python
with engine.connect() as con:
    data = ( { "Id": 1, "Name": "Audi", "Price": 52642 },
            { "Id": 3, "Name": "Skoda", "Price": 9000 },
    )
    for line in data:
        con.execute(text("""INSERT INTO Cars(Id, Name, Price) 
            VALUES(:Id, :Name, :Price)"""), **line)
    return ''
```
opencv-python
```python 
color = (255,0,0)
thickness = 10 # px
cv2.rectangle(image, (x, y), (x_org+w, y_org+h), color, thickness) #inplace
```

postgres command line cheats
``` 

```

#### Yönetici (Admin):
Kitap ekleme, zaman atlama ve kullanıcı listeleme arayüzlerinikullanır.
- Kitap ekleme: Kitabın adı ve ISBN numarasının göründüğü resim yönetici
tarafından girilir. Sistem görüntü işleme algoritmalarını kullanarak resimden ISBN numarasını alır ve veritabanına kayıt işlemini gerçekleştirir.
- Zaman atlama: Zaman atla modülünde 20 gün girilirse sistem zamanı mevcut zamandan 20 gün sonraya öteleyecektir.
- Kullanıcı listeleme: Tüm kullanıcılar ve üzerinde bulunan kitapların listelenmesi.

#### Kullanıcı (User)
Kitap arama, kitap alıp verme arayüzlerini kullanır.
- Kitap arama: Kitabın ismine ya da ISBN numarasına göre arama yapılabilir.
- Kitap Alma: Kitap **1 haftalık** süre ile kullanıcının üstüne atanır. **Başkasının üstünde bulunan kitap** sistem tarafından verilemez. Kullanıcı üstünde **en fazla 3 kitap** bulunabilir. **Kullanıcının üzerinde teslim tarihi geçmiş kitap var ise kullanıcı başka kitap alamaz**. Yeni kitap alabilmesi için teslim tarihi geçmiş tüm kitapları sisteme **geri vermelidir**.
- Kitap Verme: Kullanıcı kitabın ISBN numarasının bulunduğu resmi sisteme yükler. Sistem resimden aldığı ISBN numarasını ve kullanıcının üzerinde bulunan kitaplardaki ISBN numarasını karşılaştırır. Eşleştirme bulursa kitap sisteme geri verilir ve kullanıcının üstündeki kitap bilgileri güncellenir.

#### Veritabanı (Database)
Kullanıcı bilgileri, kitap bilgileri, hangi kitabın kimde
olduğu bilgisi vb. bilgileri tutar. Uygulamanız için gerekli tablolar geliştiriciye
bırakılmıştır.

#### Projede dikkat edilmesi gereken noktalar:
- Kullanıcı girişi olması gerekmektedir.
- Yönetici ya da kullanıcı bilgilerini veritabanına elle giriş yapabilirsiniz.
- Yönetici, kitap eklerken kitabın adı ve kitabın resmini sisteme yüklemesi gerekmektedir.
- Kullanıcı, kitabı verirken kitabın resmini sisteme yüklemesi gerekmektedir.

#### sorulacak sorular 
- bir kitabın birden fazla isbnsi olabilirmi ?
- login sistemi guvenlik onlemleri
- form evaluationları onemlimi

#### cevaplar 
- bir kitabin bir isbnsi 
- bir kitaptan bir tane
- barkod okumak yok rakamlari tanımak gerekli 
- sunucunun tarihini degistirmek gerekli
- auth onemli degil

#### eleştiri
- daha akıllı bir arama meodu olabilirdi (isbn ve kitap adı birlikte)
- sembol isimlendirme daha anlaşılır, teamullere uygun olabilirdi
- kontrol yapısı daha akıllıca insa edilebilirdi

#### ödev raporu 
[ödev raporu](https://www.mrkaurelius.xyz/pdf/yazlab2p1.pdf)