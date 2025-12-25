from nicegui import ui, app
from backend.auth import login_user, register_user
import os

def create_pages():
    @ui.page('/')
    def home():
        # Initialize user storage if not present
        if 'user' not in app.storage.user:
            app.storage.user['user'] = None

        with ui.column().classes('w-full items-center justify-center min-h-screen bg-gray-100'):
            with ui.card().classes('w-96 p-8 shadow-lg'):
                ui.label('Welcome to Roomify').classes('text-2xl font-bold mb-6 text-center w-full text-blue-600')
                
                with ui.tabs().classes('w-full') as tabs:
                    login_tab = ui.tab('Login')
                    signup_tab = ui.tab('Sign Up')

                with ui.tab_panels(tabs, value=login_tab).classes('w-full'):
                    
                    # Login Panel
                    with ui.tab_panel(login_tab):
                        email = ui.input('Email').classes('w-full mb-2')
                        password = ui.input('Password', password=True, password_toggle_button=True).classes('w-full mb-4')
                        
                        def try_login():
                            user, message = login_user(email.value, password.value)
                            if user:
                                ui.notify(message, type='positive')
                                app.storage.user['user'] = user
                                ui.open('/dashboard')
                            else:
                                ui.notify(message, type='negative')

                        ui.button('Log In', on_click=try_login).classes('w-full bg-blue-600 text-white')

                    # Sign Up Panel
                    with ui.tab_panel(signup_tab):
                        reg_name = ui.input('Name').classes('w-full mb-2')
                        reg_email = ui.input('Email').classes('w-full mb-2')
                        reg_phone = ui.input('Phone').classes('w-full mb-2')
                        reg_pass = ui.input('Password', password=True, password_toggle_button=True).classes('w-full mb-4')

                        def try_register():
                            if not all([reg_name.value, reg_email.value, reg_phone.value, reg_pass.value]):
                                ui.notify('Please fill all fields', type='warning')
                                return
                            
                            success, message = register_user(reg_name.value, reg_email.value, reg_phone.value, reg_pass.value)
                            if success:
                                ui.notify(message, type='positive')
                                tabs.set_value(login_tab) # Switch to login tab
                            else:
                                ui.notify(message, type='negative')

                        ui.button('Sign Up', on_click=try_register).classes('w-full bg-green-600 text-white')

    @ui.page('/dashboard')
    def dashboard():
        # Initialize user storage if not present, though usually it would be from home
        if 'user' not in app.storage.user:
             app.storage.user['user'] = None

        user = app.storage.user['user']
        
        with ui.column().classes('w-full items-center p-8'):
             ui.label('Dashboard').classes('text-3xl font-bold mb-4')
             if user:
                 ui.label(f'Welcome, {user["name"]}!').classes('text-lg text-gray-700')
             else:
                 ui.label('You represent not logged in.').classes('text-lg text-red-500')
             
             def logout():
                 app.storage.user['user'] = None
                 ui.open('/')

             ui.button('Log Out', on_click=logout).classes('mt-4 bg-red-500 text-white')
