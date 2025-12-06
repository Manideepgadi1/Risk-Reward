import pandas as pd

# Mapping of long names to short names
name_mapping = {
    'NIFTY 50': 'N50',
    'NIFTY NEXT 50': 'NN50',
    'NIFTY 100': 'N100',
    'NIFTY 200': 'N200',
    'Nifty Total Market': 'NTOTLM',
    'NIFTY 500': 'N500',
    'NIFTY500 MULTICAP 50:25:25': 'NMC5025',
    'NIFTY500 EQUAL WEIGHT': 'N500EQ',
    'NIFTY MIDCAP 150': 'NMC150',
    'NIFTY MIDCAP 50': 'NMC50',
    'Nifty Midcap Select': 'NMCSEL',
    'NIFTY Midcap 100': 'NMC100',
    'NIFTY SMALLCAP 250': 'NSC250',
    'NIFTY SMALLCAP 50': 'NSC50',
    'NIFTY SMALLCAP 100': 'NSC100',
    'NIFTY MICROCAP 250': 'NMICRO',
    'NIFTY LargeMidcap 250': 'NLMC250',
    'NIFTY MIDSMALLCAP 400': 'NMSC400',
    'DSP QUANT': 'DSPQ',
    'DSP ELSS': 'DSP ELSS',
    'ICICI PRU SILVER': 'ICICI SIL',
    'NIFTY 10 YR BENCHMARK G-SEC': 'N10YRGS',
    'KOTAK CONTRA': 'KBIK CON',
    'KOTAK GOLD': 'KBIK GOLD',
    'UTI FLEX': 'UTI FLEX',
    'AXIS INNOVATION': 'AXISINVE',
    'NIFTY AUTO': 'NAUTO',
    'NIFTY BANK': 'NBANK',
    'NIFTY CHEMICALS': 'NCHEM',
    'NIFTY FINANCIAL SERVICES': 'NFINSERV',
    'NIFTY FINANCIAL SERVICES 25/50': 'NFINS2550',
    'Nifty Financial Services Ex Bank': 'NFINSXB',
    'NIFTY FMCG': 'NFMCG',
    'Nifty HEALTHCARE': 'NHEALTH',
    'NIFTY IT': 'NTECH',
    'NIFTY MEDIA': 'NMEDIA',
    'NIFTY METAL': 'NMETAL',
    'NIFTY PHARMA': 'NPHARMA',
    'NIFTY PRIVATE BANK': 'NPVTBANK',
    'NIFTY PSU BANK': 'NPSUBANK',
    'NIFTY REALTY': 'NREALTY',
    'NIFTY CONSUMER DURABLES': 'NCONDUR',
    'NIFTY OIL AND GAS INDEX': 'NOILGAS',
    'Nifty MidSmall Financial Services': 'NMSFINS',
    'Nifty MidSmall Healthcare': 'NMSHC',
    'Nifty MidSmall IT & Telecom': 'NMSITT',
    'NIFTY 100 EQUAL WEIGHT': 'N100EWT',
    'NIFTY 100 LOW VOLATILITY 30': 'N100LV30',
    'NIFTY200 MOMENTUM 30': 'N200M30',
    'NIFTY200 ALPHA 30': 'N200AL30',
    'NIFTY100 ALPHA 30': 'N100AL30',
    'NIFTY ALPHA 50': 'NAL50',
    'NIFTY ALPHA LOW VOLATILITY 30': 'NALV30',
    'NIFTY ALPHA QUALITY LOW VOLATILITY 30': 'NAQLV30',
    'NIFTY ALPHA QUALITY VALUE LOW-VOLATILITY 30': 'NAQVLV30',
    'NIFTY DIVIDEND OPPORTUNITIES 50': 'NDIVOP50',
    'NIFTY GROWTH SECTORS 15': 'NGROW15',
    'NIFTY HIGH BETA 50': 'NHBET50',
    'NIFTY LOW VOLATILITY 50': 'NLV50',
    'NIFTY TOP 10 EQUAL WEIGHT': 'NT10EWT',
    'NIFTY TOP 15 EQUAL WEIGHT': 'NT15EWT',
    'NIFTY TOP 20 EQUAL WEIGHT': 'NT20EWT',
    'NIFTY100 QUALITY 30': 'N100QL30',
    'NIFTY Midcap150 Momentum 50': 'NMC150M50',
    'Nifty500 Flexicap Quality 30': 'N500FQ30',
    'NIFTY500 LOW VOLATILITY 50': 'N500LV50',
    'NIFTY500 MOMENTUM 50': 'N500M50',
    'NIFTY500 QUALITY 50': 'N500QL50',
    'NIFTY500 MULTIFACTOR MQVLv 50': 'N500MQLV',
    'NIFTY Midcap150 Quality 50': 'NMC150Q',
    'Nifty Smallcap250 Quality 50': 'NSC250Q',
    'NIFTY500 MULTICAP MOMENTUM QUALITY 50': 'N500MQ50',
    'Nifty MidSmallcap400 Momentum Quality 100': 'NMSCMQ',
    'Nifty Smallcap250 Momentum Quality 100': 'NSC250MQ',
    'NIFTY QUALITY LOW VOLATILITY 30': 'NQLLV30',
    'NIFTY50 EQUAL WEIGHT': 'N50EQWGT',
    'NIFTY50 VALUE 20': 'N50V20',
    'Nifty200 Value 30': 'N200V30',
    'NIFTY500 VALUE 50': 'N500V50',
    'NIFTY200 Quality 30': 'N200QL30',
    'NIFTY INDIA CORPORATE GROUP INDEX - ADITYA BIRLA GROUP': 'NBIRLA',
    'Nifty Capital Markets': 'NCAPMRKT',
    'NIFTY COMMODITIES': 'NCOMM',
    'Nifty Core Housing': 'NCHOUS',
    'NIFTY CPSE': 'NCPSE',
    'NIFTY ENERGY': 'NENRGY',
    'Nifty EV & New Age Automotive': 'NEVNAA',
    'Nifty Housing': 'NHOUS',
    'NIFTY100 ESG': 'N100ESG',
    'NIFTY100 Enhanced ESG': 'N100ESGE',
    'Nifty100 ESG Sector Leaders': 'N100ESGSL',
    'NIFTY INDIA CONSUMPTION': 'NICON',
    'Nifty India Defence': 'NIDEF',
    'Nifty India Digital': 'NIDIGI',
    'NIFTY INDIA INFRASTRUCTURE & LOGISTICS': 'NIIL',
    'Nifty India Internet': 'NIINT',
    'Nifty India Manufacturing': 'NIMFG',
    'NIFTY INDIA TOURISM': 'NTOUR',
    'NIFTY INFRASTRUCTURE': 'NINFRA',
    'NIFTY INDIA CORPORATE GROUP INDEX - MAHINDRA GROUP': 'NMAHIN',
    'NIFTY IPO': 'NIPO',
    'NIFTY MIDCAP LIQUID 15': 'NMCL15',
    'Nifty MidSmall India Consumption': 'NMSICON',
    'NIFTY MNC': 'NMNC',
    'Nifty Mobility': 'NMOBIL',
    'NIFTY PSE': 'NPSE',
    'Nifty REITs & InvITs': 'NREIT',
    'Nifty Rural': 'NRURAL',
    'Nifty Non-Cyclical Consumer Index': 'NNCCON',
    'NIFTY SERVICES SECTOR': 'NSERVSEC',
    'NIFTY SHARIAH 25': 'NSH25',
    'NIFTY INDIA CORPORATE GROUP INDEX - TATA GROUP': 'NTATA',
    'NIFTY INDIA CORPORATE GROUP INDEX - TATA GROUP 25% CAP': 'NTATA25',
    'Nifty Transportation & Logistics': 'NTRANS',
    'NIFTY100 LIQUID 15': 'N100LIQ15',
    'NIFTY50 SHARIAH': 'N50SH',
    'NIFTY500 SHARIAH': 'N500SH',
    'NIFTY500 MULTICAP INDIA MANUFATURING 50:30:20': 'NMF5032',
    'NIFTY500 MULTICAP INFRASTRUCTURE 50:30:20': 'NINF5032',
    'NIFTY SME EMERGE': 'NSMEE',
    'Nifty India Railways PSU': 'NIRLPSU',
    'NIFTY INDIA SELECT 5 CORPORATE GROUPS (MAATR)': 'NMAATR',
    'NIFTY INDIA NEW AGE CONSUMPTION': 'NINACON',
    'Nifty Waves': 'NWAVES'
}

# Read the CSV
print("Reading data.csv...")
df = pd.read_csv(r"d:\Risk reward - Copy\data.csv")

# Get current columns
current_cols = df.columns.tolist()
print(f"\nCurrent columns: {len(current_cols)}")

# Rename columns
renamed_cols = []
for col in current_cols:
    if col in name_mapping:
        renamed_cols.append(name_mapping[col])
        print(f"  '{col}' -> '{name_mapping[col]}'")
    else:
        renamed_cols.append(col)
        if col != 'DATE':
            print(f"  WARNING: No mapping found for '{col}'")

# Apply new column names
df.columns = renamed_cols

# Save the updated CSV
print("\nSaving updated data.csv...")
df.to_csv(r"d:\Risk reward - Copy\data.csv", index=False)

print("\n✓ Column names successfully updated!")
print(f"\nNew header preview:")
print(','.join(df.columns[:10]) + '...')
