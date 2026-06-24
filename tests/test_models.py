import unittest
from extensions import db, csrf, login_manager
from app import app
from models import User, ClosetPiece, Media, Outfit, OutfitPieces, Acquisition

# -------------------- U S E R  M E T H O D S --------------------------------------------------------------------
class TestUserMethods(unittest.TestCase):
    def setUp(self):
        self.user = User(username="testuser")
        self.user.set_password("testpassword")

    def test_user_password_hashing_correct(self):
        self.assertTrue(self.user.check_password("testpassword"))
    
    def test_user_password_hashing_wrong_password(self):
        self.assertFalse(self.user.check_password("wrongpassword"))

# -------------------- B A S E       D A T A B A S E  ---------------------------------------------------------------------
class BaseTestCase(unittest.TestCase):
    def setUp(self):
        #setUp and tearDown are unique to each test, so you can fuck up database in test B without impacting test A        
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True

        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

# -------------------- C L O S E T   P I E C E S -------------------------------------------------------------------
class TestClosetPieceHelpers(BaseTestCase):
    # test for getting the piece images and ensuring relationships are correct
    def test_piece_images_mixed_media(self):
        #create piece, media, append, and then do tests
        piece = ClosetPiece(name="test piece 01",category="test category")
        
        media_piece = Media(
            img_src="/static/media/tests/piece_01.jpg",
            alt_text="test alt text",
            media_type="piece"
        )

        media_texture = Media(
            img_src="/static/media/tests/texture_01.jpg",
            alt_text="test alt text",
            media_type="texture"
        )

        # attach relationships
        piece.media.append(media_piece)
        piece.media.append(media_texture)

        db.session.add(piece)
        db.session.commit()

        self.assertEqual(piece.piece_images, [media_piece])

    def test_piece_images_only(self):
        #create piece, media, append, and then do tests
        piece = ClosetPiece(name="test piece 02",category="test category",
        )
        media_piece = Media(
            img_src="/static/media/tests/piece_01.jpg",
            alt_text="test alt text",
            media_type="piece"
        )

        # attach relationships
        piece.media.append(media_piece)

        db.session.add(piece)
        db.session.commit()

        self.assertEqual(piece.piece_images, [media_piece])

    def test_piece_images_no_image_returns_empty_list(self):
        #create piece, media, append, and then do tests
        piece = ClosetPiece(name="test piece 03",category="test category",
        )

        db.session.add(piece)
        db.session.commit()

        self.assertEqual(piece.piece_images, [])

    def test_textures_mixed_media(self):
        #create piece, media, append, and then do tests
        piece = ClosetPiece(name="test piece 01",category="test category",
        )
        media_piece = Media(
            img_src="/static/media/tests/piece_01.jpg",
            alt_text="test alt text",
            media_type="piece"
        )

        media_texture = Media(
            img_src="/static/media/tests/texture_01.jpg",
            alt_text="test alt text",
            media_type="texture"
        )

        # attach relationships
        piece.media.append(media_piece)
        piece.media.append(media_texture)

        db.session.add(piece)
        db.session.commit()

        self.assertEqual(piece.textures, [media_texture])

    def test_textures_no_texture_returns_empty_list(self):
        #create piece, media, append, and then do tests
        piece = ClosetPiece(name="test piece 01",category="test category",
        )
        media_piece = Media(
            img_src="/static/media/tests/piece_01.jpg",
            alt_text="test alt text",
            media_type="piece"
        )

        # attach relationships
        piece.media.append(media_piece)

        db.session.add(piece)
        db.session.commit()

        self.assertEqual(piece.textures, [])
    

class TestClosetPieceModel(BaseTestCase):
    def test_piece_code_gen_first_in_cat(self):
        piece = ClosetPiece(name="test piece 01", category="test")
        db.session.add(piece)
        db.session.commit()

        self.assertEqual(piece.code, "test_1")

    def test_piece_code_gen(self):
        piece = ClosetPiece(name="test piece 01", category="test")
        piece_diff_cat = ClosetPiece(name="test piece 02", category="testtwo")

        new_piece = ClosetPiece(name="test piece 03", category="test")

        db.session.add_all([piece, piece_diff_cat, new_piece])
        db.session.commit()

        self.assertEqual(new_piece.code, "test_2")

    # def test_piece_code_gen_deleted_pieces(self):
    
    # def test_add_media_to_piece(self):

    def test_add_acquisition(self):
        
        # - adding acquisition to piece

    # test for updating closet piece: 


    # test for deleting closet piece: 
        # - if piece is deleted, what happens to piece code logic? (should still increment correctly)
        # - what happens if piece deleted is category count 2 and there are existing pieces after it? 
        # - deaccessioning piece
        # - 


# -------------------- O U T F I T S -----------------------------------------------------
# class TestOutfitHelper(unittest.TestCase):
#      # test for getting featured_texture_piece (if piece is in outfit, return texture image)
#     def test_featured_texture_piece(self):
#         self.assertEqual(self.piece_01.featured_texture_piece, self.piece_01)
#         self.assertEqual(self.piece_02.featured_texture_piece, None)
#         self.assertEqual(self.piece_03.featured_texture_piece, self.piece_03)
#         self.assertEqual(self.piece_04.featured_texture_piece, self.piece_04)

#     def test_featured_texture_piece_nonexistent_image():
#         pass