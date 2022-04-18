from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, List, Set

from backports.cached_property import cached_property
from typing_extensions import Protocol

from .autogenerated_models import *

if TYPE_CHECKING:
    from .api import E621


class Post(Post):
    @cached_property
    def all_tags(self) -> Set[str]:
        return set(
            self.tags.general
            + self.tags.species
            + self.tags.character
            + self.tags.copyright
            + self.tags.artist
            + self.tags.invalid
            + self.tags.lore
            + self.tags.meta
        )


class _HasPostIdsAndE621API(Protocol):
    _e6api: "E621"
    post_ids: List[int]


class _PostsGetterMixin:
    @cached_property
    def posts(self: _HasPostIdsAndE621API) -> List[Post]:
        return self._e6api.posts.search(tags=f"id:{','.join(map(str, self.post_ids))}")


class Pool(Pool, _PostsGetterMixin):
    pass


class EnrichedPostSet(PostSet, _PostsGetterMixin):
    pass


class BlackList(Set[str]):
    def intersects(self, iterable: Iterable[str]) -> bool:
        for val in self:
            if " " in val and all(v in iterable for v in val.replace("  ", " ").split(" ")):
                return True
            elif val in iterable:
                return True
        return False


class AuthenticatedUser(User):
    wiki_page_version_count: int
    artist_version_count: int
    pool_version_count: int
    forum_post_count: int
    comment_count: int
    flag_count: int
    positive_feedback_count: int
    neutral_feedback_count: int
    negative_feedback_count: int
    upload_limit: int
    show_avatars: bool
    blacklist_avatars: bool
    blacklist_users: bool
    description_collapsed_initially: bool
    hide_comments: bool
    show_hidden_comments: bool
    show_post_statistics: bool
    has_mail: bool
    receive_email_notifications: bool
    enable_keyboard_navigation: bool
    enable_privacy_mode: bool
    style_usernames: bool
    enable_auto_complete: bool
    has_saved_searches: bool
    disable_cropped_thumbnails: bool
    disable_mobile_gestures: bool
    enable_safe_mode: bool
    disable_responsive_mode: bool
    disable_post_tooltips: bool
    no_flagging: bool
    no_feedback: bool
    disable_user_dmails: bool
    enable_compact_uploader: bool
    replacements_beta: bool
    updated_at: str
    email: str
    last_logged_in_at: str
    last_forum_read_at: str
    recent_tags: str
    comment_threshold: int
    default_image_size: str
    favorite_tags: str
    blacklisted_tags: str
    time_zone: str
    per_page: int
    custom_style: str
    favorite_count: int
    api_regen_multiplier: int
    api_burst_limit: int
    remaining_api_limit: int
    statement_timeout: int
    favorite_limit: int
    tag_query_limit: int

    @cached_property
    def blacklist(self) -> BlackList:
        return BlackList(self.blacklisted_tags.split("\n"))
