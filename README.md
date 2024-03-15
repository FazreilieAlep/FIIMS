This branch is used to test the functionality of the authorization function which determine either a user or admin can do specific CRUDS operation based on User table in `backend/data/user database.db`

ensure to add API Query : ?user_id=<id>&username=<username> to test the API

only /api/pmetal/ for inventory CRUD and /api/musical-instrument/inventory is tested as listed below 
- /api/precious-metal/inventory
- /api/precious-metal/add-inventory
- /api/precious-metal/delete-inventory
- /api/precious-metal/update-inventory
- /api/musical-instrument/inventory

try to run the /backend file in your local database and test the API based on the following table

**Testing User database data
| id | username | add-pmetal-inventory | remove-pmetal-inventory | update-pmetal-inventory | view-pmetal-inventory | view-minstrument-inventory |
| qwe123 | admin_1 | 1 | 1 | 1 | 1 | 1 |
| qwe456 | admin_2 | 0 | 0 | 1 | 1 | 1 |
| asd123 | user_1 | 0 | 0 | 0 | 1 | 0 |
| asd456 | user_2 | 0 | 0 | 0 | 0 | 1 |

***example API call
| API | Sample |
| /api/precious-metal/inventory?user_id=qwe123&username=admin_1 | ![1](/src/assets/add-inventory-api.png)|




