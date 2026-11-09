# Veri sözlüğü
## Satış
Her satır benzersiz bir sipariştir. Seed alanları ve staging karşılıkları:

| Ham alan | Staging alanı | Anlamı |
|---|---|---|
| SiparisID | siparis_id | Benzersiz sipariş kodu |
| Tarih | tarih | Sipariş tarihi |
| Musteri_ID | musteri_id | Kaynak müşteri kodu |
| Sehir, Bolge | sehir, bolge | Kaydedilen şehir ve bölge |
| Kanal | kanal | Mağaza veya Online |
| Kategori, Urun | kategori, urun | Ürün sınıfı ve ürün |
| Miktar | miktar | Siparişteki ürün adedi |
| BirimFiyat | birim_fiyat | İndirim öncesi birim satış fiyatı (TL) |
| Maliyet | maliyet | Kaynak maliyet alanı; ciro hesabında kullanılmaz |
| IndirimOrani | indirim_orani | İndirim oranı (0–1) |

Staging modelinde net_ciro = miktar × birim_fiyat × (1 − indirim_orani), iki ondalık basamağa dönüştürülür.

## Takvim ve günlük kanal tablosu
Takvimde bir satır bir tarih, martta bir satır bir tarih ve kanal birleşimidir.

| Alan | İçerik |
|---|---|
| tarih | Takvim günü; 2024 içinde 366 farklı tarih |
| ay | 1–12 |
| hafta_gunu_iso | Pazartesi 1, pazar 7 |
| gun_turu | Normal, Tam gün veya Yarım gün |
| tatil_adi | Tatil adı; normal günlerde boş |
| kanal | Satış kanalı |
| siparis_sayisi | Tarih ve kanal içinde benzersiz sipariş sayısı |
| satilan_adet | O tarih ve kanalda toplam ürün miktarı |
| net_ciro | O tarih ve kanalda indirim sonrası toplam tutar (TL) |

## Rapordaki ölçüler
Toplam Sipariş = siparis_sayisi toplamı. Net Ciro = net_ciro toplamı. Ortalama Sipariş Tutarı = Net Ciro / Toplam Sipariş. Günlük Ortalama Ciro = Net Ciro / seçili bağlamdaki benzersiz tarih sayısı. Böylece iki kanal birlikte seçildiğinde bir tarih yalnızca bir kez sayılır.
