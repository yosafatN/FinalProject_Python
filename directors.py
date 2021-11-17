from flask import make_response, abort
from config import db
from models import *
import json


def read_all():
    '''
    Menampilkan semua data Director
    '''

    directors = Directors.query.order_by(Directors.id).all()
    directors_schame = DirectorsSchema(many=True)
    data = directors_schame.dump(directors)

    return Result(
        status=True,
        message="Success",
        data=data
    ).__dict__


def read_all_with_movie():
    '''
    Menampilkan semua data Director dan movie yang dimilikinya. Data movie yang ditampilkan hanya beratribut id, release_date, title dan vote_avarage
    '''

    directors = Directors.query.order_by(Directors.id).all()
    directors_schame = DirectorsMoviesSchame(many=True)
    data = directors_schame.dump(directors)

    return Result(
        status=True,
        message="Success",
        data=data
    ).__dict__


def read_all_with_movie_detail():
    '''
    Menampilkan semua data Director dan movie yang dimilikinya secara lengkap 
    '''

    directors = Directors.query.order_by(Directors.id).all()
    directors_schame = DirectorsMoviesDetailSchame(many=True)
    data = directors_schame.dump(directors)

    return Result(
        status=True,
        message="Success",
        data=data
    ).__dict__


def read_one(director_id):
    '''
    Menampilkan data Director berdasarkan ID Director
    '''

    director = (
        Directors.query.filter(Directors.id == director_id)
        .outerjoin(Movies)
        .one_or_none()
    )

    if director is not None:
        director_schema = DirectorsSchema()
        data = director_schema.dump(director)
        return Result(
            status=True,
            message="Success",
            data=data
        ).__dict__

    else:
        return Result(
            status=False,
            message=f"Director dengan ID {director_id} tidak ditemukan"
        ).__dict__, 404


def read_one_with_movie(director_id):
    '''
    Menampilkan data Director dan movie yang dimiliki berdasarkan ID Director. Data movie yang ditampilkan hanya beratribut id, release_date, title dan vote_avarage
    '''

    director = (
        Directors.query.filter(Directors.id == director_id)
        .outerjoin(Movies)
        .one_or_none()
    )

    if director is not None:
        director_schema = DirectorsMoviesSchame()
        data = director_schema.dump(director)
        return Result(
            status=True,
            message="Success",
            data=data
        ).__dict__

    else:
        return Result(
            status=False,
            message=f"Director dengan ID {director_id} tidak ditemukan"
        ).__dict__, 404


def read_one_with_movie_detail(director_id):
    '''
    Menampilkan data Director dan movie yang dimiliki secara detail berdasarkan ID Director
    '''

    director = (
        Directors.query.filter(Directors.id == director_id)
        .outerjoin(Movies)
        .one_or_none()
    )

    if director is not None:
        director_schema = DirectorsMoviesDetailSchame()
        data = director_schema.dump(director)
        return Result(
            status=True,
            message="Success",
            data=data
        ).__dict__

    else:
        return Result(
            status=False,
            message=f"Director dengan ID {director_id} tidak ditemukan"
        ).__dict__, 404


def create(director):

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
            message=f"Director dengan UID {uid} sudah ada"
        ).__dict__, 409


def update(director_id, director):
    update_director = (
        Directors.query.filter(Directors.id == director_id)
        .one_or_none()
    )

    if update_director is None:
        abort(
            404,
            f"Director not found for ID: {director_id}"
        )
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
                abort(
                    409,
                    f"Direcotor with User ID {uid} exists already"
                )

        schema = DirectorsSchema()
        update = schema.load(director, session=db.session)
        update.id = update_director.id
        db.session.merge(update)
        db.session.commit()

        data = schema.dump(update_director)

        return data, 200


def delete(director_id):
    director = (
        Directors.query.filter(Directors.id == director_id)
        .one_or_none()
    )

    if director is not None:
        db.session.delete(director)
        db.session.commit()

        return {
            "status": True,
            "message": f"Director with ID {director_id} deleted"
        }

    else:
        abort(
            404,
            f"Director not found for ID: {director_id}"
        )
