from app.database.supabase import supabase


# -----------------------------
# PRODUCTS
# -----------------------------

def create_product(product_data):
    response = (
        supabase
        .table("products")
        .insert(product_data)
        .execute()
    )

    return response.data[0] if response.data else None


def get_product(product_id):
    response = (
        supabase
        .table("products")
        .select("*")
        .eq("id", product_id)
        .single()
        .execute()
    )

    return response.data


# -----------------------------
# INSPECTIONS
# -----------------------------

def create_inspection(inspection_data):
    response = (
        supabase
        .table("inspections")
        .insert(inspection_data)
        .execute()
    )

    return response.data[0] if response.data else None


def get_inspections():
    response = (
        supabase
        .table("inspections")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )

    return response.data


def get_inspection(inspection_id):
    response = (
        supabase
        .table("inspections")
        .select("*")
        .eq("id", inspection_id)
        .single()
        .execute()
    )

    return response.data


# -----------------------------
# VIOLATIONS
# -----------------------------

def create_violation(violation_data):
    response = (
        supabase
        .table("violations")
        .insert(violation_data)
        .execute()
    )

    return response.data[0] if response.data else None


def get_violations(inspection_id):
    response = (
        supabase
        .table("violations")
        .select("*")
        .eq("inspection_id", inspection_id)
        .execute()
    )

    return response.data


# -----------------------------
# REPORTS
# -----------------------------

def create_report(report_data):
    response = (
        supabase
        .table("reports")
        .insert(report_data)
        .execute()
    )

    return response.data[0] if response.data else None


def get_report(report_id):
    response = (
        supabase
        .table("reports")
        .select("*")
        .eq("id", report_id)
        .single()
        .execute()
    )

    return response.data