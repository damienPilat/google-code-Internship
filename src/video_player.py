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

    # Return All User Playlists -> Object
    def get_user_playlists(self):
        return self._user_playlists

    # Return length of All User Playlists -> int
    def get_user_playlists_len(self):
        return len(self._user_playlists)

    # Get Specific Playlist from Name -> Playlist
    def get_playlist(self, playlist_name):
        for playlistName in self._user_playlists:
            if playlistName.upper() == playlist_name.upper():
                return self._user_playlists[playlistName]
        return None

    # Remove Playlist from List
    def remove_playlist(self, playlist_name):
        playlist_id_to_remove = None
        for playlistName in self._user_playlists:
            if playlistName.upper() == playlist_name.upper():
                playlist_id_to_remove = playlistName
        self._user_playlists.pop(playlist_id_to_remove)

    # Return number of videos in Library
    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    # ------
    # PART 1
    # ------

    def show_all_videos(self):
        """Returns all videos."""
        # Get all videos
        all_videos = self._video_library.get_all_videos()
        # Array to store resulting strings
        result_array = []

        # Loop through all videos
        for video in all_videos:
            # IF video has flag
            if video.flag:
                # Append to array result in given format + flag msg
                result_array.append(self.string_video_detail(video) + f" - FLAGGED (reason: {video.flag})")
            else:
                # Append to array result in given format
                result_array.append(self.string_video_detail(video))

        # Alphabetic order for Results
        result_array.sort()

        # PRINT Result
        # Print 1st line
        print("Here's a list of all available videos:")
        # Print all results
        print('\n'.join(map(str, result_array)))

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        # Get Video with given id
        video = self._video_library.get_video(video_id)

        # If video exists
        if video:
            # Check for flag
            if video.flag:
                print(f"Cannot play video: Video is currently flagged (reason: {video.flag})")
            else:
                # If video is playing, Stop it & clear paused status
                if self._video_playing:
                    self.stop_video()
                    self._video_paused = False
                # PRINT: Play current Video
                print(f"Playing video: {video.title}")
        # If video doesnt exist
        else:
            # PRINT: Error msg
            print("Cannot play video: Video does not exist")
        # Add video to self - video playing
        self._video_playing = video

    def stop_video(self):
        """Stops the current video."""
        # Check if video is playing
        if self._video_playing:
            # PRINT: Stop video
            print(f"Stopping video: {self._video_playing.title}")
            # Remove video from Self - video playing
            self._video_playing = False
        else:
            # PRINT: error msg
            print("Cannot stop video: No video is currently playing")

    def play_random_video(self):
        """Plays a random video from the video library."""
        # Check if video currently playing, stops it
        if self._video_playing:
            self.stop_video()

        # Store all videos
        all_videos = self._video_library.get_all_videos()

        # Get a random video
        random_video = random.choice(all_videos)

        # Loop if video has flag or no more last video
        while random_video.flag:
            if len(all_videos) > 1:
                # Remove last video from list
                all_videos = self.remove_video(random_video, all_videos)
                random_video = random.choice(all_videos)
            else:
                break

        # IF Last video has flag
        if all_videos[0].flag:
            # Err - No video
            print("No videos available")
        else:
            # Play video
            self.play_video(random_video.video_id)

    def remove_video(self, video, video_list):
        """Remove video from given list if present

           Args:
               video: Video Instance to be removed.
               video_list: List of several Video Instances
           Return:
               video_list without video element (if was present)
        """
        for video_key, video_element in enumerate(video_list):
            # print("video_key:", video_key, ", vid_el:", video_element)
            if video_element.video_id == video.video_id:
                video_list.pop(video_key)
        # print("Finished looping")
        return video_list

    def pause_video(self):
        """Pauses the current video."""
        # IF video playing
        if self._video_playing:
            # If video paused
            if self._video_paused:
                # PRINT: video already paused
                print(f"Video already paused: {self._video_playing.title}")
            # IF video not paused
            else:
                # PRINT: pausing video
                print(f"Pausing video: {self._video_playing.title}")
                # Add Paused status to Self
                self._video_paused = True
        # Else: Video not playing
        else:
            print("Cannot pause video: No video is currently playing")

    def continue_video(self):
        """Resumes playing the current video."""
        # If video playing
        if self._video_playing:
            # If video paused
            if self._video_paused:
                # Playing video
                print(f"Continuing video: {self._video_playing.title}")
                # Removing paused status from Self
                self._video_paused = False
            # If not paused
            else:
                # PRINT: Err msg
                print("Cannot continue video: Video is not paused")
        # Else: video not playing
        else:
            # Print: Err msg
            print("Cannot continue video: No video is currently playing")

    def show_playing(self):
        """Displays video currently playing."""
        # Check video playing
        if self._video_playing:
            # Store details of current video
            current_video = self._video_playing
            # Create status string
            status_string = f"Currently playing: {self.string_video_detail(current_video)}"
            # Add prefix if video paused
            if self._video_paused:
                print(status_string + " - PAUSED")
            else:
                print(status_string)
        # If no video playing
        else:
            # PRINT: Err msg
            print("No video is currently playing")

    # ------
    # PART 2
    # ------

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        # check playlist with same name exists
        if self.check_playlist_exists(playlist_name):
            print("Cannot create playlist: A playlist with the same name already exists")
        else:
            # Add to Arary
            # self._user_playlists.append(Playlist(playlist_name))
            self._user_playlists[playlist_name] = Playlist(playlist_name)
            print(f"Successfully created new playlist: {playlist_name}")

    def check_playlist_exists(self, playlist_name):
        # If len 0, return false
        if len(self._user_playlists) == 0:
            return False

        # Loop through playlists
        for playlist in self._user_playlists:
            # Case insensitive - return if name match
            if playlist.upper() == playlist_name.upper():
                return True
        return False

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        current_video = self._video_library.get_video(video_id)
        current_playlist = self.get_playlist(playlist_name)

        # If playlist exists
        if current_playlist:
            # If video exists
            if current_video:
                # Check if video has flag
                if current_video.flag:
                    # Err - video flagged
                    print(f"Cannot add video to {playlist_name}: Video is currently flagged (reason: {current_video.flag})")
                else:
                    # Check if video in playlist
                    if current_playlist.check_video_in_playlist(current_video.video_id):
                        print(f"Cannot add video to {playlist_name}: Video already added")
                    else:
                        # Add video to playlist
                        current_playlist.add_video(current_video.video_id)
                        print(f"Added video to {playlist_name}: {current_video.title}")
            else:
                # Err - video doesnt exist
                print(f"Cannot add video to {playlist_name}: Video does not exist")
        else:
            # Err- no playilst
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")

    def show_all_playlists(self):
        """Display all playlists."""
        if len(self._user_playlists) == 0:
            # Err - no playlists
            print("No playlists exist yet")
        else:
            print("Showing all playlists:")
            all_playlists_names = []
            for playlist in self._user_playlists:
                all_playlists_names.append(playlist)

            # alphabetic order
            all_playlists_names.sort()
            print('\n'.join(map(str, all_playlists_names)))

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if len(self._user_playlists) == 0:
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist yet")
        else:
            print(f"Showing playlist: {playlist_name}")
            playlist = self.get_playlist(playlist_name)
            all_video_ids = playlist.get_all_video_ids
            if len(all_video_ids) == 0:
                print("No videos here yet")
            else:
                for video_id in all_video_ids:
                    current_video = self._video_library.get_video(video_id)
                    if current_video.flag:
                        print(self.string_video_detail(current_video) + f" - FLAGGED (reason: {current_video.flag})")
                    else:
                        print(self.string_video_detail(current_video))

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        if len(self._user_playlists) == 0:
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")
        else:
            current_video = self._video_library.get_video(video_id)
            current_playlist = self.get_playlist(playlist_name)

            # Check playlist exists
            if current_playlist:
                # Check video exists
                if current_video:
                    # Check if video in playlist
                    if current_playlist.check_video_in_playlist(current_video.video_id):
                        # Remove vid from playlist
                        print(f"Removed video from {playlist_name}: {current_video.title}")
                        current_playlist.remove_video_from_playlist(video_id)
                    else:
                        # Err - video not in playlist
                        print(f"Cannot remove video from {playlist_name}: Video is not in playlist")
                else:
                    # Err - video does not exist
                    print(f"Cannot remove video from {playlist_name}: Video does not exist")
            else:
                # Err - playlist doesnt exist
                print(f"Cannot remove video from {playlist_name}: Playlist does not exist")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if len(self._user_playlists) == 0:
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")
        else:
            current_playlist = self.get_playlist(playlist_name)
            # If playlist exists
            if current_playlist:
                # Empty playlist
                current_playlist.remove_all_videos()
                print(f"Successfully removed all videos from {playlist_name}")
            else:
                # Err - Playlist doesnt exist
                print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if len(self._user_playlists) == 0:
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")
        else:
            current_playlist = self.get_playlist(playlist_name)
            # if playlist exists
            if current_playlist:
                # Remove playlist
                self.remove_playlist(playlist_name)
                print(f"Deleted playlist: {playlist_name}")

    # ------
    # PART 3
    # ------

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        # Get all videos
        all_videos = self._video_library.get_all_videos()
        # Array to store matching videos
        search_match_videos = []

        # Loop through videos & all where title matches
        for video in all_videos:
            if self.search_term_in_video_title(search_term, video):
                search_match_videos.append(video)

        # If no matches found
        if len(search_match_videos) == 0:
            # Err - no results
            print(f"No search results for {search_term}")
        # If matches
        else:
            self.manage_search_results(search_term, search_match_videos)

    def manage_search_results(self, search_term, resulting_videos):
        # Print header
        print(f"Here are the results for {search_term}:")
        # Loop through matches & Print line
        for index, match_video in enumerate(resulting_videos):
            print(f"{index + 1}) {self.string_video_detail(match_video)}")
        # Print two footer msgs
        print("Would you like to play any of the above? If yes, specify the number of the video.")
        print("If your answer is not a valid number, we will assume it's a no.")

        # Check if input is int (ignore if not)
        try:
            user_response = int(input()) - 1    # Array index starts at 0, user input starts at 1
            # If value less than length of response array
            if user_response < len(resulting_videos):
                # Play video
                self.play_video(resulting_videos[user_response].video_id)
        except ValueError:
            pass

    def search_term_in_video_title(self, search_term, video):
        """Searches for search term in video title - Case insensitive
           Disregards videos with flags

        Args:
            search_term: The query to be used in search.
            video: Specified video instance

        Return:
            Boolean if term in title.
        """
        if video.flag:
            return False

        video_title = video.title.upper()

        term_starts_at = video_title.find(search_term.upper())
        if term_starts_at >= 0:
            return True
        return False

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        # Get all videos
        all_videos = self._video_library.get_all_videos()
        # Array to store matching videos
        search_match_videos = []

        # Loop through videos & all where tags match
        for video in all_videos:
            if self.search_tag_in_video(video_tag, video):
                search_match_videos.append(video)

        # if no matches found
        if len(search_match_videos) == 0:
            # Err - no results
            print(f"No search results for {video_tag}")
        # If matches
        else:
            self.manage_search_results(video_tag, search_match_videos)

    def search_tag_in_video(self, video_tag, video):
        """Searches for video tag in videos - case insensitive

            Args:
                video_tag: user provided tag to be searched
                video: Specified Video instance

            Return:
                Boolean if term in tags
        """
        if video.flag:
            return False
        # Loop through video tags
        for tag in video.tags:
            if tag.upper() == video_tag.upper():
                return True
        return False

    # ------
    # PART 4
    # ------

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        # Get video from id
        video = self._video_library.get_video(video_id)

        # Check if video is playing, and stops it
        if self._video_playing and self._video_playing.video_id == video.video_id:
            self.stop_video()

        # if Video exists
        if video:
            # Check if video has flag
            if video.flag:
                # Err - Video already flagged
                print("Cannot flag video: Video is already flagged")
            else:
                # Add flag to video
                video.flag = flag_reason if flag_reason != "" else "Not supplied"
                print(f"Successfully flagged video: {video.title} (reason: {video.flag})")
        else:
            # Err - video doesnt exist
            print("Cannot flag video: Video does not exist")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        video = self._video_library.get_video(video_id)

        # Checks video exists
        if video:
            # Checks video has flag
            if video.flag:
                video.flag = None
                print(f"Successfully removed flag from video: {video.title}")
            else:
                # Err - no flag
                print("Cannot remove flag from video: Video is not flagged")
        else:
            # Err - vid doesnt exist
            print("Cannot remove flag from video: Video does not exist")

    def string_video_detail(self, video):
        tag_string = ' '.join(map(str, video.tags))
        return f"{video.title} ({video.video_id}) [{tag_string}]"
