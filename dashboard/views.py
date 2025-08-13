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
    
    orders_by_date = defaultdict(int)
    money_by_date = defaultdict(float)
    for row in rows:
        fecha_str = row.get('fecha')
        try:
            fecha = datetime.strptime(fecha_str, "%d/%m/%Y").strftime("%d/%m/%Y")
            orders_by_date[fecha] += 1
            money_by_date[fecha] += 9.31  # Assuming each order is 9.31$
        except Exception:
            continue

    # Sort dates
    sorted_dates = sorted(orders_by_date.keys(), key=lambda d: datetime.strptime(d, "%d/%m/%Y"))
    orders_counts = [orders_by_date[date] for date in sorted_dates]
    money_counts = [money_by_date[date] for date in sorted_dates]
    
    data = {
        'title': "JMStore: Pedidos ",
        'total_responses': len(rows),
        'rows': rows,
        'ultimomes' : len(filtered_rows),
        'ganancia' :  str(round(len(rows)*9.31,2)) + "$",
        'masvendido' : producto_mas_vendido,
        'chart_labels': json.dumps(sorted_dates),
        'chart_orders': json.dumps(orders_counts),
        'chart_money': json.dumps(money_counts),
    }
    
    return render(request, 'dashboard/index.html', data)