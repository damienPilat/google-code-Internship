"""A video player class."""

import random
from .video_library import VideoLibrary
from .video_playlist import Playlist


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        """Video Player Constructor"""
        self._video_library = VideoLibrary()
        self._video_playing = False
        self._video_paused = False
        self._user_playlists = {}

    @property
    def all_videos(self):
        """Returns List of all """
        return self._video_library.get_all_videos()

    def get_video(self, video_id):
        """Returns video from video id or None"""
        return self._video_library.get_video(video_id)

    def get_user_playlists(self):
        """Returns the user playlists stored -> List"""
        return self._user_playlists

    def get_user_playlists_len(self):
        """Returns length of All User Playlists -> int"""
        return len(self._user_playlists)

    def get_playlist(self, playlist_name):
        """Returns Playlist with specifc name or None"""
        for playlistName in self._user_playlists:
            if playlistName.upper() == playlist_name.upper():
                return self._user_playlists[playlistName]
        return None

    def remove_playlist(self, playlist_name):
        """Removes Playlist with specific name if exists"""
        playlist_id_to_remove = None
        for playlistName in self._user_playlists:
            if playlistName.upper() == playlist_name.upper():
                playlist_id_to_remove = playlistName
        self._user_playlists.pop(playlist_id_to_remove)

    def number_of_videos(self):
        """Prints number of videos in Library"""
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    # ------
    # PART 1
    # ------

    def show_all_videos(self):
        """PRINT all videos"""
        all_videos = self.all_videos                                        # Get all videos
        videos_resulting_array = self.videos_to_string_array(all_videos)    # Array to store resulting strings

        print("Here's a list of all available videos:")                     # Print Header
        print('\n'.join(map(str, videos_resulting_array)))                  # Join and Print all videos

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """

        def play_video_logic():
            """Stop & put on Pause any currently playing video, then play current video """
            if self._video_playing:
                self.stop_video()
                self._video_paused = False
            print(f"Playing video: {video.title}")                          # PRINT: Play video
            self._video_playing = video                                     # Add video to currently playing video

        video = self.get_video(video_id)                                    # Get Video with given id

        if video:                                                           # Check if video exists
            if video.flag:                                                  # Check if video has flag
                print(f"Cannot play video: Video is currently flagged (reason: {video.flag})")
            else:
                play_video_logic()
        else:                                                               # Video doesnt exist
            print("Cannot play video: Video does not exist")

    def stop_video(self):
        """Stops the current video."""
        if self._video_playing:                                             # Check if video is playing
            print(f"Stopping video: {self._video_playing.title}")           # PRINT: Stop video
            self._video_playing = False                                     # Remove video from currently playing video
        else:                                                               # No video playing
            print("Cannot stop video: No video is currently playing")       # PRINT: error msg

    def play_random_video(self):
        """Plays a random video from the video library."""

        def random_video_logic():
            """Gets a random video without any flags"""
            _all_videos = self.all_videos                                   # Store all videos
            _random_video = random.choice(_all_videos)                      # Get a random video

            while _random_video.flag:                                       # Loop while video has flag
                if len(_all_videos) > 1:
                    _all_videos = self.remove_video(_random_video, _all_videos)     # Remove last video from list
                    _random_video = random.choice(_all_videos)                      # Get new random video from updated list
                break
            return _random_video

        if self._video_playing:                                             # Check if video currently playing
            self.stop_video()                                               # Stop video

        random_video = random_video_logic()                                 # Get random Video

        if random_video.flag:                                               # Check if video has flag
            print("No videos available")
        else:
            self.play_video(random_video.video_id)                          # Play video

    def remove_video(self, video, video_list):
        """Remove video from given list if present

           Args:
               video: Video Instance to be removed.
               video_list: List of several Video Instances
           Return:
               video_list without video element (if was present)
        """
        for video_key, video_element in enumerate(video_list):              # Get key,value pair from provided List
            if video_element.video_id == video.video_id:                    # Check if video_ids match
                video_list.pop(video_key)                                   # Remove video if so
        return video_list

    def pause_video(self):
        """Pauses the current video."""
        if self._video_playing:                                             # Check if video playing exists
            if self._video_paused:                                          # Check if video paused
                print(f"Video already paused: {self._video_playing.title}") # Err - already paused
            else:                                                       # Video not paused
                print(f"Pausing video: {self._video_playing.title}")        # Print Pausing msg
                self._video_paused = True                                   # Update paused status
        else:                                                           # Err - no video playing
            print("Cannot pause video: No video is currently playing")

    def continue_video(self):
        """Resumes playing the current video."""
        if self._video_playing:                                             # Check if video playing exists
            if self._video_paused:                                          # Check if video paused
                print(f"Continuing video: {self._video_playing.title}")     # Play video
                self._video_paused = False                                  # Update paused status
            else:                                                       # If not paused
                print("Cannot continue video: Video is not paused")         # Err - Video not paused
        else:                                                           # Video not playing
            print("Cannot continue video: No video is currently playing")   # Err - not playing

    def show_playing(self):
        """Displays video currently playing."""
        if self._video_playing:                                             # Check if video playing exists
            current_video = self._video_playing                             # Store current video
            status_string = f"Currently playing: {self.string_video_detail(current_video)}"     # Create status string
            if self._video_paused:                                          # Add prefix if video paused
                status_string += " - PAUSED"
            print(status_string)                                            # PRINT: Video paused
        else:                                                           # Video doesnt exist
            print("No video is currently playing")                          # Err - no video

    # ------
    # PART 2
    # ------

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if self.check_playlist_exists(playlist_name):                       # Check playlist with same name exists
            print("Cannot create playlist: A playlist with the same name already exists")
        else:
            self._user_playlists[playlist_name] = Playlist(playlist_name)   # Add playlist to List
            print(f"Successfully created new playlist: {playlist_name}")    # Print: Playlist added

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        current_video = self.get_video(video_id)                                            # Store current video
        current_playlist = self.get_playlist(playlist_name)                                 # & playlist

        if current_playlist:                                                                # Check playlist exists
            if current_video:                                                               # Check video exists
                if current_video.flag:                                                      # Check if video has flag
                    print(f"Cannot add video to {playlist_name}: Video is currently flagged (reason: {current_video.flag})")
                else:                                                                   # Video not flagged
                    if current_playlist.check_video_in_playlist(current_video.video_id):    # Check if video in playlist
                        print(f"Cannot add video to {playlist_name}: Video already added")
                    else:                                                               # Video not in Playlist
                        current_playlist.add_video(current_video.video_id)                  # Add video to playlist
                        print(f"Added video to {playlist_name}: {current_video.title}")
            else:                                                                       # Video doesnt exist
                print(f"Cannot add video to {playlist_name}: Video does not exist")         # Err - video doesnt exist
        else:                                                                           # Playlist doesnt exist
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")          # Err- no playlist

    def show_all_playlists(self):
        """Display all playlists."""
        if len(self._user_playlists) == 0:                                  # EXIT if no playlist in list
            print("No playlists exist yet")
        else:                                                           # Playlists present
            print("Showing all playlists:")                                 # Print header
            all_playlists_names = []
            for playlist in self._user_playlists:                           # Append playlist names
                all_playlists_names.append(playlist)

            all_playlists_names.sort()                                      # Sort in alphabetic order
            print('\n'.join(map(str, all_playlists_names)))                 # Print resulting array of playlist names

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if len(self._user_playlists) == 0:                                              # Exit if no playlist in list
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist yet")
        else:                                                                       # Playlists present
            print(f"Showing playlist: {playlist_name}")                                 # Print header
            playlist = self.get_playlist(playlist_name)
            all_video_ids = playlist.get_all_video_ids                                  # Get all video ids
            if len(all_video_ids) == 0:                                                 # If result empty, print Err
                print("No videos here yet")
            else:
                for video_id in all_video_ids:                                          # Loop through resulting array
                    current_video = self._video_library.get_video(video_id)
                    video_to_string = self.string_video_detail(current_video)           # Generic video to string
                    if current_video.flag:                                              # Check for flag
                        video_to_string += f" - FLAGGED (reason: {current_video.flag})"
                    print(video_to_string)

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        if len(self._user_playlists) == 0:                                              # Exit if no playlist in list
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")
        else:                                                                           # Playlists present
            current_video = self.get_video(video_id)
            current_playlist = self.get_playlist(playlist_name)

            if current_playlist:                                                        # Check playlist exists
                if current_video:                                                       # Check video exists
                    if current_playlist.check_video_in_playlist(current_video.video_id):    # Check if video in playlist
                        print(f"Removed video from {playlist_name}: {current_video.title}") # Remove vid from playlist
                        current_playlist.remove_video_from_playlist(video_id)
                    else:                                                               # Video not in playlist
                        print(f"Cannot remove video from {playlist_name}: Video is not in playlist")
                else:                                                                   # Video doesnt exist
                    print(f"Cannot remove video from {playlist_name}: Video does not exist")
            else:                                                                       # Playlist doesnt exist
                print(f"Cannot remove video from {playlist_name}: Playlist does not exist")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if len(self._user_playlists) == 0:                                              # Exit if no playlist in list
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")
        else:                                                                           # Playlists present
            current_playlist = self.get_playlist(playlist_name)
            if current_playlist:                                                        # Check if playlist exists
                current_playlist.remove_all_videos()                                    # Empty out playlist
                print(f"Successfully removed all videos from {playlist_name}")
            else:                                                                       # Playlist doesnt exist
                print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if len(self._user_playlists) == 0:                                              # Exit if no playlist in list
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")
        else:                                                                           # Playlist present
            current_playlist = self.get_playlist(playlist_name)
            if current_playlist:                                                        # Check if playlist exists
                self.remove_playlist(playlist_name)                                     # Remove playlist
                print(f"Deleted playlist: {playlist_name}")

    # ------
    # PART 3
    # ------

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        all_videos = self.all_videos                                            # Get all videos
        search_match_videos = []                                                # Array to store matching videos

        for video in all_videos:                                                # Loop through videos
            if self.search_term_in_video_title(search_term, video):             # Check for search term in title
                search_match_videos.append(video)                                   # Append to array

        if len(search_match_videos) == 0:                                       # No matches, Err
            print(f"No search results for {search_term}")
        else:                                                                   # Matches - apply logic
            self.search_results_logic(search_term, search_match_videos)

    def search_results_logic(self, search_term, resulting_videos):
        """Logic for results of searching word in title

            Args: search_term: user provide search term.
            resulting_videos: all videos that match search term.
        """

        def print_search_results():
            """Print all results with Header/Footer """
            print(f"Here are the results for {search_term}:")                       # Print Header
            for index, match_video in enumerate(resulting_videos):                  # Loop through matches & Print line
                print(f"{index + 1}) {self.string_video_detail(match_video)}")
            print("Would you like to play any of the above? If yes, specify the number of the video.")  # Print Footer
            print("If your answer is not a valid number, we will assume it's a no.")

        def user_response_logic():
            """Deal with user response"""
            try:                                                # Check if input is int (ignore if not)
                user_response = int(input()) - 1                     # Array index starts at 0, user input starts at 1
                if user_response < len(resulting_videos):            # Check if value less than length of response array
                    self.play_video(resulting_videos[user_response].video_id)       # Play corresponding video
            except ValueError:
                pass

        print_search_results()                                      # Print search results
        user_response_logic()                                       # Deal with user response

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        all_videos = self.all_videos                                # Get all videos
        search_match_videos = []                                    # Array to store matching videos

        for video in all_videos:                                    # Loop through videos
            if self.search_tag_in_video(video_tag, video):          # Check if tags match
                search_match_videos.append(video)                   # Append to array

        if len(search_match_videos) == 0:                           # Exit if no matches found
            print(f"No search results for {video_tag}")
        else:                                                       # Match found
            self.search_results_logic(video_tag, search_match_videos)   # Apply Search results logic

    # ------
    # PART 4
    # ------

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        current_video = self.get_video(video_id)                                            # Store current video
        if self._video_playing and self._video_playing.video_id == current_video.video_id:  # Check if current video is playing
            self.stop_video()                                                               # Stop video if yes

        if current_video:                                                                   # Check if video exists
            if current_video.flag:                                                          # Check if video has flag
                print("Cannot flag video: Video is already flagged")                        # Err - video already has flag
            else:
                current_video.flag = flag_reason if flag_reason != "" else "Not supplied"   # Add Frag (provide or default)
                print(f"Successfully flagged video: {current_video.title} (reason: {current_video.flag})")
        else:                                                                               # Video doesnt exist
            print("Cannot flag video: Video does not exist")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        video = self.get_video(video_id)                                            # Store current video

        if video:                                                                   # Checks video exists
            if video.flag:                                                          # Checks video has flag
                video.flag = None                                                   # Remove Flag
                print(f"Successfully removed flag from video: {video.title}")
            else:                                                               # Video has no flag
                print("Cannot remove flag from video: Video is not flagged")        # Err - no flag
        else:                                                                   # No video
            print("Cannot remove flag from video: Video does not exist")            # Err - no video

    # ----------------
    # HELPER FUNCTIONS
    # ----------------
    def string_video_detail(self, video):
        """Convert a videos details to string"""
        tag_string = ' '.join(map(str, video.tags))
        return f"{video.title} ({video.video_id}) [{tag_string}]"

    def videos_to_string_array(self, all_videos):
        """Create String array of all videos

        Args: all_videos - List of all videos to convert

        Return: String array of videos
        """
        _videos_resulting_array = []                                        # Temp array to store resulting strings
        for video in all_videos:                                            # Loop through all videos
            _videos_resulting_array.append(self.get_video_to_string(video))
        _videos_resulting_array.sort()                                      # Alphabetic order for Results
        return _videos_resulting_array

    def get_video_to_string(self, video):
        """Return String conversion of Video details + flag status

        Args: video - Video instance to get details from
        Return: String of video details
        """
        video_to_string = self.string_video_detail(video)                   # Default video to string
        if video.flag:                                                      # Check if video has flag
            video_to_string += f" - FLAGGED (reason: {video.flag})"         # Append Flag tag to string
        return video_to_string

    def check_playlist_exists(self, playlist_name):
        """Check if Playlist already exists - case insensitive

            Args: playlist_name - playlist name to check for.
        """
        if len(self._user_playlists) == 0:                                  # EXIT : If no playlist in list
            return False

        for playlist in self._user_playlists:                               # Loop through playlists
            if playlist.upper() == playlist_name.upper():                   # Compare playlist name - case insensitive
                return True
        return False

    def search_term_in_video_title(self, search_term, video):
        """Searches for search term in video title - Case insensitive
           Disregards videos with flags

        Args:
            search_term: The query to be used in search.
            video: Specified video instance

        Return:
            Boolean if term in title.
        """
        if video.flag:                                              # Exit if video has flag
            return False

        video_title = video.title.upper()                           # Get video title (uppercase)

        term_starts_at = video_title.find(search_term.upper())      # Look for search_term in video_title
        if term_starts_at >= 0:                                     # Term found if index has positive value
            return True
        return False

    def search_tag_in_video(self, video_tag, video):
        """Searches for video tag in videos - case insensitive

        Args:
            video_tag: user provided tag to be searched
            video: Specified Video instance

        Return:
            Boolean if term in tags
        """
        if video.flag:                                              # Exit if video has flag
            return False
        for tag in video.tags:                                      # Loop through video tags
            if tag.upper() == video_tag.upper():                    # Check if tag matches (case insensitive)
                return True
        return False
