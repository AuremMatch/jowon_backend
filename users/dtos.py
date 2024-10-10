class UserInfo(object):
    def __init__(self) -> None:
        self.id: int = None
        self.이름: str = None
        self.학번: str = None
        self.학과: str = None
        self.대회참가횟수: int = None
        self.총받은상금: int = None
        self.예상상금: int = None
        self.개발경력: int = None
        self.깃주소: str = None
        self.포토폴리오링크: str = None


class TokenInfo(object):
    def __init__(self) -> None:
        self.token: str = None


class LoginResponse(object):
    def __init__(self, user_info: UserInfo, tokens: TokenInfo) -> None:
        self.user_info: UserInfo = None
        self.tokens: TokenInfo = None


# {
#    "user_info": {},
#    "tokens": {"token": str},
#}
