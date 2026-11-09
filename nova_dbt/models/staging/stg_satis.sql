select
    SiparisID as siparis_id,
    cast(Tarih as date) as tarih,
    Musteri_ID as musteri_id,
    trim(Sehir) as sehir,
    trim(Bolge) as bolge,
    trim(Kanal) as kanal,
    trim(Kategori) as kategori,
    trim(Urun) as urun,
    Miktar as miktar,
    BirimFiyat as birim_fiyat,
    Maliyet as maliyet,
    IndirimOrani as indirim_orani,
    cast(Miktar * BirimFiyat * (1 - IndirimOrani) as decimal(18, 2)) as net_ciro
from {{ ref('satis') }}