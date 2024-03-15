# Authorization Functionality Testing

This branch is dedicated to testing the functionality of the authorization system, which determines whether a user or admin can perform specific CRUD operations based on roles assigned in the User table of the `backend/data/user database.db`.

## API Usage

To test the API, ensure to add the following query parameters to the API endpoints:

?user_id=<id>&username=<username>

## Tested Endpoints

- `/api/precious-metal/inventory`
- `/api/precious-metal/add-inventory`
- `/api/precious-metal/delete-inventory`
- `/api/precious-metal/update-inventory`
- `/api/musical-instrument/inventory`

## Testing User Database Data

### User Permissions

| id     | username | add-pmetal-inventory | remove-pmetal-inventory | update-pmetal-inventory | view-pmetal-inventory | view-minstrument-inventory |
|--------|----------|----------------------|-------------------------|-------------------------|-----------------------|----------------------------|
| qwe123 | admin_1  | 1                    | 1                       | 1                       | 1                     | 1                          |
| qwe456 | admin_2  | 0                    | 0                       | 1                       | 1                     | 1                          |
| asd123 | user_1   | 0                    | 0                       | 0                       | 1                     | 0                          |
| asd456 | user_2   | 0                    | 0                       | 0                       | 0                     | 1                          |

## Example API Calls

| Username | Operation | Sample | Status |
|----------|-----------|--------|--------|
| user_1   | VIEW      | <img src="/src/assets/pmetal-inventory-user-1.png" alt="user_1"> | Authorized |
| user_2   | VIEW      | <img src="/src/assets/pmetal-inventory-user-2.png" alt="user_2"> | Restricted |
| admin_1  | DELETE    | <img src="/src/assets/remove-pmetal-inventory-admin-1.png" alt="admin_1"> | Authorized |
| admin_2  | DELETE    | <img src="/src/assets/remove-pmetal-inventory-admin-2.png" alt="admin_2"> | Restricted |




