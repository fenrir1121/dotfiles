import vk_api, time, os, atexit

def clean():
  os.system('echo "No music is playing" > .track; rm -f .cover.jpg')

def load():
  try:
    response = vk.method("status.get", {"user_id": 1234567})
  except:
    return "", 0
  if "audio" in response:
    title = response["audio"]["artist"] + " - " + response["audio"]["title"]
    return title, response
  else:
    title = ""
    clean()
    return title, 0

def main():
  temp   = ""
  while 1:
    title, response = load()
    if temp != title and title != "":
      temp = title
      url  = response["audio"]["url"]
      url  = url[:url.find("?")]
      os.system('echo "' + title + '" > .track')
      os.system("rm -f .cover.jpg; ffmpeg -loglevel panic -i " + \
        url + " .cover.jpg; [ ! -f .cover.jpg ] && cp .blankcover.jpg .cover.jpg")
    time.sleep(1)

#   --= Run =--

vk = vk_api.VkApi("login", "passwd")
try:
    vk.authorization()
except vk_api.AuthorizationError as error_msg:
    print(error_msg)
    exit()

atexit.register(clean)
main()