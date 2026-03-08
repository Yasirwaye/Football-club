from app import app, db
from models import Squad, Player
import time
import sys

def init_database():
    """Initialize database with proper error handling"""
    max_retries = 10
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            with app.app_context():
                print("Creating database tables...")
                db.create_all()
                
                if Squad.query.count() == 0:
                    print("Seeding initial data...")
                    
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
                    
                    u18 = Squad.query.filter_by(name='Under 18').first()
                    if u18:
                        players = [
                            Player(first_name='Marcus', last_name='Chen', age=16, position='MID', 
                                   squad_id=u18.id, stats_goals=24, stats_assists=18, stats_matches=32,
                                   image_url='https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400',
                                   quote='The academy transformed my game completely.'),
                            Player(first_name='James', last_name='Wilson', age=17, position='FWD', 
                                   squad_id=u18.id, stats_goals=31, stats_assists=12, stats_matches=30,
                                   image_url='https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=400',
                                   quote='Professional coaching every single day.'),
                            Player(first_name='Tyler', last_name='Brooks', age=15, position='FWD', 
                                   squad_id=u18.id, stats_goals=18, stats_assists=22, stats_matches=28,
                                   image_url='https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400',
                                   quote='Best facilities I have ever trained at.'),
                            Player(first_name='Sam', last_name='Okonkwo', age=16, position='DEF', 
                                   squad_id=u18.id, stats_goals=3, stats_assists=5, stats_matches=34,
                                   image_url='https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400',
                                   quote='Tactical awareness improved massively.')
                        ]
                        db.session.add_all(players)
                        db.session.commit()
                    
                    print(f"Created {Squad.query.count()} squads and {Player.query.count()} players")
                else:
                    print("Database already initialized")
                
                print("✅ Database initialization successful!")
                return True
                
        except Exception as e:
            retry_count += 1
            print(f"⚠️  Database connection attempt {retry_count}/{max_retries} failed: {str(e)}")
            
            if retry_count >= max_retries:
                print("❌ Failed to initialize database after maximum retries")
                print("Continuing startup anyway - database may initialize on next request")
                return False
            
            # Wait before retrying
            wait_time = min(2 ** retry_count, 10)  # Exponential backoff, max 10 seconds
            print(f"Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
    
    return False

if __name__ == '__main__':
    success = init_database()
    sys.exit(0 if success else 0)  # Exit 0 even on failure to let the server start