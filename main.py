# Auto-reload trigger for removing duplicates
from nicegui import ui, app
import json
import os

DATA_FILE = os.path.join('data', 'cars.json')

# Serve static assets
app.add_static_files('/assets', 'assets')

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

cars_data = load_data()

# Extract unique brands for filtering
brands = sorted(list(set(car['make'] for car in cars_data)))
brands.insert(0, 'All Brands')

def get_class_style(class_pi):
    text = class_pi.upper()
    if ' X' in text or text.startswith('X'):
        return 'background-color: #55a33a; color: white;' # Green
    elif 'S2' in text:
        return 'background-color: #1a4fba; color: white;' # Blue
    elif 'S1' in text:
        return 'background-color: #8327a3; color: white;' # Purple
    elif ' A' in text or text.startswith('A'):
        return 'background-color: #d12222; color: white;' # Red
    elif ' B' in text or text.startswith('B'):
        return 'background-color: #d66418; color: white;' # Orange
    elif ' C' in text or text.startswith('C'):
        return 'background-color: #d6ba18; color: black;' # Yellow
    elif ' D' in text or text.startswith('D'):
        return 'background-color: #27a3a3; color: white;' # Cyan
    return 'background-color: #333333; color: white;'


@ui.page('/')
def main_page():
    # Set dark mode
    ui.dark_mode().enable()
    
    # Custom CSS for Forza styling
    ui.add_head_html('''
        <style>
            body {
                background-color: #0d0d0d !important;
                color: white !important;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            .forza-header {
                padding: 20px;
                text-align: center;
                margin-bottom: 20px;
            }
            .car-card {
                background-color: #1a1a1a;
                border: 1px solid #333;
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 10px;
                transition: transform 0.2s, box-shadow 0.2s;
            }
            .car-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 10px rgba(224, 0, 90, 0.2);
                border-color: #e0005a;
            }
            /* Styling Quasar Checkboxes for Forza Pink */
            .q-checkbox__inner--truthy .q-checkbox__bg {
                background: #e0005a !important;
                border-color: #e0005a !important;
            }
            .q-checkbox__bg {
                border-color: #666 !important;
            }
        </style>
    ''')

    with ui.column().classes('w-full max-w-4xl mx-auto p-4'):
        # Header
        with ui.element('div').classes('w-full forza-header flex flex-col items-center justify-center'):
            ui.image('/assets/Forza_Horizon_logo.svg').style('width: 300px; max-width: 100%; margin: 0 auto;')
            ui.label('CAR MANAGER').classes('text-2xl font-bold tracking-widest text-white mt-2')
        
        # Controls
        with ui.row().classes('w-full items-center mb-4 q-gutter-md p-4 bg-gray-900 rounded-lg border border-gray-800'):
            ui.label('Filter by Brand:').classes('text-lg font-semibold')
            brand_select = ui.select(brands, value='All Brands').classes('w-64 bg-black text-white')
            
            with ui.column().classes('ml-4 -mt-2'):
                ui.label('Adquirido:').classes('text-sm font-semibold text-gray-400 mb-[-8px]')
                with ui.row().classes('q-gutter-sm'):
                    show_adq_sim = ui.checkbox('Sim', value=True)
                    show_adq_nao = ui.checkbox('Não', value=True)
                    
            with ui.column().classes('ml-4 -mt-2'):
                ui.label('Capturado:').classes('text-sm font-semibold text-gray-400 mb-[-8px]')
                with ui.row().classes('q-gutter-sm'):
                    show_cap_sim = ui.checkbox('Sim', value=True)
                    show_cap_nao = ui.checkbox('Não', value=True)
            
            ui.space()
            
            # Simple stats
            stats_label = ui.label('').classes('text-sm text-gray-400')
            
            def update_stats():
                adquiridos = sum(1 for c in cars_data if c.get('adquirido', False))
                capturados = sum(1 for c in cars_data if c.get('capturado', False))
                total = len(cars_data)
                stats_label.set_text(f"Adquiridos: {adquiridos}/{total} | Capturados: {capturados}/{total}")

            update_stats()

        # Car List container
        car_container = ui.column().classes('w-full')
        
        def update_ui():
            car_container.clear()
            filter_val = brand_select.value
            # Filter cars
            filtered_cars = cars_data
            if filter_val != 'All Brands':
                filtered_cars = [c for c in filtered_cars if c['make'] == filter_val]
                
            filtered_cars = [c for c in filtered_cars if 
                             ((c.get('adquirido', False) and show_adq_sim.value) or 
                              (not c.get('adquirido', False) and show_adq_nao.value)) and
                             ((c.get('capturado', False) and show_cap_sim.value) or 
                              (not c.get('capturado', False) and show_cap_nao.value))]
                
            with car_container:
                if not filtered_cars:
                    ui.label('No cars found. (Did you run scraper.py first?)').classes('text-xl text-gray-500 mt-8 text-center w-full')
                    return
                    
                for car in filtered_cars:
                    with ui.row().classes('car-card w-full items-center justify-between flex-nowrap'):
                        with ui.column().classes('flex-1 min-w-0 pr-4'):
                            with ui.row().classes('items-center gap-2 mb-1'):
                                ui.label(car['make']).classes('text-sm text-pink-400 font-bold uppercase tracking-wide')
                                if car.get('class_pi'):
                                    class_style = get_class_style(car['class_pi'])
                                    display_text = car['class_pi'].replace(' ', ' | ')
                                    ui.label(display_text).classes('text-xs px-2 py-0.5 rounded font-mono font-bold shadow-sm').style(class_style)
                            ui.label(car['car_name']).classes('text-xl font-semibold break-words whitespace-normal')
                        
                        with ui.row().classes('q-gutter-md shrink-0 flex-nowrap'):
                            def toggle_adquirido(e, c=car):
                                c['adquirido'] = e.value
                                save_data(cars_data)
                                update_stats()
                            
                            def toggle_capturado(e, c=car):
                                c['capturado'] = e.value
                                save_data(cars_data)
                                update_stats()
                                
                            ui.checkbox('Adquirido', value=car.get('adquirido', False), on_change=toggle_adquirido).classes('text-lg')
                            ui.checkbox('Capturado', value=car.get('capturado', False), on_change=toggle_capturado).classes('text-lg')
        
        brand_select.on_value_change(update_ui)
        show_adq_sim.on_value_change(update_ui)
        show_adq_nao.on_value_change(update_ui)
        show_cap_sim.on_value_change(update_ui)
        show_cap_nao.on_value_change(update_ui)
        update_ui()

ui.run(title='Forza Horizon 6 Cars', port=8080, dark=True)

# Reload trigger

# Reload trigger

# Reload trigger

# Reload trigger
