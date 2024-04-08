from django.urls import path
from .views import (
    CategoryListCreateView,
    CategoryRetrieveUpdateDestroyView,
    StoryListCreateView,
    StoryRetrieveUpdateDestroyView,
    UserFeedView,
    UserInverseFeedView,
    StoriesByCategoryView,
    LikeCreateView,
    DislikeCreateView,
    LikeDestroyView,
    DislikeDestroyView,
    BookmarkCreateListView,
    BookmarkRetrieveUpdateDestroyView,
    BookmarkRetrieveUpdateDestroyViewByStoryId,
    TrendingStoriesView,
)
from .neo_views import (
    StorylineListView,
    StorylinesForStoryView,
    StoriesByHashtagsView,
    TrendingHashtagsListView,
    StorylineDetailView,
    StorylineStoriesView,
    SpecificStorylineHashtagsView,
)


urlpatterns = [
    path("categories/", CategoryListCreateView.as_view(), name="category-list-create"),
    path(
        "categories/<slug:slug>/",
        CategoryRetrieveUpdateDestroyView.as_view(),
        name="category-retrieve-update-destroy",
    ),
    path("stories/", StoryListCreateView.as_view(), name="story-list-create"),
    path(
        "stories/category/<slug:category_slug>/",
        StoriesByCategoryView.as_view(),
        name="stories-by-category",
    ),
    path("user-feed/", UserFeedView.as_view(), name="user-feed"),
    path("user-inverse-feed/", UserInverseFeedView.as_view(), name="user-inverse-feed"),
    path("trending-stories/", TrendingStoriesView.as_view(), name="trending-stories"),
    path(
        "stories/hashtag/<slug:hashtag_name>/",
        StoriesByHashtagsView.as_view(),
        name="trending-hashtags",
    ),
    path(
        "stories/trending/",
        TrendingHashtagsListView.as_view(),
        name="trending-hashtags-list",
    ),
    path(
        "storylines/<str:storyline_id>/hashtags/",
        SpecificStorylineHashtagsView.as_view(),
        name="storyline-hashtags",
    ),
    path(
        "stories/<slug:story_slug>/",
        StoryRetrieveUpdateDestroyView.as_view(),
        name="story-retrieve-update-destroy",
    ),
    path(
        "stories/<int:story_id>/like/",
        LikeCreateView.as_view(),
        name="like-story-by-id",
    ),
    path(
        "stories/<int:story_id>/dislike/",
        DislikeCreateView.as_view(),
        name="dislike-story-by-id",
    ),
    path(
        "stories/<int:story_id>/unlike/",
        LikeDestroyView.as_view(),
        name="unlike-story-by-id",
    ),
    path(
        "stories/<int:story_id>/undislike/",
        DislikeDestroyView.as_view(),
        name="undislike-story-by-id",
    ),
    path(
        "stories/<slug:slug>/storylines/",
        StorylinesForStoryView.as_view(),
        name="story-storylines",
    ),
    path("storylines/", StorylineListView.as_view(), name="storyline-list"),
    path(
        "storylines/<str:storyline_id>/",
        StorylineDetailView.as_view(),
        name="storyline-detail",
    ),
    path(
        "storylines/<str:storyline_id>/stories/",
        StorylineStoriesView.as_view(),
        name="storyline-stories",
    ),
    # Add URLs for Media, Category, and UserInterest views.
    path("bookmarks/", BookmarkCreateListView.as_view(), name="bookmark-list-create"),
    path(
        "bookmarks/<int:bookmark_id>/",
        BookmarkRetrieveUpdateDestroyView.as_view(),
        name="bookmark-retrieve-update-destroy",
    ),
    path(
        "bookmarks/story/<int:story_id>/",
        BookmarkRetrieveUpdateDestroyViewByStoryId.as_view(),
        name="bookmark-detail-by-story",
    ),
]

# stories/urls.py
