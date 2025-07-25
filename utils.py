def normalize_asset_data(data):
    return {
        'name': data.get('name', '').strip().title(),
        'category': data.get('category', '').lower(),
        'owner': data.get('owner', '').strip(),
        'status': data.get('status', 'available').lower()
    }

# Full field schema with updated order
default_asset_fields = {
    "category": "",  # Asset Type comes first
    "name": "",  # Asset Name comes after category
    "new_type": "",  # Optional New Type
    "third_party_code": "",
    "user_code": "",
    "area": "",
    "username": "",
    "given_date": "",
    "license": "",
    "os": "",
    "system": "",
    "system_manufacturer": "",
    "serial_no": "",
    "processor": "",
    "ram": "",
    "harddisk": "",
    "specification": "",
    "date_of_purchase": "",
    "vendor": "",
    "invoice_no": "",
    "amount": "",
    "status": "available",  
    "remarks": ""  # Remarks comes last
}

def fill_missing_asset_fields(data):
    filled = default_asset_fields.copy()
    for k, v in data.items():
        if k in filled:
            filled[k] = v
    return filled
