from app.database.supabase import supabase

data = {
    "product_name": "Test Biscuit",
    "manufacturer": "Test Company",
    "mrp": "₹50",
    "net_quantity": "100 g",
    "packing_date": "01/09/2026",
    "consumer_care": "1800-123-456",
    "country_of_origin": "India",
    "best_before": "6 months"
}

response = supabase.table("products").insert(data).execute()

print("INSERT RESULT:")
print(response.data)

response = supabase.table("products").select("*").execute()

print("\nSELECT RESULT:")
print(response.data)