from citra_framework.core import Citra, Response

core = Citra(
    debug=False,
    enable_db=True,
    config_db={
        'hostname': 'localhost',
        'username': 'root',
        'password': '',
        'database': 'user_db'
    }
)

# --- GET FORM
async def form_page(request):
    return core.templates.display('form.html')

# --- CREATE DATA
async def submit_form(request):
    name = request.form['name']
    age = request.form['age']
    
    core.database.insert(
        'users',
        name=name,
        age=age
    )
    core.templates.message('User added successfully!', 'success')
    users = core.database.select('users')
    return core.templates.display('users.html', {'users': users})

# --- READ DATA
async def list_users(request):
    users = core.database.select('users')
    return core.templates.display('users.html', {'users': users})

# --- UPDATE DATA
async def update_form(request, age):
    user = core.database.select(
        'users',
        where='age=%s',
        where_values=(age,)
    )
    
    if not user:
        return Response('User not found.', 404)

    return core.templates.display('update.html', {'user': user[0]})
 
# --- SUBMIT UPDATED DATA
async def submit_update(request, age):
    new_name = request.form['name']
    new_age = request.form['age']
    
    core.database.update(
        'users',
        where='age=%s',
        where_values=(int(age),),
        name=new_name,
        age=new_age
    )
    core.templates.message('User updated successfully!', 'success')
    users = core.database.select('users')
    return core.templates.forward('list_users', users=users)

# --- DELETE DATA
async def delete_form(request, age):
    core.database.delete(
        'users',
        where='age=%s',
        where_values=(int(age),)
    )
    core.templates.message('User deleted successfully!', 'success')
    users = core.database.select('users')
    return core.templates.forward('list_users', users=users)

async def divide(request):
    return 10 / 0

# ---- ROUTES
core.send('/', form_page, method='GET', name='form_page')
core.send('/submit', submit_form, method='POST', name='submit_user')
core.send('/users', list_users, method='GET', name='list_users')
core.send('/delete/<age>', delete_form, method='GET')
core.send('/update_form/<age>', update_form, method='GET')
core.send('/update/<age>', submit_update, method='POST')
core.send('/divide', divide, method='GET')
core.serve()