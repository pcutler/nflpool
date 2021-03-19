import pendulum
from nflpool.data.seasoninfo import SeasonInfo
from nflpool.data.dbsession import DbSessionFactory
from nflpool.services.time_service import TimeService


# Set the timezone we will be working with
timezone = pendulum.timezone("America/New_York")

# Don't change this - change the now_time in TimeService
now_time = TimeService.get_time()


def season_opener():

    session = DbSessionFactory.create_session()

    season_start_query = session.query(SeasonInfo.season_start_date).first()
    # print("Season Start Query:", season_start_query)

    # season_start_query is returned as a tuple and need to get the first part of the tuple:
    season_opener_date = str(season_start_query[0])

    # Use the string above in a Pendulum instance and get the time deltas needed
    season_start_date = pendulum.parse(season_opener_date, tz=timezone)

    session.close()

    return season_start_date


class GameDayService:
    @staticmethod
    def admin_check():
        session = DbSessionFactory.create_session()

        season_start_query = session.query(SeasonInfo.season_start_date).first()

        session.close()

        return season_start_query

    @staticmethod
    def season_opener_date():
        """Get the time of the season opener's game"""

        return season_opener()

    @staticmethod
    def timezone():
        return pendulum.timezone("America/New_York")

    @staticmethod
    def time_due():
        season_start_date = season_opener()
        # print("Season start date", season_start_date, "time_due", time_due)

        return season_start_date.format("h:m A")

    @staticmethod
    def picks_due():
        season_start_date = season_opener()
        # print("picks_due_date", picks_due_date)

        return season_start_date.to_formatted_date_string()

    @staticmethod
    def delta_days():

        season_start_date = season_opener()
        now = now_time

        delta = season_start_date - now
        return delta.days

    @staticmethod
    def delta_hours():

        season_start_date = season_opener()
        now = now_time

        delta = season_start_date - now
        return delta.hours

    @staticmethod
    def delta_minutes():

        season_start_date = season_opener()
        now = now_time

        delta = season_start_date - now
        return delta.minutes
