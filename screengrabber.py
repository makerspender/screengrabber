from selenium import webdriver
import time
from PIL import Image
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
# Change this line
wp = Client('http://localhost/wordpress/xmlrpc.php', 'USERNAME', 'PASSWORD')

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized --lang=en-GB")
driver = webdriver.Chrome(chrome_options=options)
lines = [line.rstrip() for line in open('websites.csv')]
htmlcontent = []

for idx, val in enumerate(lines):
    # CHANGE THIS VARIABLE TO YOUR CORRECT SYSTEM FOLDER BUT DONT CHANGE THE LAST BIT
    imagelocation = "C:/CHANGE/THIS/PATH/img/%s.jpg" %idx
    # Getting website url from csv file
    driver.get(val)
    # Waiting to make sure everything is ready
    time.sleep(0.5)
    # removing distracting div container from view (Can be removed if not needed, or modified for other sites)
    if "github.com" in val: 
        print("Found github site")
        customcss = driver.find_element_by_css_selector(".signup-prompt-bg")
        driver.execute_script("arguments[0].setAttribute('style','display:none;')", customcss)
    # saving screenshot and opening it with pillow
    screenshot = driver.save_screenshot(imagelocation)
    im = Image.open(imagelocation)
    # resizing and cropping image to remove scrollbar.
    # this hack should be updated with scrollbar remove option on chromedriver but it doesnt work at the moment
    imResize = im.resize((650,291), Image.ANTIALIAS)
    imCrop = imResize.crop((0, 0, 640, 291))
    imCrop.save(imagelocation, 'JPEG', quality=95)
    filename = imagelocation
    # prepare metadata
    data = {
        'name': '%s.jpg' %idx,
        'type': 'image/jpeg',  # mimetype
    }
    # read the binary file and let the XMLRPC library encode it into base64
    with open(filename, 'rb') as img:
        data['bits'] = xmlrpc_client.Binary(img.read())
    response = wp.call(media.UploadFile(data))
    attachment_url = response['url']
    # Prepare the HTML content for publishing in a single list
    htmlcontent.append("<h2><a href='" + val + "'>" + driver.title + "</a></h2>")
    htmlcontent.append("<img src='%s'><br>" % attachment_url)

    print("Screenshot grabbed and posted to WP with ID: %d" %idx)
#done getting the last screenshot
driver.quit()

# start posting to WordPress
postcontent = ''.join(htmlcontent)
post = WordPressPost()
post.title = 'XMLRPC Import'
post.content = postcontent
post.post_status = 'draft'
post.id = wp.call(posts.NewPost(post))
