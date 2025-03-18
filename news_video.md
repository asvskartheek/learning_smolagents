# From a topic, generate a YouTube video using agent

- research a topic using web_search. (o3-mini + manual prompting)
- find good source documents. (o3-mini + manual prompting)
- write a youtube script. (4o + document + prompt) [script](./test_script.txt)
- use the script and download all the needed images. [agent (WIP)](./download_photos_agent.py)
    - right now, it will download image for a particular topic (~15cents per image, 11s)
    - TODO: given the entire script, figure out every image needed then do the entire download. (I think it kinda works now)
- use all the images, create a powerpoint presentation.
- sync the presentation, with eleven labs audio output.