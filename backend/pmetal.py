from flask import Blueprint
from flask import jsonify, g, request
import sqlite3
from markupsafe import escape
import random

pmetal_blueprint = Blueprint('pmetal', __name__)

@pmetal_blueprint.route('/')
def index():
    return 'Pmetal Index Page'

DATABASE_PRECIOUS_METAL = 'data/database 1.db'

@pmetal_blueprint.route('/testing')
def test():
    return 'testing'

def get_pmdb():
    db = getattr(g, '_database', None)
    if db is None:
        db = sqlite3.connect(DATABASE_PRECIOUS_METAL)
        db.row_factory = sqlite3.Row
        g._database = db
    return db

def close_connection():
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@pmetal_blueprint.teardown_app_request
def teardown(exception):
    close_connection()

""" APPLICATION API """
@pmetal_blueprint.route('/api/precious-metal/inventory', methods=['GET'])
def get_all_precious_metal_inventory():
    conn = get_pmdb()
    cursor = conn.cursor()
    cursor.execute('''
                    SELECT Product.*, Supplier.*, Images.link AS imageLink
                    FROM Product
                    LEFT JOIN Supplier ON Product.supplierID = Supplier.supplierID
                    LEFT JOIN (
                        SELECT productID, MIN(link) AS link
                        FROM Images
                        GROUP BY productID
                    ) AS Images ON Product.productID = Images.productID;
                   ''')
    products = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]  # Get column names

    result = []
    for product in products:
        product_dict = {}
        for idx, value in enumerate(product):
            product_dict[column_names[idx]] = value

        # Fetch price
        unit = product_dict['measurement']
        metal = product_dict['metal']
        unit_price = 'myr'
        cursor_price = conn.cursor()
        cursor_price.execute('''
                            SELECT price_per_unit
                            FROM Metal_Price
                            WHERE price_unit = ? AND unit = ? AND metal = ?
                            ''', (unit_price, unit, metal))

        price = cursor_price.fetchone()
        if price:
            product_dict["price"] = round(price[0] * product_dict['weight'], 2) # Assuming price is a single value
            product_dict["price_with_premium"] = round(price[0] * product_dict['weight'] * (1 + product_dict['premium']), 2)
        else:
            product_dict["price"] = None  # Handle case where price is not found

        result.append(product_dict)

    cursor.close()

    # Return the data as JSON
    return jsonify(result)


@pmetal_blueprint.route('/api/precious-metal/inventory/<int:productID>', methods=['GET'])
def get_product_by_id(productID):
    try:
        conn = get_pmdb()
        cursor = conn.cursor()
        cursor.execute('''
                        SELECT *
                        FROM Product
                        LEFT JOIN Supplier ON Product.supplierID = Supplier.supplierID
                        WHERE Product.productID = ?
                       ''', (productID,))
        product = cursor.fetchone()

        if product:
            column_names = [description[0] for description in cursor.description]  # Get column names

            product_dict = {}
            for idx, value in enumerate(product):
                product_dict[column_names[idx]] = value

            # Fetch price
            unit = product_dict['measurement']
            metal = product_dict['metal']
            unit_price = 'myr'
            cursor_price = conn.cursor()
            cursor_price.execute('''
                         SELECT price_per_unit
                         FROM Metal_Price
                         WHERE price_unit = ? AND unit = ? AND metal = ?
                         ''', (unit_price, unit, metal))

            price = cursor_price.fetchone()
            if price:
                product_dict["price"] = round(price[0] * product_dict['weight'], 2) # Assuming price is a single value
                product_dict["price_with_premium"] = round(price[0] * product_dict['weight'] * (1 + product_dict['premium']), 2)
            else:
                product_dict["price"] = None  # Handle case where price is not found

            # Fetch images
            cursorImage = conn.cursor()
            cursorImage.execute('''
                                SELECT link
                                FROM Images
                                WHERE Images.productID = ?
                                ''', (productID,))
            images = cursorImage.fetchall()

            # Convert images to a list
            images_list = [{
                'itemImageSrc': image['link'],
                'thumbnailImageSrc': image['link'],
                'alt': '',
                'title': ''
            } for image in images]


            product_dict["images"] = images_list
            cursor.close()
            cursorImage.close()
            cursor_price.close()
            conn.close()  # Close connection
            return jsonify(product_dict)
        else:
            cursor.close()
            conn.close()  # Close connection
            return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Return error message and status code 500 for internal server error


