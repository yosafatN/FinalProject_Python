from config import db, ma
from marshmallow import fields
import re
import datetime


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


class MoviesDirectorsSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Movies
        sqla_session = db.session
        load_instance = True

    class Schame(ma.SQLAlchemyAutoSchema):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

        id = fields.Int()
        name = fields.Str()

    directors = fields.Nested(Schame, default=None)


class MoviesDirectorsDetailSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Movies
        sqla_session = db.session
        load_instance = True

    class Schame(ma.SQLAlchemyAutoSchema):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

        id = fields.Int()
        name = fields.Str()
        gender = fields.Int()
        uid = fields.Int()
        department = fields.Str()

    directors = fields.Nested(Schame, default=None)


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


class Result():
    def __init__(self, status, message, data=None):
        self.status = status
        self.message = message
        self.data = data


class ValidationResult():
    def __init__(self, status, message):
        self.status = status
        self.message = message


class ValidationDirector():
    def __init__(self, director):
        self.name = director.get('name')
        self.gender = director.get('gender')
        self.department = director.get('department')
        self.uid = director.get('uid')

    def nameValidator(self) -> ValidationResult:
        if self.name != None:
            if len(self.name) < 3:
                return ValidationResult(
                    status=False,
                    message="Nama tidak valid. Tidak boleh kosong dan minimal 3 karakter"
                )
        else:
            return ValidationResult(
                status=False,
                message="Nama tidak boleh Kosong"
            )

        return ValidationResult(
            status=True,
            message="Valid"
        )

    def genderValidator(self) -> ValidationResult:
        if self.gender != None:
            if type(self.gender) == int:
                if self.gender > 2 or self.gender < 0:
                    return ValidationResult(
                        status=False,
                        message="Gender tidak valid"
                    )
            else:
                return ValidationResult(
                    status=False,
                    message="Gender harus numerik"
                )
        else:
            return ValidationResult(
                status=False,
                message="Gender tidak boleh Kosong"
            )

        return ValidationResult(
            status=True,
            message="Valid"
        )

    def departmentValidator(self) -> ValidationResult:
        if self.department != None:
            if len(self.department) < 3:
                return ValidationResult(
                    status=False,
                    message="Department tidak valid. Tidak boleh kosong dan minimal 3 karakter"
                )
        else:
            return ValidationResult(
                status=False,
                message="Department tidak boleh Kosong"
            )

        return ValidationResult(
            status=True,
            message="Valid"
        )

    def uidValidator(self) -> ValidationResult:
        if self.uid != None:
            if type(self.uid) == int:
                if self.uid < 0:
                    return ValidationResult(
                        status=False,
                        message="User ID tidak valid"
                    )
            else:
                return ValidationResult(
                    status=False,
                    message="User ID harus numerik"
                )
        else:
            return ValidationResult(
                status=False,
                message="User ID tidak boleh Kosong"
            )

        return ValidationResult(
            status=True,
            message="Valid"
        )

    def isValid(self) -> ValidationResult:
        is_name_valid = self.nameValidator()
        is_gender_valid = self.genderValidator()
        is_department_valid = self.departmentValidator()
        is_uid_valid = self.uidValidator()

        if is_name_valid.status != True:
            return is_name_valid
        elif is_gender_valid.status != True:
            return is_gender_valid
        elif is_department_valid.status != True:
            return is_department_valid
        elif is_uid_valid.status != True:
            return is_uid_valid
        else:
            return ValidationResult(
                status=True,
                message="Valid"
            )


