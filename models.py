from config import db, ma
from marshmallow import fields


class Directors(db.Model):
    __tablename__ = 'directors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    gender = db.Column(db.Integer)
    uid = db.Column(db.Integer)
    department = db.Column(db.String(256))

    movies = db.relationship(
        'Movies',
        backref='directors',
        cascade='all, delete, delete-orphan',
        single_parent=True
    )


class Movies(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    original_title = db.Column(db.String(256))
    budget = db.Column(db.Integer)
    popularity = db.Column(db.Integer)
    release_date = db.Column(db.String(256))
    revenue = db.Column(db.Integer)
    title = db.Column(db.String(256))
    vote_average = db.Column(db.Float)
    vote_count = db.Column(db.Integer)
    overview = db.Column(db.String(256))
    tagline = db.Column(db.String(256))
    uid = db.Column(db.Integer)
    director_id = db.Column(db.Integer, db.ForeignKey('directors.id'))


class DirectorsSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Directors
        sqla_session = db.session
        load_instance = True


class MoviesSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Movies
        sqla_session = db.session
        load_instance = True

    directors = fields.Nested("MoviesDirectorNameSchema", default=None)


class MoviesRawSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Movies
        sqla_session = db.session
        load_instance = True

    director_id = fields.Int()


class MoviesDirectorNameSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    id = fields.Int()
    name = fields.Str()


class DirectorsMoviesSchame(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Directors
        sqla_session = db.session
        load_instance = True

    class Schame(ma.SQLAlchemyAutoSchema):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

        id = fields.Int()
        release_date = fields.Str()
        title = fields.Str()
        vote_average = fields.Float()

    movies = fields.Nested(Schame, default=[], many=True)


class DirectorsMoviesDetailSchame(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Directors
        sqla_session = db.session
        load_instance = True

    class Schame(ma.SQLAlchemyAutoSchema):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

        id = fields.Int()
        original_title = fields.Str()
        budget = fields.Int()
        popularity = fields.Int()
        release_date = fields.Str()
        revenue = fields.Int()
        title = fields.Str()
        vote_average = fields.Float()
        vote_count = fields.Int()
        overview = fields.Str()
        tagline = fields.Str()
        uid = fields.Int()
        director_id = fields.Int()

    movies = fields.Nested(Schame, default=[], many=True)


class MoviesDirectorsSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    id = fields.Int()
    name = fields.Str()
    gender = fields.Int()
    uid = fields.Int()
    department = fields.Str()


class Result():
    def __init__(self, status, message, data=None):
        self.status = status
        self.message = message
        self.data = data
