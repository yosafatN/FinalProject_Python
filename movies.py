from config import db
from models import *


def read_all(sort_by=None, reverse=False, limit=0, director=None):
    '''
    Menampilkan semua Movie
    :param sort_by: atribut Movie yang ingin di sort | None or string
    :param reverse: tipe sort Movie, asc atau desc | None or bool
    :param limit: limit data Directory yang ingin diambil | int
    :param director: jenis schema data director | None or 'half' or 'full'

    :return: data Movie | object
    '''

    notes = Movies.query.order_by(Movies.id).all()
    movies_schame = None

    if director != None:
        if validatorParamDirectorMovie(director) == True:
            if director == 'full':
                movies_schame = MoviesDirectorsDetailSchema(many=True)
            elif director == 'half':
                movies_schame = MoviesDirectorsSchema(many=True)
        else:
            return Result(
                status=False,
                message=f"Parameter director tidak valid"
            ).__dict__, 400
    else:
        movies_schame = MoviesSchema(many=True)

    data = movies_schame.dump(notes)

    if sort_by != None:
        if validatorParamSortMovieFull(sort_by) == True:
            data.sort(key=lambda x: x[sort_by], reverse=reverse)
        else:
            return Result(
                status=False,
                message=f"Parameter sort tidak valid"
            ).__dict__, 400

    if limit > 0:
        if len(data) >= limit:
            data = data[:limit]

    return Result(
        status=True,
        message="Success",
        data=data
    ).__dict__, 200


def read_one(director_id, movie_id):
    '''
    Menampilkan data Movie berdasarkan ID
    :param director_id: Movie berdasarkan milik ID Director  | int
    :param movie_id: Data ID Movie yang ingin ditampikan | int

    :return: data Movie | object
    '''

    existing_director = (
        Directors.query.filter(Directors.id == director_id)
        .one_or_none()
    )

    if existing_director is not None:
        movie = (
            Movies.query.filter(Movies.id == movie_id)
            .one_or_none()
        )

        if movie is not None:
            movie_schema = MoviesDirectorsDetailSchema()
            data = movie_schema.dump(movie)

            return Result(
                status=True,
                message="Success",
                data=data
            ).__dict__, 200

        else:
            return Result(
                status=False,
                message=f"Movie dengan ID {movie_id} tidak ditemukan"
            ).__dict__, 404

    else:
        return Result(
            status=False,
            message=f"Director dengan ID {director_id} tidak ditemukan"
        ).__dict__, 404


def create(director_id, movie):
    '''
    Menyimpan data Movie
    :param director_id: ID director yang movienya ingin ditambahkan | int
    :param movie: data movie yang ingin di disimpan | object

    :return: data Movie yang berhasil disimpan | object
    '''

    validator = ValidationMovie(movie).isValid()

    if validator.status != True:
        return Result(
            status=False,
            message=validator.message
        ).__dict__, 400

    director = (
        Directors.query.filter(Directors.id == director_id)
        .one_or_none()
    )

    if director is not None:
        uid = movie.get("uid")

        existing_movie = (
            Movies.query.filter(Movies.uid == uid)
            .one_or_none()
        )

        if existing_movie is None:
            del movie['director_id']
            schema = MoviesSchema()
            new_movie = schema.load(movie, session=db.session)

            director.movies.append(new_movie)
            db.session.commit()

            data = schema.dump(new_movie)

            return Result(
                status=True,
                message=f"Berhasil menambahkan Movie baru",
                data=data
            ).__dict__, 201

        else:
            return Result(
                status=False,
                message=f"Movie dengan User ID {uid} sudah ada"
            ).__dict__, 409
    else:
        return Result(
            status=False,
            message=f"Director dengan ID {director_id} tidak ditemukan"
        ).__dict__, 404


def update(director_id, movie_id, movie):
    '''
    Mengubah data Movie
    :param director_id: ID director yang movienya ingin diubah | int
    :param movie_id: ID movie yang ingin diubah | int
    :param movie: data Movie yang ingin di diubah | object

    :return: data Movie yang berhasil diubah | object
    '''

    validator = ValidationMovie(movie).isValid()

    if validator.status != True:
        return Result(
            status=False,
            message=validator.message
        ).__dict__, 400

    update_movie = (
        Movies.query.filter(Directors.id == director_id)
        .filter(Movies.id == movie_id)
        .one_or_none()
    )

    if update_movie is None:
        return Result(
            status=False,
            message=f"Movie dengan ID {movie_id} tidak ditemukan"
        ).__dict__, 404
    else:
        uid = movie.get("uid")

        # Cek apakah UID juga diedit
        if uid != update_movie.uid:
            existing_uid = (
                Movies.query.filter(Movies.uid == uid)
                .one_or_none()
            )

            # Cek apakah UID yg diganti sudah terpakai atau belum
            if existing_uid is not None:
                return Result(
                    status=False,
                    message=f"Movie dengan User ID {uid} sudah ada"
                ).__dict__, 409

        # check ID Director jika ID Director di movie ingin di edit
        movie_director_id = movie.get('director_id')

        schema = MoviesRawSchema()
        update = schema.load(movie, session=db.session)

        if director_id != movie_director_id:
            check_director = (
                Directors.query.filter(Directors.id == movie_director_id)
                .one_or_none()
            )

            if check_director is None:
                return Result(
                    status=False,
                    message=f"Director dengan ID {director_id} tidak ditemukan"
                ).__dict__, 404
            else:
                update.director_id = movie_director_id

        update.id = update_movie.id

        db.session.merge(update)
        db.session.commit()

        data = schema.dump(update)

        return Result(
            status=True,
            message=f"Berhasil mengubah Movie",
            data=data
        ).__dict__, 200


def delete(director_id, movie_id):
    '''
    Menghapus data Directory
    :param director_id: ID director yang ingin movienya akan dihapus | int
    :param movie_id: ID movie yang ingin dihapus | int

    :return: pesan bahwa data berhasil dihapus | string
    '''

    existing_director = (
        Directors.query.filter(Directors.id == director_id)
        .one_or_none()
    )

    if existing_director is not None:
        movie = (
            Movies.query.filter(Movies.id == movie_id)
            .one_or_none()
        )

        if movie is not None:
            db.session.delete(movie)
            db.session.commit()
            return Result(
                status=True,
                message="Berhasil menghapus Movie",
            ).__dict__, 200

        else:
            return Result(
                status=False,
                message=f"Movie dengan ID {movie_id} tidak ditemukan"
            ).__dict__, 404
    else:
        return Result(
            status=False,
            message=f"Director dengan ID {director_id} tidak ditemukan"
        ).__dict__, 404
