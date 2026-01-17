import pandas as pd
import json

# 1. Ucitaj podatke
df = pd.read_csv("..\data\world_bank_countries.csv")
df = df[df['Year'] > 1998]
df = df[df['Year'] < 2023]
# 2. Zadrzi samo WB regione
df = df[df["Entity"].str.contains(r"\(WB\)", na=False)]

# 3. Definisi kolone po education levelima
levels = {
    "primary": (
        "Combined total net enrolment rate, primary, female",
        "Combined total net enrolment rate, primary, male"
    ),
    "lower_secondary": (
        "Net enrolment rate in lower secondary education among girls",
        "Net enrolment rate in lower secondary education among boys"
    ),
    "upper_secondary": (
        "Net enrolment rate in upper secondary education among girls",
        "Net enrolment rate in upper secondary education among boys"
    ),
    "tertiary": (
        "Combined gross enrolment ratio for tertiary education, female",
        "Combined gross enrolment ratio for tertiary education, male"
    )
}

records = []

# 4. Napravi gender gap zapise
for level, (f_col, m_col) in levels.items():
    temp = df[["Entity", "Year", f_col, m_col]].dropna()
    temp["gender_gap"] = temp[m_col] - temp[f_col]

    grouped = (
        temp
        .groupby(["Entity", "Year"])["gender_gap"]
        .mean()
        .reset_index()
    )

    for _, row in grouped.iterrows():
        records.append({
            "region": row["Entity"],
            "year": int(row["Year"]),
            "level": level,
            "gender_gap": round(row["gender_gap"], 3)
        })

# 5. Snimi u JSON
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(records, f, indent=2)

print("data.json generated successfully")
