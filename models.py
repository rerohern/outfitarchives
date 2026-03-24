from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# ____ user model ___________________________________________________________________________________

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f"username: {self.username}"
    
# ___ association tables __________________________________________________________________________________


class OutfitPieces(db.Model):
    __tablename__ = "outfit_pieces"

    id = db.Column(db.Integer, primary_key=True)
    outfit_id = db.Column(db.Integer, db.ForeignKey("outfits.id"))
    piece_id = db.Column(db.Integer, db.ForeignKey("closet_pieces.id"))


# ____ media model _______________________________________________________________________________________

class Media(db.Model):
    __tablename__ = "media"

    id = db.Column(db.Integer, primary_key=True)

    #core info

    img_src = db.Column(db.String(400), index=True, unique=True, nullable=True)
    alt_text = db.Column(db.String(200), index=False, unique=False)
   
    #media types: piece, texture, outfit, outfit_alt, month
    media_type = db.Column(db.String(30), index=True, unique=False, nullable=True)
    
    #view options: front, left, back, right
    view = db.Column(db.String(10), index=True, unique=False, nullable=True)

    #foreign keys
    outfit_id = db.Column(db.Integer, db.ForeignKey("outfits.id"), nullable=True)
    closet_piece_id = db.Column(db.Integer, db.ForeignKey("closet_pieces.id"), nullable=True)

    #relationships
    #many to many
    outfit = db.relationship("Outfit", foreign_keys=[outfit_id], back_populates="media")
    closet_piece = db.relationship("ClosetPiece", back_populates="media")

# ___ closet piece model ___________________________________________________________________________________

class ClosetPiece(db.Model):
    __tablename__ = "closet_pieces"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(80), index=True, unique=True, nullable=False)

    # core info
    name = db.Column(db.String(100), index=True, unique=False)
    category = db.Column(db.String(50), index=True, unique=False)
    brand = db.Column(db.String(80), index=True, unique=False, nullable=True)
    year_made = db.Column(db.String(10), index=True, unique=False, nullable=True)
    deaccessioned = db.Column(db.Boolean, default=False, index=True, unique=False, nullable=True)
    deaccessioned_notes = db.Column(db.String(100), unique=False, nullable=True)

    # credit/acquisition info
    acquisition_id = db.Column(db.Integer, db.ForeignKey("acquisition.id"))
    acquisition = db.relationship("Acquisition", backref="closet_pieces", uselist=False)

    # ____ relationships _____

    #many to many
    outfits = db.relationship("Outfit", secondary="outfit_pieces", back_populates="pieces")

    #one to many
    media = db.relationship("Media", back_populates="closet_piece", cascade="all, delete-orphan")

    # ___ functions ____

    def __init__(self, name, category, brand=None, year_made=None, acquisition_id=None):
        self.name = name
        self.category = category
        self.brand = brand
        self.year_made = year_made
        self.acquisition_id = acquisition_id

        self.generate_piece_code()

    def generate_piece_code(self):
        count = ClosetPiece.query.filter_by(category=self.category).count()
        self.code = f"{self.category}_{count + 1}"

    # ____ helper properties for images _____
    @property
    def piece_images(self):
        """all standard piece images"""
        return [m for m in self.media if m.media_type == "piece"]

    @property
    def textures(self):
        """all texture images"""
        return [m for m in self.media if m.media_type == "texture"]

    @property
    def get_texture(self):
        """return texture image"""
        return self.textures[0].img_src if self.textures else None

    @property
    def featured_texture(self):
        if self.featured_texture_piece:
            return self.featured_texture_piece.get_texture
        return None

# ____ outfit models ___________________________________________________________________________________

class Outfit(db.Model):
    __tablename__ = "outfits"

    #core info
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), index=True, unique=True)
    date_worn = db.Column(db.Date, index=True, unique=False)
    notes = db.Column(db.String(240), nullable=True)
    tags = db.Column(db.String(50), index=True, unique=False, nullable=True)
    featured_texture_piece_id = db.Column(db.Integer, db.ForeignKey("closet_pieces.id"))

    #___relationships___

    #many to many
    pieces = db.Relationship("ClosetPiece", secondary="outfit_pieces", back_populates="outfits")

    #one to many
    media = db.Relationship("Media", foreign_keys=[Media.outfit_id], back_populates="outfit")
    featured_texture_piece = db.relationship("ClosetPiece")

    # ___ helper properties _____

    @property
    def images(self):
        """all standard outfit images"""
        return [m for m in self.media if m.media_type == "outfit"]

    @property
    def alt_images(self):
        """all alt outfit images"""
        return [m for m in self.media if m.media_type == "outfit_alt"]

    # @property
    # def month_gifs(self):
    #where do month gifs get placed? in media? 

    @property
    def get_view(self, media_type, view=None):
        """return image path for a given media_type and optional view"""
        if view:
            return next(
                (m.img_src for m in self.media if m.media_type == media_type and m.view == view), None
            )
        
        #fallback to first image of m.media_type 
        type_images = [m.img_src for m in self.media if m.media_type == media_type]
        return type_images[0] if type_images else None

# ___ credit/acquisition model ___________________________________________________________________________________

class Acquisition(db.Model):
    __tablename__ = "acquisition"

    id = db.Column(db.Integer, primary_key = True)
    year_acquired = db.Column(db.Integer, index=True, unique=False)
    credit_type = db.Column(db.String(50), index=True, unique=False)
    store_name = db.Column(db.String(80), index=True, unique=False, nullable=True)
    store_location = db.Column(db.String(180), index=True, unique=False, nullable=True)

    #if loan, gift
    from_who = db.Column(db.String(80), index=True, unique=False, nullable=True)


