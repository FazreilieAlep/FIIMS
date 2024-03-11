# Inventory Management System Personal Project

**Live Site**: [Inventory Management System](https://fiims-1.onrender.com/)

**Important Note:**
- Please avoid refreshing the page to prevent encountering 'Not Found' errors due to cloud server issues.
- The precious metal inventory section emphasizes backend functionality, while the musical instrument inventory section focuses on frontend design. As a result, CRUD operations for musical inventory are not available on the frontend at the moment. However, CRUD operations can still be performed through the API.
  

## Tech Stack
- **Frontend**: Angular
- **Backend**: Flask
- **Database**: SQLite

## Repository Structure
The frontend is located in the root of this repository, while the backend part is in the `/backend` folder.

## Deployment on Local Machine
Follow the steps below to deploy the project on your local computer.

### Setup
1. Clone this project to your local directory (e.g., `C:\\FIIMS_project`). The cloned codes in the root folder constitute your Angular or frontend application.
2. Open the project (`C:\\FIIMS_project`) in a code editor and run `npm install` in the project terminal to install Angular dependencies. For more details, visit the [Angular Setup Guide](https://angular.io/guide/setup-local).
3. Now, open `C:\\FIIMS_project\backend` in another code editor and run `pip install -r requirements.txt` in the terminal to install Python dependencies.

### Deployment
1. Run `ng serve` to start the frontend server.
2. Run `flask run --debug` in the `backend` directory to start the backend server.

### Access
- Access the frontend application via `http://localhost:4200/`.
- Access the backend API through `http://127.0.0.1:5000/` followed by the specific API calls.

# API Call List
- For POST, PUT, or DELETE request methods, users should send JSON object data as described in the table given.
  
## Precious Metal Inventory ( /api/precious-metal + API )
| API                            | Method | JSON Data Format | Description |
|--------------------------------|--------|---------------|------|
| /inventory  | GET, POST | None   | Get the precious metal data list. Has a working API query params (refer Example of API usage section --> Fetch Operation section) |
| /inventory/<int:productID>         | GET  | None | Get precious metal data with id == productID |
| /supplier     | GET  | None   | Get the supplier data |
| /supplier/<int:supplierID>     | GET  | None   | Get the supplier data where its id = supplierID |
| /add-inventory     | POST  | {"supplierName" : string, "productName" : string, "category" : string, "metal" : string, "measurement" : string, "weight" : int, "images" : string[]? 'year': int?, 'quantity': int?, 'premium': float?,}   | Add new precious metal product |
| /delete-inventory     | POST, DELETE  | {"productID" : int, "productName" : string} | Remove a precious metal product |
| /add-supplier     | POST  | {"supplierName" : string} | Add new supplier |
| /delete-supplier     | POST, DELETE  | {"supplierID" : int, "supplierName" : string} | Remove a supplier |
| /update-inventory | POST, PUT | { "productID": int, "update_columns": string[]; "column_name_1": ?, "column_name_2": ?, ..., "column_name_n": ?} | Update a precious metal product |
| /update-supplier  | POST | { "supplierID": int, "update_columns": string[]; "column_name_1": ?, "column_name_2": ?, ..., "column_name_n": ?} | Update a supplier |
| /filtered-inventory | GET, POST | { "search data" : string, "filter data" : { "category" : string[], "metal" : string[], "weight" : string[], "measurement" : string[] } | Get a filtered precious metal list |
| /add-1000-random-rows  | GET | None | Add 1000 randomly generated rows of precious metal data |
| /delete-random-rows | GET | None | Delete the newly created random data |


## Musical Instrument Inventory ( /api/musical-instrument + API)
| API                                               | Method       | JSON Data | Description                                           |
|---------------------------------------------------|--------------|-----------|--------------------------------------------------------|
| /inventory                 | GET          | None      | Get the musical instrument data list                  |
| /inventory/<int:productID> | GET          | None      | Get musical instrument data with id == productID       |
| /supplier                  | GET          | None      | Get the supplier data                                 |
| /supplier/<int:supplierID> | GET          | None      | Get the supplier data where its id = supplierID        |
| /add-inventory             | POST         | {'supplierName' : string, 'instrumentName' : string, 'productCategory' : string[], 'brand' : string, 'variation': string?, 'quantity': int?, 'price': float?, 'images': string[]?, 'desc': string?, 'address': string?} | Add new musical instrument product                    | 
| /delete-inventory          | POST, DELETE | {"instrumentID" : int, "instrumentName" : string} | Remove a musical instrument product                    |
| /add-supplier              | POST         | {"supplierID" : int, "supplierName" : string}, "address": string | Add new supplier                                      |
| /delete-supplier           | POST, DELETE | {"supplierID" : int, "supplierName" : string} | Remove a supplier                                      |
| /update-inventory          | POST, PUT    | { "instrumentID": int, "update_columns": string[]; "column_name_1": ?, "column_name_2": ?, ..., "column_name_n": ?} | Update a musical instrument product                   |
| /update-supplier           | POST         | { "supplierID": int, "update_columns": string[]; "column_name_1": ?, "column_name_2": ?, ..., "column_name_n": ?} | Update a supplier                                     |
| /add-category              | POST         | {"productCategoryName" : string} | Add a new instrument category                         |
| /add-brand                 | POST         | {"brandName" : string} | Add a new brand                                       |
| /delete-category           | POST, DELETE | {"productCategoryID": int, "productCategoryName": string} | Delete an instrument category label if and only if there are no instrument exist for the removed category |
| /delete-brand              | POST, DELETE | {"brandID" : int, "brandName" : string} | Delete a brand label if and only if there are no instrument exist for the removed brand |
| /update-category           | POST         | { "productCategoryID": int, "update_columns": string[]; "column_name_1": ?, "column_name_2": ?, ..., "column_name_n": ?} | Update a category label details                      |

### Example of API Usage
API testing is done by using **APIDOG**: [https://apidog.com/]

#### Fetch Operation
- get all precious metal inventory data `http://localhost:5000/api/precious-metal/inventory` : access hosted API here [https://izz123.pythonanywhere.com/api/precious-metal/inventory]
- get all musical instrument inventory data `http://localhost:5000/api/musical-instrument/inventory` : access hosted API here [https://izz123.pythonanywhere.com/api/musical-instrument/inventory]
- get specific precious metal by id `http://localhost:5000/api/precious-metal/inventory/:id` : access hosted API here [https://izz123.pythonanywhere.com/api/precious-metal/inventory/1]
- get filtered data though API query by `http://localhost:5000/api/precious-metal/inventory?params=...` : sample query [https://izz123.pythonanywhere.com/api/precious-metal/inventory?metal=silver&search=scottdale&category=bar&measurement=oz]
![/api/precious-metal/inventory?params...](/src/assets/pmetal-inventory-api-query.png)

query details

search : any string

metal : [gold, silver]

category : [coin, bar]

measurement : [oz,g,kg]

to select 2 or more categorical params(metal, category and measurement), insert params one by one. eg `[https://izz123.pythonanywhere.com/api/precious-metal/inventory?category=bar&category=coin]`

#### Add operation
![/api/precious-metal/add-inventory](/src/assets/add-inventory-api.png)
![/api/musical-instrument/add-inventory](/src/assets/add-inventory-api-2.png)

#### Delete operation
![/api/precious-metal/delete-supplier](/src/assets/delete-supplier-api.png)

#### Update operation
![/api/precious-metal/update-inventory](/src/assets/update-inventory-api.png)
![/api/musical-instrument/update-supplier](/src/assets/update-category-api.png)

to get column names to pass to update_columns in update API, refer the ERD diagram below:

##### Precious Metal ERD
![Precious Metal ERD](/src/assets/Precious-Metal-Inventory-ERD.png)

##### Musical Instrument ERD
![Musical Instrument ERD](/src/assets/Musical-Instrument-Inventory-ERD.png)


#### Search/Filter through JSON query
![/api/precious-metal/filter-inventory](/src/assets/filter-inventory-api.png)

#### Search/Filter through API query

Feel free to reach out if you have any questions or need further assistance. Happy coding!
