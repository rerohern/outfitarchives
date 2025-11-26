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
    year_made = db.Column(db.Integer, index=True, unique=False, nullable=True)

    # credit/acquisition info
    acquisition = db.Column(db.Integer, db.ForeignKey("acquisition.id"))

    # ____ relationships _____

    #many to many
    outfits = db.relationship("Outfit", secondary="outfit_pieces", back_populates="pieces")

    #one to many
    media = db.relationship("Media", back_populates="closet_piece", cascade="all, delete-orphan")

    # ___ functions ____
    def generate_piece_code(self, category):
        count = ClosetPiece.query.filter_by(category=category).count()
        return f"{category}_{count + 1}"

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
        return self.texture[0].img_src if self.textures else None

# ____ outfit models ___________________________________________________________________________________

class Outfit(db.Model):
    __tablename__ = "outfits"

    #core info
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), index=True, unique=True)
    date_worn = db.Column(db.Date, index=True, unique=False)
    notes = db.Column(db.String(240), nullable=True)
    tags = db.Column(db.String(50), index=True, unique=False, nullable=True)

    #___relationships___

    #many to many
    pieces = db.Relationship("ClosetPiece", secondary="outfit_pieces", back_populates="outfits")

    #one to many
    media = db.Relationship("Media", foreign_keys=[Media.outfit_id], back_populates="outfit")

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

    #if purchase, thrift
    store_name = db.Column(db.String(80), index=True, unique=True, nullable=True)
    store_location = db.Column(db.String(180), index=True, unique=False, nullable=True)

    #if loan, gift
    from_who = db.Column(db.String(80), index=True, unique=False, nullable=True)


