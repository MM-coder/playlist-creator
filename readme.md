# Playlist Creator by Mauro M.

Allows multiple users to create a single playlist. Was originally intened for a party. It allows each user to submit 3 songs to a playlist, by submitting a Spotify or Youtube link, the program then stores said links to a database.

## Screenshots

![index](https://raw.githubusercontent.com/MM-coder/playlist-creator/master/.github/screenshots/index.png?token=AFN6RUGXAKQLSEXULVON4SS7FRIMU)
![submit](https://raw.githubusercontent.com/MM-coder/playlist-creator/master/.github/screenshots/submit.png?token=AFN6RUCDWU7YNM6C6GXIWRK7FRIOY)

## Deployment Instructions
The program is ready for deployment to [heroku](https://herokuapp.com) 
1. Fork the repository 
2. Set a valid PostgreSQL url in `music.py`
3. Create user accounts using `user_creator.py`
4. Sync the github repository with Heroku
5. Activate the web worker 
6. All done!

## Not Implemeted

[] Exporting of playlist to MP3 using `youtube_dl` (requires bug testing)

## License

![License Badge](https://mirrors.creativecommons.org/presskit/buttons/80x15/svg/by-nc-nd.svg)

The aforementioned code is protected and released to the public under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0) License which can be viewed in license.md or on the Creative Commons website (https://creativecommons.org/licenses/by-nc-nd/4.0/). Any failure to comply with the terms designated in the license will be met with swift judicial action by the author.

By downloading, executing or otherwise transferring the code by any means you are legally bound to the terms stipulated in the license