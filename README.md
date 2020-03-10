# Yazlab 2 Ödev 1
uyduruk görüntü işlemeli sözde kütüphane otomasyonu

### araçlar 
- python
- flask
- opencv
- postgresql
- pyzbar

### TODO
#### basic login mechanism
#### understand request data flow
#### templates

### snippets 
postgres cli tool
```bash
$ psql -d yazlab3 -h localhost -U mrk0
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
- Kitap Alma: Kitap 1 haftalık süre ile kullanıcının üstüne atanır. Başkasının üstünde bulunan kitap sistem tarafından verilemez. Kullanıcı üstünde en fazla 3 kitap bulunabilir. Kullanıcının üzerinde teslim tarihi geçmiş kitap var ise kullanıcı başka kitap alamaz. Yeni kitap alabilmesi için teslim tarihi geçmiş tüm kitapları sisteme geri vermelidir.
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
- login sistemi guvenlik onlemleri
- form evaluationları onemlimi

#### proje raporu 
[ödev raporu](https://www.mrkaurelius.xyz/pdf/yazlab2p1.pdf)
