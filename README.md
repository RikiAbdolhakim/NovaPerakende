# NovaPerakende | 2024 Satış Analizi
YBS305 · Bölüm 1 · DuckDB, dbt Core ve Power BI Desktop

## İş sorusu
Mağaza ve online kanallarda günlük ortalama net ciro normal günlerde, tam tatillerde ve yarım tatillerde nasıl değişiyor? Örnek olay olarak 29 Ekim 2024 Salı gününü aynı ayın diğer dört salısının günlük ortalamasıyla karşılaştırıyoruz.

## Kaynaklar ve yöntem
- Dersin Teams alanında sağlanan `perakende_satis.xlsx` dosyasının Sheet1 sayfasında 2.000 benzersiz sipariş bulunur. Tarih anahtarıyla takvime bağlanır.
- [Bursa İl Millî Eğitim Müdürlüğü 2024–2025 Çalışma Takvimi, Ek-1](https://bursa.meb.gov.tr/meb_iys_dosyalar/2024_07/23150726_2024_2025_calisma_takvimi.pdf) kullanılarak 14 tam ve 3 yarım tatil elle kodlandı. 31 Aralık normal gün kabul edildi. İdari izinler ve yerel etkinlikler kapsam dışında.
- Python ham girdilerden satış ve takvim CSV’lerini üretir. dbt iki seed'i DuckDB'ye yükler. `stg_satis` satış alanlarını temizler ve indirim sonrası ciroyu hesaplar. `stg_takvim` tarihleri ve gün türlerini düzenler. `mart_gunluk_kanal` 366 tarih ile iki kanalın bütün eşleşmelerini üretir ve satış toplamlarını ekler. Sipariş bulunmayan gün–kanal eşleşmelerinde tutar, miktar ve sipariş sayısı sıfırdır.

## Sonuçlar ve kullanım
| Kanal | Sipariş | Net ciro (TL) |
|---|---:|---:|
| Mağaza | 745 | 2.808.065,50 |
| Online | 1.255 | 4.398.763,50 |
| Toplam | 2.000 | 7.206.829,00 |

Ortalama sipariş tutarı 3.603,41 TL. Tüm kanallarda 29 Ekim cirosu 11.454 TL (4 sipariş), diğer ekim salılarının ortalaması 12.814,50 TL. Fark yaklaşık −%10,6. Kanal filtresiyle mağaza ve online sonuçlarını ayrı inceleyin. Personel ve stok kararından önce aynı karşılaştırmayı başka tatiller ve yıllarda tekrarlayın. Tek gün nedensel etkiyi ölçmez. Saat bilgisi olmadığı için yarım gün satışları saat bazında ayrıştırılamaz. Üç tarihte sipariş kaydı bulunmamasının nedeni veriden belirlenemez.

## Windows Komut İstemi ile çalıştırma
Komutları README'nin bulunduğu ana klasörde çalıştırın. Yerel veritabanı bu klasörde oluşturulur. Hazır CSV seed'leri ve Parquet çıktısı da repoda bulunur.

```bat
py -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python veriyi_hazirla.py
copy /Y data\satis.csv nova_dbt\seeds\satis.csv
copy /Y data\takvim_2024.csv nova_dbt\seeds\takvim_2024.csv
dbt build --project-dir nova_dbt --profiles-dir nova_dbt
dbt docs generate --project-dir nova_dbt --profiles-dir nova_dbt
python -c "import duckdb; db=duckdb.connect('dev.duckdb',read_only=True); db.sql('select * from mart_gunluk_kanal order by tarih, kanal').write_parquet('data/gunluk_kanal.parquet')"
```

Beklenen sonuç iki seed, üç model ve yedi başarılı veri testi. Hazır dbt belgelerini incelemek için docs/dbt_docs.html dosyasını indirip tarayıcıda açın.

GitHub'daki [Power BI raporunu](NovaPerakende_Satis_Analizi.pbix) indirip Power BI Desktop'ta açın. Tüm kanalları görmek için kanal seçimini temizleyin. Yenileme sırasında eski dosya yolu sorulursa Power Query'de gunluk_kanal sorgusunun Kaynak adımını bu projedeki data/gunluk_kanal.parquet dosyasına yönlendirin, değişiklikleri uygulayıp yenileyin.

[Veri sözlüğü](docs/VERI_SOZLUGU.md) · dbt belgelerini yerelde gezmek için:
```bat
dbt docs serve --project-dir nova_dbt --profiles-dir nova_dbt
```
