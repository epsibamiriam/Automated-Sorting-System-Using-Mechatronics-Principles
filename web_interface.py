from flask import Flask, render_template_string
from flask_socketio import SocketIO
import threading
import time

app = Flask(_name_)
socketio = SocketIO(app, async_mode='threading')

# Shared data storage
system_data = {
    'color_counts': {'Red': 0, 'Green': 0, 'Blue': 0},
    'color_totals': {'Red': 0, 'Green': 0, 'Blue': 0},
    'total_sorted': 0,
    'logs': [],
    'last_update': time.time()
}

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Sorting System Monitor</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
            background-color: #f5f5f5;
        }
        .header {
            background-color: #2c3e50;
            color: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            text-align: center;
        }
        .container { 
            display: flex; 
            gap: 20px; 
            flex-wrap: wrap;
        }
        .panel {
            flex: 1;
            min-width: 300px;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .counters {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 20px;
        }
        .counter {
            padding: 15px;
            border-radius: 8px;
            color: white;
            text-align: center;
        }
        .current-count {
            font-size: 2em;
            font-weight: bold;
        }
        .total-count {
            font-size: 1.2em;
            opacity: 0.9;
        }
        .red { background-color: #e74c3c; }
        .green { background-color: #2ecc71; }
        .blue { background-color: #3498db; }
        .log-window {
            height: 400px;
            overflow-y: auto;
            border: 1px solid #ddd;
            padding: 10px;
            background: white;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
        }
        .log-entry {
            margin: 5px 0;
            padding: 8px;
            border-bottom: 1px solid #eee;
            font-size: 0.9em;
        }
        .log-time {
            color: #7f8c8d;
            margin-right: 10px;
        }
        .total-panel {
            background-color: #34495e;
            color: white;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            margin-bottom: 20px;
            font-size: 1.3em;
        }
        @media (max-width: 768px) {
            .container {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Color Sorting System Monitor</h1>
        <div class="total-panel">
            Total Objects Sorted: <span id="total-sorted">0</span>
        </div>
    </div>
    
    <div class="container">
        <div class="panel">
            <h2>Current Detection</h2>
            <div class="counters">
                <div class="counter red">
                    <div>Red Objects</div>
                    <div class="current-count" id="red-count">0</div>
                </div>
                <div class="counter green">
                    <div>Green Objects</div>
                    <div class="current-count" id="green-count">0</div>
                </div>
                <div class="counter blue">
                    <div>Blue Objects</div>
                    <div class="current-count" id="blue-count">0</div>
                </div>
            </div>
            
            <h2>Total Sorted</h2>
            <div class="counters">
                <div class="counter red">
                    <div>Total Red</div>
                    <div class="total-count" id="total-red">0</div>
                </div>
                <div class="counter green">
                    <div>Total Green</div>
                    <div class="total-count" id="total-green">0</div>
                </div>
                <div class="counter blue">
                    <div>Total Blue</div>
                    <div class="total-count" id="total-blue">0</div>
                </div>
            </div>
        </div>
        
        <div class="panel">
            <h2>System Activity Log</h2>
            <div class="log-window" id="log-window">
                {% for log in logs %}
                    <div class="log-entry">
                        <span class="log-time">{{ log[:8] }}</span>
                        <span>{{ log[10:] }}</span>
                    </div>
                {% endfor %}
            </div>
        </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <script>
        const socket = io();
        
        socket.on('update_counts', function(data) {
            // Update current detection counts
            document.getElementById('red-count').textContent = data.current_red;
            document.getElementById('green-count').textContent = data.current_green;
            document.getElementById('blue-count').textContent = data.current_blue;
            
            // Update total counts
            document.getElementById('total-red').textContent = data.total_red;
            document.getElementById('total-green').textContent = data.total_green;
            document.getElementById('total-blue').textContent = data.total_blue;
            
            // Update total sorted
            document.getElementById('total-sorted').textContent = data.total;
        });
        
        socket.on('update_logs', function(log) {
            const logWindow = document.getElementById('log-window');
            const logEntry = document.createElement('div');
            logEntry.className = 'log-entry';
            
            const timeSpan = document.createElement('span');
            timeSpan.className = 'log-time';
            timeSpan.textContent = log.substring(0, 8);
            
            const messageSpan = document.createElement('span');
            messageSpan.textContent = log.substring(10);
            
            logEntry.appendChild(timeSpan);
            logEntry.appendChild(messageSpan);
            logWindow.appendChild(logEntry);
            logWindow.scrollTop = logWindow.scrollHeight;
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, logs=system_data['logs'])

def background_update_thread():
    while True:
        # Update every second
        socketio.emit('update_counts', {
            'current_red': system_data['color_counts']['Red'],
            'current_green': system_data['color_counts']['Green'],
            'current_blue': system_data['color_counts']['Blue'],
            'total_red': system_data['color_totals']['Red'],
            'total_green': system_data['color_totals']['Green'],
            'total_blue': system_data['color_totals']['Blue'],
            'total': system_data['total_sorted']
        })
        time.sleep(1)

def start_web_interface():
    socketio.start_background_task(background_update_thread)
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if _name_ == '_main_':
    start_web_interface()
