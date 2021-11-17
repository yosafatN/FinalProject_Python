from flask import make_response, abort
from config import db
from models import *


def read_all():
    notes = Movies.query.order_by(Movies.id).all()
    movies_schame = MoviesSchema(many=True)
    data = movies_schame.dump(notes)
    return data


def read_one(director_id, movie_id):

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
            movie_schema = MoviesSchema()
            data = movie_schema.dump(movie)
            return data

        else:
            abort(404, f'Movie not found for ID: {movie_id}')

    else:
        abort(404, f'Director not found for ID: {director_id}')


def create(director_id, movie):

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

            schema = MoviesSchema()
            new_movie = schema.load(movie, session=db.session)

            director.movies.append(new_movie)
            db.session.commit()

            data = schema.dump(new_movie)

            return data, 201

        else:
            abort(
                409,
                f"Movie with User ID {uid} exists already"
            )
    else:
        abort(404, f'Director not found for ID: {director_id}')


def update(director_id, movie_id, movie):
    update_movie = (
        Movies.query.filter(Directors.id == director_id)
        .filter(Movies.id == movie_id)
        .one_or_none()
    )

    if update_movie is None:
        abort(
            404,
            f"Movie not found for ID: {movie_id}"
        )
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
                abort(
                    409,
                    f"Movie with User ID {uid} exists already"
                )

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
                abort(
                    404,
                    f"Director not found for ID: {movie_director_id}"
                )
            else:
                update.director_id = movie_director_id

        update.id = update_movie.id

        db.session.merge(update)
        db.session.commit()

        data = schema.dump(update)

        return data, 200


def delete(director_id, movie_id):
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
            return make_response(
                f"Movie with ID {movie_id} deleted"
            )

        else:
            abort(
                404,
                f"Movie not found for ID: {movie_id}"
            )
    else:
        abort(404, f'Director not found for ID: {director_id}')
