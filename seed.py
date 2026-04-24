from app import app, db
from models import User, ClosetPiece, Outfit, Acquisition
from datetime import date


def seed_closet_pieces():
    print("👕 Seeding closet pieces...")

    pieces = {}

    # --- Acquisition for pieces ---
    acq1 = Acquisition(
        year_acquired=2019,
        credit_type="thrift",
        store_name=None,
        store_location="italy",
        from_who=None
    )

    acq2 = Acquisition(
        year_acquired=2024,
        credit_type="purchase",
        store_name="Esty",
        store_location=None,
        from_who=None
    )

    acq3 = Acquisition(
        year_acquired=2025,
        credit_type="gift",
        store_name="unknown",
        store_location="Japan",
        from_who="Omari"
    )

    acq4 = Acquisition(
        year_acquired=2023,
        credit_type="purchase",
        store_name="Asics",
        store_location="Chelsea, New York",
        from_who=None
    )

    db.session.add(acq1)
    db.session.add(acq2)
    db.session.add(acq3)
    db.session.add(acq4)
    db.session.commit() 

    # --- Pieces ---
    top = ClosetPiece(
        name="white cropped peasant top",
        category="tops",
        brand="Hess Frackmann",
        year_made=None,
        acquisition_id=acq1.id
    )

    accessory = ClosetPiece(
        name="pink tourmaline ring",
        category="accessories",
        brand="CaitlynMinimalist",
        year_made="2024",
        acquisition_id=acq2.id
    )

    bottom = ClosetPiece(
        name="navy full length wrap skirt",
        category="bottoms",
        brand="Homspun",
        year_made=None,
        acquisition_id=acq3.id
    )
  

    shoe = ClosetPiece(
        name="gel lyte 3 ogs",
        category="shoes",
        brand="Asics",
        year_made="2023",
        acquisition_id=acq4.id
    )

    all_pieces = [top, accessory, bottom, shoee]

    db.session.add_all(all_pieces)
    db.session.commit()

    # Store references for outfit creation in the dictionary from above
    pieces["top"] = top
    pieces["bottom"] = bottom
    pieces["accessory"] = accessory
    pieces["shoe"] = shoe

    return pieces


def seed_outfits(pieces):
    print("👗 Seeding outfits...")

    outfit = Outfit(
        date_worn=date.today(),
        notes="Seed outfit for testing rendering",
        tags="casual"
    )

    # Assign all pieces to outfit
    outfit.pieces = [
        pieces["top"],
        pieces["bottom"],
        pieces["accessory"],
        pieces["shoe"]
    ]

    # Optional featured texture piece
    outfit.featured_texture_piece = pieces["bottom"]

    db.session.add(outfit)
    db.session.commit()

    return [outfit]


def run_seed():
    print("🌱 Starting seed process...")

    user = seed_user()
    pieces = seed_closet_pieces()
    outfits = seed_outfits(pieces)

    print("✅ Seeding complete!")
    print(f"User: {user.username}")
    print(f"Closet pieces: {len(pieces)}")
    print(f"Outfits: {len(outfits)}")


if __name__ == "__main__":
    with app.app_context():
        run_seed()