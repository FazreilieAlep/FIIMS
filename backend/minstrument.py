from flask import Blueprint
from flask import jsonify, g, request
import sqlite3
from markupsafe import escape

minstrument_blueprint = Blueprint('minstrument', __name__)

@minstrument_blueprint.route('/instrument')
def index():
    return 'Minstrument Index Page'

DATABASE_INSTRUMENT = 'data/database 2.db'

def get_idb():
    db = getattr(g, '_database', None)
    if db is None:
        db = sqlite3.connect(DATABASE_INSTRUMENT)
        db.row_factory = sqlite3.Row
        g._database = db
    return db

def close_connection():
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@minstrument_blueprint.teardown_app_request
def teardown(exception):
    close_connection()


""" APPLICATION API """
@minstrument_blueprint.route('/api/musical-instrument/inventory', methods=['GET'])
def get_all_musical_instrument_inventory():
    conn = get_idb()
    cursor = conn.cursor()
    cursor.execute('''
                    SELECT Instrument.*, Supplier.*, Images.link AS imageLink, Brand.brandName AS brand
                    FROM Instrument
                    LEFT JOIN Supplier ON Instrument.supplierID = Supplier.supplierID
                    LEFT JOIN (
                        SELECT instrumentID, MIN(link) AS link
                        FROM Images
                        GROUP BY instrumentID
                    ) AS Images ON Instrument.instrumentID = Images.instrumentID
                    LEFT JOIN Brand ON Instrument.brand = brandID;
                   ''')
    instruments = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]  # Get column names

    result = []
    for instrument in instruments:
        instrument_dict = {}
        for idx, value in enumerate(instrument):
            instrument_dict[column_names[idx]] = value

        result.append(instrument_dict)

    cursor.close()

    # Return the data as JSON
    return jsonify(result)


