# Permission Based Example and repository standarization



## data inside sqlite3

**permission list**
- Super Permission (SUPER)
- Account Management (ACCOUNTMANAGEMENT)
- Permission 1 (PERMISSION1)
- Permission 2 (PERMISSION2)

Default Role will be Admin and Superadmin.

**role list with each role's permission**
- Super Admin = Super Permission, Account Management, Permission 1, Permission 2
- Admin = Account Management, Permission 1, Permission 2
- Test Role = Permission 1, Permission 2


## Access Setup in this repo

Account management viewset only can be accessed if account's role has "Account Management" permission
Role management viewset only can be accessed if account's role has "Super" permission


## how to run

```bash
git clone https://github.com/Gerardy01/permission-based
cd permisson-based
python -m venv ./venv

venv/Scripts/activate <for windows>
. venv/bin/activate <for macos>

python manage.py install -r requirements.txt
python manage.py runserver



