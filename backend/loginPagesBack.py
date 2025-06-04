from repositories.user_repository import UserRepository

class LoginPagesBack:
    def checkUserType(self, username, password):

        user_repository = UserRepository()
        return user_repository.check_user(username, password)

