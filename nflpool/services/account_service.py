from passlib.handlers.sha2_crypt import sha512_crypt
from nflpool.data.dbsession import DbSessionFactory
from nflpool.data.account import Account
from nflpool.data.passwordreset import PasswordReset
import datetime
import nflpool.data.secret as secret
from nflpool.data.player_picks import PlayerPicks


class AccountService:
    @staticmethod
    def create_account(email, first_name, last_name, plain_text_password, twitter):
        session = DbSessionFactory.create_session()

        account = Account()
        account.email = email
        account.first_name = first_name[0].upper() + first_name[1:]
        account.last_name = last_name[0].upper() + last_name[1:]
        account.password_hash = AccountService.hash_text(plain_text_password)

        if secret.su_email == account.email:
            account.is_super_user = True

        if twitter != "" and twitter[0] != "@":
            twitter = "@" + twitter

        account.twitter = twitter

        session.add(account)
        session.commit()

        return account

    @classmethod
    def find_account_by_email(cls, email):

        if not email or not email.strip():
            return None

        email = email.lower().strip()

        session = DbSessionFactory.create_session()

        return session.query(Account).filter(Account.email == email).first()

    @staticmethod
    def hash_text(plain_text_password):
        return sha512_crypt.encrypt(plain_text_password, rounds=150000)

    @classmethod
    def get_authenticated_account(cls, email, plain_text_password):
        account = AccountService.find_account_by_email(email)
        if not account:
            return None

        if not sha512_crypt.verify(plain_text_password, account.password_hash):
            return None

        return account

    @classmethod
    def find_account_by_id(cls, user_id):
        if not user_id:
            return None

        user_id = user_id.strip()

        session = DbSessionFactory.create_session()

        return session.query(Account).filter(Account.id == user_id).first()

    @staticmethod
    def create_reset_code(email):

        account = AccountService.find_account_by_email(email)
        if not account:
            return None

        session = DbSessionFactory.create_session()

        reset = PasswordReset()
        reset.used_ip_address = "1.2.3.4"  # set for real
        reset.user_id = account.id

        session.add(reset)
        session.commit()

        return reset

    @classmethod
    def find_reset_code(cls, code):

        if not code or not code.strip():
            return None

        session = DbSessionFactory.create_session()
        return session.query(PasswordReset).filter(PasswordReset.id == code).first()

    @classmethod
    def use_reset_code(cls, reset_code, user_ip):
        session = DbSessionFactory.create_session()

        reset = (
            session.query(PasswordReset).filter(PasswordReset.id == reset_code).first()
        )

        if not reset:
            return

        reset.used_ip_address = user_ip
        reset.was_used = True
        reset.used_date = datetime.datetime.now()

        session.commit()

    @classmethod
    def set_password(cls, plain_text_password, account_id):
        print("Resetting password for user {}".format(account_id))
        session = DbSessionFactory.create_session()

        account = session.query(Account).filter(Account.id == account_id).first()

        if not account:
            print("Warning: Cannot reset password, no account found.")
            return

        print("New password set.")
        account.password_hash = AccountService.hash_text(plain_text_password)
        session.commit()

    @classmethod
    def get_account_info(cls, user_id):
        session = DbSessionFactory.create_session()

        return session.query(Account).filter(Account.id == user_id).all()

    @classmethod
    def get_account_date(cls, user_id):
        session = DbSessionFactory.create_session()

        account_created = session.query(Account.created).first()
        account_string = str(account_created[0])
        account_date_split = account_string.split()
        return account_date_split[0]

    @classmethod
    def seasons_played(cls, user_id):
        session = DbSessionFactory.create_session()

        return (
            session.query(PlayerPicks.season)
            .distinct(PlayerPicks.season)
            .filter(Account.id == user_id)
            .order_by(PlayerPicks.season.desc())
        )
