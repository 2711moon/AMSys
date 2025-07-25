from flask import Blueprint, request, render_template, session, redirect, url_for, flash
from bson.objectid import ObjectId
from datetime import datetime
from models import assets_collection, asset_types_collection
from forms import AssetForm
from utils import normalize_asset_data, fill_missing_asset_fields
from dateutil.parser import parse as date_parse
from bson import json_util
import json

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def landing():
    return render_template('landing.html')


@main_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    assets = list(assets_collection.find())
    return render_template('dashboard.html', assets=assets)

@main_bp.route("/create_asset", methods=["GET", "POST"])
def create_asset():
    form = AssetForm()

    # Debugging the form validity and submitted data
    print("Form Validity:", form.validate_on_submit())  # Check if form is valid
    print("Form Data:", form.data)  # Print form data to see what's being submitted

    if form.validate_on_submit():
        selected_type = form.category.data
        new_type = form.new_type.data.strip()

        # Handle new type creation if "Add New Type" is selected
        if selected_type == "Add New Type" and new_type:
            if not asset_types_collection.find_one({"type_name": new_type}):
                asset_types_collection.insert_one({"type_name": new_type})
            selected_type = new_type

        # Collect and normalize form data
        raw_data = form.data
        raw_data["category"] = selected_type

        # Convert `datetime.date` fields to `datetime.datetime` for MongoDB
        def to_datetime(val):
            return datetime.combine(val, datetime.min.time()) if val else None

        raw_data["given_date"] = to_datetime(raw_data.get("given_date"))
        raw_data["purchase_date"] = to_datetime(raw_data.get("purchase_date"))

        # Clean the amount (remove ₹ and commas)
        if raw_data.get("amount"):
            raw_data["amount"] = raw_data["amount"].replace("₹", "").replace(",", "")

        # Remove unwanted fields before insert
        raw_data.pop("csrf_token", None)
        raw_data.pop("submit", None)

        # Normalize asset data if you have a function for it
        normalized = normalize_asset_data(raw_data)
        raw_data.update(normalized)

        # Insert into MongoDB
        result = assets_collection.insert_one(raw_data)

        flash("Asset added successfully.", "success")

        # Redirect to the view page with the inserted asset's ID
        return redirect(url_for("main.view_asset", asset_id=str(result.inserted_id)))

    if form.errors:
        print("Form errors:", form.errors)

    return render_template("create_new_asset.html", form=form)

@main_bp.route('/view/<asset_id>')
def view_asset(asset_id):
    asset = assets_collection.find_one({'_id': ObjectId(asset_id)})
    if not asset:
        flash('Asset not found.', 'danger')
        return redirect(url_for('main.dashboard'))

    # Convert string dates to datetime objects, if needed
    for date_field in ['given_date', 'purchase_date']:
        if date_field in asset and isinstance(asset[date_field], str):
            try:
                asset[date_field] = datetime.strptime(asset[date_field], '%Y-%m-%d')
            except ValueError:
                # If it's already in dd-mm-yyyy or invalid, skip or handle accordingly
                pass

    return render_template('view_asset.html', asset=asset)

@main_bp.route('/edit/<asset_id>', methods=['GET', 'POST'])
def edit_asset(asset_id):
    asset = assets_collection.find_one({'_id': ObjectId(asset_id)})
    if not asset:
        flash('Asset not found.', 'danger')
        return redirect(url_for('main.dashboard'))

    # Keep the original _id for later use
    original_id = asset['_id']

    def to_date(val):
        if isinstance(val, datetime):
            return val.date()
        if isinstance(val, str):
            try:
                return date_parse(val, dayfirst=False).date()
            except:
                return None
        return None

    # ✅ Convert to proper format for WTForms (date fields need datetime.date)
    asset_data = dict(asset)
    asset_data.pop('_id', None)

    asset_data['given_date'] = to_date(asset.get('given_date'))
    asset_data['purchase_date'] = to_date(asset.get('purchase_date'))  # Ensure match

    asset_data['category'] = asset.get('category', '').lower().replace(" ", "_")
    asset_data['status'] = asset.get('status', '').lower()

    form = AssetForm(data=asset_data)

    if form.validate_on_submit():
        selected_type = form.category.data
        new_type = form.new_type.data.strip()

        if selected_type == "Add New Type" and new_type:
            if not asset_types_collection.find_one({"type_name": new_type}):
                asset_types_collection.insert_one({"type_name": new_type})
            selected_type = new_type

        # Collect all form data
        raw_data = request.form.to_dict()
        raw_data["category"] = selected_type

        dynamic_fields = [
            "third_party_code", "user_code", "area", "username",
            "owner", "license", "os", "system", "system_manufacturer",
            "serial_no", "processor", "ram", "harddisk", "specification",
            "vendor", "invoice_no", "amount", "status", "remarks"
        ]

        for field in dynamic_fields:
            raw_data[field] = request.form.get(field, "").strip()

        def to_datetime(val):
            try:
                return datetime.strptime(val, "%Y-%m-%d") if val else None
            except:
                return None

        # ✅ Dates
        raw_data["given_date"] = to_datetime(request.form.get("given_date"))
        raw_data["purchase_date"] = to_datetime(request.form.get("purchase_date"))

        # ✅ Ensure owner field is updated
        raw_data["owner"] = request.form.get("owner", "").strip()

        # Normalize, fill, and update
        normalized = normalize_asset_data(raw_data)
        raw_data.update(normalized)

        updated_asset = fill_missing_asset_fields(raw_data)
        assets_collection.update_one({'_id': original_id}, {'$set': updated_asset})

        flash('Asset updated successfully!', 'success')
        return redirect(url_for("main.view_asset", asset_id=asset_id))
    asset_serializable = json.loads(json_util.dumps(asset))

    return render_template(
        "create_new_asset.html",
        form=form,
        editing=True,
        asset_data=asset_serializable,
        asset_id=asset_id
    )
