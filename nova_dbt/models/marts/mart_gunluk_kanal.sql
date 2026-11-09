{{ config(materialized='table') }}

with kanallar as (
    select distinct kanal
    from {{ ref('stg_satis') }}
),

gunluk_satis as (
    select
        tarih,
        kanal,
        count(distinct siparis_id) as siparis_sayisi,
        sum(miktar) as satilan_adet,
        sum(net_ciro) as net_ciro
    from {{ ref('stg_satis') }}
    group by tarih, kanal
)

select
    t.tarih,
    t.ay,
    t.hafta_gunu_iso,
    t.gun_turu,
    t.tatil_adi,
    k.kanal,
    coalesce(s.siparis_sayisi, 0) as siparis_sayisi,
    coalesce(s.satilan_adet, 0) as satilan_adet,
    coalesce(s.net_ciro, 0) as net_ciro
from {{ ref('stg_takvim') }} as t
cross join kanallar as k
left join gunluk_satis as s
    on s.tarih = t.tarih
    and s.kanal = k.kanal