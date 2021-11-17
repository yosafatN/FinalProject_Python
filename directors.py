from config import db
from models import *


def read_all(id=None, sort_by=None, reverse=False, movie=None, limit=0, movie_sort=None, movie_sort_reverse=False, movie_limit=0):
    '''
    Menampilkan data Director
    :param id: menampilkan berdasarkan ID | None or int
    :param sort_by: atribut Directory yang ingin di sort | None or string
    :param reverse: tipe sort Directory, asc atau desc | None or bool
    :param movie: jenis schema data movie | None or 'half' or 'full'
    :param limit: limit data Directory yang ingin diambil | int
    :param movie_sort: atribut Movie yang ingin di sort | None or string
    :param movie_sort_reverse: tipe sort Movie, asc atau desc | None or bool
    :param movie_limit: limit data Movie yang ingin diambil | int

    :return: data Directory atau data Directory beserta Movie | object
    '''
    is_many = False

    directors = None
    if id == None:
        directors = Directors().query.all()
        is_many = True
    else:
        directors = (
            Directors.query.filter(Directors.id == id)
            .outerjoin(Movies)
            .one_or_none()
        )
        is_many = False

        if directors is None:
            return Result(
                status=False,
                message=f"Director dengan ID {id} tidak ditemukan"
            ).__dict__, 404

    directors_schame = None

    if movie != None:
        if validatorParamMovieDirector(movie) == True:
            if movie == 'full':
                directors_schame = DirectorsMoviesDetailSchame(many=is_many)
            elif movie == 'half':
                directors_schame = DirectorsMoviesSchame(many=is_many)
        else:
            return Result(
                status=False,
                message=f"Parameter movie tidak valid"
            ).__dict__, 400
    else:
        directors_schame = DirectorsSchema(many=is_many)

    data = directors_schame.dump(directors)

    if is_many:
        if sort_by != None:
            if validatorParamSortDirectorFull(sort_by) == True:
                data.sort(key=lambda x: x[sort_by], reverse=reverse)
            else:
                return Result(
                    status=False,
                    message=f"Parameter sort tidak valid"
                ).__dict__, 400

    if movie != None:
        if movie_sort != None:
            is_param_movie_valid = False
            if movie == 'half':
                is_param_movie_valid = validatorParamSortMovieHalf(movie_sort)
            elif movie == 'full':
                is_param_movie_valid = validatorParamSortMovieFull(movie_sort)

            if is_param_movie_valid == True:
                if is_many:
                    i = 0
                    while i < len(data):
                        sorted_movie = data[i].get('movies')
                        sorted_movie.sort(
                            key=lambda x: x[movie_sort], reverse=movie_sort_reverse)

                        if movie_limit > 0:
                            if len(sorted_movie) >= movie_limit:
                                sorted_movie = sorted_movie[:movie_limit]

                        data[i]['movies'] = sorted_movie
                        i += 1
                else:
                    sorted_movie = data.get('movies')
                    sorted_movie.sort(
                        key=lambda x: x[movie_sort], reverse=movie_sort_reverse)

                    if movie_limit > 0:
                        if len(sorted_movie) >= movie_limit:
                            sorted_movie = sorted_movie[:movie_limit]

                    data['movies'] = sorted_movie
            else:
                return Result(
                    status=False,
                    message=f"Parameter sort tidak valid"
                ).__dict__, 400

    if is_many:
        if limit > 0:
            if len(data) >= limit:
                data = data[:limit]

    return Result(
        status=True,
        message="Success",
        data=data
    ).__dict__, 200


def read_one(director_id, movie=None):
    '''
    Menampilkan data Director
    :param director_id: menampilkan berdasarkan ID | int
    :param movie: jenis schema data movie | None or 'half' or 'full'

    :return: data Directory atau data Directory beserta Movie | object
    '''

    director = (
        Directors.query.filter(Directors.id == director_id)
        .outerjoin(Movies)
        .one_or_none()
    )

    if director is not None:
        directors_schame = None

        if movie != None:
            if validatorParamMovieDirector(movie) == True:
                if movie == 'full':
                    directors_schame = DirectorsMoviesDetailSchame()
                elif movie == 'half':
                    directors_schame = DirectorsMoviesSchame()
            else:
                return Result(
                    status=False,
                    message=f"Parameter movie tidak valid"
                ).__dict__, 400
        else:
            directors_schame = DirectorsSchema()

        data = directors_schame.dump(director)
        return Result(
            status=True,
            message="Success",
            data=data
        ).__dict__, 200

    else:
        return Result(
            status=False,
            message=f"Director dengan ID {director_id} tidak ditemukan"
        ).__dict__, 404


def create(director):
    '''
    Menyimpan data Directory
    :param director: data Directory yang ingin di disimpan | object

    :return: data Directory yang berhasil disimpan | object
    '''

    validator = ValidationDirector(director=director).isValid()

    if validator.status != True:
        return Result(
            status=False,
            message=validator.message
        ).__dict__, 400

    uid = director.get("uid")
    existring_director = (
        Directors.query.filter(Directors.uid == uid)
        .one_or_none()
    )

    if existring_director is None:
        schema = DirectorsSchema()
        new_director = schema.load(director, session=db.session)
        db.session.add(new_director)
        db.session.commit()

        data = schema.dump(new_director)
        return Result(
            status=True,
            message=f"Berhasil menambahkan Director baru",
            data=data
        ).__dict__, 201

    else:
        return Result(
            status=False,
            message=f"Director dengan User ID {uid} sudah ada"
        ).__dict__, 409


def update(director_id, director):
    '''
    Mengubah data Directory
    :param director_id: ID director yang ingin diubah | int
    :param director: data Directory yang ingin di diubah | object

    :return: data Directory yang berhasil diubah | object
    '''

    validator = ValidationDirector(director=director).isValid()

    if validator.status != True:
        return Result(
            status=False,
            message=validator.message
        ).__dict__, 400

    update_director = (
        Directors.query.filter(Directors.id == director_id)
        .one_or_none()
    )

    if update_director is None:
        return Result(
            status=False,
            message=f"Director dengan ID {director_id} tidak ditemukan"
        ).__dict__, 404

    else:
        uid = director.get("uid")

        # Cek apakah UID juga diedit
        if uid != update_director.uid:
            existing_uid = (
                Directors.query.filter(Directors.uid == uid)
                .one_or_none()
            )

            # Cek apakah UID yg diganti sudah terpakai atau belum
            if existing_uid is not None:
                return Result(
                    status=False,
                    message=f"Director dengan User ID {uid} sudah ada"
                ).__dict__, 409

        schema = DirectorsSchema()
        update = schema.load(director, session=db.session)
        update.id = update_director.id
        db.session.merge(update)
        db.session.commit()

        data = schema.dump(update_director)

        return Result(
            status=True,
            message=f"Berhasil mengubah Director",
            data=data
        ).__dict__, 200


def delete(director_id):
    '''
    Menghapus data Directory
    :param director_id: ID director yang ingin dihapus | int

    :return: pesan bahwa data berhasil dihapus | string
    '''

    director = (
        Directors.query.filter(Directors.id == director_id)
        .one_or_none()
    )

    if director is not None:
        db.session.delete(director)
        db.session.commit()

        return Result(
            status=True,
            message="Berhasil menghapus Director",
        ).__dict__, 200

    else:
        return Result(
            status=False,
            message=f"Director dengan ID {director_id} tidak ditemukan"
        ).__dict__, 404
