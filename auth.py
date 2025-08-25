# auth.py
import hashlib
from typing import Dict, Optional
from nicegui import ui, app

# User database with hashed passwords
# In production, use a proper database with salted hashes
USERS: Dict[str, Dict[str, str]] = {
    'admin': {
        'password_hash': hashlib.sha256('Blueberry33@@'.encode()).hexdigest(),
        'role': 'admin'
    },
    'jeremy': {
        'password_hash': hashlib.sha256('melbourne'.encode()).hexdigest(),
        'role': 'user'
    }
}

# Session configuration
SESSION_TIMEOUT = 3600  # 1 hour in seconds


def hash_password(password: str) -> str:
    """Hash a password for storing."""
    return hashlib.sha256(password.encode()).hexdigest()


def authenticate(username: str, password: str) -> bool:
    """Authenticate user credentials."""
    if not username or not password:
        return False

    user = USERS.get(username)
    if not user:
        return False

    return user['password_hash'] == hash_password(password)


def get_current_user() -> Optional[str]:
    """Get the currently logged-in user."""
    try:
        return app.storage.user.get('username')
    except (AttributeError, RuntimeError):
        return None


def get_user_role(username: str) -> Optional[str]:
    """Get the role of a user."""
    user = USERS.get(username)
    return user.get('role') if user else None


def is_authenticated() -> bool:
    """Check if user is authenticated."""
    try:
        return app.storage.user.get('authenticated', False)
    except (AttributeError, RuntimeError):
        return False


def login_required():
    """Redirect to login if not authenticated (for use in page functions)."""
    if not is_authenticated():
        ui.navigate.to('/login')
        return False
    return True


def logout():
    """Log out the current user."""
    try:
        app.storage.user.clear()
        ui.notify('Logged out successfully', color='positive')
    except (AttributeError, RuntimeError):
        ui.notify('Logged out', color='positive')
    ui.navigate.to('/login')


def render_login_page():
    """Render the login page with improved styling and validation."""
    # Apply global styles
    ui.add_head_html('''
        <style>
            body {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                font-family: 'Roboto', sans-serif;
                min-height: 100vh;
            }
        </style>
    ''')

    with ui.column().classes('w-full h-screen justify-center items-center'):
        with ui.card().classes('w-96 p-8 shadow-2xl'):
            with ui.column().classes('w-full gap-4'):
                # Header
                ui.label('Welcome Back').classes('text-2xl font-bold text-center mb-4 text-gray-800')

                # Form fields
                username = ui.input('Username').props('outlined dense').classes('w-full')
                password = ui.input('Password', password=True).props('outlined dense').classes('w-full')

                # Error message placeholder
                error_label = ui.label('').classes('text-red-500 text-sm min-h-4 text-center')

                def clear_error():
                    error_label.text = ''

                # Add event listeners to clear errors on input
                username.on('focus', clear_error)
                password.on('focus', clear_error)

                def attempt_login():
                    # Clear previous errors
                    error_label.text = ''

                    # Validate inputs
                    if not username.value or not username.value.strip():
                        error_label.text = 'Username is required'
                        username.run_method('focus')
                        return

                    if not password.value:
                        error_label.text = 'Password is required'
                        password.run_method('focus')
                        return

                    # Attempt authentication
                    if authenticate(username.value.strip(), password.value):
                        try:
                            app.storage.user.update({
                                'username': username.value.strip(),
                                'authenticated': True,
                                'login_time': str(ui.context.client.id)  # Store serializable data
                            })
                        except (AttributeError, RuntimeError) as e:
                            # Fallback if storage fails
                            print(f"Storage warning: {e}")
                        ui.notify(f'Welcome back, {username.value}!', color='positive')
                        ui.navigate.to('/')
                    else:
                        error_label.text = 'Invalid username or password'
                        password.value = ''  # Clear password field
                        username.run_method('focus')

                # Handle Enter key press
                username.on('keydown.enter', attempt_login)
                password.on('keydown.enter', attempt_login)

                # Login button
                login_btn = ui.button('Login', on_click=attempt_login).props('color=primary')
                login_btn.classes('w-full mt-4')


def render_protected_content(username: str):
    """Render content for authenticated users."""
    user_role = get_user_role(username)

    with ui.row().classes('w-full justify-between items-center p-4 bg-white shadow-sm'):
        with ui.row().classes('items-center gap-4'):
            ui.label(f'Welcome, {username}!').classes('text-xl font-semibold')
            if user_role:
                ui.chip(user_role.title()).props('color=blue outline')
        ui.button('Logout', on_click=logout).props('color=red outline icon=logout')


# ---------------------------------------------------
# 🧪 Demo if run as a script
# ---------------------------------------------------
if __name__ in {"__main__", "__mp_main__"}:
    @ui.page('/login')
    def login_page():
        # Check if already authenticated
        if is_authenticated():
            ui.navigate.to('/')
            return
        render_login_page()


    @ui.page('/')
    def home_page():
        if not login_required():
            return

        current_user = get_current_user()
        render_protected_content(current_user)

        # Example protected content
        with ui.column().classes('p-6 gap-6 max-w-4xl mx-auto'):
            ui.label('Dashboard').classes('text-3xl font-bold text-gray-800')

            with ui.card().classes('p-6'):
                ui.label('Your Account Information').classes('text-lg font-semibold mb-4')
                ui.label(f'Username: {current_user}').classes('text-gray-600')
                ui.label(f'Role: {get_user_role(current_user)}').classes('text-gray-600')

            # Role-based content
            if get_user_role(current_user) == 'admin':
                with ui.card().classes('p-6 border-l-4 border-red-500'):
                    ui.label('Admin Panel').classes('text-lg font-bold text-red-600 mb-2')
                    ui.label('You have administrative privileges').classes('text-gray-600')
                    ui.button('Go to Admin Dashboard',
                              on_click=lambda: ui.navigate.to('/admin')).props('color=red')


    @ui.page('/admin')
    def admin_page():
        if not login_required():
            return

        current_user = get_current_user()
        if get_user_role(current_user) != 'admin':
            ui.notify('Access denied: Admin privileges required', color='negative')
            ui.navigate.to('/')
            return

        render_protected_content(current_user)
        with ui.column().classes('p-6 gap-6 max-w-4xl mx-auto'):
            ui.label('Admin Dashboard').classes('text-3xl font-bold text-red-600')

            with ui.card().classes('p-6'):
                ui.label('Admin Controls').classes('text-lg font-semibold mb-4')
                ui.label('This is an admin-only page with special privileges.').classes('text-gray-600 mb-4')

                with ui.row().classes('gap-4'):
                    ui.button('User Management', icon='people').props('color=blue')
                    ui.button('System Settings', icon='settings').props('color=green')
                    ui.button('Reports', icon='assessment').props('color=orange')


    # Redirect logout requests
    @ui.page('/logout')
    def logout_page():
        logout()


    # Run with required storage secret for app.storage.user
    ui.run(
        title='Secure NiceGUI App',
        port=8080,
        storage_secret='your-secret-key-change-in-production',  # Required for app.storage.user
        reload=True,  # For development
        show=False  # Suppress the storage file warnings in development
    )