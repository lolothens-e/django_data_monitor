from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests
from django.conf import settings
from datetime import datetime, timedelta
from collections import Counter, defaultdict
import json

@login_required
def index(request):
    
    response = requests.get(settings.API_URL)  
    rows = response.json() if response.status_code == 200 else []

    filtered_rows = []
    now = datetime.now()
    three_months_ago = now - timedelta(days=30)
    
    for row in rows:
        fecha_str = row.get('fecha')
        try:
            fecha = datetime.strptime(fecha_str, "%d/%m/%Y")
            if fecha >= three_months_ago:
                filtered_rows.append(row)
        except Exception:
            continue
        
    productos = [row.get('producto') for row in rows if row.get('producto')]
    producto_mas_vendido = None
    if productos:
        counter = Counter(productos)
        producto_mas_vendido = counter.most_common(1)[0][0]
    

    # Calcular pedidos y ganancia por fecha
    orders_by_date = defaultdict(int)
    revenue_by_date = defaultdict(float)
    for row in rows:
        fecha_str = row.get('fecha')
        try:
            fecha = datetime.strptime(fecha_str, "%d/%m/%Y").strftime("%d/%m/%Y")
            orders_by_date[fecha] += 1
            revenue_by_date[fecha] += 9.31  # Suponiendo cada pedido es 9.31$
        except Exception:
            continue

    # Ordenar fechas y calcular acumulados
    sorted_dates = sorted(set(list(orders_by_date.keys()) + list(revenue_by_date.keys())), key=lambda d: datetime.strptime(d, "%d/%m/%Y"))
    orders_cumulative = []
    revenue_cumulative = []
    total_orders = 0
    total_revenue = 0.0
    for date in sorted_dates:
        total_orders += orders_by_date[date]
        total_revenue += revenue_by_date[date]
        orders_cumulative.append(total_orders)
        revenue_cumulative.append(round(total_revenue, 2))
    
    data = {
        'title': "JMStore: Pedidos ",
        'total_responses': len(rows),
        'rows': rows,
        'ultimomes' : len(filtered_rows),
        'ganancia' :  str(round(len(rows)*9.31,2)) + "$",
        'masvendido' : producto_mas_vendido,
        'orders_labels': json.dumps(list(orders_by_date.keys())),
        'orders_data': json.dumps(list(orders_by_date.values())),
        'revenue_labels': json.dumps(sorted_dates),
        'revenue_data': json.dumps(revenue_cumulative),
    }
    
    return render(request, 'dashboard/index.html', data)