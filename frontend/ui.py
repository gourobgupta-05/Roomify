from nicegui import ui, app
from backend.auth import login_user, register_user
from backend.rooms import (
    get_all_available_rooms, search_rooms, get_room_details, 
    is_room_available, get_all_rooms, get_all_locations,
    create_room, update_room, delete_room
)
from backend.bookings import (
    create_booking, get_user_bookings, get_all_bookings,
    update_booking_status, calculate_total_cost
)
from datetime import datetime, timedelta

# Helper function to check if user is logged in
def require_login():
    """Check if user is logged in, redirect to home if not."""
    if 'user' not in app.storage.user or not app.storage.user['user']:
        ui.navigate.to('/')
        return None
    return app.storage.user['user']

def require_admin():
    """Check if user is admin, redirect if not."""
    user = require_login()
    if not user or user.get('user_type') != 'admin':
        ui.navigate.to('/')
        return None
    return user

def create_pages():
    
    # ==================== LOGIN / SIGNUP PAGE ====================
    @ui.page('/')
    def home():
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
                                
                                # Redirect based on user type
                                if user.get('user_type') == 'admin':
                                    ui.navigate.to('/admin')
                                else:
                                    ui.navigate.to('/dashboard')
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
                                tabs.set_value(login_tab)
                            else:
                                ui.notify(message, type='negative')

                        ui.button('Sign Up', on_click=try_register).classes('w-full bg-green-600 text-white')

    # ==================== USER DASHBOARD ====================
    @ui.page('/dashboard')
    def dashboard():
        user = require_login()
        if not user:
            return
        if user.get('user_type') == 'admin':
            ui.navigate.to('/admin')
            return

        with ui.column().classes('w-full p-4'):
            # Header
            with ui.row().classes('w-full items-center justify-between mb-4'):
                ui.label('Roomify - Browse Rooms').classes('text-3xl font-bold')
                with ui.row():
                    ui.button('My Bookings', on_click=lambda: ui.navigate.to('/my-bookings')).classes('bg-blue-500 text-white')
                    ui.button('Logout', on_click=lambda: (app.storage.user.update({'user': None}), ui.navigate.to('/'))).classes('bg-red-500 text-white')
            
            # Search bar
            with ui.row().classes('w-full gap-2 mb-4'):
                search_input = ui.input('Search by city or area').classes('flex-grow')
                ui.button('Search', on_click=lambda: load_rooms(search_input.value)).classes('bg-blue-600 text-white')
            
            # Room cards container
            rooms_container = ui.column().classes('w-full')
            
            def load_rooms(search_query=None):
                rooms_container.clear()
                
                if search_query:
                    rooms = search_rooms(search_query)
                else:
                    rooms = get_all_available_rooms()
                
                if not rooms:
                    with rooms_container:
                        ui.label('No rooms available').classes('text-gray-500 text-center')
                    return
                
                with rooms_container:
                    with ui.row().classes('w-full flex-wrap gap-4'):
                        for room in rooms:
                            with ui.card().classes('w-80 cursor-pointer hover:shadow-xl transition-shadow'):
                                # Room image
                                if room.get('image_url'):
                                    ui.image(room['image_url']).classes('w-full h-48 object-cover')
                                else:
                                    ui.label('📷 No Image').classes('w-full h-48 flex items-center justify-center text-4xl bg-gray-200')
                                
                                with ui.column().classes('p-4'):
                                    ui.label(f"{room.get('city', 'Unknown')}, {room.get('area', '')}").classes('font-bold text-lg')
                                    ui.label(room.get('description', 'No description')[:100]).classes('text-gray-600 text-sm')
                                    ui.label(f"TK {room['price']}/night").classes('text-blue-600 font-bold text-xl mt-2')
                                    ui.button('View Details', on_click=lambda r=room: ui.navigate.to(f'/room/{r["Room_id"]}')).classes('w-full bg-blue-600 text-white mt-2')
            
            search_input.on('keydown.enter', lambda: load_rooms(search_input.value))
            search_input.on('change', lambda: load_rooms(search_input.value))
            load_rooms()

    # ==================== ROOM DETAILS & BOOKING ====================
    @ui.page('/room/{room_id}')
    def room_details(room_id: int):
        user = require_login()
        if not user:
            return
        if user.get('user_type') == 'admin':
            ui.navigate.to('/admin')
            return

        room = get_room_details(room_id)
        if not room:
            ui.label('Room not found').classes('text-red-600')
            return

        with ui.column().classes('w-full p-8 max-w-4xl mx-auto'):
            ui.button('← Back to Rooms', on_click=lambda: ui.navigate.to('/dashboard')).classes('mb-4')
            
            # Room Image
            if room.get('image_url'):
                ui.image(room['image_url']).classes('w-full h-96 object-cover rounded-lg')
            else:
                ui.label('📷 No Image Available').classes('w-full h-96 flex items-center justify-center text-6xl bg-gray-200 rounded-lg')
            
            # Room Info
            ui.label(f"{room.get('city', 'Unknown')}, {room.get('area', '')}").classes('text-2xl font-bold mt-4')
            ui.label(room.get('description', 'No description')).classes('text-gray-700 mt-2')
            ui.label(f"Price: TK {room['price']}/night").classes('text-3xl text-blue-600 font-bold mt-4')
            
            # Booking Form
            ui.label('Book This Room').classes('text-xl font-bold mt-8 mb-4')
            
            tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            day_after = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')
            
            check_in_input = ui.input('Check-in Date', value=tomorrow).props('type=date')
            check_out_input = ui.input('Check-out Date', value=day_after).props('type=date')
            
            def show_payment_popup():
                check_in = check_in_input.value
                check_out = check_out_input.value
                
                if not check_in or not check_out:
                    ui.notify('Please select check-in and check-out dates', type='warning')
                    return
                
                if check_in >= check_out:
                    ui.notify('Check-out date must be after check-in date', type='warning')
                    return
                
                # Check availability
                if not is_room_available(room_id, check_in, check_out):
                    ui.notify('Room is not available for selected dates', type='negative')
                    return
                
                total_cost, num_nights = calculate_total_cost(room['price'], check_in, check_out)
                
                with ui.dialog() as dialog, ui.card().classes('p-6'):
                    ui.label('Confirm Payment').classes('text-2xl font-bold mb-4')
                    ui.label(f'Room: {room.get("city")}, {room.get("area")}').classes('mb-2')
                    ui.label(f'Check-in: {check_in}').classes('mb-2')
                    ui.label(f'Check-out: {check_out}').classes('mb-2')
                    ui.label(f'Nights: {num_nights}').classes('mb-2')
                    ui.label(f'Total Cost: TK {total_cost:.2f}').classes('text-2xl font-bold text-blue-600 mb-4')
                    
                    def confirm_booking():
                        success, message, booking_id = create_booking(
                            user['user_id'], room_id, check_in, check_out, room['price']
                        )
                        if success:
                            ui.notify(message, type='positive')
                            dialog.close()
                            ui.navigate.to('/my-bookings')
                        else:
                            ui.notify(message, type='negative')
                    
                    with ui.row().classes('w-full gap-2'):
                        ui.button('Confirm & Pay', on_click=confirm_booking).classes('flex-1 bg-green-600 text-white')
                        ui.button('Cancel', on_click=dialog.close).classes('flex-1 bg-gray-500 text-white')
                
                dialog.open()
            
            ui.button('Book Now', on_click=show_payment_popup).classes('w-full bg-green-600 text-white text-lg mt-4')

    # ==================== MY BOOKINGS ====================
    @ui.page('/my-bookings')
    def my_bookings():
        user = require_login()
        if not user:
            return
        if user.get('user_type') == 'admin':
            ui.navigate.to('/admin')
            return

        with ui.column().classes('w-full p-8'):
            with ui.row().classes('w-full items-center justify-between mb-4'):
                ui.label('My Bookings').classes('text-3xl font-bold')
                ui.button('← Back to Dashboard', on_click=lambda: ui.navigate.to('/dashboard')).classes('bg-blue-500 text-white')
            
            bookings = get_user_bookings(user['user_id'])
            
            if not bookings:
                ui.label('No bookings yet').classes('text-gray-500 text-center mt-8')
                return
            
            for booking in bookings:
                with ui.card().classes('w-full p-4 mb-4'):
                    with ui.row().classes('w-full items-center justify-between'):
                        with ui.column():
                            ui.label(f"{booking.get('city', 'Unknown')}, {booking.get('area', '')}").classes('font-bold text-lg')
                            ui.label(f"Check-in: {booking['check_in_date']} | Check-out: {booking['check_out_date']}").classes('text-gray-600')
                            ui.label(f"Total: TK {booking['Total_cost']:.2f}").classes('text-blue-600 font-bold')
                        
                        status_color = {
                            'Pending': 'bg-yellow-500',
                            'Confirmed': 'bg-green-500',
                            'Cancelled': 'bg-red-500',
                            'Completed': 'bg-blue-500'
                        }.get(booking['status'], 'bg-gray-500')
                        
                        ui.label(booking['status']).classes(f'{status_color} text-white px-4 py-2 rounded')

    # ==================== ADMIN DASHBOARD ====================
    @ui.page('/admin')
    def admin_dashboard():
        user = require_admin()
        if not user:
            return

        with ui.column().classes('w-full p-8'):
            with ui.row().classes('w-full items-center justify-between mb-4'):
                ui.label('Admin Dashboard').classes('text-3xl font-bold')
                ui.button('Logout', on_click=lambda: (app.storage.user.update({'user': None}), ui.navigate.to('/'))).classes('bg-red-500 text-white')
            
            with ui.tabs().classes('w-full') as tabs:
                rooms_tab = ui.tab('Manage Rooms')
                bookings_tab = ui.tab('Manage Bookings')
            
            with ui.tab_panels(tabs, value=rooms_tab).classes('w-full'):
                
                # ========== MANAGE ROOMS TAB ==========
                with ui.tab_panel(rooms_tab):
                    rooms_container = ui.column().classes('w-full')
                    
                    def load_admin_rooms():
                        rooms_container.clear()
                        
                        with rooms_container:
                            # Add Room Button
                            def show_add_room_dialog():
                                with ui.dialog() as dialog, ui.card().classes('p-6 w-96'):
                                    ui.label('Add New Room').classes('text-2xl font-bold mb-4')
                                    
                                    price_input = ui.input('Price per Night').props('type=number')
                                    desc_input = ui.textarea('Description')
                                    image_input = ui.input('Image URL')
                                    
                                    locations = get_all_locations()
                                    location_options = {f"{loc['city']}, {loc['area']}": loc['Postal_code'] for loc in locations}
                                    location_select = ui.select(location_options, label='Location')
                                    
                                    def add_room():
                                        if not all([price_input.value, desc_input.value, location_select.value]):
                                            ui.notify('Please fill all required fields', type='warning')
                                            return
                                        
                                        try:
                                            price = float(price_input.value)
                                        except ValueError:
                                            ui.notify('Invalid price format', type='warning')
                                            return
                                            
                                        # Use admin_id from user session, ensuring it exists
                                        admin_id = user.get('admin_id')
                                        if not admin_id:
                                            ui.notify('Admin session invalid. Please relogin.', type='negative')
                                            return
                                        
                                        print(f"DEBUG UI: location_select.value = '{location_select.value}' (type: {type(location_select.value)})")
                                        
                                        try:
                                            success, message = create_room(
                                                price,
                                                desc_input.value,
                                                image_input.value if image_input.value else None,
                                                location_select.value,
                                                admin_id
                                            )
                                            ui.notify(message, type='positive' if success else 'negative')
                                            if success:
                                                dialog.close()
                                                load_admin_rooms()
                                        except Exception as e:
                                            ui.notify(f'Error creating room: {str(e)}', type='negative')
                                    
                                    with ui.row():
                                        ui.button('Add Room', on_click=add_room).classes('bg-green-600 text-white')
                                        ui.button('Cancel', on_click=dialog.close).classes('bg-gray-500 text-white')
                                
                                dialog.open()
                            
                            ui.button('+ Add New Room', on_click=show_add_room_dialog).classes('bg-green-600 text-white mb-4')
                            
                            # Rooms Table
                            rooms = get_all_rooms()
                            
                            if not rooms:
                                ui.label('No rooms available').classes('text-gray-500')
                            else:
                                columns = [
                                    {'name': 'id', 'label': 'ID', 'field': 'Room_id'},
                                    {'name': 'location', 'label': 'Location', 'field': 'city'},
                                    {'name': 'price', 'label': 'Price', 'field': 'price'},
                                    {'name': 'description', 'label': 'Description', 'field': 'description'},
                                    {'name': 'actions', 'label': 'Actions', 'field': 'actions'}
                                ]
                                
                                rows = []
                                for r in rooms:
                                    # Convert Decimal to float/string for safety
                                    r_safe = r.copy()
                                    if 'price' in r_safe:
                                        r_safe['price'] = float(r_safe['price'])
                                    
                                    rows.append({
                                        'Room_id': r['Room_id'],
                                        'city': f"{r.get('city', '')}, {r.get('area', '')}",
                                        'price': f"TK {r['price']}",
                                        'description': r.get('description', '')[:50] + '...' if r.get('description') else '',
                                        'actions': '',
                                        '_data': r_safe
                                    })
                                
                                table = ui.table(columns=columns, rows=rows, row_key='Room_id').classes('w-full')
                                
                                def delete_room_action(evt):
                                    row = evt.args
                                    success, message = delete_room(row['Room_id'])
                                    ui.notify(message, type='positive' if success else 'negative')
                                    if success:
                                        load_admin_rooms()
                                
                                table.add_slot('body-cell-actions', r'''
                                    <q-td :props="props">
                                        <q-btn icon="delete" size="sm" color="red" @click="$parent.$emit('delete', props.row)" dense />
                                    </q-td>
                                ''')
                                table.on('delete', delete_room_action)
                    
                    load_admin_rooms()
                
                # ========== MANAGE BOOKINGS TAB ==========
                with ui.tab_panel(bookings_tab):
                    bookings_container = ui.column().classes('w-full')
                    
                    def load_admin_bookings():
                        bookings_container.clear()
                        
                        with bookings_container:
                            bookings = get_all_bookings()
                            
                            if not bookings:
                                ui.label('No bookings yet').classes('text-gray-500')
                            else:
                                for booking in bookings:
                                    with ui.card().classes('w-full p-4 mb-4'):
                                        with ui.row().classes('w-full items-center justify-between'):
                                            with ui.column():
                                                ui.label(f"User: {booking['user_name']} ({booking['user_email']})").classes('font-bold')
                                                ui.label(f"Room: {booking.get('city', 'Unknown')}, {booking.get('area', '')}").classes('text-gray-700')
                                                ui.label(f"{booking['check_in_date']} to {booking['check_out_date']}").classes('text-gray-600')
                                                ui.label(f"Total: TK {booking['Total_cost']:.2f}").classes('text-blue-600 font-bold')
                                            
                                            def update_status(e, booking_id):
                                                success, message = update_booking_status(booking_id, e.value)
                                                ui.notify(message, type='positive' if success else 'negative')
                                                if success:
                                                    load_admin_bookings()
                                            
                                            ui.select(
                                                ['Pending', 'Confirmed', 'Cancelled', 'Completed'],
                                                value=booking['status'],
                                                label='Status',
                                                on_change=lambda e, bid=booking['booking_id']: update_status(e, bid)
                                            )
                    
                    load_admin_bookings()
