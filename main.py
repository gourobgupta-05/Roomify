import os
from nicegui import ui
from frontend.ui import create_pages
from dotenv import load_dotenv

load_dotenv()

def main():
    # Load all pages
    create_pages()
    
    # Run the app
    ui.run(title='Roomify', storage_secret=os.getenv('STORAGE_SECRET', 'fallback_secret_if_env_missing'))

if __name__ in {"__main__", "__mp_main__"}:
    main()
