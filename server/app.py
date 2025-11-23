# server/app.py
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from server.models import db, Episode, Guest, Appearance

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.json.compact = False

    db.init_app(app)
    migrate = Migrate(app, db)

    @app.route('/')
    def index():
        return jsonify({"message": "Late Show API up"}), 200

    # GET /episodes -> list of episodes with minimal fields
    @app.route('/episodes', methods=['GET'])
    def get_episodes():
        episodes = Episode.query.all()
        result = [{"id": e.id, "date": e.date, "number": e.number} for e in episodes]
        return jsonify(result), 200

    # GET /episodes/<int:id> -> episode with appearances nested
    @app.route('/episodes/<int:id>', methods=['GET'])
    def get_episode(id):
        ep = Episode.query.get(id)
        if not ep:
            return jsonify({"error": "Episode not found"}), 404

        appearances_data = []
        for a in ep.appearances:
            appearances_data.append({
                "id": a.id,
                "rating": a.rating,
                "episode_id": a.episode_id,
                "guest_id": a.guest_id,
                "guest": {
                    "id": a.guest.id,
                    "name": a.guest.name,
                    "occupation": a.guest.occupation
                }
            })

        payload = {
            "id": ep.id,
            "date": ep.date,
            "number": ep.number,
            "appearances": appearances_data
        }
        return jsonify(payload), 200

    # DELETE /episodes/<int:id> -> delete episode and cascade appearances
    @app.route('/episodes/<int:id>', methods=['DELETE'])
    def delete_episode(id):
        ep = Episode.query.get(id)
        if not ep:
            return jsonify({"error": "Episode not found"}), 404
        db.session.delete(ep)
        db.session.commit()
        return '', 204

    # GET /guests -> list all guests
    @app.route('/guests', methods=['GET'])
    def get_guests():
        guests = Guest.query.all()
        result = [{"id": g.id, "name": g.name, "occupation": g.occupation} for g in guests]
        return jsonify(result), 200

    # POST /appearances -> create new appearance, validate rating
    @app.route('/appearances', methods=['POST'])
    def create_appearance():
        data = request.get_json() or {}
        required = ['rating', 'episode_id', 'guest_id']
        errors = []
        for key in required:
            if key not in data:
                errors.append(f"Missing {key}")

        if errors:
            return jsonify({"errors": errors}), 400

        # Validate episode and guest exist
        episode = Episode.query.get(data['episode_id'])
        guest = Guest.query.get(data['guest_id'])
        if not episode:
            return jsonify({"errors": [f"Episode id {data['episode_id']} not found"]}), 400
        if not guest:
            return jsonify({"errors": [f"Guest id {data['guest_id']} not found"]}), 400

        try:
            appearance = Appearance(
                rating=int(data['rating']),
                episode=episode,
                guest=guest
            )
            db.session.add(appearance)
            db.session.commit()
        except ValueError as ve:
            db.session.rollback()
            return jsonify({"errors": [str(ve)]}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({"errors": [str(e)]}), 400

        payload = {
            "id": appearance.id,
            "rating": appearance.rating,
            "guest_id": appearance.guest_id,
            "episode_id": appearance.episode_id,
            "episode": {"id": episode.id, "date": episode.date, "number": episode.number},
            "guest": {"id": guest.id, "name": guest.name, "occupation": guest.occupation}
        }
        return jsonify(payload), 201

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(port=5555, debug=True)
