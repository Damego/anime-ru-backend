from enum import IntFlag


class Permissions(IntFlag):
    NONE = 0
    MANAGE_ANIME_TITLES = 1 << 0
    MANAGE_RATINGS = 1 << 1
