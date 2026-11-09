"""Proje klasöründe python veriyi_hazirla.py komutuyla çalıştırılır."""
import csv
from collections import Counter
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

from openpyxl import load_workbook

DATA = Path(__file__).resolve().parent / "data"


def save(name, headers, rows):
    with (DATA / name).open("w", newline="", encoding="utf-8-sig") as output:
        writer = csv.writer(output)
        writer.writerow(headers)
        writer.writerows(rows)


with (DATA / "tatiller_2024.csv").open(encoding="utf-8-sig") as source:
    holidays = {r["tarih"]: r for r in csv.DictReader(source)}

calendar = {}
for i in range(366):
    day = date(2024, 1, 1) + timedelta(days=i)
    key = day.isoformat()
    holiday = holidays.get(key, {})
    calendar[key] = [key, day.month, day.isoweekday(), holiday.get("gun_turu", "Normal"),
                     holiday.get("tatil_adi", "")]
assert set(holidays) <= set(calendar)
save("takvim_2024.csv", ["tarih", "ay", "hafta_gunu_iso", "gun_turu", "tatil_adi"], calendar.values())

book = load_workbook(DATA / "perakende_satis.xlsx", read_only=True, data_only=True)
rows = iter(book.active.values)
headers = next(rows)
sales = [dict(zip(headers, r)) for r in rows]
book.close()
assert len(sales) == len({r["SiparisID"] for r in sales}) == 2000
assert all(r["Tarih"] in calendar for r in sales)
assert all(all(v is not None for v in r.values()) for r in sales)
save("satis.csv", headers, (r.values() for r in sales))

day_counts = Counter()
example = []
for r in sales:
    key = r["Tarih"]
    day_counts[key] += 1
    if key in {"2024-10-01", "2024-10-08", "2024-10-15", "2024-10-22", "2024-10-29"}:
        revenue = r["Miktar"] * Decimal(str(r["BirimFiyat"])) * (1 - Decimal(str(r["IndirimOrani"])))
        example.append([key, r["Kanal"], r["SiparisID"], round(revenue, 2)])

print(f"{len(sales)} sipariş eşleşti. {len(day_counts)} tarihte kayıt var.")
print("Kayıt bulunmayan tarihler:", ", ".join(sorted(set(calendar) - set(day_counts))))
for key in sorted({r[0] for r in example}):
    selected = [r for r in example if r[0] == key]
    print(key, len(selected), "sipariş;", sum(r[3] for r in selected), "TL")