class ValidationMovie():
    def __init__(self, movie):
        self.original_title = movie.get('original_title')
        self.budget = movie.get('budget')
        self.popularity = movie.get('popularity')
        self.release_date = movie.get('release_date')
        self.revenue = movie.get('revenue')
        self.title = movie.get('title')
        self.vote_average = movie.get('vote_average')
        self.vote_count = movie.get('vote_count')
        self.overview = movie.get('overview')
        self.tagline = movie.get('tagline')
        self.uid = movie.get('uid')
        self.director_id = movie.get('director_id')

    def originalTitleValidator(self) -> ValidationResult:
        if self.original_title != None:
            if len(self.original_title) < 3:
                return ValidationResult(
                    status=False,
                    message="Original Title tidak valid. Tidak boleh kosong dan minimal 3 karakter"
                )
        else:
            return ValidationResult(
                status=False,
                message="Original Title tidak boleh Kosong"
            )

        return ValidationResult(
            status=True,
            message="Valid"
        )

    def budgetValidator(self) -> ValidationResult:
        if self.budget != None:
            if type(self.budget) == int:
                if self.budget < 0:
                    return ValidationResult(
                        status=False,
                        message="Budget tidak valid"
                    )
            else:
                return ValidationResult(
                    status=False,
                    message="Budget harus numerik"
                )
        else:
            return ValidationResult(
                status=False,
                message="Budget tidak boleh Kosong"
            )

        return ValidationResult(
            status=True,
            message="Valid"
        )

    def popularityValidator(self) -> ValidationResult:
        if self.popularity != None:
            if type(self.popularity) == int:
                if self.popularity < 0:
                    return ValidationResult(
                        status=False,
                        message="Popularity tidak valid"
                    )
            else:
                return ValidationResult(
                    status=False,
                    message="Popularity harus numerik"
                )
        else:
            return ValidationResult(
                status=False,
                message="Popularity tidak boleh Kosong"
            )

        return ValidationResult(
            status=True,
            message="Valid"
        )

    def releaseDateValidator(self) -> ValidationResult:
        if self.release_date != None:
            try:
                datetime.datetime.strptime(self.release_date, '%Y-%m-%d')
            except ValueError:
                return ValidationResult(
                    status=False,
                    message="Release Date tidak valid. Tidak boleh kosong dan berformat yyyy-mm-dd"
                )
        else:
            return ValidationResult(
                status=False,
                message="Release Date tidak boleh Kosong"
            )

        return ValidationResult(
            status=True,
            message="Valid"
        )

    def revenueValidator(self) -> ValidationResult:
        if self.revenue != None:
            if type(self.revenue) == int:
                if self.revenue < 0:
                    return ValidationResult(
                        status=False,
                        message="Revenue tidak valid"
                    )
            else:
                return ValidationResult(
                    status=False,
                    message="Revenue harus numerik"
                )
        else:
            return ValidationResult(
                status=False,
                message="Revenue tidak boleh Kosong"
            )

        return ValidationResult(
            status=True,
            message="Valid"
        )

    def titleValidator(self) -> ValidationResult:
        if self.title != None:
            if len(self.title) < 3:
                return ValidationResult(
                    status=False,
                    message="Title tidak valid. Tidak boleh kosong dan minimal 3 karakter"
                )
        else:
            return ValidationResult(
                status=False,
                message="Title tidak boleh Kosong"
            )

        return ValidationResult(
            status=True,
            message="Valid"
        )

    def voteAvarageValidator(self) -> ValidationResult:
        if self.vote_average != None:
            if type(self.vote_average) == float or type(self.vote_average) == int:
                if self.vote_average < 0 or self.vote_average > 10:
                    return ValidationResult(
                        status=False,
                        message="Vote Average tidak valid"
                    )
            else:
                return ValidationResult(
                    status=False,
                    message="Vote Average harus numerik"
                )
        else:
            return ValidationResult(
                status=False,
                message="Vote Average tidak boleh Kosong"
            )

        return ValidationResult(
            status=True,
            message="Valid"
        )

    def voteCountValidator(self) -> ValidationResult:
        if self.vote_count != None:
            if type(self.vote_count) == int:
                if self.vote_count < 0:
                    return ValidationResult(
                        status=False,
                        message="Vote Count tidak valid"
                    )
            else:
                return ValidationResult(
                    status=False,
                    message="Vote Count harus numerik"
                )
        else:
            return ValidationResult(
                status=False,
                message="Vote Count tidak boleh Kosong"
            )

        return ValidationResult(
            status=True,
            message="Valid"
        )

    def overviewValidator(self) -> ValidationResult:
        if self.overview != None:
            if len(self.overview) < 3:
                return ValidationResult(
                    status=False,
                    message="Overview tidak valid. Tidak boleh kosong dan minimal 3 karakter"
                )
        else:
            return ValidationResult(
                status=False,
                message="Overview tidak boleh Kosong"
            )

        return ValidationResult(
            status=True,
            message="Valid"
        )

    def taglineValidator(self) -> ValidationResult:
        if self.tagline != None:
            if len(self.tagline) < 3:
                return ValidationResult(
                    status=False,
                    message="Tagline tidak valid. Tidak boleh kosong dan minimal 3 karakter"
                )
        else:
            return ValidationResult(
                status=False,
                message="Tagline tidak boleh Kosong"
            )

        return ValidationResult(
            status=True,
            message="Valid"
        )

    def uidValidator(self) -> ValidationResult:
        if self.uid != None:
            if type(self.uid) == int:
                if self.uid < 0:
                    return ValidationResult(
                        status=False,
                        message="User ID tidak valid"
                    )
            else:
                return ValidationResult(
                    status=False,
                    message="User ID harus numerik"
                )
        else:
            return ValidationResult(
                status=False,
                message="User ID tidak boleh Kosong"
            )

        return ValidationResult(
            status=True,
            message="Valid"
        )

    def directorIdValidator(self) -> ValidationResult:
        if self.director_id != None:
            if type(self.director_id) == int:
                if self.director_id < 0:
                    return ValidationResult(
                        status=False,
                        message="Director ID tidak valid"
                    )
            else:
                return ValidationResult(
                    status=False,
                    message="Director ID harus numerik"
                )
        else:
            return ValidationResult(
                status=False,
                message="Director ID tidak boleh Kosong"
            )

        return ValidationResult(
            status=True,
            message="Valid"
        )

    def isValid(self) -> ValidationResult:
        origin_title_valid = self.originalTitleValidator()
        budget_valid = self.budgetValidator()
        popularity_valid = self.popularityValidator()
        release_date_valid = self.releaseDateValidator()
        revenue_valid = self.revenueValidator()
        title_valid = self.titleValidator()
        vote_average_valid = self.voteAvarageValidator()
        vote_count_valid = self.voteCountValidator()
        overview_valid = self.overviewValidator()
        tagline_valid = self.taglineValidator()
        uid_valid = self.uidValidator()
        director_id_valid = self.directorIdValidator()

        if origin_title_valid.status != True:
            return origin_title_valid

        elif budget_valid.status != True:
            return budget_valid

        elif popularity_valid.status != True:
            return popularity_valid

        elif release_date_valid.status != True:
            return release_date_valid

        elif revenue_valid.status != True:
            return revenue_valid

        elif title_valid.status != True:
            return title_valid

        elif vote_average_valid.status != True:
            return vote_average_valid

        elif vote_count_valid.status != True:
            return vote_count_valid

        elif overview_valid.status != True:
            return overview_valid

        elif tagline_valid.status != True:
            return tagline_valid

        elif uid_valid.status != True:
            return uid_valid

        elif director_id_valid.status != True:
            return director_id_valid

        else:
            return ValidationResult(
                status=True,
                message="Valid"
            )


def validatorParamSortDirectorFull(sort) -> bool:
    if sort == 'name' or sort == 'id' or sort == 'department' or sort == 'gender' or sort == 'uid':
        return True
    else:
        return False


def validatorParamSortDirectorHalf(sort) -> bool:
    if sort == 'name' or sort == 'id':
        return True
    else:
        return False


def validatorParamDirectorMovie(director) -> bool:
    if director == 'full' or director == 'half':
        return True
    else:
        return False


def validatorParamMovieDirector(movie) -> bool:
    if movie == 'full' or movie == 'half':
        return True
    else:
        return False


def validatorParamSortMovieFull(sort) -> bool:
    if sort == 'budget' or sort == 'id' or sort == 'original_title' or sort == 'overview' or sort == 'popularity' or sort == 'release_date' or sort == 'revenue' or sort == 'tagline' or sort == 'title' or sort == 'uid' or sort == 'vote_average' or sort == 'vote_count':
        return True
    else:
        return False


def validatorParamSortMovieHalf(sort) -> bool:
    if sort == 'id' or sort == 'release_date' or sort == 'title' or sort == 'vote_average':
        return True
    else:
        return False
