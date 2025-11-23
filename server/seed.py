from server.app import app, db
from server.models import Episode, Guest, Appearance

# Create the app context
with app.app_context():
    # Delete existing data
    print("Deleting old data...")
    Appearance.query.delete()
    Episode.query.delete()
    Guest.query.delete()

    # Create sample episodes
    ep1 = Episode(date="1/11/25", number=1)
    ep2 = Episode(date="1/12/25", number=2)

    # Create sample guests
    guest1 = Guest(name="Makokha Big", occupation="actor")
    guest2 = Guest(name="Papa Willie", occupation="Comedian")
    guest3 = Guest(name="Sue Mdogo", occupation="television actress")

    # Add to session
    db.session.add_all([ep1, ep2, guest1, guest2, guest3])
    db.session.commit()

    # Create sample appearances
    app1 = Appearance(rating=4, episode=ep1, guest=guest1)
    app2 = Appearance(rating=5, episode=ep2, guest=guest3)

    db.session.add_all([app1, app2])
    db.session.commit()

    print("Database seeded!")