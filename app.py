"""
Ashok Watch Company - Flask Backend Server
Complete backend with order management and Razorpay payment gateway.
"""

from flask import Flask, render_template, send_from_directory, request, jsonify
import razorpay
import os
import json
from datetime import datetime
import hashlib
import hmac

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')

# Configuration
app.config['DEBUG'] = os.environ.get('DEBUG', 'True').lower() == 'true'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ashok-watch-company-secret-key-2025')

# ============================================
# RAZORPAY CONFIGURATION
# ============================================
# Get your API keys from: https://dashboard.razorpay.com/app/keys
# For testing, use Test Mode keys (they start with 'rzp_test_')
# For production, use Live Mode keys (they start with 'rzp_live_')

RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID', 'rzp_test_YOUR_KEY_ID')
RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET', 'YOUR_KEY_SECRET')

# Initialize Razorpay client
razorpay_client = None
try:
    if RAZORPAY_KEY_ID and 'YOUR_KEY' not in RAZORPAY_KEY_ID:
        razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
except Exception as e:
    print(f"Razorpay initialization error: {e}")

# ============================================
# DATABASE (Simple JSON file storage)
# ============================================
ORDERS_FILE = 'orders.json'

def load_orders():
    """Load orders from JSON file."""
    try:
        if os.path.exists(ORDERS_FILE):
            with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading orders: {e}")
    return []

def save_order(order):
    """Save a new order to JSON file."""
    try:
        orders = load_orders()
        orders.append(order)
        with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(orders, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving order: {e}")
        return False

# ============================================
# ROUTES - Pages
# ============================================

@app.route('/')
def index():
    """Serve the main store page."""
    return render_template('index.html', razorpay_key_id=RAZORPAY_KEY_ID)

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files (images, css, js)."""
    return send_from_directory(app.static_folder, filename)

# ============================================
# ROUTES - API Endpoints
# ============================================

@app.route('/api/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'ok', 
        'message': 'Ashok Watch Company server is running!',
        'payment_gateway': 'configured' if razorpay_client else 'not_configured'
    })

@app.route('/api/create-order', methods=['POST'])
def create_order():
    """Create a Razorpay order for payment."""
    try:
        data = request.get_json()
        amount = data.get('amount')  # Amount in paise (₹1 = 100 paise)
        
        if not amount or amount <= 0:
            return jsonify({'error': 'Invalid amount'}), 400
        
        if not razorpay_client:
            return jsonify({'error': 'Payment gateway not configured. Please use COD.'}), 503
        
        # Create Razorpay order
        order_data = {
            'amount': int(amount),  # Amount in paise
            'currency': 'INR',
            'receipt': f'order_{datetime.now().strftime("%Y%m%d%H%M%S")}',
            'notes': {
                'shop': 'Ashok Watch Company'
            }
        }
        
        razorpay_order = razorpay_client.order.create(data=order_data)
        
        return jsonify({
            'success': True,
            'order_id': razorpay_order['id'],
            'amount': razorpay_order['amount'],
            'currency': razorpay_order['currency'],
            'key_id': RAZORPAY_KEY_ID
        })
        
    except Exception as e:
        print(f"Error creating order: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/verify-payment', methods=['POST'])
def verify_payment():
    """Verify Razorpay payment signature."""
    try:
        data = request.get_json()
        
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_signature = data.get('razorpay_signature')
        
        if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature]):
            return jsonify({'error': 'Missing payment details'}), 400
        
        # Verify signature
        message = f"{razorpay_order_id}|{razorpay_payment_id}"
        generated_signature = hmac.new(
            RAZORPAY_KEY_SECRET.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        if generated_signature == razorpay_signature:
            return jsonify({
                'success': True,
                'message': 'Payment verified successfully'
            })
        else:
            return jsonify({'error': 'Payment verification failed'}), 400
            
    except Exception as e:
        print(f"Error verifying payment: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/save-order', methods=['POST'])
def api_save_order():
    """Save order details after successful payment or COD."""
    try:
        data = request.get_json()
        
        order = {
            'id': f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'timestamp': datetime.now().isoformat(),
            'customer': {
                'name': data.get('name'),
                'phone': data.get('phone'),
                'address': data.get('address')
            },
            'items': data.get('items', []),
            'total': data.get('total'),
            'payment_method': data.get('payment_method'),
            'payment_id': data.get('payment_id'),
            'status': 'confirmed'
        }
        
        if save_order(order):
            return jsonify({
                'success': True,
                'order_id': order['id'],
                'message': 'Order saved successfully!'
            })
        else:
            return jsonify({'error': 'Failed to save order'}), 500
            
    except Exception as e:
        print(f"Error saving order: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/orders')
def get_orders():
    """Get all orders (admin endpoint)."""
    # In production, add authentication here
    orders = load_orders()
    return jsonify(orders)

# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500

# ============================================
# MAIN
# ============================================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    print(f"""
    ╔══════════════════════════════════════════════════════════════╗
    ║       🕐 Ashok Watch Company - Online Store Server 🕐        ║
    ╠══════════════════════════════════════════════════════════════╣
    ║  Server running at: http://127.0.0.1:{port}                     ║
    ║  Payment Gateway: {'✓ Razorpay Configured' if razorpay_client else '✗ Not Configured (COD Only)'}
    ║  Press CTRL+C to stop the server                             ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])
