import json
import bcrypt

from email_validation import valid_email_address

from touchpoint.requesthandlers import ViewHandler, BaseHandler, APIHandler
from touchpoint.utils import api_assert, io_schema


class PublicHome(ViewHandler):

    def get(self):
        self.render("homepublic.html")


class SignUp(APIHandler):

    # Populate this dict with "input_schema", "output_schema", and "doc"
    #  for each implemented HTTP method
    api_documentation = {}

    def _validate_email_suffix(self, email):
        """Validate email suffix

        Validates the suffix of email against all valid_suffixes.

        :type  email: str
        :param email: email to be validated
        :returns: True for valid suffix, and False for invalid
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

        :type  email: str
        :param email: email to be validated
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

    api_documentation["post"] = {
        "input_schema": {
            "type": "object",
            "properties": {
                "first": {"type": "string"},
                "last": {"type": "string"},
                "email": {"type": "string"},
                "password": {"type": "string"},
            },
            "required": ["first", "last", "email", "password"],
        },
        "output_schema": {
            "type": "string",
        },
        "doc": (
            "The `password` field must match the following criteria; "
            "while the API cannot verify that these steps have been taken, "
            "it is important that the front-end interface implement these "
            "for users' password security:\n\n"
            "* Assert a minimum password length of 8 characters\n"
            "* The original password must be salted and hashed before being "
            "sent. This prevents against reverse lookup of common passwords "
            "in rainbow tables.The salt must be `salt = email+\"touchpoint\"`"
            " and then the Password field can be "
            "`Password = bcrypt(salt+password)`."
        ),
    }

    @io_schema("post")
    def post(self, body):
        """POST RequestHandler

        - Hashes password with a random salt
        - Stores a new person in the DB if all is well

        :type  body: list or dict
        :param body: json.loads(self.request.body)
        :returns: Message of success as well as any related data
        """
        # Validate email
        self._validate_email(body["email"])
        # Generate salt, hash password with salt
        salt = bcrypt.gensalt(rounds=12)  # default rounds are 12
        body.update(
            {"salt": salt,
             "password": bcrypt.hashpw(str(body["password"]), salt)}
        )
        # Add person to DB and write back on successful entry
        self.db_conn.create_person(body)
        return "Signup successful!"


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