@pmetal_blueprint.route('/api/precious-metal/supplier', methods=['GET'])
def get_all_precious_metal_supplier():
    conn = get_pmdb()
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

@pmetal_blueprint.route('/api/precious-metal/supplier/<int:supplierID>', methods=['GET'])
def get_supplier_by_id(supplierID):
    conn = get_pmdb()
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


@pmetal_blueprint.route('/api/precious-metal/add-inventory', methods=['POST'])
def add_pmetal_inventory():
    try:
        conn = get_pmdb()
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
            'year': None,
            'quantity': 0,
            'premium': 0.0,
            'images': []
        }

        # Check for missing required fields
        required_fields = ['supplierName', 'productName', 'category', 'metal', 'measurement', 'weight']
        missing_fields = [field for field in required_fields if field not in data]

        # Assign default values to missing fields
        for field, default_value in default_values.items():
            if field not in data:
                data[field] = default_value

        if missing_fields:
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

        # Convert supplier name and product name to lowercase for case-insensitive matching
        supplier_name = data['supplierName'].lower()
        product_name = data['productName'].lower()

        # Check if product with the same name already exists
        cursor.execute('SELECT * FROM Product WHERE LOWER(productName) = ?', (product_name,))
        existing_product = cursor.fetchone()
        if existing_product:
            return jsonify({'error': f'Product "{data["productName"]}" already exists'}), 400

        # Check if supplier exists; if not, add new supplier
        cursor.execute('SELECT supplierID FROM Supplier WHERE LOWER(supplierName) = ?', (supplier_name,))
        supplier_id = cursor.fetchone()
        if supplier_id is None:
            cursor.execute('INSERT INTO Supplier (supplierName) VALUES (?)', (data['supplierName'],))
            supplier_id = cursor.lastrowid
        else:
            supplier_id = supplier_id[0]

        # Retrieve last product ID and generate new product ID
        cursor.execute('SELECT COALESCE(MAX(productID), 0) FROM Product')
        last_product_id = cursor.fetchone()[0]
        new_product_id = last_product_id + 1

        # Insert new product into the database
        cursor.execute('''
            INSERT INTO Product (productID, supplierID, productName, premium, category, metal, year,
                                measurement, weight, quantity)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (new_product_id, supplier_id, data['productName'], data['premium'], data['category'], data['metal'], data['year'], data['measurement'], data['weight'], data['quantity']))

        # Insert image links if exist
        for image in data['images']:
            cursor.execute('SELECT COALESCE(MAX(imageID), 0) FROM Images')
            last_image_id = cursor.fetchone()[0]
            new_image_id = last_image_id + 1
            cursor.execute('''
                            INSERT INTO Images (imageID, productID, link)
                            VALUES (?, ?, ?)
                            ''', (new_image_id, new_product_id, image))

        conn.commit()
        cursor.close()

        # Prepare response with new product details
        new_product = {
            'productID': new_product_id,
            'supplierID': supplier_id,
            'productName': product_name,
            'premium': data['premium'],
            'category': data['category'],
            'metal': data['metal'],
            'year': data['year'],
            'measurement': data['measurement'],
            'weight': data['weight'],
            'quantity': data['quantity'],
            'images' : data['images']
        }

        return jsonify({'new_product': new_product}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@pmetal_blueprint.route('/api/precious-metal/delete-inventory', methods=['POST', 'DELETE'])
def remove_pmetal_inventory():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data received'}), 400

        product_id = data.get('productID')
        product_name = data.get('productName')
        if not product_id or not product_name:
            return jsonify({'error': 'productID and productName are required fields'}), 400

        conn = get_pmdb()
        cursor = conn.cursor()

        # Check if product exists
        cursor.execute('SELECT * FROM Product WHERE productID = ?', (product_id,))
        if not cursor.fetchone():
            return jsonify({'error': 'Product does not exist'}), 404

        # Delete product
        cursor.execute('DELETE FROM Product WHERE productID = ?', (product_id,))

        # Delete images
        cursor.execute('DELETE FROM Images WHERE productID = ?', (product_id,))

        conn.commit()
        cursor.close()

        return jsonify({'message': f'{product_name} has been removed'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@pmetal_blueprint.route('/api/precious-metal/delete-supplier', methods=['POST','DELETE'])
def remove_pmetal_supplier():
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
                return jsonify({'error': 'supplierID and supplierName are required fields'}), 400

            conn = get_pmdb()
            cursor = conn.cursor()

            # only delete if there are no product attached to the supplier
            # force mode delete {mode: force} (KIV)  : change product.supplierID to null
            cursor.execute('SELECT * FROM Product WHERE supplierID = ?', (supplier_id,))
            if cursor.fetchone() is not None:
                return jsonify({'error': 'There still exist product from this supplier. Cannot delete supplier'}), 404

            # Check if supplier exists
            cursor.execute('SELECT * FROM Supplier WHERE supplierID = ?', (supplier_id,))
            if cursor.fetchone() is None:
                return jsonify({'error': 'supplier does not exist'}), 404

            # # change product supplierID to none
            # dataToUpdate = {

            # }
            # update_pmetal_inventory();

            # Delete supplier
            cursor.execute('DELETE FROM Supplier WHERE supplierID = ?', (supplier_id,))
            conn.commit()
            cursor.close()

            return jsonify({'message': f'{supplier_name} has been removed'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return 'Error'


@pmetal_blueprint.route('/api/precious-metal/update-inventory', methods=['POST', 'PUT'])
def update_pmetal_inventory():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data received'}), 400

        product_id = data.get('productID')
        update_columns = data.get('update_columns')
        if not product_id or not update_columns:
            return jsonify({'error': 'productID and update_columns are required fields'}), 400

        conn = get_pmdb()
        cursor = conn.cursor()

        # Check if product with given ID exists
        cursor.execute('SELECT * FROM Product WHERE productID = ?', (product_id,))
        existing_product = cursor.fetchone()
        if not existing_product:
            return jsonify({'error': f'Product with ID {product_id} not found'}), 404

        print(update_columns)
        # Construct the SQL query
        if "images" in update_columns:
            update_columns_without_images = [col for col in update_columns if col != "images"]
        else:
            update_columns_without_images = update_columns

        placeholders = ', '.join(f'{col} = ?' for col in update_columns_without_images)
        values = tuple(data[col] for col in update_columns_without_images)

        # Update product details
        query = f'''
            UPDATE Product
            SET {placeholders}
            WHERE productID = ?
            '''
        cursor.execute(query, (*values, product_id))

        # Update product images
        insert_query = f'''
            INSERT INTO Images (imageID, productID, link)
            VALUES (?, ?, ?)
            '''
        delete_query = f'''
            DELETE FROM Images
            WHERE productID = ? AND link NOT IN ({', '.join(['?'] * len(data["images"]))})
            '''

        # Insert new image links
        for image in data["images"]:
            cursor.execute('SELECT link FROM Images WHERE lower(link) = ? AND productID = ?', (image.lower(), product_id))
            existing_image = cursor.fetchone()
            if existing_image is None:
                cursor.execute('SELECT COALESCE(MAX(imageID), 0) FROM Images')
                last_image_id = cursor.fetchone()[0]
                new_image_id = last_image_id + 1
                cursor.execute(insert_query, (new_image_id, product_id, image))


        # Delete images that don't exist for the product
        cursor.execute(delete_query, (product_id,) + tuple(data["images"]))

        conn.commit()
        cursor.close()

        updated_product = {col: val for col, val in zip(update_columns, values)}

        return jsonify({'updated_product': updated_product}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pmetal_blueprint.route('/api/precious-metal/update-supplier', methods=['POST'])
def update_pmetal_supplier():
    if request.method == 'POST':
        try:
            conn = get_pmdb()
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


@pmetal_blueprint.route('/api/precious-metal/add-supplier', methods=['POST'])
def add_pmetal_supplier():
    if request.method == 'POST':
        try:
            # Connect to the database
            conn = get_pmdb()
            cursor = conn.cursor()

            # Determine content type of the request
            content_type = request.headers.get('Content-Type', '')

            if 'application/json' in content_type:
                # If JSON data, parse JSON from request body
                data = request.get_json(force=True)
                supplier_name = data.get('supplierName')
            else:
                # If form data, retrieve data from request.form
                supplier_name = request.form.get('supplierName')

            # Check if supplierName already exists in lowercase
            cursor.execute('SELECT COUNT(*) FROM Supplier WHERE LOWER(supplierName) = ?', (supplier_name.lower(),))
            existing_supplier_count = cursor.fetchone()[0]
            if existing_supplier_count > 0:
                return jsonify({'error': 'Supplier already exists'}), 400

            # Get the maximum supplierID
            cursor.execute('SELECT MAX(supplierID) FROM Supplier')
            max_supplier_id = cursor.fetchone()[0]
            new_supplier_id = max_supplier_id + 1

            # Insert the new supplier into the Supplier table
            cursor.execute('INSERT INTO Supplier (supplierID, supplierName) VALUES (?, ?)',
                           (new_supplier_id, supplier_name))
            conn.commit()
            cursor.close()

            return jsonify({'message': 'Supplier added successfully', 'supplierID': new_supplier_id}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return 'Error'

@pmetal_blueprint.route('/api/precious-metal/filtered-inventory', methods=['GET', 'POST'])
def get_filtered_precious_metal_inventory():
    try:
        if request.method == 'POST':
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No JSON data received'}), 400

            conn = get_pmdb()
            cursor = conn.cursor()

            # Construct the SQL query dynamically based on filter conditions
            query = '''
                    SELECT Product.*, Supplier.*, Images.link AS imageLink
                    FROM Product
                    LEFT JOIN Supplier ON Product.supplierID = Supplier.supplierID
                    LEFT JOIN (
                        SELECT productID, MIN(link) AS link
                        FROM Images
                        GROUP BY productID
                    ) AS Images ON Product.productID = Images.productID
                    '''

            conditions = []
            params = []

            # search
            search_data = data.get('search data', '').replace(' ', '').lower()
            if search_data:
                conditions.append('''
                                    (LOWER(REPLACE(productName, ' ', '')) LIKE ?
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
            products = cursor.fetchall()

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

            # Map prices to products
            result = []
            for product in products:
                product_dict = dict(zip(column_names, product))

                # Calculate price
                price_per_unit = price_dict.get((product_dict['metal'], product_dict['measurement']))
                if price_per_unit is not None:
                    product_dict["price"] = round(price_per_unit * product_dict['weight'], 2)
                    product_dict["price_with_premium"] = round(price_per_unit * product_dict['weight'] * (1 + product_dict['premium']), 2)
                else:
                    product_dict["price"] = None

                result.append(product_dict)

            cursor.close()
            cursor_price.close()

            return jsonify(result)
        elif request.method == 'GET':
            conn = get_pmdb()
            cursor = conn.cursor()
            cursor.execute('''
                            SELECT Product.*, Supplier.*, Images.link AS imageLink
                            FROM Product
                            LEFT JOIN Supplier ON Product.supplierID = Supplier.supplierID
                            LEFT JOIN (
                                SELECT productID, MIN(link) AS link
                                FROM Images
                                GROUP BY productID
                            ) AS Images ON Product.productID = Images.productID;
                        ''')
            products = cursor.fetchall()
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

            # Map prices to products
            result = []
            for product in products:
                product_dict = dict(zip(column_names, product))

                # Calculate price
                price_per_unit = price_dict.get((product_dict['metal'], product_dict['measurement']))
                if price_per_unit is not None:
                    product_dict["price"] = round(price_per_unit * product_dict['weight'], 2)
                    product_dict["price_with_premium"] = round(price_per_unit * product_dict['weight'] * (1 + product_dict['premium']), 2)
                else:
                    product_dict["price"] = None

                result.append(product_dict)

            cursor.close()
            cursor_price.close()

            return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return 'Error'

# API to populate db with 1000 random rows
@pmetal_blueprint.route('/api/precious-metal/add-1000-random-rows')
def add_1000_random_pmetal_inventory():
    try:
        conn = get_pmdb()
        cursor = conn.cursor()

        # Get products
        cursor.execute('SELECT productID FROM Product WHERE LOWER(productName) LIKE ?', ('%random%',))
        existing_rows = cursor.fetchall()
        if existing_rows:
            return jsonify({'message': 'Random rows already exist'})

        supplier_names = ['supplier ' + str(n) for n in range(20)]
        categories = ['coin', 'bar']
        metals = ['gold', 'silver']
        measurements = ['oz', 'g', 'kg']
        images = ['image', 'urlx', 'img']
        weight_range = (0.5, 5.0)
        year_range = (2000, 2025)
        quantity_range = (5, 50)
        premium_range = (0.25, 1.3)

        for i in range(1000):
            data = {
                'supplierName': random.choice(supplier_names),
                'productName': "random product " + str(i),
                'category': random.choice(categories),
                'metal': random.choice(metals),
                'measurement': random.choice(measurements),
                'weight': random.uniform(weight_range[0], weight_range[1]),
                'year': random.randint(year_range[0], year_range[1]),
                'quantity': random.randint(quantity_range[0], quantity_range[1]),
                'premium': random.uniform(premium_range[0], premium_range[1]),
                'images': [random.choice(images) + str(i) + '.jpg']
            }

            supplier_name = data['supplierName'].lower()

            cursor.execute('SELECT supplierID FROM Supplier WHERE LOWER(supplierName) = ?', (supplier_name,))
            supplier_id = cursor.fetchone()

            if supplier_id is None:
                cursor.execute('INSERT INTO Supplier (supplierName) VALUES (?)', (data['supplierName'],))
                supplier_id = cursor.lastrowid
            else:
                supplier_id = supplier_id[0]

            cursor.execute('''
                INSERT INTO Product (supplierID, productName, premium, category, metal, year,
                                    measurement, weight, quantity)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (supplier_id, data['productName'], data['premium'], data['category'], data['metal'], data['year'], data['measurement'], data['weight'], data['quantity']))

            product_id = cursor.lastrowid

            # Insert image links if exist
            for image in data['images']:
                cursor.execute('SELECT COALESCE(MAX(imageID), 0) FROM Images')
                last_image_id = cursor.fetchone()[0]
                new_image_id = last_image_id + 1
                cursor.execute('''
                                INSERT INTO Images (imageID, productID, link)
                                VALUES (?, ?, ?)
                                ''', (new_image_id, product_id, image))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': '1000 random rows added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# remove the 1000 random data
@pmetal_blueprint.route('/api/precious-metal/delete-random-rows')
def remove_random_pmetal_inventory():
    try:
        conn = get_pmdb()
        cursor = conn.cursor()

        # Get products
        cursor.execute('SELECT productID FROM Product WHERE LOWER(productName) LIKE ?', ('%random%',))
        productIDs = cursor.fetchall()

        # Delete product
        for id_tuple in productIDs:
            product_id = id_tuple[0]
            cursor.execute('DELETE FROM Product WHERE productID = ?', (product_id,))

        # Delete images
        for id_tuple in productIDs:
            product_id = id_tuple[0]
            cursor.execute('DELETE FROM Images WHERE productID = ?', (product_id,))

        # Delete supplier
        cursor.execute('''
                        DELETE FROM Supplier
                        WHERE supplierID NOT IN (SELECT DISTINCT supplierID FROM Product)
                    ''')

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Random rows have been removed'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Optionally, define a function to get the blueprint
def get_pmetal_blueprint():
    return pmetal_blueprint