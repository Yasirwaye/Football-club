from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config
from models import db, Squad, Player, Application
from datetime import datetime
import os

app = Flask(__name__)
app.config.from_object(Config)

# Configure CORS based on environment
if os.environ.get('FLASK_ENV') == 'production':
    # In production, allow from environment variables
    cors_origins = os.environ.get('CORS_ORIGINS', 'http://localhost:3000').split(',')
else:
    # In development, allow localhost origins
    cors_origins = ["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000", "http://127.0.0.1:3001"]

CORS(app, resources={
    r"/api/*": {
        "origins": cors_origins,
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

db.init_app(app)
migrate = Migrate(app, db)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

# ==================== SQUAD ROUTES ====================

@app.route('/api/squads', methods=['GET'])
def get_squads():
    try:
        squads = Squad.query.all()
        return jsonify([squad.to_dict() for squad in squads])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/squads/<int:id>', methods=['GET'])
def get_squad(id):
    try:
        squad = Squad.query.get_or_404(id)
        return jsonify(squad.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/squads', methods=['POST'])
def create_squad():
    try:
        data = request.get_json()
        
        if not data or 'name' not in data or 'age_group' not in data:
            return jsonify({'error': 'Missing required fields: name, age_group'}), 400
        
        new_squad = Squad(
            name=data['name'],
            age_group=data['age_group'],
            formation=data.get('formation', '4-3-3'),
            head_coach=data.get('head_coach', ''),
            assistant_coach=data.get('assistant_coach', '')
        )
        
        db.session.add(new_squad)
        db.session.commit()
        
        return jsonify(new_squad.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/squads/<int:id>', methods=['PUT'])
def update_squad(id):
    try:
        squad = Squad.query.get_or_404(id)
        data = request.get_json()
        
        squad.name = data.get('name', squad.name)
        squad.age_group = data.get('age_group', squad.age_group)
        squad.formation = data.get('formation', squad.formation)
        squad.head_coach = data.get('head_coach', squad.head_coach)
        squad.assistant_coach = data.get('assistant_coach', squad.assistant_coach)
        
        db.session.commit()
        return jsonify(squad.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/squads/<int:id>', methods=['DELETE'])
def delete_squad(id):
    try:
        squad = Squad.query.get_or_404(id)
        db.session.delete(squad)
        db.session.commit()
        return jsonify({'message': 'Squad deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== PLAYER ROUTES ====================

@app.route('/api/players', methods=['GET'])
def get_players():
    try:
        squad_id = request.args.get('squad_id', type=int)
        position = request.args.get('position')
        
        query = Player.query
        
        if squad_id:
            query = query.filter_by(squad_id=squad_id)
        if position:
            query = query.filter_by(position=position)
        
        players = query.all()
        return jsonify([player.to_dict() for player in players])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/players/<int:id>', methods=['GET'])
def get_player(id):
    try:
        player = Player.query.get_or_404(id)
        return jsonify(player.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/players', methods=['POST'])
def create_player():
    try:
        data = request.get_json()
        
        required_fields = ['first_name', 'last_name', 'position', 'squad_id']
        for field in required_fields:
            if not data or field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Verify squad exists
        squad = Squad.query.get(data['squad_id'])
        if not squad:
            return jsonify({'error': 'Squad not found'}), 404
        
        new_player = Player(
            first_name=data['first_name'],
            last_name=data['last_name'],
            age=data.get('age'),
            position=data['position'],
            squad_id=data['squad_id'],
            stats_goals=data.get('stats_goals', 0),
            stats_assists=data.get('stats_assists', 0),
            stats_matches=data.get('stats_matches', 0),
            image_url=data.get('image_url', ''),
            quote=data.get('quote', '')
        )
        
        db.session.add(new_player)
        db.session.commit()
        
        return jsonify(new_player.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/players/<int:id>', methods=['PUT'])
def update_player(id):
    try:
        player = Player.query.get_or_404(id)
        data = request.get_json()
        
        player.first_name = data.get('first_name', player.first_name)
        player.last_name = data.get('last_name', player.last_name)
        player.age = data.get('age', player.age)
        player.position = data.get('position', player.position)
        player.squad_id = data.get('squad_id', player.squad_id)
        player.stats_goals = data.get('stats_goals', player.stats_goals)
        player.stats_assists = data.get('stats_assists', player.stats_assists)
        player.stats_matches = data.get('stats_matches', player.stats_matches)
        player.image_url = data.get('image_url', player.image_url)
        player.quote = data.get('quote', player.quote)
        player.is_active = data.get('is_active', player.is_active)
        
        db.session.commit()
        return jsonify(player.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/players/<int:id>', methods=['DELETE'])
def delete_player(id):
    try:
        player = Player.query.get_or_404(id)
        db.session.delete(player)
        db.session.commit()
        return jsonify({'message': 'Player deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/players/<int:id>/move', methods=['POST'])
def move_player(id):
    try:
        player = Player.query.get_or_404(id)
        data = request.get_json()
        new_squad_id = data.get('squad_id')
        
        if not new_squad_id:
            return jsonify({'error': 'squad_id is required'}), 400
        
        new_squad = Squad.query.get(new_squad_id)
        if not new_squad:
            return jsonify({'error': 'Target squad not found'}), 404
        
        player.squad_id = new_squad_id
        db.session.commit()
        
        return jsonify(player.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== APPLICATION ROUTES ====================

@app.route('/api/applications', methods=['GET'])
def get_applications():
    try:
        status = request.args.get('status')
        query = Application.query
        
        if status:
            query = query.filter_by(status=status)
        
        applications = query.order_by(Application.created_at.desc()).all()
        return jsonify([app.to_dict() for app in applications])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/applications', methods=['POST'])
def create_application():
    try:
        data = request.get_json()
        
        required_fields = ['first_name', 'last_name', 'date_of_birth', 'position', 'email']
        for field in required_fields:
            if not data or field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        new_application = Application(
            first_name=data['first_name'],
            last_name=data['last_name'],
            date_of_birth=datetime.fromisoformat(data['date_of_birth'].replace('Z', '+00:00')),
            position=data['position'],
            previous_club=data.get('previous_club', ''),
            email=data['email'],
            phone=data.get('phone', ''),
            message=data.get('message', '')
        )
        
        db.session.add(new_application)
        db.session.commit()
        
        return jsonify(new_application.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/applications/<int:id>/status', methods=['PUT'])
def update_application_status(id):
    try:
        application = Application.query.get_or_404(id)
        data = request.get_json()
        
        if 'status' not in data:
            return jsonify({'error': 'status is required'}), 400
            
        application.status = data['status']
        db.session.commit()
        
        return jsonify(application.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/applications/<int:id>', methods=['DELETE'])
def delete_application(id):
    try:
        application = Application.query.get_or_404(id)
        db.session.delete(application)
        db.session.commit()
        return jsonify({'message': 'Application deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== HEALTH & INIT ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'eastleigh-academy-api',
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/init', methods=['POST'])
def init_database():
    try:
        db.create_all()
        
        # Seed initial data if empty
        if Squad.query.count() == 0:
            squads = [
                Squad(name='Senior Squad', age_group='18+', formation='4-3-3', 
                      head_coach='Gareth Southgate', assistant_coach='Steve Holland'),
                Squad(name='Under 23', age_group='20-23', formation='4-2-3-1', 
                      head_coach='Lee Carsley', assistant_coach='Ashley Cole'),
                Squad(name='Under 18', age_group='16-18', formation='4-3-3', 
                      head_coach='Neil Ryan', assistant_coach='Paul McGuinness')
            ]
            db.session.add_all(squads)
            db.session.commit()
            
            # Add sample players to U18
            u18 = Squad.query.filter_by(name='Under 18').first()
            if u18:
                players = [
                    Player(first_name='Marcus', last_name='Chen', age=16, position='MID', 
                           squad_id=u18.id, stats_goals=24, stats_assists=18, stats_matches=32,
                           quote='The academy transformed my game completely.'),
                    Player(first_name='James', last_name='Wilson', age=17, position='FWD', 
                           squad_id=u18.id, stats_goals=31, stats_assists=12, stats_matches=30,
                           quote='Professional coaching every single day.')
                ]
                db.session.add_all(players)
                db.session.commit()
        
        return jsonify({
            'message': 'Database initialized successfully',
            'squads': Squad.query.count(),
            'players': Player.query.count()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5001, debug=True)