@minstrument_blueprint.route('/api/musical-instrument/inventory/<int:instrumentID>', methods=['GET'])
def get_instrument_by_id(instrumentID):
    try:
        conn = get_idb()
        cursor = conn.cursor()
        cursor.execute('''
                        SELECT Instrument.*, Supplier.*, Images.link AS imageLink, Brand.brandName AS brand
                        FROM Instrument
                        LEFT JOIN Supplier ON Instrument.supplierID = Supplier.supplierID
                        LEFT JOIN (
                            SELECT instrumentID, MIN(link) AS link
                            FROM Images
                            GROUP BY instrumentID
                        ) AS Images ON Instrument.instrumentID = Images.instrumentID
                        LEFT JOIN Brand ON Instrument.brand = brandID
                        WHERE Instrument.instrumentID = ?;
                       ''', (instrumentID,))
        instrument = cursor.fetchone()

        if instrument:
            column_names = [description[0] for description in cursor.description]  # Get column names

            instrument_dict = {}
            for idx, value in enumerate(instrument):
                instrument_dict[column_names[idx]] = value

            # Fetch images
            cursorImage = conn.cursor()
            cursorImage.execute('''
                                SELECT link
                                FROM Images
                                WHERE Images.instrumentID = ?
                                ''', (instrumentID,))
            images = cursorImage.fetchall()

            # Convert images to a list
            images_list = [{
                'itemImageSrc': image['link'],
                'thumbnailImageSrc': image['link'],
                'alt': '',
                'title': ''
            } for image in images]
            instrument_dict["images"] = images_list

            # Fetch product category
            cursorCat = conn.cursor()
            cursorCat.execute('''
                                SELECT ProductCategory.*, ProductCategoryIndex.productCategoryName AS productCategoryName
                                FROM ProductCategory
                                LEFT JOIN ProductCategoryIndex ON ProductCategory.productCategoryID = ProductCategoryIndex.productCategoryID
                                WHERE instrumentID = ?;
                                ''', (instrumentID,))
            categories = cursorCat.fetchall()

            # Convert images to a list
            category_list = [category['productCategoryName'] for category in categories]
            instrument_dict["category"] = category_list


            cursor.close()
            cursorImage.close()
            cursorCat.close()
            conn.close()  # Close connection
            return jsonify(instrument_dict)
        else:
            cursor.close()
            conn.close()  # Close connection
            return jsonify({'error': 'instrument not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Return error message and status code 500 for internal server error



@minstrument_blueprint.route('/api/musical-instrument/supplier', methods=['GET'])
def get_all_musical_instrument_supplier():
    conn = get_idb()
    cursor = conn.cursor()
    cursor.execute('''
                    SELECT *
                    FROM Supplier
                   ''')
    suppliers = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]  # Get column names

    result = []
    for supplier in suppliers:
        supplier_dict = {}
        for idx, value in enumerate(supplier):
            supplier_dict[column_names[idx]] = value
        result.append(supplier_dict)

    cursor.close()

    # Return the data as JSON
    return jsonify(result)

@minstrument_blueprint.route('/api/musical-instrument/supplier/<int:supplierID>', methods=['GET'])
def get_supplier_by_id(supplierID):
    conn = get_idb()
    cursor = conn.cursor()
    cursor.execute('''
                    SELECT *
                    FROM Supplier
                    WHERE Supplier.supplierID = ?
                   ''', (supplierID,))
    supplier = cursor.fetchone()

    if supplier:
        column_names = [description[0] for description in cursor.description]  # Get column names

        supplier_dict = {}
        for idx, value in enumerate(supplier):
            supplier_dict[column_names[idx]] = value

        cursor.close()
        return jsonify(supplier_dict)
    else:
        cursor.close()
        return jsonify({'error': 'Supplier not found'}), 404


@minstrument_blueprint.route('/api/musical-instrument/add-inventory', methods=['POST'])
def add_minstrument_inventory():
    try:
        conn = get_idb()
        cursor = conn.cursor()

        # Check content type to determine how to retrieve data
        content_type = request.headers.get('Content-Type', '')

        if 'application/json' in content_type:
            # If JSON data, parse JSON from request body
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No JSON data received'}), 400
        else:
            # If form data, retrieve data from request.form
            data = request.form

        # Define default values for missing fields
        default_values = {
            'variation': None,
            'quantity': 0,
            'price': 0.0,
            'images': [],
            'desc': ''
        }

        # Check for missing required fields
        required_fields = ['supplierName', 'instrumentName', 'productCategory', 'brand']
        missing_fields = [field for field in required_fields if field not in data]

        # Assign default values to missing fields
        for field, default_value in default_values.items():
            if field not in data:
                data[field] = default_value

        if missing_fields:
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

        # Convert supplier name and instrument name to lowercase for case-insensitive matching
        supplier_name = data['supplierName'].lower()
        instrument_name = data['instrumentName'].lower()
        brand_name = data["brand"].lower()

        # Check if instrument with the same name already exists
        cursor.execute('SELECT * FROM Instrument WHERE LOWER(instrumentName) = ?', (instrument_name,))
        existing_instrument = cursor.fetchone()
        if existing_instrument:
            return jsonify({'error': f'instrument "{data["instrumentName"]}" already exists'}), 400

        # Check if supplier exists; if not, add new supplier
        cursor.execute('SELECT supplierID FROM Supplier WHERE LOWER(supplierName) = ?', (supplier_name,))
        supplier_id = cursor.fetchone()
        if supplier_id is None:
            supplier_address = data['address'] if data['address'] else ''
            cursor.execute('INSERT INTO Supplier (supplierName, address) VALUES (?, ?)', (data['supplierName'], supplier_address))
            supplier_id = cursor.lastrowid
        else:
            supplier_id = supplier_id[0]

        # Check if brand with the same name already exists
        cursor.execute('SELECT brandID FROM Brand WHERE LOWER(brandName) = ?', (brand_name,))
        brand_id = cursor.fetchone()
        if brand_id is None:
            try:
                cursor.execute('INSERT INTO Brand (brandName) VALUES (?)', (data['brand'],))
                brand_id = cursor.lastrowid
            except sqlite3.IntegrityError:
                # Handle the case where insertion failed due to UNIQUE constraint violation
                return "Brand already exists in the database."
        else :
            brand_id = brand_id[0]

        # Retrieve last instrument ID and generate new instrument ID
        cursor.execute('SELECT COALESCE(MAX(instrumentID), 0) FROM Instrument')
        last_instrument_id = cursor.fetchone()[0]
        new_instrument_id = last_instrument_id + 1

        # Insert new instrument into the database
        cursor.execute('''
            INSERT INTO instrument (instrumentID, supplierID, instrumentName, variation, price, quantity, brand, desc )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (new_instrument_id, supplier_id, data['instrumentName'], data['variation'], data['price'], data['quantity'], brand_id, data['desc']))

        # Insert image links if exist
        for image in data['images']:
            cursor.execute('SELECT COALESCE(MAX(imageID), 0) FROM Images')
            last_image_id = cursor.fetchone()[0]
            new_image_id = last_image_id + 1
            cursor.execute('''
                            INSERT INTO Images (imageID, instrumentID, link)
                            VALUES (?, ?, ?)
                            ''', (new_image_id, new_instrument_id, image))

        # Check if productCategory exists; if not, add new category
        category_list = [];
        for category in data["productCategory"]:
            cursor.execute('SELECT productCategoryID FROM ProductCategoryIndex WHERE LOWER(productCategoryName) = ?', (category.lower(), ))
            category_id = cursor.fetchone()
            if category_id is None:
                cursor.execute('INSERT INTO ProductCategoryIndex (productCategoryName) VALUES (?)', (category,))
                category_id = cursor.lastrowid
            else:
                category_id = category_id[0]
            cursor.execute('INSERT INTO ProductCategory (instrumentID, productCategoryID) VALUES (?, ?)', (new_instrument_id, category_id,))
            category_list.append(category_id)

        conn.commit()
        cursor.close()

        # Prepare response with new instrument details
        new_instrument = {
            'instrumentID': new_instrument_id,
            'supplierID': supplier_id,
            'instrumentName': instrument_name,
            'variation': data['variation'],
            'price': data['price'],
            'quantity': data['quantity'],
            'brand': data['brand'],
            'desc': data['desc'],
            'productCategory': data['productCategory'],
            'images' : data['images']
        }

        return jsonify({'new_instrument': new_instrument}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@minstrument_blueprint.route('/api/musical-instrument/delete-inventory', methods=['POST', 'DELETE'])
def remove_minstrument_inventory():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data received'}), 400

        instrument_id = data.get('instrumentID')
        instrument_name = data.get('instrumentName')
        if not instrument_id or not instrument_name:
            return jsonify({'error': 'instrumentID and instrumentName are required fields'}), 400

        conn = get_idb()
        cursor = conn.cursor()

        # Check if instrument exists
        cursor.execute('SELECT * FROM instrument WHERE instrumentID = ?', (instrument_id,))
        if not cursor.fetchone():
            return jsonify({'error': 'instrument does not exist'}), 404

        # Delete instrument
        cursor.execute('DELETE FROM instrument WHERE instrumentID = ?', (instrument_id,))

        # Delete images
        cursor.execute('DELETE FROM Images WHERE instrumentID = ?', (instrument_id,))

        # Delete category
        cursor.execute('DELETE FROM ProductCategory WHERE instrumentID = ?', (instrument_id,))

        conn.commit()
        cursor.close()

        return jsonify({'message': f'{instrument_name} has been removed'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@minstrument_blueprint.route('/api/musical-instrument/delete-supplier', methods=['POST','DELETE'])
def remove_minstrument_supplier():
    try:
        if request.method in ['POST', 'DELETE']:
            # Parse request data
            if request.is_json:
                data = request.get_json()
                supplier_id = data.get('supplierID')
                supplier_name = data.get('supplierName')
            else:
                supplier_id = request.form.get('supplierID')
                supplier_name = request.form.get('supplierName')

            if supplier_id is None or supplier_name is None:
                return jsonify({'error': 'supplierID and/or supplierName are required fields'}), 400

            conn = get_idb()
            cursor = conn.cursor()

            # Check if supplier exists
            cursor.execute('SELECT * FROM Supplier WHERE supplierID = ?', (supplier_id,))
            if cursor.fetchone() is None:
                return jsonify({'error': 'supplier does not exist'}), 404

            # Check instrument with supplier
            cursor.execute('SELECT * FROM Instrument WHERE supplierID = ?', (supplier_id,))
            if cursor.fetchone() is not None:
                return jsonify({'error': 'There is/are instrument(s) from ' + supplier_name}), 404

            # Delete supplier
            cursor.execute('DELETE FROM Supplier WHERE supplierID = ?', (supplier_id,))
            conn.commit()
            cursor.close()

            return jsonify({'message': f'{supplier_name} has been removed'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return 'Error'

@minstrument_blueprint.route('/api/musical-instrument/delete-category', methods=['POST','DELETE'])
def remove_minstrument_category():
    try:
        if request.method in ['POST', 'DELETE']:
            # Parse request data
            if request.is_json:
                data = request.get_json()
                product_category_id = data.get('productCategoryID')
                product_category_name = data.get('productCategoryName')
            else:
                product_category_id = request.form.get('productCategoryID')
                product_category_name = request.form.get('productCategoryName')

            if product_category_id is None or product_category_name is None:
                return jsonify({'error': 'productCategoryID and/or productCategoryName are required fields'}), 400

            conn = get_idb()
            cursor = conn.cursor()

            # Check if category exists
            cursor.execute('SELECT * FROM ProductCategoryIndex WHERE productCategoryID = ?', (product_category_id,))
            if cursor.fetchone() is None:
                return jsonify({'error': 'product category does not exist'}), 404

            # Check instrument with category
            cursor.execute('SELECT * FROM ProductCategory WHERE productCategoryID = ?', (product_category_id,))
            if cursor.fetchone() is not None:
                return jsonify({'error': 'There is/are instrument(s) from ' + product_category_name}), 404

            # Delete category
            cursor.execute('DELETE FROM ProductCategoryIndex WHERE productCategoryID = ?', (product_category_id,))
            conn.commit()
            cursor.close()

            return jsonify({'message': f'{product_category_name} has been removed'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return 'Error'

@minstrument_blueprint.route('/api/musical-instrument/delete-brand', methods=['POST','DELETE'])
def remove_minstrument_brand():
    try:
        if request.method in ['POST', 'DELETE']:
            # Parse request data
            if request.is_json:
                data = request.get_json()
                brand_id = data.get('brandID')
                brand_name = data.get('brandName')
            else:
                brand_id = request.form.get('brandID')
                brand_name = request.form.get('brandName')

            if brand_id is None or brand_name is None:
                return jsonify({'error': 'brandID and/or brandName are required fields'}), 400

            conn = get_idb()
            cursor = conn.cursor()

            # Check if Brand exists
            cursor.execute('SELECT * FROM Brand WHERE brandID = ?', (brand_id,))
            if cursor.fetchone() is None:
                return jsonify({'error': 'Brand does not exist'}), 404

            # Check instrument with Brand
            cursor.execute('SELECT * FROM Instrument WHERE brand = ?', (brand_id,))
            if cursor.fetchone() is not None:
                return jsonify({'error': 'There is/are instrument(s) from ' + brand_name}), 404

            # Delete Brand
            cursor.execute('DELETE FROM Brand WHERE brandID = ?', (brand_id,))
            conn.commit()
            cursor.close()

            return jsonify({'message': f'{brand_name} has been removed'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return 'Error'


@minstrument_blueprint.route('/api/musical-instrument/update-inventory', methods=['POST'])
def update_minstrument_inventory():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data received'}), 400

        instrument_id = data.get('instrumentID')
        update_columns = data.get('update_columns')
        if not instrument_id or not update_columns:
            return jsonify({'error': 'instrumentID and update_columns are required fields'}), 400

        conn = get_idb()
        cursor = conn.cursor()

        # Check if instrument with given ID exists
        cursor.execute('SELECT * FROM instrument WHERE instrumentID = ?', (instrument_id,))
        existing_instrument = cursor.fetchone()
        if not existing_instrument:
            return jsonify({'error': f'instrument with ID {instrument_id} not found'}), 404

        print(update_columns)
        # Construct the SQL query
        if "images" in update_columns or "productCategory" in update_columns or "brand" in update_columns:
            update_columns_without_images = [col for col in update_columns if col not in ["images", "productCategory", "brand"]]
        else:
            update_columns_without_images = update_columns

        if "brand" in update_columns:
            # Fetch the brand ID based on the provided brand name
            cursor.execute("SELECT brandID FROM Brand WHERE brandName = ?", (data["brand"],))
            brand_row = cursor.fetchone()

            # Check if a brand with the provided name exists
            if brand_row:
                brand_id = brand_row[0]

                # Update the brand for the specified instrument ID
                cursor.execute('''
                            UPDATE instrument
                            SET brand = ?
                            WHERE instrumentID = ?
                            ''', (brand_id, instrument_id))

        placeholders = ', '.join(f'{col} = ?' for col in update_columns_without_images)
        values = tuple(data[col] for col in update_columns_without_images)

        # Update instrument details
        query = f'''
            UPDATE instrument
            SET {placeholders}
            WHERE instrumentID = ?
            '''
        cursor.execute(query, (*values, instrument_id))

        # Update instrument images
        insert_query = f'''
            INSERT INTO Images (imageID, instrumentID, link)
            VALUES (?, ?, ?)
            '''
        delete_query = f'''
            DELETE FROM Images
            WHERE instrumentID = ? AND link NOT IN ({', '.join(['?'] * len(data["images"]))})
            '''

        # Insert new image links
        cursor.execute('SELECT link FROM Images WHERE instrumentID = ? ', (instrument_id,))
        img_rows = cursor.fetchall()
        image_link_list = [row[0] for row in img_rows]
        for image in data["images"]:
            if image not in image_link_list:
                cursor.execute('SELECT COALESCE(MAX(imageID), 0) FROM Images')
                last_image_id = cursor.fetchone()[0]
                new_image_id = last_image_id + 1
                cursor.execute(insert_query, (new_image_id, instrument_id, image))

        # Delete images that don't exist for the instrument
        cursor.execute(delete_query, (instrument_id,) + tuple(data["images"]))


        # update category (cant add new category as per adding new instrument, super admin power )
        insert_category_query = f'''
            INSERT INTO ProductCategory (id, instrumentID, productCategoryID)
            VALUES (?, ?, ?)
            '''
        delete_category_query = f'''
            DELETE FROM ProductCategory
            WHERE instrumentID = ? AND productCategoryID NOT IN ({', '.join(['?'] * len(data["productCategory"]))})
            '''
        cursor.execute('SELECT productCategoryID FROM ProductCategory WHERE instrumentID = ?', (instrument_id,))
        cat_rows = cursor.fetchall()
        product_category_ids = [row[0] for row in cat_rows]
        for category in data["productCategory"]:
            cursor.execute('SELECT productCategoryID FROM ProductCategoryIndex WHERE productCategoryName = ?', (category,))
            result = cursor.fetchall()
            if result:  # Check if the result is not empty
                category_index_id = result[0][0]  # Fetch the category index ID from the first row
                if category_index_id not in product_category_ids:
                    cursor.execute('SELECT COALESCE(MAX(id), 0) FROM ProductCategory')
                    last_category_id = cursor.fetchone()[0]
                    new_category_id = last_category_id + 1
                    cursor.execute(insert_category_query, (new_category_id, instrument_id, category_index_id))

        update_category_ids = cursor.execute('SELECT productCategoryID FROM ProductCategoryIndex WHERE productCategoryName IN ({})'.format(', '.join(['?'] * len(data["productCategory"]))), data["productCategory"]).fetchall()
        update_category_ids = [row[0] for row in update_category_ids]
        cursor.execute(delete_category_query, (instrument_id,) + tuple(update_category_ids))

        conn.commit()
        cursor.close()

        updated_instrument = {col: val for col, val in zip(update_columns, values)}

        return jsonify({'updated_instrument': updated_instrument}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@minstrument_blueprint.route('/api/musical-instrument/update-supplier', methods=['POST'])
def update_minstrument_supplier():
    if request.method == 'POST':
        try:
            conn = get_idb()
            cursor = conn.cursor()

            # Determine content type of the request
            content_type = request.headers.get('Content-Type', '')

            if 'application/json' in content_type:
                # If JSON data, parse JSON from request body
                data = request.get_json(force=True)
                supplier_id = data['supplierID']
                update_columns = data.get('update_columns', None)
                if not update_columns:
                    return jsonify({'error': 'No columns specified for update'}), 400

                # Construct the SQL query
                placeholders = ', '.join(f'{col} = ?' for col in update_columns)
                values = tuple(data[col] for col in update_columns)
            else:
                # If form data, retrieve data from request.form
                supplier_id = request.form['supplierID']
                update_columns = request.form.getlist('update_columns')
                if not update_columns:
                    return jsonify({'error': 'No columns specified for update'}), 400

                # Construct the SQL query
                placeholders = ', '.join(f'{col} = ?' for col in update_columns)
                values = tuple(request.form[col] for col in update_columns)

            # Check if supplier with given ID exists
            cursor.execute('SELECT * FROM supplier WHERE supplierID = ?', (supplier_id,))
            existing_supplier = cursor.fetchone()
            if not existing_supplier:
                return jsonify({'error': f'supplier with ID {supplier_id} not found'}), 404

            # Update supplier details
            query = f'''
                UPDATE supplier
                SET {placeholders}
                WHERE supplierID = ?
                '''
            cursor.execute(query, (*values, supplier_id))

            conn.commit()
            cursor.close()

            updated_supplier = {col: val for col, val in zip(update_columns, values)}

            return jsonify({'updated_supplier': updated_supplier}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return 'Error'

@minstrument_blueprint.route('/api/musical-instrument/update-category', methods=['POST'])
def update_minstrument_category():
    if request.method == 'POST':
        try:
            conn = get_idb()
            cursor = conn.cursor()

            # Determine content type of the request
            content_type = request.headers.get('Content-Type', '')

            if 'application/json' in content_type:
                # If JSON data, parse JSON from request body
                data = request.get_json(force=True)
                productCategoryIndex_id = data['productCategoryID']
                update_columns = data.get('update_columns', None)
                if not update_columns:
                    return jsonify({'error': 'No columns specified for update'}), 400

                # Construct the SQL query
                placeholders = ', '.join(f'{col} = ?' for col in update_columns)
                values = tuple(data[col] for col in update_columns)
            else:
                # If form data, retrieve data from request.form
                productCategoryIndex_id = request.form['productCategoryID']
                update_columns = request.form.getlist('update_columns')
                if not update_columns:
                    return jsonify({'error': 'No columns specified for update'}), 400

                # Construct the SQL query
                placeholders = ', '.join(f'{col} = ?' for col in update_columns)
                values = tuple(request.form[col] for col in update_columns)

            # Check if category with given ID exists
            cursor.execute('SELECT * FROM ProductCategoryIndex WHERE productCategoryID = ?', (productCategoryIndex_id,))
            existing_category = cursor.fetchone()
            if not existing_category:
                return jsonify({'error': f'category with ID {productCategoryIndex_id} not found'}), 404

            # Update category details
            query = f'''
                UPDATE ProductCategoryIndex
                SET {placeholders}
                WHERE productCategoryID = ?
                '''
            cursor.execute(query, (*values, productCategoryIndex_id))

            conn.commit()
            cursor.close()

            updated_category = {col: val for col, val in zip(update_columns, values)}

            return jsonify({'updated_category': updated_category}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return 'Error'


@minstrument_blueprint.route('/api/musical-instrument/add-supplier', methods=['POST'])
def add_minstrument_supplier():
    if request.method == 'POST':
        try:
            # Connect to the database
            conn = get_idb()
            cursor = conn.cursor()

            # Determine content type of the request
            content_type = request.headers.get('Content-Type', '')

            if 'application/json' in content_type:
                # If JSON data, parse JSON from request body
                data = request.get_json(force=True)
                supplier_name = data.get('supplierName')
                address = data.get('address')
            else:
                # If form data, retrieve data from request.form
                supplier_name = request.form.get('supplierName')
                address = request.form.get('address')

            # Check if supplierName already exists in lowercase
            cursor.execute('SELECT COUNT(*) FROM Supplier WHERE LOWER(supplierName) = ?', (supplier_name.lower(),))
            existing_supplier_count = cursor.fetchone()[0]
            if existing_supplier_count > 0:
                return jsonify({'error': supplier_name + ' already exists'}), 400

            # Get the maximum supplierID
            cursor.execute('SELECT MAX(supplierID) FROM Supplier')
            max_supplier_id = cursor.fetchone()[0]
            new_supplier_id = max_supplier_id + 1

            # Insert the new supplier into the Supplier table
            cursor.execute('INSERT INTO Supplier (supplierID, supplierName, address) VALUES (?, ?, ?)',
                           (new_supplier_id, supplier_name, address))
            conn.commit()
            cursor.close()

            return jsonify({'message': 'Supplier added successfully', 'supplierID': new_supplier_id}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return 'Error'

@minstrument_blueprint.route('/api/musical-instrument/add-category', methods=['POST'])
def add_minstrument_category():
    if request.method == 'POST':
        try:
            # Connect to the database
            conn = get_idb()
            cursor = conn.cursor()

            # Determine content type of the request
            content_type = request.headers.get('Content-Type', '')

            if 'application/json' in content_type:
                # If JSON data, parse JSON from request body
                data = request.get_json(force=True)
                product_category_name = data.get('productCategoryName')
            else:
                # If form data, retrieve data from request.form
                product_category_name = request.form.get('productCategoryName')

            # Check if productCategoryName already exists in lowercase
            cursor.execute('SELECT COUNT(*) FROM ProductCategoryIndex WHERE LOWER(productCategoryName) = ?', (product_category_name.lower(),))
            existing_category_count = cursor.fetchone()[0]
            if existing_category_count > 0:
                return jsonify({'error': product_category_name + ' already exists'}), 400

            # Get the maximum categoryID
            cursor.execute('SELECT MAX(productCategoryID) FROM ProductCategoryIndex')
            max_category_id = cursor.fetchone()[0]
            new_category_id = max_category_id + 1

            # Insert the new category into the category table
            cursor.execute('INSERT INTO ProductCategoryIndex (productCategoryID, productCategoryName) VALUES (?, ?)',
                           (new_category_id, product_category_name))
            conn.commit()
            cursor.close()

            return jsonify({'message': 'category added successfully', 'productCategoryID': new_category_id}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return 'Error'

@minstrument_blueprint.route('/api/musical-instrument/add-brand', methods=['POST'])
def add_minstrument_brand():
    if request.method == 'POST':
        try:
            # Connect to the database
            conn = get_idb()
            cursor = conn.cursor()

            # Determine content type of the request
            content_type = request.headers.get('Content-Type', '')

            if 'application/json' in content_type:
                # If JSON data, parse JSON from request body
                data = request.get_json(force=True)
                brand_name = data.get('brandName')
            else:
                # If form data, retrieve data from request.form
                brand_name = request.form.get('brandName')

            # Check if brandName already exists in lowercase
            cursor.execute('SELECT COUNT(*) FROM Brand WHERE LOWER(brandName) = ?', (brand_name.lower(),))
            existing_category_count = cursor.fetchone()[0]
            if existing_category_count > 0:
                return jsonify({'error': brand_name + ' already exists'}), 400

            # Get the maximum categoryID
            cursor.execute('SELECT MAX(brandID) FROM Brand')
            max_brand_id = cursor.fetchone()[0]
            new_brand_id = max_brand_id + 1

            # Insert the new category into the category table
            cursor.execute('INSERT INTO Brand (brandID, brandName) VALUES (?, ?)',
                           (new_brand_id, brand_name))
            conn.commit()
            cursor.close()

            return jsonify({'message': 'brand added successfully', 'brandID': new_brand_id}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return 'Error'

@minstrument_blueprint.route('/api/musical-instrument/filtered-inventory', methods=['GET', 'POST'])
def get_filtered_musical_instrument_inventory():
    try:
        if request.method == 'POST':
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No JSON data received'}), 400

            conn = get_idb()
            cursor = conn.cursor()

            # Construct the SQL query dynamically based on filter conditions
            query = '''
                    SELECT instrument.*, Supplier.*, Images.link AS imageLink
                    FROM instrument
                    LEFT JOIN Supplier ON instrument.supplierID = Supplier.supplierID
                    LEFT JOIN (
                        SELECT instrumentID, MIN(link) AS link
                        FROM Images
                        GROUP BY instrumentID
                    ) AS Images ON instrument.instrumentID = Images.instrumentID
                    '''

            conditions = []
            params = []

            # search
            search_data = data.get('search data', '').replace(' ', '').lower()
            if search_data:
                conditions.append('''
                                    (LOWER(REPLACE(instrumentName, ' ', '')) LIKE ?
                                    OR LOWER(REPLACE(supplierName, ' ', '')) LIKE ?
                                    OR LOWER(REPLACE(metal, ' ', '')) LIKE ?
                                    OR LOWER(REPLACE(category, ' ', '')) LIKE ?
                                    OR LOWER(REPLACE(measurement, ' ', '')) LIKE ?)
                                    ''')
                params.extend([f'%{search_data}%'] * 5)

            # filter
            filter_data = data.get('filter data', {})
            metal_list = filter_data.get('metal', [])
            category_list = filter_data.get('category', [])
            measurement_list = filter_data.get('measurement', [])
            supplier_list = filter_data.get('supplier', [])
            weight_list = filter_data.get('weight', [])

            if supplier_list:
                temp = ', '.join(f"'{item}'" for item in supplier_list)
                conditions.append('LOWER(supplierName) IN (' + temp + ')')

            if metal_list:
                temp = ', '.join(f"'{item}'" for item in metal_list)
                conditions.append('LOWER(metal) IN (' + temp + ')')

            if category_list:
                temp = ', '.join(f"'{item}'" for item in category_list)
                conditions.append('LOWER(category) IN (' + temp + ')')

            if measurement_list:
                temp = ', '.join(f"'{item}'" for item in measurement_list)
                conditions.append('LOWER(measurement) IN (' + temp + ')')

            if weight_list:
                temp = ', '.join(weight_list)
                conditions.append('weight IN (' + temp + ')')

            if conditions:
                query += ' WHERE ' + ' AND '.join(conditions)

            cursor.execute(query, params)
            instruments = cursor.fetchall()

            column_names = [description[0] for description in cursor.description]

            # Fetch all prices at once
            unit_price = 'myr'
            cursor_price = conn.cursor()
            cursor_price.execute('''
                                SELECT metal, unit, price_per_unit
                                FROM Metal_Price
                                WHERE price_unit = ?
                                ''', (unit_price,))

            price_data = cursor_price.fetchall()
            price_dict = {(row[0], row[1]): row[2] for row in price_data}

            # Map prices to instruments
            result = []
            for instrument in instruments:
                instrument_dict = dict(zip(column_names, instrument))

                # Calculate price
                price_per_unit = price_dict.get((instrument_dict['metal'], instrument_dict['measurement']))
                if price_per_unit is not None:
                    instrument_dict["price"] = round(price_per_unit * instrument_dict['weight'], 2)
                    instrument_dict["price_with_premium"] = round(price_per_unit * instrument_dict['weight'] * (1 + instrument_dict['premium']), 2)
                else:
                    instrument_dict["price"] = None

                result.append(instrument_dict)

            cursor.close()
            cursor_price.close()

            return jsonify(result)
        elif request.method == 'GET':
            conn = get_idb()
            cursor = conn.cursor()
            cursor.execute('''
                            SELECT instrument.*, Supplier.*, Images.link AS imageLink
                            FROM instrument
                            LEFT JOIN Supplier ON instrument.supplierID = Supplier.supplierID
                            LEFT JOIN (
                                SELECT instrumentID, MIN(link) AS link
                                FROM Images
                                GROUP BY instrumentID
                            ) AS Images ON instrument.instrumentID = Images.instrumentID;
                        ''')
            instruments = cursor.fetchall()
            column_names = [description[0] for description in cursor.description]

            # Fetch all prices at once
            unit_price = 'myr'
            cursor_price = conn.cursor()
            cursor_price.execute('''
                                SELECT metal, unit, price_per_unit
                                FROM Metal_Price
                                WHERE price_unit = ?
                                ''', (unit_price,))

            price_data = cursor_price.fetchall()
            price_dict = {(row[0], row[1]): row[2] for row in price_data}

            # Map prices to instruments
            result = []
            for instrument in instruments:
                instrument_dict = dict(zip(column_names, instrument))

                # Calculate price
                price_per_unit = price_dict.get((instrument_dict['metal'], instrument_dict['measurement']))
                if price_per_unit is not None:
                    instrument_dict["price"] = round(price_per_unit * instrument_dict['weight'], 2)
                    instrument_dict["price_with_premium"] = round(price_per_unit * instrument_dict['weight'] * (1 + instrument_dict['premium']), 2)
                else:
                    instrument_dict["price"] = None

                result.append(instrument_dict)

            cursor.close()
            cursor_price.close()

            return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return 'Error'

 # API to populate db with 1000 random rows

 # API to romove populated 1000 random rows from db



# Optionally, define a function to get the blueprint
def get_minstrument_blueprint():
    return minstrument_blueprint

@minstrument_blueprint.route('/testing2')
def test2():
    return 'testing2'