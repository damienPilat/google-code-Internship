"""A video playlist class."""


class Playlist:
    """A class used to represent a Playlist."""
    def __init__(self, playlist_title: str):
        self._title = playlist_title
        self._video_ids = []

    @property
    def title(self) -> str:
        """Returns the title of a Playlist"""
        return self._title

    @property
    def get_all_video_ids(self):
        return self._video_ids

    def remove_video_from_playlist(self, video_id):
        self._video_ids.remove(video_id)

    def remove_all_videos(self):
        self._video_ids = []

    def add_video(self, video_id):
        """Checks video not already in Playlist before adding"""
        if not self.check_video_in_playlist(video_id):
            self._video_ids.append(video_id)

    def check_video_in_playlist(self, video_id):
        """Checks if video_id in Playlist"""
        if len(self._video_ids) == 0:
            return False
        for vid_id in self._video_ids:
            if vid_id == video_id:
                return True
        return False
