import pyramid_handlers
from nflpool.controllers.base_controller import BaseController
from nflpool.viewmodels.newinstallviewmodel import NewInstallViewModel
from nflpool.viewmodels.newseasonviewmodel import NewSeasonViewModel
from nflpool.viewmodels.update_nflplayers_viewmodel import UpdateNFLPlayersViewModel
from nflpool.services.new_install_service import NewInstallService
from nflpool.services.new_season_service import NewSeasonService
from nflpool.services.activeplayers_service import ActivePlayersService
from nflpool.viewmodels.update_nflschedule_viewmodel import UpdateNFLScheduleViewModel
from nflpool.services.update_nflschedule_service import UpdateScheduleService
from nflpool.data.account import Account
from nflpool.data.dbsession import DbSessionFactory


class AdminController(BaseController):
    @pyramid_handlers.action(renderer='templates/admin/index.pt')
    def index(self):
        session = DbSessionFactory.create_session()
        su__query = session.query(Account.id).filter(Account.is_super_user == 1)\
            .filter(Account.id == self.logged_in_user_id).first()

        if su__query is None:
            print("You must be an administrator to view this page")
            self.redirect('/home')

        return {}

    # GET /admin/new_install
    @pyramid_handlers.action(renderer='templates/admin/new_install.pt',
                             request_method='GET',
                             name='new_install')
    def new_install_get(self):
        session = DbSessionFactory.create_session()
        su__query = session.query(Account.id).filter(Account.is_super_user == 1)\
            .filter(Account.id == self.logged_in_user_id).first()

        if su__query is None:
            print("You must be an administrator to view this page")
            self.redirect('/home')

        vm = NewInstallViewModel()
        return vm.to_dict()

    # POST /admin/new_install
    @pyramid_handlers.action(renderer='templates/admin/new_install.pt',
                             request_method='POST',
                             name='new_install')
    def new_install_post(self):
        vm = NewInstallViewModel()
        vm.from_dict(self.request.POST)

        # Insert team info
        team_data = NewInstallService.get_team_info()
        division_data = NewInstallService.create_division_info()
        conference_data = NewInstallService.create_conference_info()
        pick_types = NewInstallService.create_pick_types()

        # redirect
        self.redirect('/admin/new_season')

    @pyramid_handlers.action(renderer='templates/admin/new_season.pt',
                             request_method='GET',
                             name='new_season')
    def new_season_get(self):
        session = DbSessionFactory.create_session()
        su__query = session.query(Account.id).filter(Account.is_super_user == 1)\
            .filter(Account.id == self.logged_in_user_id).first()

        if su__query is None:
            print("You must be an administrator to view this page")
            self.redirect('/home')

        vm = NewSeasonViewModel()
        return vm.to_dict()

    @pyramid_handlers.action(renderer='templates/admin/new_season.pt',
                             request_method='POST',
                             name='new_season')
    def new_season_post(self):
        vm = NewSeasonViewModel()
        vm.from_dict(self.request.POST)

        # Insert NFLPlayer info
        new_season_input = NewSeasonService.create_season(vm.new_season_input)

        # redirect
        self.redirect('/admin/update_nflplayers')

    @pyramid_handlers.action(renderer='templates/admin/update_nflplayers.pt',
                             request_method='GET',
                             name='update_nflplayers')
    def update_nfl_players(self):
        session = DbSessionFactory.create_session()
        su__query = session.query(Account.id).filter(Account.is_super_user == 1)\
            .filter(Account.id == self.logged_in_user_id).first()

        if su__query is None:
            print("You must be an administrator to view this page")
            self.redirect('/home')

        vm = UpdateNFLPlayersViewModel()
        return vm.to_dict()

    @pyramid_handlers.action(renderer='templates/admin/update_nflplayers',
                             request_method='POST',
                             name='update_nflplayers')
    def update_nfl_players_post(self):
        vm = UpdateNFLPlayersViewModel()
        vm.from_dict(self.request.POST)

        # Insert NFLPlayer info
        active_players = ActivePlayersService.add_active_nflplayers(vm.firstname, vm.lastname, vm.player_id,
                                                                    vm.team_id, vm.position, vm.season)

        # redirect
        self.redirect('/admin/update_nflschedule')

    @pyramid_handlers.action(renderer='templates/admin/update_nflschedule.pt',
                             request_method='GET',
                             name='update_nflschedule')
    def update_nfl_schedule(self):
        session = DbSessionFactory.create_session()
        su__query = session.query(Account.id).filter(Account.is_super_user == 1)\
            .filter(Account.id == self.logged_in_user_id).first()

        if su__query is None:
            print("You must be an administrator to view this page")
            self.redirect('/home')

        vm = UpdateNFLScheduleViewModel()
        return vm.to_dict()

    @pyramid_handlers.action(renderer='templates/admin/update_nflschedule',
                             request_method='POST',
                             name='update_nflschedule')
    def update_nfl_schedule_post(self):
        vm = UpdateNFLScheduleViewModel()
        vm.from_dict(self.request.POST)

        # Insert NFL Schedule
        update_nflschedule = UpdateScheduleService.update_nflschedule(vm.game_id, vm.game_date, vm.away_team,
                                                                      vm.home_team, vm.week, vm.season)

        # redirect
        self.redirect('/admin')
