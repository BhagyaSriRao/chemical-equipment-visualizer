def analyze_csv(file):
    df = pd.read_csv(file)

    return {
        "total_equipment": len(df),
        "average_flowrate": round(df["Flowrate"].mean(), 2),
        "average_pressure": round(df["Pressure"].mean(), 2),
        "average_temperature": round(df["Temperature"].mean(), 2),
        "equipment_type_distribution": df["Type"].value_counts().to_dict(),
        "table_data": df.to_dict(orient="records")   # ⭐ ADD THIS
    }
