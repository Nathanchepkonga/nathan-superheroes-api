from flask import Blueprint, jsonify, request
from .models import Hero, Power, HeroPower
from . import db

app = Blueprint('app', __name__)

# Get all heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([{'id': hero.id, 'name': hero.name, 'superpower': hero.superpower} for hero in heroes])

# Add a new hero
@app.route('/heroes', methods=['POST'])
def add_hero():
    data = request.get_json()
    new_hero = Hero(name=data['name'], superpower=data['superpower'])
    db.session.add(new_hero)
    db.session.commit()
    return jsonify({'id': new_hero.id, 'name': new_hero.name, 'superpower': new_hero.superpower}), 201

# Get all powers
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return jsonify([{'id': power.id, 'name': power.name} for power in powers])

# Add a new power
@app.route('/powers', methods=['POST'])
def add_power():
    data = request.get_json()
    new_power = Power(name=data['name'])
    db.session.add(new_power)
    db.session.commit()
    return jsonify({'id': new_power.id, 'name': new_power.name}), 201

# Assign power to a hero
@app.route('/heroes/<int:hero_id>/powers/<int:power_id>', methods=['POST'])
def assign_power(hero_id, power_id):
    new_hero_power = HeroPower(hero_id=hero_id, power_id=power_id)
    db.session.add(new_hero_power)
    db.session.commit()
    return jsonify({'hero_id': hero_id, 'power_id': power_id}), 201
