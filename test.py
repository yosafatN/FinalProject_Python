import unittest
from models import *


class TestValidatorDirector(unittest.TestCase):
    data_benar = {
        "department": "Shoting",
        "gender": 1,
        "name": "Director Satu",
        "uid": 22
    }

    data_salah = {
        "department": "as",
        "gender": 3,
        "name": "as",
        "uid": -1
    }

    benar_result = ValidationDirector(data_benar)
    salah_result = ValidationDirector(data_salah)

    # corret

    def test_correct_name(self):
        self.assertEqual(self.benar_result.nameValidator().status, True)

    def test_correct_department(self):
        self.assertEqual(self.benar_result.departmentValidator().status, True)

    def test_correct_gender(self):
        self.assertEqual(self.benar_result.genderValidator().status, True)

    def test_correct_uid(self):
        self.assertEqual(self.benar_result.uidValidator().status, True)

    def test_correct_all(self):
        self.assertEqual(self.benar_result.isValid().status, True)

    # incorrect

    def test_incorrect_name(self):
        self.assertEqual(self.salah_result.nameValidator().status, False)

    def test_incorrect_department(self):
        self.assertEqual(self.salah_result.departmentValidator().status, False)

    def test_incorrect_gender(self):
        self.assertEqual(self.salah_result.genderValidator().status, False)

    def test_incorrect_uid(self):
        self.assertEqual(self.salah_result.uidValidator().status, False)

    def test_incorrect_all(self):
        self.assertEqual(self.salah_result.isValid().status, False)


class TestValidatorMovie(unittest.TestCase):
    data_benar = {
        "budget": 380000000,
        "director_id": 43614,
        "original_title": "Pirates of the Caribbean: On Stranger Tides",
        "overview": "Captain Jack Sparrow crosses paths with a woman from his past, and he's not sure if it's love -- or if she's a ruthless con artist who's using him to find the fabled Fountain of Youth. When she forces him aboard the Queen Anne's Revenge, the ship of the formidable pirate Blackbeard, Jack finds himself on an unexpected adventure in which he doesn't know who to fear more: Blackbeard or the woman from his past.",
        "popularity": 135,
        "release_date": "2011-05-14",
        "revenue": 1045713802,
        "tagline": "Live Forever Or Die Trying.",
        "title": "Pirates of the Caribbean: On Stranger Tides",
        "uid": 1865,
        "vote_average": 6.4,
        "vote_count": 4948
    }

    data_salah = {
        "budget": -1,
        "director_id": -1,
        "original_title": "as",
        "overview": "as",
        "popularity": -1,
        "release_date": "2011-05-50",
        "revenue": -1,
        "tagline": "as",
        "title": "as",
        "uid": -1,
        "vote_average": -1,
        "vote_count": -1
    }

    benar_result = ValidationMovie(data_benar)
    salah_result = ValidationMovie(data_salah)

    # correct

    def test_correct_budget(self):
        self.assertEqual(self.benar_result.budgetValidator().status, True)

    def test_correct_director_id(self):
        self.assertEqual(self.benar_result.directorIdValidator().status, True)

    def test_correct_original_title(self):
        self.assertEqual(
            self.benar_result.originalTitleValidator().status, True)

    def test_correct_overview(self):
        self.assertEqual(self.benar_result.overviewValidator().status, True)

    def test_correct_popularity(self):
        self.assertEqual(self.benar_result.popularityValidator().status, True)

    def test_correct_release_date(self):
        self.assertEqual(self.benar_result.releaseDateValidator().status, True)

    def test_correct_revenue(self):
        self.assertEqual(self.benar_result.revenueValidator().status, True)

    def test_correct_tagline(self):
        self.assertEqual(self.benar_result.taglineValidator().status, True)

    def test_correct_title(self):
        self.assertEqual(self.benar_result.titleValidator().status, True)

    def test_correct_uid(self):
        self.assertEqual(self.benar_result.uidValidator().status, True)

    def test_correct_vote_average(self):
        self.assertEqual(self.benar_result.voteAvarageValidator().status, True)

    def test_correct_vote_count(self):
        self.assertEqual(self.benar_result.voteCountValidator().status, True)

    def test_correct_all(self):
        self.assertEqual(self.benar_result.isValid().status, True)

    # Incorret

    def test_incorrect_budget(self):
        self.assertEqual(self.salah_result.budgetValidator().status, False)

    def test_incorrect_director_id(self):
        self.assertEqual(self.salah_result.directorIdValidator().status, False)

    def test_incorrect_original_title(self):
        self.assertEqual(
            self.salah_result.originalTitleValidator().status, False)

    def test_incorrect_overview(self):
        self.assertEqual(self.salah_result.overviewValidator().status, False)

    def test_incorrect_popularity(self):
        self.assertEqual(self.salah_result.popularityValidator().status, False)

    def test_incorrect_release_date(self):
        self.assertEqual(
            self.salah_result.releaseDateValidator().status, False)

    def test_incorrect_revenue(self):
        self.assertEqual(self.salah_result.revenueValidator().status, False)

    def test_incorrect_tagline(self):
        self.assertEqual(self.salah_result.taglineValidator().status, False)

    def test_incorrect_title(self):
        self.assertEqual(self.salah_result.titleValidator().status, False)

    def test_incorrect_uid(self):
        self.assertEqual(self.salah_result.uidValidator().status, False)

    def test_incorrect_vote_average(self):
        self.assertEqual(
            self.salah_result.voteAvarageValidator().status, False)

    def test_incorrect_vote_count(self):
        self.assertEqual(self.salah_result.voteCountValidator().status, False)

    def test_ibcorrect_all(self):
        self.assertEqual(self.salah_result.isValid().status, False)


if __name__ == '__main__':
    unittest.main()
