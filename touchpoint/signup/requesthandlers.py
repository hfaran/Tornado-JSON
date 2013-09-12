import json
import bcrypt
import os
from email_validation import valid_email_address
from tornado.web import HTTPError

from touchpoint.requesthandlers import ViewHandler, BaseHandler, APIHandler
from touchpoint.utils import api_assert


class PublicHome(ViewHandler):

    def get(self):
        self.render("homepublic.html")


class SignUp(APIHandler):

    def _validate_email_suffix(self, email):
        """Validate email suffix

        Validates the suffix of email against all valid_suffixes.
        Returns True for valid suffix, and False for invalid.
        """
        for suffix in [s["suffix"] for s in self.db_conn.get_email_suffixes()]:
            if any(map(email.endswith, [p + suffix for p in ["@", "."]])):
                return True
        return False

    def _validate_email(self, email):
        """Validates email

        Validates email as a proper-form email address with allowed suffix.
        If email address is not valid, or if suffix is invalid,
        raise a 400. If email address has already been used, raises 409.
        """
        api_assert(
            valid_email_address(email),
            400, log_message="Not a valid email address"
        )

        api_assert(
            self._validate_email_suffix(email),
            400, log_message="Not a valid email suffix"
        )

        api_assert(
            not email in [d["email"] for d in self.db_conn.get_all_emails()],
            409, log_message="Someone else is already using this email"
        )

    def post(self):
        """POST RequestHandler

        * Asserts request data contains required fields
        * Hashes password with a random salt
        * Stores a new person in the DB if all is well
        """
        json_body = json.loads(self.request.body)

        # Assert that all required fields are present in the request
        required_fields = ["first", "last", "email", "password"]
        api_assert(
            all(field in json_body.keys() for field in required_fields),
            400, log_message="API request missing required fields"
        )
        # Validate email
        self._validate_email(json_body["email"])
        # Generate salt, hash password with salt
        salt = bcrypt.gensalt(rounds=12)  # default rounds are 12
        json_body.update(
            {"salt": salt,
             "password": bcrypt.hashpw(str(json_body["password"]), salt)}
        )
        # Add person to DB and write back on successful entry
        self.db_conn.create_person(json_body)
        self.success("Signup successful!")


class SignUpFb(BaseHandler):

    def get(self):
        self.write("I am a stub.")


class SignUpFbEmail(BaseHandler):

    def get(self):
        self.write("I am a stub.")


class SignUpDetails1(ViewHandler):

    def get(self):
        self.render("signup_part1.html")


class SignUpDetails2(ViewHandler):

    def get(self):
        self.render("signup_part2.html")


class SignUpDetails3(ViewHandler):

    def get(self):
        self.render("signup_part3.html")
