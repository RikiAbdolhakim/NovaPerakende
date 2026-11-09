select
    cast(tarih as date) as tarih,
    cast(ay as integer) as ay,
    cast(hafta_gunu_iso as integer) as hafta_gunu_iso,
    trim(gun_turu) as gun_turu,
    nullif(trim(tatil_adi), '') as tatil_adi
from {{ ref('takvim_2024') }}