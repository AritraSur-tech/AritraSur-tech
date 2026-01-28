from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime, timedelta
import statistics

app = Flask(__name__)
DATABASE = 'fitness.db'


def get_db():
    """Connect to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database with the weight_entries table."""
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS weight_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            weight REAL NOT NULL,
            date TEXT NOT NULL UNIQUE,
            notes TEXT
        )
    ''')
    conn.commit()
    conn.close()


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/api/entries', methods=['GET'])
def get_entries():
    """Get all weight entries."""
    conn = get_db()
    entries = conn.execute(
        'SELECT * FROM weight_entries ORDER BY date ASC'
    ).fetchall()
    conn.close()
    return jsonify([dict(entry) for entry in entries])


@app.route('/api/entries', methods=['POST'])
def add_entry():
    """Add a new weight entry."""
    data = request.json
    weight = data.get('weight')
    date = data.get('date', datetime.now().strftime('%Y-%m-%d'))
    notes = data.get('notes', '')

    if not weight:
        return jsonify({'error': 'Weight is required'}), 400

    try:
        conn = get_db()
        conn.execute(
            'INSERT INTO weight_entries (weight, date, notes) VALUES (?, ?, ?)',
            (weight, date, notes)
        )
        conn.commit()
        conn.close()
        return jsonify({'message': 'Entry added successfully'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Entry for this date already exists'}), 400


@app.route('/api/entries/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    """Delete a weight entry."""
    conn = get_db()
    conn.execute('DELETE FROM weight_entries WHERE id = ?', (entry_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Entry deleted successfully'})


@app.route('/api/forecast', methods=['GET'])
def get_forecast():
    """
    Calculate weight forecast using linear regression.
    Returns predicted weight for the next 4, 8, and 12 weeks.
    """
    conn = get_db()
    entries = conn.execute(
        'SELECT * FROM weight_entries ORDER BY date ASC'
    ).fetchall()
    conn.close()

    if len(entries) < 2:
        return jsonify({
            'error': 'Need at least 2 entries to forecast',
            'forecast': None
        })

    # Convert dates to numeric values (days since first entry)
    first_date = datetime.strptime(entries[0]['date'], '%Y-%m-%d')
    x_values = []  # days
    y_values = []  # weights

    for entry in entries:
        entry_date = datetime.strptime(entry['date'], '%Y-%m-%d')
        days = (entry_date - first_date).days
        x_values.append(days)
        y_values.append(entry['weight'])

    # Simple linear regression
    n = len(x_values)
    sum_x = sum(x_values)
    sum_y = sum(y_values)
    sum_xy = sum(x * y for x, y in zip(x_values, y_values))
    sum_x2 = sum(x ** 2 for x in x_values)

    # Calculate slope and intercept
    denominator = (n * sum_x2 - sum_x ** 2)
    if denominator == 0:
        return jsonify({
            'error': 'Cannot calculate forecast with current data',
            'forecast': None
        })

    slope = (n * sum_xy - sum_x * sum_y) / denominator
    intercept = (sum_y - slope * sum_x) / n

    # Calculate predictions for 4, 8, and 12 weeks from last entry
    last_day = x_values[-1]
    last_date = datetime.strptime(entries[-1]['date'], '%Y-%m-%d')

    forecasts = []
    for weeks in [4, 8, 12]:
        future_day = last_day + (weeks * 7)
        predicted_weight = slope * future_day + intercept
        future_date = last_date + timedelta(weeks=weeks)
        forecasts.append({
            'weeks': weeks,
            'date': future_date.strftime('%Y-%m-%d'),
            'predicted_weight': round(predicted_weight, 1)
        })

    # Calculate weekly rate of change
    weekly_change = slope * 7

    # Calculate statistics
    current_weight = y_values[-1]
    starting_weight = y_values[0]
    total_change = current_weight - starting_weight

    return jsonify({
        'forecast': forecasts,
        'stats': {
            'starting_weight': starting_weight,
            'current_weight': current_weight,
            'total_change': round(total_change, 1),
            'weekly_change': round(weekly_change, 2),
            'trend': 'losing' if weekly_change < 0 else 'gaining' if weekly_change > 0 else 'maintaining'
        }
    })


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get basic statistics about weight entries."""
    conn = get_db()
    entries = conn.execute(
        'SELECT * FROM weight_entries ORDER BY date ASC'
    ).fetchall()
    conn.close()

    if not entries:
        return jsonify({'error': 'No entries found'})

    weights = [entry['weight'] for entry in entries]

    return jsonify({
        'total_entries': len(entries),
        'starting_weight': weights[0],
        'current_weight': weights[-1],
        'lowest_weight': min(weights),
        'highest_weight': max(weights),
        'average_weight': round(statistics.mean(weights), 1),
        'total_change': round(weights[-1] - weights[0], 1)
    })


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
