import csv

def save_market(m):
    with open("src/mm_bot/data/dataset.csv","a",newline="") as f:
        w=csv.writer(f)
        w.writerow([
            m.get("liquidity"),m.get("trades"),m.get("creator_score"),
            m.get("probability")/100,m.get("resolved")
        ])
