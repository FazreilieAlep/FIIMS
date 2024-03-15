This branch is used to test the functionality of the authorization function which determine either a user or admin can do specific CRUDS operation based on User table in `backend/data/user database.db`

try to run the /backend file in your local database and test the API based on the following table

Testing User database data
| id | username | add-pmetal-inventory | remove-pmetal-inventory | update-pmetal-inventory | view-pmetal-inventory | view-minstrument-inventory |
| qwe123 | admin_1 | 1 | 1 | 1 | 1 | 1 |
| qwe456 | admin_2 | 0 | 0 | 1 | 1 | 1 |
| asd123 | user_1 | 0 | 0 | 0 | 1 | 0 |
| asd456 | user_2 | 0 | 0 | 0 | 0 | 1 |

example API call


